# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .s3_data_source_config_param import S3DataSourceConfigParam
from .slack_data_source_config_param import SlackDataSourceConfigParam
from .s3_data_source_auth_config_param import S3DataSourceAuthConfigParam
from .confluence_data_source_config_param import ConfluenceDataSourceConfigParam
from .slack_data_source_auth_config_param import SlackDataSourceAuthConfigParam
from .share_point_data_source_config_param import SharePointDataSourceConfigParam
from .google_drive_data_source_config_param import GoogleDriveDataSourceConfigParam
from .confluence_data_source_auth_config_param import ConfluenceDataSourceAuthConfigParam
from .share_point_data_source_auth_config_param import SharePointDataSourceAuthConfigParam
from .google_drive_data_source_auth_config_param import GoogleDriveDataSourceAuthConfigParam
from .azure_blob_storage_data_source_config_param import AzureBlobStorageDataSourceConfigParam
from .azure_blob_storage_data_source_auth_config_param import AzureBlobStorageDataSourceAuthConfigParam

__all__ = ["KnowledgeBaseDataSourceCreateParams", "DataSourceConfig", "DataSourceAuthConfig", "TaggingInformation"]


class KnowledgeBaseDataSourceCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    data_source_config: Required[DataSourceConfig]

    name: Required[str]

    data_source_auth_config: DataSourceAuthConfig

    description: str

    tagging_information: TaggingInformation


DataSourceConfig: TypeAlias = Union[
    S3DataSourceConfigParam,
    SharePointDataSourceConfigParam,
    GoogleDriveDataSourceConfigParam,
    AzureBlobStorageDataSourceConfigParam,
    ConfluenceDataSourceConfigParam,
    SlackDataSourceConfigParam,
]

DataSourceAuthConfig: TypeAlias = Union[
    SharePointDataSourceAuthConfigParam,
    AzureBlobStorageDataSourceAuthConfigParam,
    GoogleDriveDataSourceAuthConfigParam,
    S3DataSourceAuthConfigParam,
    ConfluenceDataSourceAuthConfigParam,
    SlackDataSourceAuthConfigParam,
]


class TaggingInformation(TypedDict, total=False):
    tags_to_apply: object

    type: Literal["all"]
