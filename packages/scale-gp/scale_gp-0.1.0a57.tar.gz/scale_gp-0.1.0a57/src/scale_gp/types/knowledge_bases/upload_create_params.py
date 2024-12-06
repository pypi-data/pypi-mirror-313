# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..s3_data_source_config_param import S3DataSourceConfigParam
from ..slack_data_source_config_param import SlackDataSourceConfigParam
from ..local_chunks_source_config_param import LocalChunksSourceConfigParam
from ..s3_data_source_auth_config_param import S3DataSourceAuthConfigParam
from ..confluence_data_source_config_param import ConfluenceDataSourceConfigParam
from ..slack_data_source_auth_config_param import SlackDataSourceAuthConfigParam
from ..share_point_data_source_config_param import SharePointDataSourceConfigParam
from ..token_chunking_strategy_config_param import TokenChunkingStrategyConfigParam
from ..custom_chunking_strategy_config_param import CustomChunkingStrategyConfigParam
from ..google_drive_data_source_config_param import GoogleDriveDataSourceConfigParam
from ..character_chunking_strategy_config_param import CharacterChunkingStrategyConfigParam
from ..confluence_data_source_auth_config_param import ConfluenceDataSourceAuthConfigParam
from ..share_point_data_source_auth_config_param import SharePointDataSourceAuthConfigParam
from ..google_drive_data_source_auth_config_param import GoogleDriveDataSourceAuthConfigParam
from ..azure_blob_storage_data_source_config_param import AzureBlobStorageDataSourceConfigParam
from ..azure_blob_storage_data_source_auth_config_param import AzureBlobStorageDataSourceAuthConfigParam

__all__ = [
    "UploadCreateParams",
    "CreateKnowledgeBaseV2UploadFromDataSourceRequest",
    "CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceConfig",
    "CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfig",
    "CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfigPreChunkedStrategyConfig",
    "CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceAuthConfig",
    "CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformation",
    "CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformationTaggingInformationPerFile",
    "CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformationTaggingInformationAll",
    "CreateKnowledgeBaseV2UploadFromLocalChunksRequest",
    "CreateKnowledgeBaseV2UploadFromLocalChunksRequestChunk",
    "CreateKnowledgeBaseV2UploadFromLocalChunksRequestTaggingInformation",
    "CreateKnowledgeBaseV2UploadFromLocalChunksRequestTaggingInformationTaggingInformationPerFile",
    "CreateKnowledgeBaseV2UploadFromLocalChunksRequestTaggingInformationTaggingInformationAll",
    "CreateKnowledgeBaseV2UploadFromDataSourceIDRequest",
    "CreateKnowledgeBaseV2UploadFromDataSourceIDRequestChunkingStrategyConfig",
    "CreateKnowledgeBaseV2UploadFromDataSourceIDRequestChunkingStrategyConfigPreChunkedStrategyConfig",
    "CreateKnowledgeBaseV2UploadFromDataSourceIDRequestTaggingInformation",
    "CreateKnowledgeBaseV2UploadFromDataSourceIDRequestTaggingInformationTaggingInformationPerFile",
    "CreateKnowledgeBaseV2UploadFromDataSourceIDRequestTaggingInformationTaggingInformationAll",
]


class CreateKnowledgeBaseV2UploadFromDataSourceRequest(TypedDict, total=False):
    data_source_config: Required[CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceConfig]
    """Configuration for the data source which describes where to find the data."""

    chunking_strategy_config: CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfig
    """Configuration for the chunking strategy which describes how to chunk the data."""

    data_source_auth_config: CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceAuthConfig
    """
    Configuration for the data source which describes how to authenticate to the
    data source.
    """

    force_reupload: bool
    """Force reingest, regardless the change of the source file."""

    tagging_information: CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformation
    """A dictionary of tags to apply to all artifacts added from the data source."""


CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceConfig: TypeAlias = Union[
    S3DataSourceConfigParam,
    SharePointDataSourceConfigParam,
    GoogleDriveDataSourceConfigParam,
    AzureBlobStorageDataSourceConfigParam,
    ConfluenceDataSourceConfigParam,
    SlackDataSourceConfigParam,
]


class CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfigPreChunkedStrategyConfig(
    TypedDict, total=False
):
    strategy: Required[Literal["pre_chunked"]]


CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfig: TypeAlias = Union[
    CharacterChunkingStrategyConfigParam,
    TokenChunkingStrategyConfigParam,
    CustomChunkingStrategyConfigParam,
    CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfigPreChunkedStrategyConfig,
]

CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceAuthConfig: TypeAlias = Union[
    SharePointDataSourceAuthConfigParam,
    AzureBlobStorageDataSourceAuthConfigParam,
    GoogleDriveDataSourceAuthConfigParam,
    S3DataSourceAuthConfigParam,
    ConfluenceDataSourceAuthConfigParam,
    SlackDataSourceAuthConfigParam,
]


class CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformationTaggingInformationPerFile(
    TypedDict, total=False
):
    tags_to_apply: Dict[str, Optional[object]]

    type: Literal["per_file"]


class CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformationTaggingInformationAll(TypedDict, total=False):
    tags_to_apply: object

    type: Literal["all"]


CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformation: TypeAlias = Union[
    CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformationTaggingInformationPerFile,
    CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformationTaggingInformationAll,
]


class CreateKnowledgeBaseV2UploadFromLocalChunksRequest(TypedDict, total=False):
    data_source_config: Required[LocalChunksSourceConfigParam]
    """Configuration for the data source which describes where to find the data."""

    chunks: Iterable[CreateKnowledgeBaseV2UploadFromLocalChunksRequestChunk]
    """List of chunks."""

    force_reupload: bool
    """Force reingest, regardless the change of the source file."""

    tagging_information: CreateKnowledgeBaseV2UploadFromLocalChunksRequestTaggingInformation
    """A dictionary of tags to apply to all artifacts added from the data source."""


class CreateKnowledgeBaseV2UploadFromLocalChunksRequestChunk(TypedDict, total=False):
    chunk_position: Required[int]
    """Position of the chunk in the artifact."""

    text: Required[str]
    """Associated text of the chunk."""

    metadata: object
    """Additional metadata associated with the chunk."""


class CreateKnowledgeBaseV2UploadFromLocalChunksRequestTaggingInformationTaggingInformationPerFile(
    TypedDict, total=False
):
    tags_to_apply: Dict[str, Optional[object]]

    type: Literal["per_file"]


class CreateKnowledgeBaseV2UploadFromLocalChunksRequestTaggingInformationTaggingInformationAll(TypedDict, total=False):
    tags_to_apply: object

    type: Literal["all"]


CreateKnowledgeBaseV2UploadFromLocalChunksRequestTaggingInformation: TypeAlias = Union[
    CreateKnowledgeBaseV2UploadFromLocalChunksRequestTaggingInformationTaggingInformationPerFile,
    CreateKnowledgeBaseV2UploadFromLocalChunksRequestTaggingInformationTaggingInformationAll,
]


class CreateKnowledgeBaseV2UploadFromDataSourceIDRequest(TypedDict, total=False):
    chunking_strategy_config: Required[CreateKnowledgeBaseV2UploadFromDataSourceIDRequestChunkingStrategyConfig]
    """Configuration for the chunking strategy which describes how to chunk the data."""

    data_source_id: Required[str]
    """Id of the data source to fetch."""

    force_reupload: bool
    """Force reingest, regardless the change of the source file."""

    tagging_information: CreateKnowledgeBaseV2UploadFromDataSourceIDRequestTaggingInformation
    """A dictionary of tags to apply to all artifacts added from the data source."""


class CreateKnowledgeBaseV2UploadFromDataSourceIDRequestChunkingStrategyConfigPreChunkedStrategyConfig(
    TypedDict, total=False
):
    strategy: Required[Literal["pre_chunked"]]


CreateKnowledgeBaseV2UploadFromDataSourceIDRequestChunkingStrategyConfig: TypeAlias = Union[
    CharacterChunkingStrategyConfigParam,
    TokenChunkingStrategyConfigParam,
    CustomChunkingStrategyConfigParam,
    CreateKnowledgeBaseV2UploadFromDataSourceIDRequestChunkingStrategyConfigPreChunkedStrategyConfig,
]


class CreateKnowledgeBaseV2UploadFromDataSourceIDRequestTaggingInformationTaggingInformationPerFile(
    TypedDict, total=False
):
    tags_to_apply: Dict[str, Optional[object]]

    type: Literal["per_file"]


class CreateKnowledgeBaseV2UploadFromDataSourceIDRequestTaggingInformationTaggingInformationAll(TypedDict, total=False):
    tags_to_apply: object

    type: Literal["all"]


CreateKnowledgeBaseV2UploadFromDataSourceIDRequestTaggingInformation: TypeAlias = Union[
    CreateKnowledgeBaseV2UploadFromDataSourceIDRequestTaggingInformationTaggingInformationPerFile,
    CreateKnowledgeBaseV2UploadFromDataSourceIDRequestTaggingInformationTaggingInformationAll,
]

UploadCreateParams: TypeAlias = Union[
    CreateKnowledgeBaseV2UploadFromDataSourceRequest,
    CreateKnowledgeBaseV2UploadFromLocalChunksRequest,
    CreateKnowledgeBaseV2UploadFromDataSourceIDRequest,
]
