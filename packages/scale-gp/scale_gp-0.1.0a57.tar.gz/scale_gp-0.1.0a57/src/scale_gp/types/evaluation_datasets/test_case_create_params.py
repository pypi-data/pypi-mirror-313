# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypeAlias, TypedDict

from .flexible_test_case_schema_param import FlexibleTestCaseSchemaParam
from .artifact_schema_generation_param import ArtifactSchemaGenerationParam
from .generation_test_case_schema_param import GenerationTestCaseSchemaParam

__all__ = ["TestCaseCreateParams", "TestCaseData"]


class TestCaseCreateParams(TypedDict, total=False):
    test_case_data: Required[TestCaseData]

    account_id: str

    chat_history: object

    test_case_metadata: object


TestCaseData: TypeAlias = Union[
    ArtifactSchemaGenerationParam, GenerationTestCaseSchemaParam, FlexibleTestCaseSchemaParam
]
