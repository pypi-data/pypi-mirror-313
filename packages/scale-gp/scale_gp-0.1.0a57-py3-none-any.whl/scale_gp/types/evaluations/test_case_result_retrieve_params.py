# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["TestCaseResultRetrieveParams"]


class TestCaseResultRetrieveParams(TypedDict, total=False):
    evaluation_id: Required[str]

    view: Optional[List[Literal["AnnotationResults", "Metrics", "Task", "TestCaseVersion", "Trace"]]]
