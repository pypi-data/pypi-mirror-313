# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ApplicationVariantProcessParams", "History", "Overrides"]


class ApplicationVariantProcessParams(TypedDict, total=False):
    inputs: Required[object]
    """Input data for the application. You must provide inputs for each input node"""

    history: Iterable[History]
    """History of the application"""

    operation_metadata: object
    """
    Arbitrary user-defined metadata that can be attached to the process operations
    and will be registered in the interaction.
    """

    overrides: Dict[str, Overrides]
    """Optional overrides for the application"""

    stream: bool
    """Control to have streaming of the endpoint.

    If the last node before the output is a completion node, you can set this to
    true to get the output as soon as the completion node has a token
    """


class History(TypedDict, total=False):
    request: Required[str]
    """Request inputs"""

    response: Required[str]
    """Response outputs"""

    session_data: object
    """Session data corresponding to the request response pair"""


class Overrides(TypedDict, total=False):
    artifact_ids_filter: List[str]

    artifact_name_regex: List[str]

    type: Literal["knowledge_base_schema"]
