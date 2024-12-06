# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["QuestionCreateParams", "Choice", "NumberOptions", "RatingOptions"]


class QuestionCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    prompt: Required[str]

    title: Required[str]

    type: Required[Literal["categorical", "free_text", "rating", "number"]]
    """The type of question"""

    choices: Iterable[Choice]
    """List of choices for the question. Required for CATEGORICAL questions."""

    conditions: Iterable[object]
    """Conditions for the question to be shown."""

    dropdown: bool
    """Whether the question is displayed as a dropdown in the UI."""

    multi: bool
    """Whether the question allows multiple answers."""

    number_options: Annotated[NumberOptions, PropertyInfo(alias="numberOptions")]
    """Options for number questions."""

    rating_options: Annotated[RatingOptions, PropertyInfo(alias="ratingOptions")]
    """Options for rating questions."""

    required: bool
    """
    [To be deprecated in favor of question set question_id_to_config] Whether the
    question is required.
    """


class Choice(TypedDict, total=False):
    label: Required[str]

    value: Required[Union[str, bool, float]]

    audit_required: bool


class NumberOptions(TypedDict, total=False):
    max: float
    """Maximum value for the number"""

    min: float
    """Minimum value for the number"""


class RatingOptions(TypedDict, total=False):
    max_label: Required[Annotated[str, PropertyInfo(alias="maxLabel")]]
    """Maximum value for the rating"""

    min_label: Required[Annotated[str, PropertyInfo(alias="minLabel")]]
    """Minimum value for the rating"""

    scale_steps: Required[Annotated[int, PropertyInfo(alias="scaleSteps")]]
    """Number of steps in the rating scale"""
