# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._compat import PYDANTIC_V2, ConfigDict
from ..._models import BaseModel

__all__ = ["ModelServerInfo"]


class ModelServerInfo(BaseModel):
    account_id: str

    model_deployment_id: str

    model_server_id: str

    name: str

    alias: Optional[str] = None

    if PYDANTIC_V2:
        # allow fields with a `model_` prefix
        model_config = ConfigDict(protected_namespaces=tuple())
