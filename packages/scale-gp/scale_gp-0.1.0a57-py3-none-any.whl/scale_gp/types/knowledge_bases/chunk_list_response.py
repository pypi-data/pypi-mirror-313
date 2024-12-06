# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["ChunkListResponse"]


class ChunkListResponse(BaseModel):
    chunk_id: str
    """The unique ID of the chunk with embedding"""

    text: str
    """The text associated with the chunk"""

    attachment_url: Optional[str] = None
    """Original attachment URL from which this chunk got its data from"""

    embedding: Optional[List[float]] = None
    """The vector embedding of the text associated with the chunk"""

    metadata: Optional[object] = None
    """
    Any additional key value pairs of information stored by you on the chunk with
    embedding
    """

    title: Optional[str] = None
    """Title for this chunk, for example the file name"""

    user_supplied_metadata: Optional[object] = None
    """
    Any additional key value pairs of information returned from the custom chunking.
    """
