import asyncio
import itertools
import logging
from collections import Counter, defaultdict
from dataclasses import dataclass, replace
from enum import Enum
from typing import Any, Iterable, Iterator, List, Tuple, Type

import torch
from tdm import TalismanDocument, not_filter
from tdm.abstract.datamodel import AbstractFact, FactStatus
from tdm.datamodel.facts import AtomValueFact, MentionFact
from tdm.datamodel.mentions import TextNodeMention
from tdm.datamodel.values import StringValue
from transformers import pipeline
from typing_extensions import Self

from tie_ml_base.env import get_cpu_batch_size, get_gpu_batch_size
from tie_ml_base.tools.memory_management import cuda_handler
from tie_ml_base.torch_wrapper import TorchModule
from tp_interfaces.abstract import AbstractConfigConstructableModel, AbstractDocumentProcessor, ImmutableBaseModel

logger = logging.Logger(__name__)


@dataclass
class TextMentionData:
    language: str
    related_fact: AtomValueFact
    text: str

    def __init__(self, mention: MentionFact, language: str = None):
        self.language = language
        self.related_fact = mention.value
        if isinstance(mention.mention, TextNodeMention):
            self.text = mention.mention.node.content[mention.mention.start: mention.mention.end]
        else:
            raise ValueError


class UnsupportedMentionAction(str, Enum):
    """
    IGNORE: keep only mentions with supported languages
    IGNORE_ABSOLUTELY: ignore them, if there aren't other mentions and keep them if there are
    KEEP: keep them considering as already normalized
    """
    IGNORE = "ignore"
    IGNORE_ABSOLUTELY = "ignore_absolutely"
    KEEP = "keep"


class StringNormalizerConfig(ImmutableBaseModel):
    """
    lang: language of normalization if the document's language is None
    not_supported_mentions: how to deal mentions, which languages are not supported
    """
    lang: str = "ru"
    unsupported_mentions: UnsupportedMentionAction = UnsupportedMentionAction.KEEP


class Text2TextNormalizer(
    TorchModule,
    AbstractConfigConstructableModel,
    AbstractDocumentProcessor[StringNormalizerConfig]
):
    """
    A hugging face pipeline wrapper for AtomValueFact's StringValue normalization using text2text model,
    for some supported languages.
    """
    def __init__(self, normalizer_pipeline: pipeline, batch_size: int, model_languages: Iterable[str],
                 preferred_device: str | torch.device = None):
        super().__init__(preferred_device=preferred_device)
        self._pipeline = normalizer_pipeline
        self._model = self._pipeline.model
        self._model_languages = model_languages
        self._tokenizer = self._pipeline.tokenizer
        self._cpu_batch_size = get_cpu_batch_size()
        self._gpu_batch_size = get_gpu_batch_size()
        self._batch_size = batch_size

    @classmethod
    def from_config(cls, config: dict) -> Self:
        return cls.from_model_name(**config)

    @classmethod
    def from_model_name(cls, model_name_or_path: str, model_languages: Iterable[str],
                        preferred_device: str | torch.device = None, batch_size: int = None) -> Self:
        pl = pipeline(
            model=model_name_or_path,
            tokenizer=model_name_or_path,
            task='text2text-generation',
            framework='pt',
            device=torch.device('cpu')
        )
        return cls(pl, batch_size, model_languages, preferred_device)

    @classmethod
    def from_existing_pipeline(cls, pl, model_languages: Iterable[str], batch_size: int = None,
                               preferred_device: str | torch.device = None) -> Self:
        return cls(pl, batch_size, model_languages, preferred_device)

    async def process_doc(self, document: TalismanDocument, config: StringNormalizerConfig) -> TalismanDocument:
        facts = document.get_facts(
            type_=AtomValueFact,
            filter_=(not_filter(AtomValueFact.status_filter([FactStatus.APPROVED, FactStatus.DECLINED])),
                     AtomValueFact.empty_value_filter())
        )
        processed_facts = await asyncio.to_thread(self.normalize_facts, facts=list(facts), doc=document, config=config)
        return document.with_facts(processed_facts)

    @property
    def config_type(self) -> Type[StringNormalizerConfig]:
        return StringNormalizerConfig

    def forward(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    @staticmethod
    def validate_facts_types(func):
        def wrap(self, facts: Iterable[AbstractFact], *args, **kwargs):
            if not all(isinstance(fact, AtomValueFact) for fact in facts):
                raise ValueError
            return func(self, facts, *args, **kwargs)

        return wrap

    async def normalize_fact(self, fact: AtomValueFact, doc: TalismanDocument, config: StringNormalizerConfig) -> AtomValueFact:
        fact_iterator = await asyncio.to_thread(self.normalize_facts, facts=[fact], doc=doc, config=config)
        return list(fact_iterator)[0]

    @validate_facts_types
    def normalize_facts(self, facts: Iterable[AtomValueFact], doc: TalismanDocument, config: StringNormalizerConfig) \
            -> Iterator[AtomValueFact]:

        # Step 1: We get all mentions that are related to the doc facts and normalize them
        mentions = itertools.chain(*(doc.related_facts(fact, type_=MentionFact) for fact in facts))
        normalized_mentions_data: List[TextMentionData] = self._normalize_mentions(mentions, config)

        # Step 2: Conversion the most common normalized mention into the value(s) of fact
        normalized_mentions = [normalized_mention.text for normalized_mention in normalized_mentions_data]
        related_facts = [normalized_mention.related_fact for normalized_mention in normalized_mentions_data]
        normalized_values = tuple(map(self._convert, normalized_mentions))
        fact_values = defaultdict(list)
        for normalized_value, related_fact in zip(normalized_values, related_facts):
            fact_values[related_fact].append(normalized_value)

        # Step 3: Yielding replaced facts if they are normalized (preserving order)
        for fact in facts:
            if fact in fact_values:
                normalized_value = self._set_confidence(fact_values[fact])
                yield replace(fact, value=tuple(normalized_value))
            else:
                yield fact

    @cuda_handler
    def _normalize_mentions(self, mentions: Iterable[MentionFact], config: StringNormalizerConfig) -> List[TextMentionData]:
        # Separate supported and unsupported mentions and store their data
        supported_mentions, unsupported_mentions = self._process_mentions(mentions, config, self._model_languages)

        # If there are not supported mentions, then normalization is not needed
        if not supported_mentions:
            return self._apply_config(supported_mentions, unsupported_mentions, config)

        # Normalization part
        self._pipeline.device = self.device
        batch_size = self._batch_size if self._batch_size is not None else \
            (self._cpu_batch_size if self.device == torch.device('cpu') else self._gpu_batch_size)
        to_be_normalized = [f">>{mention.language}<< {mention.text}" for mention in supported_mentions]
        # Setting the maximum output tokens' number to (1.5 * maximum input tokens' number) to prevent value cutting.
        max_output_tokens = int(1.5 * len(max(map(self._tokenizer.encode, to_be_normalized), key=len)))
        try:
            results = self._pipeline(to_be_normalized, clean_up_tokenization_spaces=True, num_beams=5,
                                     batch_size=batch_size, max_new_tokens=max_output_tokens)
        except ValueError:
            logger.warning(f'ValueError occurred during normalization of mentions: {", ".join([sm.text for sm in supported_mentions])}.')
            return []

        # Updating values, applying config, returning normalized mentions' data
        normalized_mentions_str = [res['generated_text'] for res in results]
        for i in range(len(supported_mentions)):
            supported_mentions[i].text = normalized_mentions_str[i]
        return self._apply_config(supported_mentions, unsupported_mentions, config)

    @staticmethod
    def _set_confidence(normalized_mentions: Iterable[StringValue]) -> Iterator[StringValue]:
        """
        Counts the confidence for each normalized value and sorts the values by confidence.
        """
        c = Counter(normalized_mentions)
        for value, value_count in c.most_common():
            yield replace(value, confidence=value_count / c.total())

    @staticmethod
    def _convert(value: str) -> StringValue | None:
        try:
            return StringValue(value=value)
        except ValueError:
            logger.warning(f'ValueError occurred during conversion of "{value}".')

    @staticmethod
    def _process_mentions(mentions: Iterable[MentionFact], config: StringNormalizerConfig, model_languages: Iterable[str]) \
            -> Tuple[List[TextMentionData], List[TextMentionData]]:
        supported_mentions: List[TextMentionData] = []
        unsupported_mentions: List[TextMentionData] = []
        for mention in mentions:
            if isinstance(mention.mention, TextNodeMention):
                language = mention.mention.node.metadata.language
                if language is None or language == 'unknown':
                    language = config.lang
                if language not in model_languages:
                    unsupported_mentions.append(TextMentionData(mention, language))
                else:
                    supported_mentions.append(TextMentionData(mention, language))
        return supported_mentions, unsupported_mentions

    @staticmethod
    def _apply_config(supported_mentions: List[TextMentionData],
                      unsupported_mentions: List[TextMentionData], config: StringNormalizerConfig) \
            -> List[TextMentionData] | None:
        if config.unsupported_mentions == UnsupportedMentionAction.IGNORE:
            return supported_mentions
        elif config.unsupported_mentions == UnsupportedMentionAction.IGNORE_ABSOLUTELY:
            supported_facts = [s.related_fact for s in supported_mentions]
            return supported_mentions + list(filter(lambda m: m.related_fact in supported_facts, unsupported_mentions))
        elif config.unsupported_mentions == UnsupportedMentionAction.KEEP:
            return supported_mentions + unsupported_mentions
        else:
            raise ValueError("Inappropriate value for not supported languages' configuration")
