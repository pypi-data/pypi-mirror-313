# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from ..chat_thread import ChatThread
from .chat_threads.chat_thread_feedback import ChatThreadFeedback

__all__ = ["ChatThreadHistory", "Message", "MessageEntry"]


class MessageEntry(BaseModel):
    id: str

    aggregated: bool
    """
    Boolean of whether this interaction has been uploaded to s3 bucket yet, default
    is false
    """

    application_spec_id: str

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    duration_ms: int
    """How much time the step took in milliseconds(ms)"""

    input: object

    operation_status: Literal["SUCCESS", "ERROR"]
    """The outcome of the operation"""

    output: object

    start_timestamp: datetime

    chat_thread_id: Optional[str] = None

    interaction_source: Optional[Literal["EXTERNAL_AI", "EVALUATION", "SGP_CHAT", "AGENTS_SERVICE"]] = None

    operation_metadata: Optional[object] = None
    """The JSON representation of the metadata insights emitted through the execution.

    This can differ based on different types of operations
    """


class Message(BaseModel):
    entry: MessageEntry

    feedback: Optional[ChatThreadFeedback] = None


class ChatThreadHistory(BaseModel):
    application_spec_id: str
    """The ID of the application spec that the thread belongs to."""

    messages: List[Message]

    thread: ChatThread
