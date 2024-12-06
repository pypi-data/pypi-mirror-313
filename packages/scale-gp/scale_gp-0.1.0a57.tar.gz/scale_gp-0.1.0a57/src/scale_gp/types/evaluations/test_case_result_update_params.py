# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union
from typing_extensions import Literal, Required, TypedDict

__all__ = ["TestCaseResultUpdateParams"]


class TestCaseResultUpdateParams(TypedDict, total=False):
    evaluation_id: Required[str]

    account_id: str

    annotated_by_user_id: str

    application_spec_id: str

    audit_comment: str

    audit_required: bool

    audit_status: Literal["UNAUDITED", "FIXED", "APPROVED"]

    evaluation_dataset_version_num: str

    result: Dict[str, Union[str, bool, float, List[Union[str, bool, float]]]]

    test_case_evaluation_data: object

    test_case_id: str

    time_spent_labeling_s: int
