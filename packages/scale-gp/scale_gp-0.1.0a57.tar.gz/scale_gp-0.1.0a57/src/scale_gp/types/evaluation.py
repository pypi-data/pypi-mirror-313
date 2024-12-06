# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .annotation_config import AnnotationConfig

__all__ = ["Evaluation"]


class Evaluation(BaseModel):
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

    application_variant_id: Optional[str] = None

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    completed_at: Optional[datetime] = None
    """
    The date and time that all test case results for the evaluation were completed
    for the evaluation in ISO format.
    """

    evaluation_config: Optional[object] = None

    evaluation_config_id: Optional[str] = None
    """The ID of the associated evaluation config."""

    question_id_to_annotation_config: Optional[Dict[str, AnnotationConfig]] = None
    """Specifies the annotation configuration to use for specific questions."""

    tags: Optional[object] = None
