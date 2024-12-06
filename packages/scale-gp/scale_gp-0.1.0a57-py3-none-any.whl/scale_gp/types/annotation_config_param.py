# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["AnnotationConfigParam", "Component"]


class Component(TypedDict, total=False):
    data_loc: Required[List[str]]

    label: str

    optional: bool


class AnnotationConfigParam(TypedDict, total=False):
    components: Required[Iterable[Iterable[Component]]]

    annotation_config_type: Literal["flexible", "summarization", "multiturn", "translation"]

    direction: Literal["col", "row"]
