# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from ..result_schema_flexible import ResultSchemaFlexible
from ..shared.result_schema_generation import ResultSchemaGeneration

__all__ = ["TestCaseResult", "GenerationTestCaseResultResponse", "FlexibleTestCaseResultResponse"]


class GenerationTestCaseResultResponse(BaseModel):
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

    application_test_case_output_id: Optional[str] = None

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    audit_comment: Optional[str] = None

    audit_required: Optional[bool] = None

    audit_status: Optional[Literal["UNAUDITED", "FIXED", "APPROVED"]] = None

    completed_at: Optional[datetime] = None

    result: Optional[Dict[str, Union[str, bool, float, List[Union[str, bool, float]]]]] = None
    """
    The result of the test case evaluation, in JSON form where the key is the
    question ID and the value is the result.
    """

    test_case_evaluation_data_schema: Optional[Literal["GENERATION"]] = None

    time_spent_labeling_s: Optional[int] = None
    """The time spent labeling in seconds."""


class FlexibleTestCaseResultResponse(BaseModel):
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

    application_test_case_output_id: Optional[str] = None

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    audit_comment: Optional[str] = None

    audit_required: Optional[bool] = None

    audit_status: Optional[Literal["UNAUDITED", "FIXED", "APPROVED"]] = None

    completed_at: Optional[datetime] = None

    result: Optional[Dict[str, Union[str, bool, float, List[Union[str, bool, float]]]]] = None
    """
    The result of the test case evaluation, in JSON form where the key is the
    question ID and the value is the result.
    """

    test_case_evaluation_data_schema: Optional[Literal["FLEXIBLE"]] = None

    time_spent_labeling_s: Optional[int] = None
    """The time spent labeling in seconds."""


TestCaseResult: TypeAlias = Annotated[
    Union[GenerationTestCaseResultResponse, FlexibleTestCaseResultResponse],
    PropertyInfo(discriminator="test_case_evaluation_data_schema"),
]
