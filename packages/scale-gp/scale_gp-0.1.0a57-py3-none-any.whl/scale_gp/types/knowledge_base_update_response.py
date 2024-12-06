# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["KnowledgeBaseUpdateResponse"]


class KnowledgeBaseUpdateResponse(BaseModel):
    knowledge_base_name: Optional[str] = None
    """The name of the knowledge base"""

    metadata: Optional[object] = None
    """Metadata associated with the knowledge base"""
