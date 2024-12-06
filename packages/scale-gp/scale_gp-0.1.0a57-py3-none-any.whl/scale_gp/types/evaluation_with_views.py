# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel
from .application_spec import ApplicationSpec
from .annotation_config import AnnotationConfig
from .evaluation_dataset import EvaluationDataset
from .question_set_with_questions import QuestionSetWithQuestions

__all__ = [
    "EvaluationWithViews",
    "AsyncJob",
    "EvaluationConfigExpanded",
    "EvaluationConfigExpandedEvaluationConfigExpanded",
    "EvaluationConfigExpandedLegacyEvaluationConfigExpanded",
    "EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSet",
    "EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSetQuestion",
    "EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSetQuestionIDToConfig",
]


class AsyncJob(BaseModel):
    id: str
    """The unique identifier of the entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    status: str

    updated_at: datetime
    """The date and time when the entity was last updated in ISO format."""

    job_metadata: Optional[object] = None

    job_type: Optional[str] = None

    parent_job_id: Optional[str] = None

    progress: Optional[object] = None


class EvaluationConfigExpandedEvaluationConfigExpanded(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    evaluation_type: Literal["studio", "llm_auto", "human", "llm_benchmark"]
    """Evaluation type"""

    question_set: QuestionSetWithQuestions

    question_set_id: str

    auto_evaluation_model: Optional[
        Literal["gpt-4-32k-0613", "gpt-4-turbo-preview", "gpt-4-turbo-2024-04-09", "llama-3-70b-instruct"]
    ] = None
    """The name of the model to be used for auto-evaluation"""

    studio_project_id: Optional[str] = None


class EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSetQuestion(BaseModel):
    id: str
    """The unique identifier of the entity."""

    prompt: str

    title: str

    type: Literal["categorical", "free_text", "rating", "number"]

    choices: Optional[List[object]] = None
    """List of choices for the question. Required for CATEGORICAL questions."""

    conditions: Optional[List[object]] = None
    """Conditions for the question to be shown."""

    multi: Optional[bool] = None
    """Whether the question allows multiple answers."""

    required: Optional[bool] = None
    """Whether the question is required."""


class EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSetQuestionIDToConfig(BaseModel):
    required: Optional[bool] = None
    """Whether the question is required. False by default."""


class EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSet(BaseModel):
    questions: List[EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSetQuestion]

    question_id_to_config: Optional[
        Dict[str, EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSetQuestionIDToConfig]
    ] = None


class EvaluationConfigExpandedLegacyEvaluationConfigExpanded(BaseModel):
    evaluation_type: Literal["studio", "llm_auto", "human", "llm_benchmark"]

    question_set: EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSet

    studio_project_id: Optional[str] = None


EvaluationConfigExpanded: TypeAlias = Union[
    EvaluationConfigExpandedEvaluationConfigExpanded, EvaluationConfigExpandedLegacyEvaluationConfigExpanded
]


class EvaluationWithViews(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    completed_test_case_result_count: int
    """The number of test case results that have been completed for the evaluation"""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    description: str

    name: str

    status: Literal["PENDING", "COMPLETED", "FAILED"]

    total_test_case_result_count: int
    """The total number of test case results for the evaluation"""

    annotation_config: Optional[AnnotationConfig] = None
    """Annotation configuration for tasking"""

    application_spec: Optional[ApplicationSpec] = None

    application_variant_id: Optional[str] = None

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    async_jobs: Optional[List[AsyncJob]] = None

    completed_at: Optional[datetime] = None
    """
    The date and time that all test case results for the evaluation were completed
    for the evaluation in ISO format.
    """

    evaluation_config: Optional[object] = None

    evaluation_config_expanded: Optional[EvaluationConfigExpanded] = None

    evaluation_config_id: Optional[str] = None
    """The ID of the associated evaluation config."""

    evaluation_datasets: Optional[List[EvaluationDataset]] = None

    question_id_to_annotation_config: Optional[Dict[str, AnnotationConfig]] = None
    """Specifies the annotation configuration to use for specific questions."""

    tags: Optional[object] = None
