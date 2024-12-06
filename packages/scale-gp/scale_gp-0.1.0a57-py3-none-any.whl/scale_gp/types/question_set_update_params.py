# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["QuestionSetUpdateParams", "PartialQuestionSetRequest", "RestoreRequest"]


class PartialQuestionSetRequest(TypedDict, total=False):
    instructions: str
    """Instructions to answer questions"""

    name: str

    question_ids: List[str]
    """IDs of questions in the question set"""

    restore: Literal[False]
    """Set to true to restore the entity from the database."""


class RestoreRequest(TypedDict, total=False):
    restore: Required[Literal[True]]
    """Set to true to restore the entity from the database."""


QuestionSetUpdateParams: TypeAlias = Union[PartialQuestionSetRequest, RestoreRequest]
