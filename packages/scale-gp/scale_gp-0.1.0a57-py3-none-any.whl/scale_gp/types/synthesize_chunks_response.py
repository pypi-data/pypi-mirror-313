# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["SynthesizeChunksResponse", "SourceNode", "SourceNodeNode", "SourceNodeNodeRelationships"]


class SourceNodeNodeRelationships(BaseModel):
    hash: str

    metadata: object

    node_id: str

    node_type: Optional[str] = None


class SourceNodeNode(BaseModel):
    text: str

    embedding: Optional[List[float]] = None

    end_char_idx: Optional[int] = None

    extra_info: Optional[object] = None

    hash: Optional[str] = None

    id: Optional[str] = FieldInfo(alias="id_", default=None)

    relationships: Optional[Dict[str, SourceNodeNodeRelationships]] = None

    start_char_idx: Optional[int] = None


class SourceNode(BaseModel):
    node: SourceNodeNode

    score: float


class SynthesizeChunksResponse(BaseModel):
    response: str
    """Natural language response addressing the query."""

    metadata: Optional[Dict[str, object]] = None
    """Optional metadata present on each chunk."""

    source_nodes: Optional[List[SourceNode]] = None
    """List of chunks used to synthesize the response."""
