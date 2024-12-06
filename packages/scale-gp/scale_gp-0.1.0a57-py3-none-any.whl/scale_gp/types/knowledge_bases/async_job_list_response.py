# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["AsyncJobListResponse"]


class AsyncJobListResponse(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    job_type: Literal[
        "evaluation-auto-eval",
        "evaluation-test-cases-result-gen",
        "evaluation-builder",
        "evaluation-dataset-generation",
        "knowledge_base_upload",
        "application-variant-report-generation",
        "application-interaction-evaluation",
    ]

    status: str

    updated_at: datetime
    """The date and time when the entity was last updated in ISO format."""

    created_by_user_id: Optional[str] = None
    """The user who originally created the entity."""

    job_metadata: Optional[object] = None

    parent_job_id: Optional[str] = None

    progress: Optional[object] = None

    if TYPE_CHECKING:
        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
