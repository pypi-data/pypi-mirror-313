# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["EvaluationConfig"]


class EvaluationConfig(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    evaluation_type: Literal["studio", "llm_auto", "human", "llm_benchmark"]
    """Evaluation type"""

    question_set_id: str

    auto_evaluation_model: Optional[
        Literal["gpt-4-32k-0613", "gpt-4-turbo-preview", "gpt-4-turbo-2024-04-09", "llama-3-70b-instruct"]
    ] = None
    """The name of the model to be used for auto-evaluation"""

    studio_project_id: Optional[str] = None
