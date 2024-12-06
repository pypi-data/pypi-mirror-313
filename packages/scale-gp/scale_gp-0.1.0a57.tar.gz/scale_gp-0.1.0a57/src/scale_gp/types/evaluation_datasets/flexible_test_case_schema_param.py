# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .flexible_chunk_param import FlexibleChunkParam
from .flexible_message_param import FlexibleMessageParam
from ..shared_params.chunk_extra_info_schema import ChunkExtraInfoSchema
from ..shared_params.string_extra_info_schema import StringExtraInfoSchema

__all__ = [
    "FlexibleTestCaseSchemaParam",
    "InputUnionMember1InputUnionMember1Item",
    "InputUnionMember1InputUnionMember1ItemFile",
    "ExpectedExtraInfo",
    "ExpectedOutputUnionMember1ExpectedOutputUnionMember1Item",
    "ExpectedOutputUnionMember1ExpectedOutputUnionMember1ItemFile",
]


class InputUnionMember1InputUnionMember1ItemFile(TypedDict, total=False):
    file_type: Required[Literal["image"]]

    uri: Required[str]


InputUnionMember1InputUnionMember1Item: TypeAlias = Union[
    str,
    float,
    Iterable[FlexibleChunkParam],
    Iterable[FlexibleMessageParam],
    Iterable[object],
    InputUnionMember1InputUnionMember1ItemFile,
    object,
]

ExpectedExtraInfo: TypeAlias = Union[ChunkExtraInfoSchema, StringExtraInfoSchema]


class ExpectedOutputUnionMember1ExpectedOutputUnionMember1ItemFile(TypedDict, total=False):
    file_type: Required[Literal["image"]]

    uri: Required[str]


ExpectedOutputUnionMember1ExpectedOutputUnionMember1Item: TypeAlias = Union[
    str,
    float,
    Iterable[FlexibleChunkParam],
    Iterable[FlexibleMessageParam],
    Iterable[object],
    ExpectedOutputUnionMember1ExpectedOutputUnionMember1ItemFile,
    object,
]


class FlexibleTestCaseSchemaParam(TypedDict, total=False):
    input: Required[Union[str, Dict[str, InputUnionMember1InputUnionMember1Item]]]

    expected_extra_info: ExpectedExtraInfo

    expected_output: Union[str, Dict[str, ExpectedOutputUnionMember1ExpectedOutputUnionMember1Item]]
