# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, TypedDict

__all__ = ["KnowledgeBaseRetrieveParams"]


class KnowledgeBaseRetrieveParams(TypedDict, total=False):
    include_artifacts_status: bool
    """Optional query parameter to include a count of artifacts by status"""

    view: Optional[List[Literal["Connections", "ArtifactCount"]]]
