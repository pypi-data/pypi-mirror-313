# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .annotation_config_param import AnnotationConfigParam
from .multiturn_annotation_config_param import MultiturnAnnotationConfigParam
from .translation_annotation_config_param import TranslationAnnotationConfigParam
from .summarization_annotation_config_param import SummarizationAnnotationConfigParam

__all__ = [
    "EvaluationCreateParams",
    "EvaluationBuilderRequest",
    "EvaluationBuilderRequestAnnotationConfig",
    "EvaluationBuilderRequestAnnotationConfigAnnotationConfigRequestBase",
    "EvaluationBuilderRequestAnnotationConfigAnnotationConfigRequestBaseComponent",
    "DefaultEvaluationRequest",
    "DefaultEvaluationRequestAnnotationConfig",
    "DefaultEvaluationRequestAnnotationConfigAnnotationConfigRequestBase",
    "DefaultEvaluationRequestAnnotationConfigAnnotationConfigRequestBaseComponent",
]


class EvaluationBuilderRequest(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_spec_id: Required[str]

    application_variant_id: Required[str]

    description: Required[str]

    evaluation_dataset_id: Required[str]

    name: Required[str]

    annotation_config: EvaluationBuilderRequestAnnotationConfig
    """Annotation configuration for tasking"""

    application_test_case_output_group_id: str

    evaluation_config: object

    evaluation_config_id: str
    """The ID of the associated evaluation config."""

    evaluation_dataset_version: int

    question_id_to_annotation_config: Dict[str, AnnotationConfigParam]
    """Specifies the annotation configuration to use for specific questions."""

    tags: object

    type: Literal["builder"]
    """
    create standalone evaluation or build evaluation which will auto generate test
    case results
    """


class EvaluationBuilderRequestAnnotationConfigAnnotationConfigRequestBaseComponent(TypedDict, total=False):
    data_loc: Required[List[str]]

    label: str

    optional: bool


class EvaluationBuilderRequestAnnotationConfigAnnotationConfigRequestBase(TypedDict, total=False):
    components: Required[
        Iterable[Iterable[EvaluationBuilderRequestAnnotationConfigAnnotationConfigRequestBaseComponent]]
    ]

    direction: Literal["col", "row"]


EvaluationBuilderRequestAnnotationConfig: TypeAlias = Union[
    EvaluationBuilderRequestAnnotationConfigAnnotationConfigRequestBase,
    MultiturnAnnotationConfigParam,
    SummarizationAnnotationConfigParam,
    TranslationAnnotationConfigParam,
]


class DefaultEvaluationRequest(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_spec_id: Required[str]

    description: Required[str]

    name: Required[str]

    annotation_config: DefaultEvaluationRequestAnnotationConfig
    """Annotation configuration for tasking"""

    application_variant_id: str

    evaluation_config: object

    evaluation_config_id: str
    """The ID of the associated evaluation config."""

    question_id_to_annotation_config: Dict[str, AnnotationConfigParam]
    """Specifies the annotation configuration to use for specific questions."""

    tags: object

    type: Literal["default"]
    """
    create standalone evaluation or build evaluation which will auto generate test
    case results
    """


class DefaultEvaluationRequestAnnotationConfigAnnotationConfigRequestBaseComponent(TypedDict, total=False):
    data_loc: Required[List[str]]

    label: str

    optional: bool


class DefaultEvaluationRequestAnnotationConfigAnnotationConfigRequestBase(TypedDict, total=False):
    components: Required[
        Iterable[Iterable[DefaultEvaluationRequestAnnotationConfigAnnotationConfigRequestBaseComponent]]
    ]

    direction: Literal["col", "row"]


DefaultEvaluationRequestAnnotationConfig: TypeAlias = Union[
    DefaultEvaluationRequestAnnotationConfigAnnotationConfigRequestBase,
    MultiturnAnnotationConfigParam,
    SummarizationAnnotationConfigParam,
    TranslationAnnotationConfigParam,
]

EvaluationCreateParams: TypeAlias = Union[EvaluationBuilderRequest, DefaultEvaluationRequest]
