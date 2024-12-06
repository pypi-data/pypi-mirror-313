# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .application_configuration_param import ApplicationConfigurationParam
from .application_agent_graph_node_param import ApplicationAgentGraphNodeParam

__all__ = [
    "ApplicationVariantCreateParams",
    "ApplicationVariantV0Request",
    "ApplicationVariantAgentsServiceRequest",
    "ApplicationVariantAgentsServiceRequestConfiguration",
    "ApplicationVariantAgentsServiceRequestConfigurationGraph",
    "ApplicationVariantAgentsServiceRequestConfigurationGraphEdge",
    "ApplicationVariantAgentsServiceRequestConfigurationInput",
    "OfflineApplicationVariantRequest",
    "OfflineApplicationVariantRequestConfiguration",
]


class ApplicationVariantV0Request(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_spec_id: Required[str]

    configuration: Required[ApplicationConfigurationParam]

    name: Required[str]

    version: Required[Literal["V0"]]

    description: str
    """Optional description of the application variant"""


class ApplicationVariantAgentsServiceRequest(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_spec_id: Required[str]

    configuration: Required[ApplicationVariantAgentsServiceRequestConfiguration]

    name: Required[str]

    version: Required[Literal["AGENTS_SERVICE"]]

    description: str
    """Optional description of the application variant"""


class ApplicationVariantAgentsServiceRequestConfigurationGraphEdge(TypedDict, total=False):
    from_node: Required[str]

    to_node: Required[str]


class ApplicationVariantAgentsServiceRequestConfigurationGraph(TypedDict, total=False):
    edges: Required[Iterable[ApplicationVariantAgentsServiceRequestConfigurationGraphEdge]]

    nodes: Required[Iterable[ApplicationAgentGraphNodeParam]]


class ApplicationVariantAgentsServiceRequestConfigurationInput(TypedDict, total=False):
    name: Required[str]

    type: Required[
        Literal[
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
    ]

    description: str

    required: bool

    title: str


class ApplicationVariantAgentsServiceRequestConfiguration(TypedDict, total=False):
    params: Required[object]

    type: Required[Literal["WORKFLOW", "PLAN", "STATE_MACHINE"]]

    graph: ApplicationVariantAgentsServiceRequestConfigurationGraph
    """The graph of the agents service configuration"""

    inputs: Iterable[ApplicationVariantAgentsServiceRequestConfigurationInput]
    """The starting inputs that this agent configuration expects"""

    metadata: object
    """User defined metadata about the application"""


class OfflineApplicationVariantRequest(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_spec_id: Required[str]

    configuration: Required[OfflineApplicationVariantRequestConfiguration]

    name: Required[str]

    version: Required[Literal["OFFLINE"]]

    description: str
    """Optional description of the application variant"""


class OfflineApplicationVariantRequestConfiguration(TypedDict, total=False):
    metadata: object
    """User defined metadata about the offline application"""


ApplicationVariantCreateParams: TypeAlias = Union[
    ApplicationVariantV0Request, ApplicationVariantAgentsServiceRequest, OfflineApplicationVariantRequest
]
