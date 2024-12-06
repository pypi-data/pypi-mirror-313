# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from ..._compat import PYDANTIC_V2, ConfigDict
from ..._models import BaseModel

__all__ = ["DeploymentRetrieveResponse"]


class DeploymentRetrieveResponse(BaseModel):
    model_deployment_id: str

    if PYDANTIC_V2:
        # allow fields with a `model_` prefix
        model_config = ConfigDict(protected_namespaces=tuple())
