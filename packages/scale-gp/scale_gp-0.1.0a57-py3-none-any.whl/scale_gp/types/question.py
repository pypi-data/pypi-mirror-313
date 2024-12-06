# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["Question", "Choice", "NumberOptions", "RatingOptions"]


class Choice(BaseModel):
    label: str

    value: Union[str, bool, float]

    audit_required: Optional[bool] = None


class NumberOptions(BaseModel):
    max: Optional[float] = None
    """Maximum value for the number"""

    min: Optional[float] = None
    """Minimum value for the number"""


class RatingOptions(BaseModel):
    max_label: str = FieldInfo(alias="maxLabel")
    """Maximum value for the rating"""

    min_label: str = FieldInfo(alias="minLabel")
    """Minimum value for the rating"""

    scale_steps: int = FieldInfo(alias="scaleSteps")
    """Number of steps in the rating scale"""


class Question(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    prompt: str

    title: str

    type: Literal["categorical", "free_text", "rating", "number"]
    """The type of question"""

    choices: Optional[List[Choice]] = None
    """List of choices for the question. Required for CATEGORICAL questions."""

    conditions: Optional[List[object]] = None
    """Conditions for the question to be shown."""

    dropdown: Optional[bool] = None
    """Whether the question is displayed as a dropdown in the UI."""

    multi: Optional[bool] = None
    """Whether the question allows multiple answers."""

    number_options: Optional[NumberOptions] = FieldInfo(alias="numberOptions", default=None)
    """Options for number questions."""

    rating_options: Optional[RatingOptions] = FieldInfo(alias="ratingOptions", default=None)
    """Options for rating questions."""

    required: Optional[bool] = None
    """
    [To be deprecated in favor of question set question_id_to_config] Whether the
    question is required.
    """
