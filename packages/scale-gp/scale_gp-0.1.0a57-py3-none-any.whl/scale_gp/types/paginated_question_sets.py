# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime

from .._models import BaseModel
from .question import Question

__all__ = ["PaginatedQuestionSets", "Item", "ItemQuestionIDToConfig"]


class ItemQuestionIDToConfig(BaseModel):
    required: Optional[bool] = None
    """Whether the question is required. False by default."""


class Item(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    name: str

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    instructions: Optional[str] = None
    """Instructions to answer questions"""

    question_id_to_config: Optional[Dict[str, ItemQuestionIDToConfig]] = None
    """
    Specifies additional configurations to use for specific questions in the context
    of the question set. For example,
    `{<question_a_id>: {required: true}, <question_b_id>: {required: true}}` sets
    two questions as required.
    """

    questions: Optional[List[Question]] = None


class PaginatedQuestionSets(BaseModel):
    current_page: int
    """The current page number."""

    items: List[Item]
    """The data returned for the current page."""

    items_per_page: int
    """The number of items per page."""

    total_item_count: int
    """The total number of items of the query"""
