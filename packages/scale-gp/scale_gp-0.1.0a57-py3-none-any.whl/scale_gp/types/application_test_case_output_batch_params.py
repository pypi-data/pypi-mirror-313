# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo
from .result_schema_flexible_param import ResultSchemaFlexibleParam
from .shared_params.result_schema_generation import ResultSchemaGeneration
from .evaluation_datasets.flexible_chunk_param import FlexibleChunkParam
from .evaluation_datasets.flexible_message_param import FlexibleMessageParam

__all__ = [
    "ApplicationTestCaseOutputBatchParams",
    "Item",
    "ItemOutput",
    "ItemTraceSpan",
    "ItemTraceSpanOperationInput",
    "ItemTraceSpanOperationInputFile",
    "ItemTraceSpanOperationOutput",
    "ItemTraceSpanOperationOutputFile",
    "ItemTraceSpanOperationExpected",
    "ItemTraceSpanOperationExpectedFile",
]


class ApplicationTestCaseOutputBatchParams(TypedDict, total=False):
    items: Required[Iterable[Item]]


ItemOutput: TypeAlias = Union[ResultSchemaGeneration, ResultSchemaFlexibleParam]


class ItemTraceSpanOperationInputFile(TypedDict, total=False):
    file_type: Required[Literal["image"]]

    uri: Required[str]


ItemTraceSpanOperationInput: TypeAlias = Union[
    str,
    float,
    Iterable[FlexibleChunkParam],
    Iterable[FlexibleMessageParam],
    Iterable[object],
    ItemTraceSpanOperationInputFile,
    object,
]


class ItemTraceSpanOperationOutputFile(TypedDict, total=False):
    file_type: Required[Literal["image"]]

    uri: Required[str]


ItemTraceSpanOperationOutput: TypeAlias = Union[
    str,
    float,
    Iterable[FlexibleChunkParam],
    Iterable[FlexibleMessageParam],
    Iterable[object],
    ItemTraceSpanOperationOutputFile,
    object,
]


class ItemTraceSpanOperationExpectedFile(TypedDict, total=False):
    file_type: Required[Literal["image"]]

    uri: Required[str]


ItemTraceSpanOperationExpected: TypeAlias = Union[
    str,
    float,
    Iterable[FlexibleChunkParam],
    Iterable[FlexibleMessageParam],
    Iterable[object],
    ItemTraceSpanOperationExpectedFile,
    object,
]


class ItemTraceSpan(TypedDict, total=False):
    node_id: Required[str]
    """Identifier for the node that emitted this trace span."""

    operation_input: Required[Dict[str, ItemTraceSpanOperationInput]]
    """The JSON representation of the input that this step received."""

    operation_output: Required[Dict[str, ItemTraceSpanOperationOutput]]
    """The JSON representation of the output that this step emitted."""

    start_timestamp: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]
    """The start time of the step."""

    duration_ms: int
    """The duration of the operation step in milliseconds."""

    operation_expected: Dict[str, ItemTraceSpanOperationExpected]
    """The JSON representation of the expected output for this step"""

    operation_metadata: object
    """The JSON representation of the metadata insights emitted during execution.

    This can differ based on different types of operations.
    """

    operation_status: Literal["SUCCESS", "ERROR"]
    """The outcome of the operation performed by this node."""

    operation_type: Literal["COMPLETION", "RERANKING", "RETRIEVAL", "CUSTOM"]
    """Type of the operation, e.g., RERANKING."""


class Item(TypedDict, total=False):
    account_id: Required[str]

    application_variant_id: Required[str]

    evaluation_dataset_version_num: Required[int]

    output: Required[ItemOutput]

    test_case_id: Required[str]

    ignore_missing: bool
    """
    If set to true, the output batch will be saved even if there are missing outputs
    for some test cases.
    """

    metrics: Dict[str, float]

    trace_spans: Iterable[ItemTraceSpan]
    """List of trace spans associated with the application's execution.

    These spans provide insight into the individual steps taken by nodes involved in
    generating the output.
    """
