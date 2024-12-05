import re
from collections import defaultdict
from itertools import starmap
from typing import Any, Iterable, Sequence, Type

import torch
from tdm import TalismanDocument
from tdm.abstract.datamodel import AbstractFact, FactStatus
from tdm.datamodel.mentions import TextNodeMention
from tdm.datamodel.nodes import TextNode
from tdm.utils.node import dfs
from transformers import pipeline
from typing_extensions import Self

from tie_ml_base.env import get_cpu_batch_size, get_gpu_batch_size
from tie_ml_base.tools.memory_management import cuda_handler
from tie_ml_base.torch_wrapper import TorchModule
from tp_interfaces.abstract import AbstractConfigConstructableModel, AbstractDocumentProcessor, ImmutableBaseModel
from tp_interfaces.domain.abstract import AbstractNERCBasedType
from tp_interfaces.domain.manager import DomainManager
from tp_interfaces.helpers.datamodel.fact import MentionedFactsFactory, mentioned_fact_factory


class TokenClassificationPipelineConfig(ImmutableBaseModel):
    """
    For the possible aggregation strategies please refer to
    https://huggingface.co/docs/transformers/v4.27.2/en/main_classes/pipelines#transformers.TokenClassificationPipeline.aggregation_strategy
    """
    aggregation_strategy: str = 'first'


NODE_DELIMITER = '\n'


class HuggingFacePipelineWrapper(
    TorchModule,
    AbstractDocumentProcessor[TokenClassificationPipelineConfig],
    AbstractConfigConstructableModel
):

    def __init__(self, model_name_or_path: str):
        super().__init__()

        self._type_mapping: dict[str, set[MentionedFactsFactory]] = defaultdict(set)
        self._pipeline = pipeline(
            model=model_name_or_path,
            tokenizer=model_name_or_path,
            task='ner',
            framework='pt',
            device=torch.device('cpu')
        )
        self._model = self._pipeline.model
        self._labels = set(re.findall(r'(?<=\w-)\w+', str.join(' ', self._model.config.label2id)))
        self._cpu_batch_size = get_cpu_batch_size()
        self._gpu_batch_size = get_gpu_batch_size()

    @property
    def get_labels(self) -> set[str]:
        return self._labels

    @classmethod
    def from_config(cls, config: dict) -> Self:
        return cls(**config)

    def forward(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    @cuda_handler
    async def process_docs(
            self,
            documents: Sequence[TalismanDocument],
            config: TokenClassificationPipelineConfig
    ) -> tuple[TalismanDocument, ...]:

        if self._pipeline is None:
            raise RuntimeError(f'{self.__class__.__name__} is not entered!')

        batch_size = self._cpu_batch_size if self.device == torch.device('cpu') else self._gpu_batch_size
        self._pipeline.device = self.device

        text_inputs = []
        nodes: list[tuple[TextNode, ...]] = []
        for document in documents:
            document_nodes = tuple(dfs(document, type_=TextNode, filter_=lambda n: bool(len(n.content))))
            nodes.append(document_nodes)

            document_text = NODE_DELIMITER.join(node.content for node in document_nodes)
            text_inputs.append(document_text)

        result = self._pipeline(text_inputs, batch_size=batch_size, **config.dict())
        return tuple(starmap(self._postprocess_ner, zip(documents, result, nodes)))

    async def process_doc(self, document: TalismanDocument, config: TokenClassificationPipelineConfig) -> TalismanDocument:
        return (await self.process_docs([document], config))[0]

    @property
    def config_type(self) -> Type[TokenClassificationPipelineConfig]:
        return TokenClassificationPipelineConfig

    async def __aenter__(self):
        async with DomainManager() as manager:
            domain = await manager.domain

        for t in domain.get_types(AbstractNERCBasedType):
            for nerc_model in await t.pretrained_nerc_models:
                self._type_mapping[nerc_model].add(mentioned_fact_factory(t))

    async def __aexit__(self, *args, **kwargs):
        self._type_mapping = defaultdict(set)
        self._label_mapping = None

    def _postprocess_ner(self, document: TalismanDocument, outputs: list[dict], processed_nodes: tuple[TextNode, ...]) -> TalismanDocument:
        if not len(processed_nodes):
            return document

        sorted_signatures = sorted((output['start'], output['end'], output['entity_group']) for output in outputs)

        def build_facts(node: TextNode, start_idx: int, end_idx: int, object_type: str) -> Iterable[AbstractFact]:
            mention = TextNodeMention(node, start_idx, end_idx)
            for factory in self._type_mapping[object_type]:
                yield from factory(mention, FactStatus.NEW)

        node_iterator = iter(processed_nodes)
        signature_iterator = iter(sorted_signatures)

        current_node_shift = 0
        current_node = next(node_iterator)

        all_facts = []
        for start, end, type_ in signature_iterator:
            while start >= current_node_shift + len(NODE_DELIMITER) + len(current_node.content):
                current_node_shift += len(NODE_DELIMITER) + len(current_node.content)
                current_node = next(node_iterator)
            all_facts.extend(build_facts(current_node, start - current_node_shift, end - current_node_shift, type_))

        return document.with_facts(all_facts, update=True)
