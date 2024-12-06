# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

__all__ = ["ApplicationAgentGraphNodeParam", "Edge"]


class Edge(TypedDict, total=False):
    from_node: Required[str]

    to_node: Required[str]


class ApplicationAgentGraphNodeParam(TypedDict, total=False):
    id: Required[str]

    name: Required[str]

    type: Required[str]

    config: object

    edges: Iterable[Edge]

    nodes: Iterable[ApplicationAgentGraphNodeParam]
