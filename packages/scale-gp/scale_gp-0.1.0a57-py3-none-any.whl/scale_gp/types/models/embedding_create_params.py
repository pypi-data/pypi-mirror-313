# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from ..parameter_bindings_param import ParameterBindingsParam

__all__ = ["EmbeddingCreateParams"]


class EmbeddingCreateParams(TypedDict, total=False):
    texts: Required[List[str]]

    model_request_parameters: ParameterBindingsParam
