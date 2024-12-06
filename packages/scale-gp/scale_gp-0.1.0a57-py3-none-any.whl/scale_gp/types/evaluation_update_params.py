# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .annotation_config_param import AnnotationConfigParam
from .multiturn_annotation_config_param import MultiturnAnnotationConfigParam
from .translation_annotation_config_param import TranslationAnnotationConfigParam
from .summarization_annotation_config_param import SummarizationAnnotationConfigParam

__all__ = [
    "EvaluationUpdateParams",
    "PartialPatchEvaluationRequest",
    "PartialPatchEvaluationRequestAnnotationConfig",
    "PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigRequestBase",
    "PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigRequestBaseComponent",
    "RestoreRequest",
]


class PartialPatchEvaluationRequest(TypedDict, total=False):
    annotation_config: PartialPatchEvaluationRequestAnnotationConfig
    """Annotation configuration for tasking"""

    application_spec_id: str

    application_variant_id: str

    description: str

    evaluation_config: object

    evaluation_config_id: str
    """The ID of the associated evaluation config."""

    evaluation_type: Literal["llm_benchmark"]
    """
    If llm_benchmark is provided, the evaluation will be updated to a hybrid
    evaluation. No-op on existing hybrid evaluations, and not available for studio
    evaluations.
    """

    name: str

    question_id_to_annotation_config: Dict[str, AnnotationConfigParam]
    """Specifies the annotation configuration to use for specific questions."""

    restore: Literal[False]
    """Set to true to restore the entity from the database."""

    tags: object


class PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigRequestBaseComponent(TypedDict, total=False):
    data_loc: Required[List[str]]

    label: str

    optional: bool


class PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigRequestBase(TypedDict, total=False):
    components: Required[
        Iterable[Iterable[PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigRequestBaseComponent]]
    ]

    direction: Literal["col", "row"]


PartialPatchEvaluationRequestAnnotationConfig: TypeAlias = Union[
    PartialPatchEvaluationRequestAnnotationConfigAnnotationConfigRequestBase,
    MultiturnAnnotationConfigParam,
    SummarizationAnnotationConfigParam,
    TranslationAnnotationConfigParam,
]


class RestoreRequest(TypedDict, total=False):
    restore: Required[Literal[True]]
    """Set to true to restore the entity from the database."""


EvaluationUpdateParams: TypeAlias = Union[PartialPatchEvaluationRequest, RestoreRequest]
