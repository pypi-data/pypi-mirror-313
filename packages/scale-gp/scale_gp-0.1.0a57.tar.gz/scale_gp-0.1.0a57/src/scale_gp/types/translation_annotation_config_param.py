# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

__all__ = ["TranslationAnnotationConfigParam"]


class TranslationAnnotationConfigParam(TypedDict, total=False):
    original_text_loc: Required[List[str]]

    translation_loc: Required[List[str]]

    expected_translation_loc: List[str]
