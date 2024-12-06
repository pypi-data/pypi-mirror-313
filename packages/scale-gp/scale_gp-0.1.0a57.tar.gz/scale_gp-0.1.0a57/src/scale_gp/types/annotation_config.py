# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["AnnotationConfig", "Component"]


class Component(BaseModel):
    data_loc: List[str]

    label: Optional[str] = None

    optional: Optional[bool] = None


class AnnotationConfig(BaseModel):
    components: List[List[Component]]

    annotation_config_type: Optional[Literal["flexible", "summarization", "multiturn", "translation"]] = None

    direction: Optional[Literal["col", "row"]] = None
