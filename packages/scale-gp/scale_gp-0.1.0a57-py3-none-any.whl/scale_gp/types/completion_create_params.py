# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "CompletionCreateParamsBase",
    "Image",
    "ModelParameters",
    "CompletionCreateParamsNonStreaming",
    "CompletionCreateParamsStreaming",
]


class CompletionCreateParamsBase(TypedDict, total=False):
    model: Required[
        Union[
            Literal[
                "gpt-4",
                "gpt-4-0613",
                "gpt-4-32k",
                "gpt-4-32k-0613",
                "gpt-4-vision-preview",
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4o-2024-08-06",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-16k-0613",
                "gemini-pro",
                "gemini-1.5-pro-001",
                "gemini-1.5-pro-002",
                "gemini-1.5-pro-preview-0409",
                "gemini-1.5-pro-preview-0514",
                "text-davinci-003",
                "text-davinci-002",
                "text-curie-001",
                "text-babbage-001",
                "text-ada-001",
                "claude-instant-1",
                "claude-instant-1.1",
                "claude-2",
                "claude-2.0",
                "llama-7b",
                "llama-2-7b",
                "llama-2-7b-chat",
                "llama-2-13b",
                "llama-2-13b-chat",
                "llama-2-70b",
                "llama-2-70b-chat",
                "llama-3-8b",
                "llama-3-8b-instruct",
                "llama-3-1-8b-instruct",
                "llama-3-1-70b-instruct",
                "llama-3-70b-instruct",
                "llama-3-2-1b-instruct",
                "llama-3-2-3b-instruct",
                "Meta-Llama-3-8B-Instruct-RMU",
                "Meta-Llama-3-8B-Instruct-RR",
                "Meta-Llama-3-8B-Instruct-DERTA",
                "Meta-Llama-3-8B-Instruct-LAT",
                "falcon-7b",
                "falcon-7b-instruct",
                "falcon-40b",
                "falcon-40b-instruct",
                "mpt-7b",
                "mpt-7b-instruct",
                "flan-t5-xxl",
                "mistral-7b",
                "mistral-7b-instruct",
                "mixtral-8x7b",
                "mixtral-8x7b-instruct",
                "mixtral-8x22b-instruct",
                "llm-jp-13b-instruct-full",
                "llm-jp-13b-instruct-full-dolly",
                "zephyr-7b-alpha",
                "zephyr-7b-beta",
                "zephyr-cat-merged",
                "codellama-7b",
                "codellama-7b-instruct",
                "codellama-13b",
                "codellama-13b-instruct",
                "codellama-34b",
                "codellama-34b-instruct",
                "phi-3-mini-4k-instruct",
                "phi-3-cat-merged",
                "dolphin-2.9-llama3-8b",
                "dolphin-2.9-llama3-70b",
            ],
            str,
        ]
    ]
    """The ID of the model to use for completions.

    Users have two options:

    - Option 1: Use one of the supported models from the dropdown.
    - Option 2: Enter the ID of a custom model.

    Note: For custom models we currently only support models finetuned using using
    the Scale-hosted LLM-Engine API.
    """

    prompt: Required[str]
    """Prompt for which to generate the completion.

    Good prompt engineering is crucial to getting performant results from the model.
    If you are having trouble getting the model to perform well, try writing a more
    specific prompt here before trying more expensive techniques such as swapping in
    other models or finetuning the underlying LLM.
    """

    account_id: str
    """The account ID to use for usage tracking. This will be gradually enforced."""

    images: Iterable[Image]
    """List of image urls to be used for image based completions.

    Leave empty for text based completions.
    """

    model_parameters: ModelParameters
    """
    Configuration parameters for the completion model, such as temperature,
    max_tokens, and stop_sequences.

    If not specified, the default value are:

    - temperature: 0.2
    - max_tokens: None (limited by the model's max tokens)
    - stop_sequences: None
    """


class Image(TypedDict, total=False):
    image_url: Required[str]
    """Image URL to run image completion on."""

    detail: str
    """Detail to run image completion with. Defaults to auto"""


class ModelParameters(TypedDict, total=False):
    frequency_penalty: float
    """Penalize tokens based on how much they have already appeared in the text.

    Positive values encourage the model to generate new tokens and negative values
    encourage the model to repeat tokens. Available for models from LLM Engine, and
    OpenAI
    """

    max_tokens: int
    """The maximum number of tokens to generate in the completion.

    The token count of your prompt plus max_tokens cannot exceed the model's context
    length. If not, specified, max_tokens will be determined based on the model
    used: | Model API family | Model API default | EGP applied default | | --- | ---
    | --- | | OpenAI Completions |
    [`16`](https://platform.openai.com/docs/api-reference/completions/create#max_tokens)
    | `context window - prompt size` | | OpenAI Chat Completions |
    [`context window - prompt size`](https://platform.openai.com/docs/api-reference/chat/create#max_tokens)
    | `context window - prompt size` | | LLM Engine |
    [`max_new_tokens`](https://github.com/scaleapi/launch-python-client/blob/207adced1c88c1c2907266fa9dd1f1ff3ec0ea5b/launch/client.py#L2910)
    parameter is required | `100` | | Anthropic Claude 2 |
    [`max_tokens_to_sample`](https://docs.anthropic.com/claude/reference/complete_post)
    parameter is required | `10000` |
    """

    presence_penalty: float
    """Penalize tokens based on if they have already appeared in the text.

    Positive values encourage the model to generate new tokens and negative values
    encourage the model to repeat tokens. Available for models from LLM Engine, and
    OpenAI.
    """

    stop_sequences: List[str]
    """List of up to 4 sequences where the API will stop generating further tokens.

    The returned text will not contain the stop sequence.
    """

    temperature: float
    """What sampling temperature to use, between [0, 1].

    Higher values like 0.8 will make the output more random, while lower values like
    0.2 will make it more focused and deterministic. Setting temperature=0.0 will
    enable fully deterministic (greedy) sampling.
    """

    top_k: Annotated[int, PropertyInfo(alias="topK")]
    """Sample from the k most likely next tokens at each step.

    Lower k focuses on higher probability tokens. Available for models from
    Anthropic, Google, and LLM Engine.
    """

    top_p: Annotated[float, PropertyInfo(alias="topP")]
    """The cumulative probability cutoff for token selection.

    Lower values mean sampling from a smaller, more top-weighted nucleus. Available
    for models from Anthropic, Google, Mistral, LLM Engine, and OpenAI.
    """


class CompletionCreateParamsNonStreaming(CompletionCreateParamsBase, total=False):
    stream: Literal[False]
    """Whether or not to stream the response.

    Setting this to True will stream the completion in real-time.
    """


class CompletionCreateParamsStreaming(CompletionCreateParamsBase):
    stream: Required[Literal[True]]
    """Whether or not to stream the response.

    Setting this to True will stream the completion in real-time.
    """


CompletionCreateParams = Union[CompletionCreateParamsNonStreaming, CompletionCreateParamsStreaming]
