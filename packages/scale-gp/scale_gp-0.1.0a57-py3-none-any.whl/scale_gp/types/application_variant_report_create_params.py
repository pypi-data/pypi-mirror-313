# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

__all__ = ["ApplicationVariantReportCreateParams"]


class ApplicationVariantReportCreateParams(TypedDict, total=False):
    application_variant_id: Required[str]

    evaluation_dataset_ids: Required[List[str]]

    account_id: str
    """The ID of the account that owns the given entity."""

    application_test_case_output_group_ids: List[str]
