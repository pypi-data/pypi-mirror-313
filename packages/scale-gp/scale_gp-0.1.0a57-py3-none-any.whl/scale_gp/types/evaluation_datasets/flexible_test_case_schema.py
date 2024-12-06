# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .flexible_chunk import FlexibleChunk
from .flexible_message import FlexibleMessage
from ..shared.chunk_extra_info_schema import ChunkExtraInfoSchema
from ..shared.string_extra_info_schema import StringExtraInfoSchema

__all__ = [
    "FlexibleTestCaseSchema",
    "InputUnionMember1InputUnionMember1Item",
    "InputUnionMember1InputUnionMember1ItemFile",
    "ExpectedExtraInfo",
    "ExpectedOutputUnionMember1ExpectedOutputUnionMember1Item",
    "ExpectedOutputUnionMember1ExpectedOutputUnionMember1ItemFile",
]


class InputUnionMember1InputUnionMember1ItemFile(BaseModel):
    file_type: Literal["image"]

    uri: str


InputUnionMember1InputUnionMember1Item: TypeAlias = Union[
    str,
    float,
    List[FlexibleChunk],
    List[FlexibleMessage],
    List[object],
    InputUnionMember1InputUnionMember1ItemFile,
    object,
]

ExpectedExtraInfo: TypeAlias = Annotated[
    Union[ChunkExtraInfoSchema, StringExtraInfoSchema], PropertyInfo(discriminator="schema_type")
]


class ExpectedOutputUnionMember1ExpectedOutputUnionMember1ItemFile(BaseModel):
    file_type: Literal["image"]

    uri: str


ExpectedOutputUnionMember1ExpectedOutputUnionMember1Item: TypeAlias = Union[
    str,
    float,
    List[FlexibleChunk],
    List[FlexibleMessage],
    List[object],
    ExpectedOutputUnionMember1ExpectedOutputUnionMember1ItemFile,
    object,
]


class FlexibleTestCaseSchema(BaseModel):
    input: Union[str, Dict[str, InputUnionMember1InputUnionMember1Item]]

    expected_extra_info: Optional[ExpectedExtraInfo] = None

    expected_output: Union[str, Dict[str, ExpectedOutputUnionMember1ExpectedOutputUnionMember1Item], None] = None
