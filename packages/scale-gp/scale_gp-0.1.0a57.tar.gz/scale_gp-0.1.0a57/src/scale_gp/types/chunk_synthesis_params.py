# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from .shared_params.chunk import Chunk

__all__ = ["ChunkSynthesisParams"]


class ChunkSynthesisParams(TypedDict, total=False):
    chunks: Required[Iterable[Chunk]]
    """List of chunks to use to synthesize the response."""

    query: Required[str]
    """Natural language query to resolve using the supplied chunks."""
