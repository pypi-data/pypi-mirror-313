# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._compat import PYDANTIC_V2
from .._models import BaseModel
from .application_configuration import ApplicationConfiguration
from .application_agent_graph_node import ApplicationAgentGraphNode

__all__ = [
    "PaginatedApplicationVariants",
    "Item",
    "ItemApplicationVariantV0Response",
    "ItemApplicationVariantAgentsServiceResponse",
    "ItemApplicationVariantAgentsServiceResponseConfiguration",
    "ItemApplicationVariantAgentsServiceResponseConfigurationGraph",
    "ItemApplicationVariantAgentsServiceResponseConfigurationGraphEdge",
    "ItemApplicationVariantAgentsServiceResponseConfigurationInput",
    "ItemOfflineApplicationVariantResponse",
    "ItemOfflineApplicationVariantResponseConfiguration",
]


class ItemApplicationVariantV0Response(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    configuration: ApplicationConfiguration

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    name: str

    version: Literal["V0"]

    created_by_user_id: Optional[str] = None
    """The user who originally created the entity."""

    description: Optional[str] = None
    """Optional description of the application variant"""


class ItemApplicationVariantAgentsServiceResponseConfigurationGraphEdge(BaseModel):
    from_node: str

    to_node: str


class ItemApplicationVariantAgentsServiceResponseConfigurationGraph(BaseModel):
    edges: List[ItemApplicationVariantAgentsServiceResponseConfigurationGraphEdge]

    nodes: List[ApplicationAgentGraphNode]


class ItemApplicationVariantAgentsServiceResponseConfigurationInput(BaseModel):
    name: str

    type: Literal[
        "ShortText",
        "SentenceText",
        "ParagraphText",
        "ArtifactId",
        "ArtifactIds",
        "KnowledgeBaseId",
        "KnowledgeBaseIds",
        "InputImageDir",
        "Message",
        "Messages",
        "integer",
        "number",
        "string",
        "boolean",
        "array",
        "object",
        "unknown",
    ]

    description: Optional[str] = None

    required: Optional[bool] = None

    title: Optional[str] = None


class ItemApplicationVariantAgentsServiceResponseConfiguration(BaseModel):
    params: object

    type: Literal["WORKFLOW", "PLAN", "STATE_MACHINE"]

    graph: Optional[ItemApplicationVariantAgentsServiceResponseConfigurationGraph] = None
    """The graph of the agents service configuration"""

    inputs: Optional[List[ItemApplicationVariantAgentsServiceResponseConfigurationInput]] = None
    """The starting inputs that this agent configuration expects"""

    metadata: Optional[object] = None
    """User defined metadata about the application"""


class ItemApplicationVariantAgentsServiceResponse(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    configuration: ItemApplicationVariantAgentsServiceResponseConfiguration

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    name: str

    version: Literal["AGENTS_SERVICE"]

    created_by_user_id: Optional[str] = None
    """The user who originally created the entity."""

    description: Optional[str] = None
    """Optional description of the application variant"""


class ItemOfflineApplicationVariantResponseConfiguration(BaseModel):
    metadata: Optional[object] = None
    """User defined metadata about the offline application"""


class ItemOfflineApplicationVariantResponse(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    configuration: ItemOfflineApplicationVariantResponseConfiguration

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    name: str

    version: Literal["OFFLINE"]

    created_by_user_id: Optional[str] = None
    """The user who originally created the entity."""

    description: Optional[str] = None
    """Optional description of the application variant"""


Item: TypeAlias = Annotated[
    Union[
        ItemApplicationVariantV0Response,
        ItemApplicationVariantAgentsServiceResponse,
        ItemOfflineApplicationVariantResponse,
    ],
    PropertyInfo(discriminator="version"),
]


class PaginatedApplicationVariants(BaseModel):
    current_page: int
    """The current page number."""

    items: List[Item]
    """The data returned for the current page."""

    items_per_page: int
    """The number of items per page."""

    total_item_count: int
    """The total number of items of the query"""


if PYDANTIC_V2:
    PaginatedApplicationVariants.model_rebuild()
    ItemApplicationVariantV0Response.model_rebuild()
    ItemApplicationVariantAgentsServiceResponse.model_rebuild()
    ItemApplicationVariantAgentsServiceResponseConfiguration.model_rebuild()
    ItemApplicationVariantAgentsServiceResponseConfigurationGraph.model_rebuild()
    ItemApplicationVariantAgentsServiceResponseConfigurationGraphEdge.model_rebuild()
    ItemApplicationVariantAgentsServiceResponseConfigurationInput.model_rebuild()
    ItemOfflineApplicationVariantResponse.model_rebuild()
    ItemOfflineApplicationVariantResponseConfiguration.model_rebuild()
else:
    PaginatedApplicationVariants.update_forward_refs()  # type: ignore
    ItemApplicationVariantV0Response.update_forward_refs()  # type: ignore
    ItemApplicationVariantAgentsServiceResponse.update_forward_refs()  # type: ignore
    ItemApplicationVariantAgentsServiceResponseConfiguration.update_forward_refs()  # type: ignore
    ItemApplicationVariantAgentsServiceResponseConfigurationGraph.update_forward_refs()  # type: ignore
    ItemApplicationVariantAgentsServiceResponseConfigurationGraphEdge.update_forward_refs()  # type: ignore
    ItemApplicationVariantAgentsServiceResponseConfigurationInput.update_forward_refs()  # type: ignore
    ItemOfflineApplicationVariantResponse.update_forward_refs()  # type: ignore
    ItemOfflineApplicationVariantResponseConfiguration.update_forward_refs()  # type: ignore
