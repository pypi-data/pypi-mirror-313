# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .evaluation_trace_span import EvaluationTraceSpan
from .result_schema_flexible import ResultSchemaFlexible
from .application_metric_score import ApplicationMetricScore
from .evaluation_datasets.test_case import TestCase
from .shared.result_schema_generation import ResultSchemaGeneration

__all__ = [
    "PaginatedApplicationTestCaseOutputWithViews",
    "Item",
    "ItemApplicationTestCaseGenerationOutputResponseWithViews",
    "ItemApplicationTestCaseGenerationOutputResponseWithViewsInteraction",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViews",
    "ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteraction",
]


class ItemApplicationTestCaseGenerationOutputResponseWithViewsInteraction(BaseModel):
    id: str

    aggregated: bool
    """
    Boolean of whether this interaction has been uploaded to s3 bucket yet, default
    is false
    """

    application_spec_id: str

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    duration_ms: int
    """How much time the step took in milliseconds(ms)"""

    input: object

    operation_status: Literal["SUCCESS", "ERROR"]
    """The outcome of the operation"""

    output: object

    start_timestamp: datetime

    chat_thread_id: Optional[str] = None

    interaction_source: Optional[Literal["EXTERNAL_AI", "EVALUATION", "SGP_CHAT", "AGENTS_SERVICE"]] = None

    operation_metadata: Optional[object] = None
    """The JSON representation of the metadata insights emitted through the execution.

    This can differ based on different types of operations
    """

    trace_spans: Optional[List[EvaluationTraceSpan]] = None


class ItemApplicationTestCaseGenerationOutputResponseWithViews(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    evaluation_dataset_id: str

    output: ResultSchemaGeneration

    test_case_id: str

    application_interaction_id: Optional[str] = None

    application_test_case_output_group_id: Optional[str] = None

    interaction: Optional[ItemApplicationTestCaseGenerationOutputResponseWithViewsInteraction] = None

    metric_scores: Optional[List[ApplicationMetricScore]] = None

    metrics: Optional[Dict[str, float]] = None

    schema_type: Optional[Literal["GENERATION"]] = None

    test_case_version: Optional[TestCase] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteraction(BaseModel):
    id: str

    aggregated: bool
    """
    Boolean of whether this interaction has been uploaded to s3 bucket yet, default
    is false
    """

    application_spec_id: str

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    duration_ms: int
    """How much time the step took in milliseconds(ms)"""

    input: object

    operation_status: Literal["SUCCESS", "ERROR"]
    """The outcome of the operation"""

    output: object

    start_timestamp: datetime

    chat_thread_id: Optional[str] = None

    interaction_source: Optional[Literal["EXTERNAL_AI", "EVALUATION", "SGP_CHAT", "AGENTS_SERVICE"]] = None

    operation_metadata: Optional[object] = None
    """The JSON representation of the metadata insights emitted through the execution.

    This can differ based on different types of operations
    """

    trace_spans: Optional[List[EvaluationTraceSpan]] = None


class ItemApplicationTestCaseFlexibleOutputResponseWithViews(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    evaluation_dataset_id: str

    output: ResultSchemaFlexible

    test_case_id: str

    application_interaction_id: Optional[str] = None

    application_test_case_output_group_id: Optional[str] = None

    interaction: Optional[ItemApplicationTestCaseFlexibleOutputResponseWithViewsInteraction] = None

    metric_scores: Optional[List[ApplicationMetricScore]] = None

    metrics: Optional[Dict[str, float]] = None

    schema_type: Optional[Literal["FLEXIBLE"]] = None

    test_case_version: Optional[TestCase] = None


Item: TypeAlias = Annotated[
    Union[
        ItemApplicationTestCaseGenerationOutputResponseWithViews, ItemApplicationTestCaseFlexibleOutputResponseWithViews
    ],
    PropertyInfo(discriminator="schema_type"),
]


class PaginatedApplicationTestCaseOutputWithViews(BaseModel):
    current_page: int
    """The current page number."""

    items: List[Item]
    """The data returned for the current page."""

    items_per_page: int
    """The number of items per page."""

    total_item_count: int
    """The total number of items of the query"""
