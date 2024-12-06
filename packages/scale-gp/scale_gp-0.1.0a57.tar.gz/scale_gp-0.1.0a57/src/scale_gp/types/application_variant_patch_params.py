# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ApplicationVariantPatchParams", "Configuration"]


class ApplicationVariantPatchParams(TypedDict, total=False):
    configuration: Required[Configuration]


class Configuration(TypedDict, total=False):
    metadata: object
    """The user-defined application variant metadata"""
