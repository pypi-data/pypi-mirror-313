# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypeAlias, TypedDict

__all__ = ["EvaluationClaimTaskParams", "ClaimTaskRequest", "Variant1"]


class ClaimTaskRequest(TypedDict, total=False):
    skip_current: bool


class Variant1(TypedDict, total=False):
    body: Required[None]


EvaluationClaimTaskParams: TypeAlias = Union[ClaimTaskRequest, Variant1]
