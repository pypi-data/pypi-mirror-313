# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from ..token_chunking_strategy_config import TokenChunkingStrategyConfig
from ..custom_chunking_strategy_config import CustomChunkingStrategyConfig
from ..character_chunking_strategy_config import CharacterChunkingStrategyConfig

__all__ = ["ArtifactUpdateResponse", "ChunkingStrategyConfig", "ChunkingStrategyConfigPreChunkedStrategyConfig"]


class ChunkingStrategyConfigPreChunkedStrategyConfig(BaseModel):
    strategy: Literal["pre_chunked"]


ChunkingStrategyConfig: TypeAlias = Annotated[
    Union[
        CharacterChunkingStrategyConfig,
        TokenChunkingStrategyConfig,
        CustomChunkingStrategyConfig,
        ChunkingStrategyConfigPreChunkedStrategyConfig,
    ],
    PropertyInfo(discriminator="strategy"),
]


class ArtifactUpdateResponse(BaseModel):
    artifact_name: str

    artifact_uri: str

    created_at: Union[str, datetime]

    knowledge_base_id: str

    source: Literal[
        "S3", "SharePoint", "LocalFile", "LocalChunks", "GoogleDrive", "AzureBlobStorage", "Confluence", "Slack"
    ]

    status: Literal["Pending", "Chunking", "Uploading", "Completed", "Failed", "Deleting", "Canceled", "Embedding"]

    updated_at: Union[str, datetime]

    artifact_id: Optional[str] = None

    artifact_uri_public: Optional[str] = None

    checkpoint: Optional[
        Literal["Pending", "Chunking", "Uploading", "Completed", "Failed", "Deleting", "Canceled", "Embedding"]
    ] = None

    chunking_strategy_config: Optional[ChunkingStrategyConfig] = None
    """Only compliant with the .chunks file type"""

    content_modification_identifier: Optional[str] = None

    deleted_at: Union[str, datetime, None] = None

    status_reason: Optional[str] = None

    tags: Optional[object] = None
