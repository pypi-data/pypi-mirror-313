# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

__all__ = ["SummarizationAnnotationConfigParam"]


class SummarizationAnnotationConfigParam(TypedDict, total=False):
    document_loc: Required[List[str]]

    summary_loc: Required[List[str]]

    expected_summary_loc: List[str]
