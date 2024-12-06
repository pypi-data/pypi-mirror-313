# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ArtifactListResponse", "ChunksStatus"]


class ChunksStatus(BaseModel):
    chunks_completed: int

    chunks_failed: int

    chunks_pending: int


class ArtifactListResponse(BaseModel):
    artifact_id: str

    artifact_name: str

    artifact_uri: str

    chunks_status: ChunksStatus

    source: Literal[
        "S3", "SharePoint", "LocalFile", "LocalChunks", "GoogleDrive", "AzureBlobStorage", "Confluence", "Slack"
    ]

    status: Literal["Pending", "Chunking", "Uploading", "Completed", "Failed", "Deleting", "Canceled", "Embedding"]

    artifact_uri_public: Optional[str] = None

    created_at: Optional[datetime] = None

    status_reason: Optional[str] = None

    tags: Optional[object] = None

    updated_at: Optional[datetime] = None
