# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._compat import PYDANTIC_V2, ConfigDict
from .._models import BaseModel

__all__ = ["ModelInstance", "BaseModelMetadata", "BaseModelMetadataModelDetails"]


class BaseModelMetadataModelDetails(BaseModel):
    alignments: Optional[int] = None

    languages: Optional[int] = None

    number_of_parameters: Optional[int] = None

    token_context_window: Optional[int] = None


class BaseModelMetadata(BaseModel):
    delivery_date: Optional[str] = None

    model_developer: Optional[str] = None

    model_license_url: Optional[str] = None

    model_details: Optional[BaseModelMetadataModelDetails] = FieldInfo(alias="modelDetails", default=None)

    ui_model_section_type: Optional[Literal["PARTNER", "OPENSOURCE", "CUSTOM"]] = None

    if PYDANTIC_V2:
        # allow fields with a `model_` prefix
        model_config = ConfigDict(protected_namespaces=tuple())


class ModelInstance(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    deployment_count: int
    """Number of deployments of this model instance"""

    model_type: Literal["COMPLETION", "CHAT_COMPLETION", "AGENT", "EMBEDDING", "RERANKING", "GENERIC"]
    """An enum representing the different types of models supported.

    Attributes: COMPLETION: Denotes that the model type is completion.
    CHAT_COMPLETION: Denotes that the model type is chat completion. AGENT: Denotes
    that the model type is agent. EMBEDDING: Denotes that the model type is
    embedding. RERANKING: Denotes that the model type is reranking. GENERIC: Denotes
    that the model type is generic.
    """

    name: str

    request_schema: object
    """JSON schema for the requests to the model instance"""

    response_schema: object
    """JSON schema for the response to the model"""

    supports_multi_turn: bool
    """True if a model supports multi-turn conversations natively"""

    base_model_id: Optional[str] = None

    base_model_metadata: Optional[BaseModelMetadata] = None

    description: Optional[str] = None

    display_name: Optional[str] = None

    model_card: Optional[str] = None

    model_creation_parameters: Optional[object] = None

    model_group_id: Optional[str] = None

    model_template_id: Optional[str] = None

    model_vendor: Optional[
        Literal["OPENAI", "COHERE", "GOOGLE", "VERTEX_AI", "ANTHROPIC", "LAUNCH", "LLMENGINE", "BEDROCK", "OTHER"]
    ] = None
    """An enum representing the different types of model vendors supported.

    Attributes: OPENAI: Denotes that the model vendor is OpenAI. COHERE: Denotes
    that the model vendor is Cohere. GOOGLE: Denotes that the model vendor is
    Google. ANTHROPIC: Denotes that the model vendor is Anthropic. LLMENGINE:
    Denotes that the model vendor is LLM Engine. OTHER: Denotes that the model
    vendor is Other.
    """

    training_data_card: Optional[str] = None

    if PYDANTIC_V2:
        # allow fields with a `model_` prefix
        model_config = ConfigDict(protected_namespaces=tuple())
