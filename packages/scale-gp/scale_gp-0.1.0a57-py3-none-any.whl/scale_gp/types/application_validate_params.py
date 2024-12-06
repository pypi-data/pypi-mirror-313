# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Iterable
from typing_extensions import Literal, Required, TypedDict

from .application_edge_param import ApplicationEdgeParam
from .application_node_param import ApplicationNodeParam

__all__ = ["ApplicationValidateParams", "Overrides"]


class ApplicationValidateParams(TypedDict, total=False):
    edges: Required[Iterable[ApplicationEdgeParam]]
    """List of edges in the application graph"""

    nodes: Required[Iterable[ApplicationNodeParam]]
    """List of nodes in the application graph"""

    version: Required[Literal["V0"]]
    """Version of the application schema"""

    overrides: Dict[str, Overrides]
    """Optional overrides for the application"""


class Overrides(TypedDict, total=False):
    artifact_ids_filter: List[str]

    artifact_name_regex: List[str]

    type: Literal["knowledge_base_schema"]
