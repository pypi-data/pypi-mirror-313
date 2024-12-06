# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .shared_params.chunk_extra_info_schema import ChunkExtraInfoSchema
from .shared_params.string_extra_info_schema import StringExtraInfoSchema
from .evaluation_datasets.flexible_chunk_param import FlexibleChunkParam
from .evaluation_datasets.flexible_message_param import FlexibleMessageParam

__all__ = [
    "ResultSchemaFlexibleParam",
    "GenerationOutputUnionMember1GenerationOutputUnionMember1Item",
    "GenerationOutputUnionMember1GenerationOutputUnionMember1ItemFile",
    "GenerationExtraInfo",
]


class GenerationOutputUnionMember1GenerationOutputUnionMember1ItemFile(TypedDict, total=False):
    file_type: Required[Literal["image"]]

    uri: Required[str]


GenerationOutputUnionMember1GenerationOutputUnionMember1Item: TypeAlias = Union[
    str,
    float,
    Iterable[FlexibleChunkParam],
    Iterable[FlexibleMessageParam],
    Iterable[object],
    GenerationOutputUnionMember1GenerationOutputUnionMember1ItemFile,
    object,
]

GenerationExtraInfo: TypeAlias = Union[ChunkExtraInfoSchema, StringExtraInfoSchema]


class ResultSchemaFlexibleParam(TypedDict, total=False):
    generation_output: Required[Union[str, Dict[str, GenerationOutputUnionMember1GenerationOutputUnionMember1Item]]]

    generation_extra_info: GenerationExtraInfo
