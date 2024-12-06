# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .test_case_result import TestCaseResult
from ..evaluation_trace_span import EvaluationTraceSpan
from ..result_schema_flexible import ResultSchemaFlexible
from ..evaluation_datasets.test_case import TestCase
from ..shared.result_schema_generation import ResultSchemaGeneration

__all__ = [
    "TestCaseResultWithViews",
    "GenerationTestCaseResultResponseWithViews",
    "GenerationTestCaseResultResponseWithViewsAnnotationResult",
    "GenerationTestCaseResultResponseWithViewsAnnotationResultSelectedChoice",
    "GenerationTestCaseResultResponseWithViewsAnnotationResultSelectedChoiceCategoricalChoice",
    "GenerationTestCaseResultResponseWithViewsAnnotationResultSelectedChoiceUnionMember1",
    "GenerationTestCaseResultResponseWithViewsAnnotationResultLlmAutoEvalMetadata",
    "GenerationTestCaseResultResponseWithViewsApplicationTestCaseOutput",
    "GenerationTestCaseResultResponseWithViewsApplicationTestCaseOutputOutput",
    "GenerationTestCaseResultResponseWithViewsApplicationTestCaseOutputInteraction",
    "GenerationTestCaseResultResponseWithViewsTask",
    "GenerationTestCaseResultResponseWithViewsTaskAssignedTo",
    "FlexibleTestCaseResultResponseWithViews",
    "FlexibleTestCaseResultResponseWithViewsAnnotationResult",
    "FlexibleTestCaseResultResponseWithViewsAnnotationResultSelectedChoice",
    "FlexibleTestCaseResultResponseWithViewsAnnotationResultSelectedChoiceCategoricalChoice",
    "FlexibleTestCaseResultResponseWithViewsAnnotationResultSelectedChoiceUnionMember1",
    "FlexibleTestCaseResultResponseWithViewsAnnotationResultLlmAutoEvalMetadata",
    "FlexibleTestCaseResultResponseWithViewsApplicationTestCaseOutput",
    "FlexibleTestCaseResultResponseWithViewsApplicationTestCaseOutputOutput",
    "FlexibleTestCaseResultResponseWithViewsApplicationTestCaseOutputInteraction",
    "FlexibleTestCaseResultResponseWithViewsTask",
    "FlexibleTestCaseResultResponseWithViewsTaskAssignedTo",
]


class GenerationTestCaseResultResponseWithViewsAnnotationResultSelectedChoiceCategoricalChoice(BaseModel):
    label: str

    value: Union[str, bool, float]

    audit_required: Optional[bool] = None


class GenerationTestCaseResultResponseWithViewsAnnotationResultSelectedChoiceUnionMember1(BaseModel):
    label: str

    value: Union[str, bool, float]

    audit_required: Optional[bool] = None


GenerationTestCaseResultResponseWithViewsAnnotationResultSelectedChoice: TypeAlias = Union[
    GenerationTestCaseResultResponseWithViewsAnnotationResultSelectedChoiceCategoricalChoice,
    List[GenerationTestCaseResultResponseWithViewsAnnotationResultSelectedChoiceUnionMember1],
    str,
    float,
]


class GenerationTestCaseResultResponseWithViewsAnnotationResultLlmAutoEvalMetadata(BaseModel):
    annotation_result_id: str
    """The ID of the associated annotation result."""

    completion_tokens: int

    llm_reasoning: str
    """The reasoning the LLM gave for the annotation it provided."""

    prompt_tokens: int

    time_elapsed_s: int
    """The time elapsed to generate this annotation in seconds."""

    cost: Optional[int] = None
    """The cost of the annotation in cents."""


class GenerationTestCaseResultResponseWithViewsAnnotationResult(BaseModel):
    id: str
    """The unique identifier of the entity."""

    annotation_type: Literal["llm_auto", "human"]
    """The type of annotation result."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    question_id: str

    selected_choice: GenerationTestCaseResultResponseWithViewsAnnotationResultSelectedChoice
    """The selected choices(s) for the annotation result, in JSON form.

    For categorical questions, this is an object or list of objects (depending on if
    multiple selections are allowed). For free text questions, this is a string. For
    numeric or rating questions, this is a number.
    """

    test_case_result_lineage_id: str

    llm_auto_eval_metadata: Optional[GenerationTestCaseResultResponseWithViewsAnnotationResultLlmAutoEvalMetadata] = (
        None
    )


GenerationTestCaseResultResponseWithViewsApplicationTestCaseOutputOutput: TypeAlias = Union[
    ResultSchemaGeneration, ResultSchemaFlexible
]


class GenerationTestCaseResultResponseWithViewsApplicationTestCaseOutputInteraction(BaseModel):
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


class GenerationTestCaseResultResponseWithViewsApplicationTestCaseOutput(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    evaluation_dataset_id: str

    output: GenerationTestCaseResultResponseWithViewsApplicationTestCaseOutputOutput

    schema_type: Literal["GENERATION", "FLEXIBLE"]

    test_case_id: str

    test_case_version_id: str

    application_interaction_id: Optional[str] = None

    application_test_case_output_group_id: Optional[str] = None

    interaction: Optional[GenerationTestCaseResultResponseWithViewsApplicationTestCaseOutputInteraction] = None


class GenerationTestCaseResultResponseWithViewsTaskAssignedTo(BaseModel):
    id: str

    email: str

    first_name: Optional[str] = None

    last_name: Optional[str] = None

    preferences: Optional[object] = None


class GenerationTestCaseResultResponseWithViewsTask(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    priority: int

    status: Literal["PENDING", "COMPLETED"]

    task_entity_id: str

    task_entity_parent_id: str

    task_type: Literal["EVALUATION_ANNOTATION"]

    assigned_to: Optional[GenerationTestCaseResultResponseWithViewsTaskAssignedTo] = None

    assignment_expires_at: Optional[datetime] = None
    """The date and time when the task assignment expires in ISO format."""

    task_entity: Optional[TestCaseResult] = None
    """The entity that the task is associated with."""


class GenerationTestCaseResultResponseWithViews(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    evaluation_dataset_id: str

    evaluation_dataset_version_num: str

    evaluation_id: str

    label_status: Literal["PENDING", "COMPLETED", "FAILED"]

    test_case_evaluation_data: ResultSchemaGeneration

    test_case_id: str

    annotated_by_user_id: Optional[str] = None
    """The user who annotated the task."""

    annotation_results: Optional[List[GenerationTestCaseResultResponseWithViewsAnnotationResult]] = None

    application_test_case_output: Optional[GenerationTestCaseResultResponseWithViewsApplicationTestCaseOutput] = None

    application_test_case_output_id: Optional[str] = None

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    audit_comment: Optional[str] = None

    audit_required: Optional[bool] = None

    audit_status: Optional[Literal["UNAUDITED", "FIXED", "APPROVED"]] = None

    completed_at: Optional[datetime] = None

    metrics: Optional[Dict[str, float]] = None

    result: Optional[Dict[str, Union[str, bool, float, List[Union[str, bool, float]]]]] = None
    """
    The result of the test case evaluation, in JSON form where the key is the
    question ID and the value is the result.
    """

    task: Optional[GenerationTestCaseResultResponseWithViewsTask] = None

    test_case_evaluation_data_schema: Optional[Literal["GENERATION"]] = None

    test_case_version: Optional[TestCase] = None

    time_spent_labeling_s: Optional[int] = None
    """The time spent labeling in seconds."""


class FlexibleTestCaseResultResponseWithViewsAnnotationResultSelectedChoiceCategoricalChoice(BaseModel):
    label: str

    value: Union[str, bool, float]

    audit_required: Optional[bool] = None


class FlexibleTestCaseResultResponseWithViewsAnnotationResultSelectedChoiceUnionMember1(BaseModel):
    label: str

    value: Union[str, bool, float]

    audit_required: Optional[bool] = None


FlexibleTestCaseResultResponseWithViewsAnnotationResultSelectedChoice: TypeAlias = Union[
    FlexibleTestCaseResultResponseWithViewsAnnotationResultSelectedChoiceCategoricalChoice,
    List[FlexibleTestCaseResultResponseWithViewsAnnotationResultSelectedChoiceUnionMember1],
    str,
    float,
]


class FlexibleTestCaseResultResponseWithViewsAnnotationResultLlmAutoEvalMetadata(BaseModel):
    annotation_result_id: str
    """The ID of the associated annotation result."""

    completion_tokens: int

    llm_reasoning: str
    """The reasoning the LLM gave for the annotation it provided."""

    prompt_tokens: int

    time_elapsed_s: int
    """The time elapsed to generate this annotation in seconds."""

    cost: Optional[int] = None
    """The cost of the annotation in cents."""


class FlexibleTestCaseResultResponseWithViewsAnnotationResult(BaseModel):
    id: str
    """The unique identifier of the entity."""

    annotation_type: Literal["llm_auto", "human"]
    """The type of annotation result."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    question_id: str

    selected_choice: FlexibleTestCaseResultResponseWithViewsAnnotationResultSelectedChoice
    """The selected choices(s) for the annotation result, in JSON form.

    For categorical questions, this is an object or list of objects (depending on if
    multiple selections are allowed). For free text questions, this is a string. For
    numeric or rating questions, this is a number.
    """

    test_case_result_lineage_id: str

    llm_auto_eval_metadata: Optional[FlexibleTestCaseResultResponseWithViewsAnnotationResultLlmAutoEvalMetadata] = None


FlexibleTestCaseResultResponseWithViewsApplicationTestCaseOutputOutput: TypeAlias = Union[
    ResultSchemaGeneration, ResultSchemaFlexible
]


class FlexibleTestCaseResultResponseWithViewsApplicationTestCaseOutputInteraction(BaseModel):
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


class FlexibleTestCaseResultResponseWithViewsApplicationTestCaseOutput(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    evaluation_dataset_id: str

    output: FlexibleTestCaseResultResponseWithViewsApplicationTestCaseOutputOutput

    schema_type: Literal["GENERATION", "FLEXIBLE"]

    test_case_id: str

    test_case_version_id: str

    application_interaction_id: Optional[str] = None

    application_test_case_output_group_id: Optional[str] = None

    interaction: Optional[FlexibleTestCaseResultResponseWithViewsApplicationTestCaseOutputInteraction] = None


class FlexibleTestCaseResultResponseWithViewsTaskAssignedTo(BaseModel):
    id: str

    email: str

    first_name: Optional[str] = None

    last_name: Optional[str] = None

    preferences: Optional[object] = None


class FlexibleTestCaseResultResponseWithViewsTask(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    priority: int

    status: Literal["PENDING", "COMPLETED"]

    task_entity_id: str

    task_entity_parent_id: str

    task_type: Literal["EVALUATION_ANNOTATION"]

    assigned_to: Optional[FlexibleTestCaseResultResponseWithViewsTaskAssignedTo] = None

    assignment_expires_at: Optional[datetime] = None
    """The date and time when the task assignment expires in ISO format."""

    task_entity: Optional[TestCaseResult] = None
    """The entity that the task is associated with."""


class FlexibleTestCaseResultResponseWithViews(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    evaluation_dataset_id: str

    evaluation_dataset_version_num: str

    evaluation_id: str

    label_status: Literal["PENDING", "COMPLETED", "FAILED"]

    test_case_evaluation_data: ResultSchemaFlexible

    test_case_id: str

    annotated_by_user_id: Optional[str] = None
    """The user who annotated the task."""

    annotation_results: Optional[List[FlexibleTestCaseResultResponseWithViewsAnnotationResult]] = None

    application_test_case_output: Optional[FlexibleTestCaseResultResponseWithViewsApplicationTestCaseOutput] = None

    application_test_case_output_id: Optional[str] = None

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    audit_comment: Optional[str] = None

    audit_required: Optional[bool] = None

    audit_status: Optional[Literal["UNAUDITED", "FIXED", "APPROVED"]] = None

    completed_at: Optional[datetime] = None

    metrics: Optional[Dict[str, float]] = None

    result: Optional[Dict[str, Union[str, bool, float, List[Union[str, bool, float]]]]] = None
    """
    The result of the test case evaluation, in JSON form where the key is the
    question ID and the value is the result.
    """

    task: Optional[FlexibleTestCaseResultResponseWithViewsTask] = None

    test_case_evaluation_data_schema: Optional[Literal["FLEXIBLE"]] = None

    test_case_version: Optional[TestCase] = None

    time_spent_labeling_s: Optional[int] = None
    """The time spent labeling in seconds."""


TestCaseResultWithViews: TypeAlias = Annotated[
    Union[GenerationTestCaseResultResponseWithViews, FlexibleTestCaseResultResponseWithViews],
    PropertyInfo(discriminator="test_case_evaluation_data_schema"),
]
