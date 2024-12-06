# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import TypeAlias

from .completion import Completion
from .completion_chunk import CompletionChunk

__all__ = ["CompletionCreateResponse"]

CompletionCreateResponse: TypeAlias = Union[Completion, CompletionChunk]
