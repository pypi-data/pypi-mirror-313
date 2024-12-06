# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["CustomChunkingStrategyConfigParam"]


class CustomChunkingStrategyConfigParam(TypedDict, total=False):
    endpoint: Required[str]
    """Endpoint path to call for custom chunking"""

    strategy: Required[Literal["custom"]]

    params: object
    """Parameters that will be appended to the body of the request for the chunk."""
