# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["File"]


class File(BaseModel):
    id: str

    created_at: datetime

    created_by_user_id: str

    filename: str

    md5_checksum: str

    mime_type: str

    size: int

    object: Optional[Literal["file"]] = None
