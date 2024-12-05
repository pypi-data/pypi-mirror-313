from typing import Type

from tp_interfaces.abstract import AbstractDocumentProcessor, ModelTypeFactory


def _get_pipeline() -> Type[AbstractDocumentProcessor]:
    from tie_ml_base.huggingface_pipeline.wrapper import HuggingFacePipelineWrapper
    return HuggingFacePipelineWrapper


def _get_string_normalizer() -> Type[AbstractDocumentProcessor]:
    from tie_ml_base.huggingface_pipeline.normalization_wrapper.string_normalizer import Text2TextNormalizer
    return Text2TextNormalizer


HF_PROCESSORS = ModelTypeFactory({
    "huggingface_pipeline": _get_pipeline,
    "string_normalizer": _get_string_normalizer,
})
