# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel
from .evaluation_datasets.flexible_chunk import FlexibleChunk
from .evaluation_datasets.flexible_message import FlexibleMessage

__all__ = [
    "EvaluationTraceSpan",
    "OperationInput",
    "OperationInputFile",
    "OperationOutput",
    "OperationOutputFile",
    "OperationExpected",
    "OperationExpectedFile",
]


class OperationInputFile(BaseModel):
    file_type: Literal["image"]

    uri: str


OperationInput: TypeAlias = Union[
    str, float, List[FlexibleChunk], List[FlexibleMessage], List[object], OperationInputFile, object
]


class OperationOutputFile(BaseModel):
    file_type: Literal["image"]

    uri: str


OperationOutput: TypeAlias = Union[
    str, float, List[FlexibleChunk], List[FlexibleMessage], List[object], OperationOutputFile, object
]


class OperationExpectedFile(BaseModel):
    file_type: Literal["image"]

    uri: str


OperationExpected: TypeAlias = Union[
    str, float, List[FlexibleChunk], List[FlexibleMessage], List[object], OperationExpectedFile, object
]


class EvaluationTraceSpan(BaseModel):
    id: str
    """Identifies the application step"""

    application_interaction_id: str
    """The id of the application insight this step belongs to"""

    duration_ms: int
    """How much time the step took in milliseconds(ms)"""

    node_id: str
    """The id of the node in the application_variant config that emitted this insight"""

    operation_input: Dict[str, OperationInput]
    """The JSON representation of the input that this step received."""

    operation_output: Dict[str, OperationOutput]
    """The JSON representation of the output that this step emitted."""

    operation_status: Literal["SUCCESS", "ERROR"]
    """The outcome of the operation"""

    operation_type: Literal[
        "TEXT_INPUT",
        "TEXT_OUTPUT",
        "COMPLETION_INPUT",
        "COMPLETION",
        "KB_RETRIEVAL",
        "KB_INPUT",
        "RERANKING",
        "EXTERNAL_ENDPOINT",
        "PROMPT_ENGINEERING",
        "DOCUMENT_INPUT",
        "MAP_REDUCE",
        "DOCUMENT_SEARCH",
        "DOCUMENT_PROMPT",
        "CUSTOM",
        "INPUT_GUARDRAIL",
        "OUTPUT_GUARDRAIL",
        "CODE_EXECUTION",
        "DATA_MANIPULATION",
        "EVALUATION",
    ]
    """Type of the operation, e.g. RERANKING"""

    start_timestamp: datetime
    """The start time of the step"""

    operation_expected: Optional[Dict[str, OperationExpected]] = None
    """The JSON representation of the expected output for this step"""

    operation_metadata: Optional[object] = None
    """The JSON representation of the metadata insights emitted through the execution.

    This can differ based on different types of operations
    """
