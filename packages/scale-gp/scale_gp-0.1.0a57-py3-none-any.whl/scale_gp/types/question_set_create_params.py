# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List
from typing_extensions import Required, TypedDict

__all__ = ["QuestionSetCreateParams", "QuestionIDToConfig"]


class QuestionSetCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    name: Required[str]

    question_ids: Required[List[str]]
    """IDs of questions in the question set"""

    instructions: str
    """Instructions to answer questions"""

    question_id_to_config: Dict[str, QuestionIDToConfig]
    """
    Specifies additional configurations to use for specific questions in the context
    of the question set. For example,
    `{<question_a_id>: {required: true}, <question_b_id>: {required: true}}` sets
    two questions as required.
    """


class QuestionIDToConfig(TypedDict, total=False):
    required: bool
    """Whether the question is required. False by default."""
