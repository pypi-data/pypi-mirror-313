# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, TypedDict

__all__ = ["ScalarRetrieveParams"]


class ScalarRetrieveParams(TypedDict, total=False):
    application_spec_id: Required[str]

    account_id: Optional[str]
    """Account ID used for authorization"""

    from_ts: int
    """The starting (oldest) timestamp window in seconds."""

    to_ts: int
    """The ending (most recent) timestamp in seconds."""

    variants: Optional[List[str]]
    """Which variants to filter on"""
