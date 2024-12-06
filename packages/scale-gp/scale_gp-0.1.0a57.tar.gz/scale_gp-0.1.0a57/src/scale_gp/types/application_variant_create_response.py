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
    "ApplicationVariantCreateResponse",
    "ApplicationVariantV0Response",
    "ApplicationVariantAgentsServiceResponse",
    "ApplicationVariantAgentsServiceResponseConfiguration",
    "ApplicationVariantAgentsServiceResponseConfigurationGraph",
    "ApplicationVariantAgentsServiceResponseConfigurationGraphEdge",
    "ApplicationVariantAgentsServiceResponseConfigurationInput",
    "OfflineApplicationVariantResponse",
    "OfflineApplicationVariantResponseConfiguration",
]


class ApplicationVariantV0Response(BaseModel):
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


class ApplicationVariantAgentsServiceResponseConfigurationGraphEdge(BaseModel):
    from_node: str

    to_node: str


class ApplicationVariantAgentsServiceResponseConfigurationGraph(BaseModel):
    edges: List[ApplicationVariantAgentsServiceResponseConfigurationGraphEdge]

    nodes: List[ApplicationAgentGraphNode]


class ApplicationVariantAgentsServiceResponseConfigurationInput(BaseModel):
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


class ApplicationVariantAgentsServiceResponseConfiguration(BaseModel):
    params: object

    type: Literal["WORKFLOW", "PLAN", "STATE_MACHINE"]

    graph: Optional[ApplicationVariantAgentsServiceResponseConfigurationGraph] = None
    """The graph of the agents service configuration"""

    inputs: Optional[List[ApplicationVariantAgentsServiceResponseConfigurationInput]] = None
    """The starting inputs that this agent configuration expects"""

    metadata: Optional[object] = None
    """User defined metadata about the application"""


class ApplicationVariantAgentsServiceResponse(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    configuration: ApplicationVariantAgentsServiceResponseConfiguration

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    name: str

    version: Literal["AGENTS_SERVICE"]

    created_by_user_id: Optional[str] = None
    """The user who originally created the entity."""

    description: Optional[str] = None
    """Optional description of the application variant"""


class OfflineApplicationVariantResponseConfiguration(BaseModel):
    metadata: Optional[object] = None
    """User defined metadata about the offline application"""


class OfflineApplicationVariantResponse(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    configuration: OfflineApplicationVariantResponseConfiguration

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    name: str

    version: Literal["OFFLINE"]

    created_by_user_id: Optional[str] = None
    """The user who originally created the entity."""

    description: Optional[str] = None
    """Optional description of the application variant"""


ApplicationVariantCreateResponse: TypeAlias = Annotated[
    Union[ApplicationVariantV0Response, ApplicationVariantAgentsServiceResponse, OfflineApplicationVariantResponse],
    PropertyInfo(discriminator="version"),
]

if PYDANTIC_V2:
    ApplicationVariantV0Response.model_rebuild()
    ApplicationVariantAgentsServiceResponse.model_rebuild()
    ApplicationVariantAgentsServiceResponseConfiguration.model_rebuild()
    ApplicationVariantAgentsServiceResponseConfigurationGraph.model_rebuild()
    ApplicationVariantAgentsServiceResponseConfigurationGraphEdge.model_rebuild()
    ApplicationVariantAgentsServiceResponseConfigurationInput.model_rebuild()
    OfflineApplicationVariantResponse.model_rebuild()
    OfflineApplicationVariantResponseConfiguration.model_rebuild()
else:
    ApplicationVariantV0Response.update_forward_refs()  # type: ignore
    ApplicationVariantAgentsServiceResponse.update_forward_refs()  # type: ignore
    ApplicationVariantAgentsServiceResponseConfiguration.update_forward_refs()  # type: ignore
    ApplicationVariantAgentsServiceResponseConfigurationGraph.update_forward_refs()  # type: ignore
    ApplicationVariantAgentsServiceResponseConfigurationGraphEdge.update_forward_refs()  # type: ignore
    ApplicationVariantAgentsServiceResponseConfigurationInput.update_forward_refs()  # type: ignore
    OfflineApplicationVariantResponse.update_forward_refs()  # type: ignore
    OfflineApplicationVariantResponseConfiguration.update_forward_refs()  # type: ignore
