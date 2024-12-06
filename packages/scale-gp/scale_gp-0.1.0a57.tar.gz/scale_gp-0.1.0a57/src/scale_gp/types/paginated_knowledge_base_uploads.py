# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .s3_data_source_config import S3DataSourceConfig
from .local_file_source_config import LocalFileSourceConfig
from .slack_data_source_config import SlackDataSourceConfig
from .local_chunks_source_config import LocalChunksSourceConfig
from .confluence_data_source_config import ConfluenceDataSourceConfig
from .share_point_data_source_config import SharePointDataSourceConfig
from .token_chunking_strategy_config import TokenChunkingStrategyConfig
from .custom_chunking_strategy_config import CustomChunkingStrategyConfig
from .google_drive_data_source_config import GoogleDriveDataSourceConfig
from .character_chunking_strategy_config import CharacterChunkingStrategyConfig
from .azure_blob_storage_data_source_config import AzureBlobStorageDataSourceConfig

__all__ = [
    "PaginatedKnowledgeBaseUploads",
    "Item",
    "ItemDataSourceConfig",
    "ItemChunkingStrategyConfig",
    "ItemChunkingStrategyConfigPreChunkedStrategyConfig",
]

ItemDataSourceConfig: TypeAlias = Annotated[
    Union[
        S3DataSourceConfig,
        SharePointDataSourceConfig,
        GoogleDriveDataSourceConfig,
        AzureBlobStorageDataSourceConfig,
        LocalChunksSourceConfig,
        LocalFileSourceConfig,
        ConfluenceDataSourceConfig,
        SlackDataSourceConfig,
    ],
    PropertyInfo(discriminator="source"),
]


class ItemChunkingStrategyConfigPreChunkedStrategyConfig(BaseModel):
    strategy: Literal["pre_chunked"]


ItemChunkingStrategyConfig: TypeAlias = Annotated[
    Union[
        CharacterChunkingStrategyConfig,
        TokenChunkingStrategyConfig,
        CustomChunkingStrategyConfig,
        ItemChunkingStrategyConfigPreChunkedStrategyConfig,
    ],
    PropertyInfo(discriminator="strategy"),
]


class Item(BaseModel):
    id: str

    data_source_config: ItemDataSourceConfig

    knowledge_base_id: str

    chunking_strategy_config: Optional[ItemChunkingStrategyConfig] = None
    """Only compliant with the .chunks file type"""

    created_at: Union[str, datetime, None] = None

    created_by_schedule_id: Optional[str] = None

    data_source_idempotency_key: Optional[str] = None

    status: Optional[str] = None

    status_reason: Optional[str] = None

    updated_at: Union[str, datetime, None] = None


class PaginatedKnowledgeBaseUploads(BaseModel):
    current_page: int
    """The current page number."""

    items: List[Item]
    """The data returned for the current page."""

    items_per_page: int
    """The number of items per page."""

    total_item_count: int
    """The total number of items of the query"""
