# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Dict, List, Union, Iterable, cast
from typing_extensions import Literal, overload

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import required_args, maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._streaming import Stream, AsyncStream
from ...._base_client import make_request_options
from ...._utils._parsing import type_to_response_format_param
from ....types.beta.chat import completion_create_params
from ....types.beta.chat.chat_completion_chunk import ChatCompletionChunk
from ....types.beta.chat.completion_create_response import CompletionCreateResponse

__all__ = ["CompletionsResource", "AsyncCompletionsResource"]


class CompletionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CompletionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return CompletionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CompletionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return CompletionsResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        *,
        messages: Iterable[completion_create_params.Message],
        model: str,
        audio: completion_create_params.Audio | NotGiven = NOT_GIVEN,
        best_of: int | NotGiven = NOT_GIVEN,
        chat_template: str | NotGiven = NOT_GIVEN,
        chat_template_kwargs: object | NotGiven = NOT_GIVEN,
        frequency_penalty: float | NotGiven = NOT_GIVEN,
        guided_choice: List[str] | NotGiven = NOT_GIVEN,
        guided_decoding_backend: str | NotGiven = NOT_GIVEN,
        guided_grammar: str | NotGiven = NOT_GIVEN,
        guided_json: object | NotGiven = NOT_GIVEN,
        guided_regex: str | NotGiven = NOT_GIVEN,
        guided_whitespace_pattern: str | NotGiven = NOT_GIVEN,
        include_stop_str_in_output: bool | NotGiven = NOT_GIVEN,
        inference_extra_headers: object | NotGiven = NOT_GIVEN,
        inference_extra_params: object | NotGiven = NOT_GIVEN,
        inference_timeout: Union[float, str] | NotGiven = NOT_GIVEN,
        logit_bias: Dict[str, int] | NotGiven = NOT_GIVEN,
        logprobs: bool | NotGiven = NOT_GIVEN,
        max_completion_tokens: int | NotGiven = NOT_GIVEN,
        max_tokens: int | NotGiven = NOT_GIVEN,
        memory_strategy: completion_create_params.MemoryStrategy | NotGiven = NOT_GIVEN,
        modalities: List[Literal["text", "audio"]] | NotGiven = NOT_GIVEN,
        n: int | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: object | NotGiven = NOT_GIVEN,
        presence_penalty: float | NotGiven = NOT_GIVEN,
        response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: int | NotGiven = NOT_GIVEN,
        stop: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        stream: Literal[False] | NotGiven = NOT_GIVEN,
        stream_options: object | NotGiven = NOT_GIVEN,
        suffix: str | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        tool_choice: completion_create_params.ToolChoice | NotGiven = NOT_GIVEN,
        tools: Iterable[completion_create_params.Tool] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_logprobs: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompletionCreateResponse:
        """### Description

        Interact with the LLM model using a chat completions interface.

        The LLM model
        will respond with an assistant message.

        ```json
        {
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "You are a name generator. Do not generate anything else than names"
            },
            { "role": "user", "content": "Generate 5 names" }
          ]
        }
        ```

        Args:
          messages: The list of messages in the conversation.

              Expand each message type to see how it works and when to use it. Most
              conversations should begin with a single `user` message.

          model: The name of the model.

              Should be formatted as `vendor/model_name` or `vendor/model_name/deployment`
              (ie: `openai/gpt-3.5-turbo`).

          audio: Audio-related parameters for chat completion

          best_of: Generates best_of completions server-side and returns the `best` (the one with
              the highest log probability per token). Results cannot be streamed.

          chat_template: A Jinja template to use for this conversion. As of transformers v4.44, default
              chat template is no longer allowed, so you must provide a chat template if the
              model's tokenizer does not define one and no override template is given

          chat_template_kwargs: Additional kwargs to pass to the template renderer. Will be accessible by the
              chat template.

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

          guided_choice: Choices for guided decoding. Only supported in vllm.

          guided_decoding_backend: If specified, will override the default guided decoding backend of the server
              for this specific request. If set, must be either 'outlines' /
              'lm-format-enforcer'

          guided_grammar: Context-free grammar for guided decoding. Only supported in vllm.

          guided_json: JSON schema for guided decoding. Only supported in vllm.

          guided_regex: Regex for guided decoding. Only supported in vllm.

          guided_whitespace_pattern: If specified, will override the default whitespace pattern for guided json
              decoding.

          include_stop_str_in_output: Whether to include the stop string in the output.

          inference_extra_headers: Additional headers to be included in the API request

          inference_extra_params: Additional params to be included in the API request

          inference_timeout: Timeout for the API request

          logit_bias: Modify the likelihood of specified tokens appearing in the completion.

              Accepts a JSON object that maps tokens (specified by their token ID in the
              tokenizer) to an associated bias value from -100 to 100. Mathematically, the
              bias is added to the logits generated by the model prior to sampling. The exact
              effect will vary per model, but values between -1 and 1 should decrease or
              increase likelihood of selection; values like -100 or 100 should result in a ban
              or exclusive selection of the relevant token.

          logprobs: Whether to return log probabilities of the output tokens or not. If true,
              returns the log probabilities of each output token returned in the content of
              message.

          max_completion_tokens: Maximum number of tokens to generate in the completion

          max_tokens: The maximum number of tokens that can be generated.

              The token count of your prompt plus max_tokens cannot exceed the model's context
              length.

          memory_strategy: The memory strategy to use for the conversation. A memory strategy is a way to
              prevent the underlying LLM's context limit from being exceeded. Only the
              `last_k` memory strategy is supported at this time.

          modalities: List of modalities for the chat completion

          n: How many completions to generate for each prompt.

              Note: Because this parameter generates many completions, it can quickly consume
              your token quota. Use carefully and ensure that you have reasonable settings for
              max_tokens and stop.

          parallel_tool_calls: Currently only supported for OpenAI models.Enables calling tools in parallel.

          prediction: Configure a predicted output to reduce latency

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

          response_format: An object specifying the format that the model must output

          seed: If specified, our system will make a best effort to sample deterministically,
              such that repeated requests with the same seed and parameters should return the
              same result.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream: Whether or not to stream the response.

              Setting this to True will stream the response in real-time.

          stream_options: Customize streaming behavior

          suffix: The suffix that comes after a completion of inserted text.This parameter is only
              supported for gpt-3.5-turbo-instruct.

          temperature: The sampling temperature to use for the completion. Higher values mean the model
              will take more risks.

          tool_choice: Currently only supported for OpenAI and Anthropic models.Controls which (if any)
              tool is called by the model.

          tools: Currently only supported for OpenAI and Anthropic models.A list of tools the
              model may call.Currently, only functions are supported as a tool.Use this to
              provide a list of functions the model may generate JSON inputs for.

          top_k: Only sample from the top K options for each subsequent token

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability. logprobs
              must be set to true if this parameter is used.

          top_p: An alternative to sampling with temperature, called nucleus sampling, where the
              model considers the results of the tokens with top_p probability mass. So 0.1
              means only the tokens comprising the top 10% probability mass are considered.

              It is generally recommended to alter this or temperature but not both.

          user: A unique identifier representing your end-user.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        messages: Iterable[completion_create_params.Message],
        model: str,
        stream: Literal[True],
        audio: completion_create_params.Audio | NotGiven = NOT_GIVEN,
        best_of: int | NotGiven = NOT_GIVEN,
        chat_template: str | NotGiven = NOT_GIVEN,
        chat_template_kwargs: object | NotGiven = NOT_GIVEN,
        frequency_penalty: float | NotGiven = NOT_GIVEN,
        guided_choice: List[str] | NotGiven = NOT_GIVEN,
        guided_decoding_backend: str | NotGiven = NOT_GIVEN,
        guided_grammar: str | NotGiven = NOT_GIVEN,
        guided_json: object | NotGiven = NOT_GIVEN,
        guided_regex: str | NotGiven = NOT_GIVEN,
        guided_whitespace_pattern: str | NotGiven = NOT_GIVEN,
        include_stop_str_in_output: bool | NotGiven = NOT_GIVEN,
        inference_extra_headers: object | NotGiven = NOT_GIVEN,
        inference_extra_params: object | NotGiven = NOT_GIVEN,
        inference_timeout: Union[float, str] | NotGiven = NOT_GIVEN,
        logit_bias: Dict[str, int] | NotGiven = NOT_GIVEN,
        logprobs: bool | NotGiven = NOT_GIVEN,
        max_completion_tokens: int | NotGiven = NOT_GIVEN,
        max_tokens: int | NotGiven = NOT_GIVEN,
        memory_strategy: completion_create_params.MemoryStrategy | NotGiven = NOT_GIVEN,
        modalities: List[Literal["text", "audio"]] | NotGiven = NOT_GIVEN,
        n: int | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: object | NotGiven = NOT_GIVEN,
        presence_penalty: float | NotGiven = NOT_GIVEN,
        response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: int | NotGiven = NOT_GIVEN,
        stop: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        stream_options: object | NotGiven = NOT_GIVEN,
        suffix: str | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        tool_choice: completion_create_params.ToolChoice | NotGiven = NOT_GIVEN,
        tools: Iterable[completion_create_params.Tool] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_logprobs: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Stream[ChatCompletionChunk]:
        """### Description

        Interact with the LLM model using a chat completions interface.

        The LLM model
        will respond with an assistant message.

        ```json
        {
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "You are a name generator. Do not generate anything else than names"
            },
            { "role": "user", "content": "Generate 5 names" }
          ]
        }
        ```

        Args:
          messages: The list of messages in the conversation.

              Expand each message type to see how it works and when to use it. Most
              conversations should begin with a single `user` message.

          model: The name of the model.

              Should be formatted as `vendor/model_name` or `vendor/model_name/deployment`
              (ie: `openai/gpt-3.5-turbo`).

          stream: Whether or not to stream the response.

              Setting this to True will stream the response in real-time.

          audio: Audio-related parameters for chat completion

          best_of: Generates best_of completions server-side and returns the `best` (the one with
              the highest log probability per token). Results cannot be streamed.

          chat_template: A Jinja template to use for this conversion. As of transformers v4.44, default
              chat template is no longer allowed, so you must provide a chat template if the
              model's tokenizer does not define one and no override template is given

          chat_template_kwargs: Additional kwargs to pass to the template renderer. Will be accessible by the
              chat template.

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

          guided_choice: Choices for guided decoding. Only supported in vllm.

          guided_decoding_backend: If specified, will override the default guided decoding backend of the server
              for this specific request. If set, must be either 'outlines' /
              'lm-format-enforcer'

          guided_grammar: Context-free grammar for guided decoding. Only supported in vllm.

          guided_json: JSON schema for guided decoding. Only supported in vllm.

          guided_regex: Regex for guided decoding. Only supported in vllm.

          guided_whitespace_pattern: If specified, will override the default whitespace pattern for guided json
              decoding.

          include_stop_str_in_output: Whether to include the stop string in the output.

          inference_extra_headers: Additional headers to be included in the API request

          inference_extra_params: Additional params to be included in the API request

          inference_timeout: Timeout for the API request

          logit_bias: Modify the likelihood of specified tokens appearing in the completion.

              Accepts a JSON object that maps tokens (specified by their token ID in the
              tokenizer) to an associated bias value from -100 to 100. Mathematically, the
              bias is added to the logits generated by the model prior to sampling. The exact
              effect will vary per model, but values between -1 and 1 should decrease or
              increase likelihood of selection; values like -100 or 100 should result in a ban
              or exclusive selection of the relevant token.

          logprobs: Whether to return log probabilities of the output tokens or not. If true,
              returns the log probabilities of each output token returned in the content of
              message.

          max_completion_tokens: Maximum number of tokens to generate in the completion

          max_tokens: The maximum number of tokens that can be generated.

              The token count of your prompt plus max_tokens cannot exceed the model's context
              length.

          memory_strategy: The memory strategy to use for the conversation. A memory strategy is a way to
              prevent the underlying LLM's context limit from being exceeded. Only the
              `last_k` memory strategy is supported at this time.

          modalities: List of modalities for the chat completion

          n: How many completions to generate for each prompt.

              Note: Because this parameter generates many completions, it can quickly consume
              your token quota. Use carefully and ensure that you have reasonable settings for
              max_tokens and stop.

          parallel_tool_calls: Currently only supported for OpenAI models.Enables calling tools in parallel.

          prediction: Configure a predicted output to reduce latency

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

          response_format: An object specifying the format that the model must output

          seed: If specified, our system will make a best effort to sample deterministically,
              such that repeated requests with the same seed and parameters should return the
              same result.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream_options: Customize streaming behavior

          suffix: The suffix that comes after a completion of inserted text.This parameter is only
              supported for gpt-3.5-turbo-instruct.

          temperature: The sampling temperature to use for the completion. Higher values mean the model
              will take more risks.

          tool_choice: Currently only supported for OpenAI and Anthropic models.Controls which (if any)
              tool is called by the model.

          tools: Currently only supported for OpenAI and Anthropic models.A list of tools the
              model may call.Currently, only functions are supported as a tool.Use this to
              provide a list of functions the model may generate JSON inputs for.

          top_k: Only sample from the top K options for each subsequent token

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability. logprobs
              must be set to true if this parameter is used.

          top_p: An alternative to sampling with temperature, called nucleus sampling, where the
              model considers the results of the tokens with top_p probability mass. So 0.1
              means only the tokens comprising the top 10% probability mass are considered.

              It is generally recommended to alter this or temperature but not both.

          user: A unique identifier representing your end-user.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        messages: Iterable[completion_create_params.Message],
        model: str,
        stream: bool,
        audio: completion_create_params.Audio | NotGiven = NOT_GIVEN,
        best_of: int | NotGiven = NOT_GIVEN,
        chat_template: str | NotGiven = NOT_GIVEN,
        chat_template_kwargs: object | NotGiven = NOT_GIVEN,
        frequency_penalty: float | NotGiven = NOT_GIVEN,
        guided_choice: List[str] | NotGiven = NOT_GIVEN,
        guided_decoding_backend: str | NotGiven = NOT_GIVEN,
        guided_grammar: str | NotGiven = NOT_GIVEN,
        guided_json: object | NotGiven = NOT_GIVEN,
        guided_regex: str | NotGiven = NOT_GIVEN,
        guided_whitespace_pattern: str | NotGiven = NOT_GIVEN,
        include_stop_str_in_output: bool | NotGiven = NOT_GIVEN,
        inference_extra_headers: object | NotGiven = NOT_GIVEN,
        inference_extra_params: object | NotGiven = NOT_GIVEN,
        inference_timeout: Union[float, str] | NotGiven = NOT_GIVEN,
        logit_bias: Dict[str, int] | NotGiven = NOT_GIVEN,
        logprobs: bool | NotGiven = NOT_GIVEN,
        max_completion_tokens: int | NotGiven = NOT_GIVEN,
        max_tokens: int | NotGiven = NOT_GIVEN,
        memory_strategy: completion_create_params.MemoryStrategy | NotGiven = NOT_GIVEN,
        modalities: List[Literal["text", "audio"]] | NotGiven = NOT_GIVEN,
        n: int | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: object | NotGiven = NOT_GIVEN,
        presence_penalty: float | NotGiven = NOT_GIVEN,
        response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: int | NotGiven = NOT_GIVEN,
        stop: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        stream_options: object | NotGiven = NOT_GIVEN,
        suffix: str | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        tool_choice: completion_create_params.ToolChoice | NotGiven = NOT_GIVEN,
        tools: Iterable[completion_create_params.Tool] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_logprobs: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompletionCreateResponse | Stream[ChatCompletionChunk]:
        """### Description

        Interact with the LLM model using a chat completions interface.

        The LLM model
        will respond with an assistant message.

        ```json
        {
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "You are a name generator. Do not generate anything else than names"
            },
            { "role": "user", "content": "Generate 5 names" }
          ]
        }
        ```

        Args:
          messages: The list of messages in the conversation.

              Expand each message type to see how it works and when to use it. Most
              conversations should begin with a single `user` message.

          model: The name of the model.

              Should be formatted as `vendor/model_name` or `vendor/model_name/deployment`
              (ie: `openai/gpt-3.5-turbo`).

          stream: Whether or not to stream the response.

              Setting this to True will stream the response in real-time.

          audio: Audio-related parameters for chat completion

          best_of: Generates best_of completions server-side and returns the `best` (the one with
              the highest log probability per token). Results cannot be streamed.

          chat_template: A Jinja template to use for this conversion. As of transformers v4.44, default
              chat template is no longer allowed, so you must provide a chat template if the
              model's tokenizer does not define one and no override template is given

          chat_template_kwargs: Additional kwargs to pass to the template renderer. Will be accessible by the
              chat template.

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

          guided_choice: Choices for guided decoding. Only supported in vllm.

          guided_decoding_backend: If specified, will override the default guided decoding backend of the server
              for this specific request. If set, must be either 'outlines' /
              'lm-format-enforcer'

          guided_grammar: Context-free grammar for guided decoding. Only supported in vllm.

          guided_json: JSON schema for guided decoding. Only supported in vllm.

          guided_regex: Regex for guided decoding. Only supported in vllm.

          guided_whitespace_pattern: If specified, will override the default whitespace pattern for guided json
              decoding.

          include_stop_str_in_output: Whether to include the stop string in the output.

          inference_extra_headers: Additional headers to be included in the API request

          inference_extra_params: Additional params to be included in the API request

          inference_timeout: Timeout for the API request

          logit_bias: Modify the likelihood of specified tokens appearing in the completion.

              Accepts a JSON object that maps tokens (specified by their token ID in the
              tokenizer) to an associated bias value from -100 to 100. Mathematically, the
              bias is added to the logits generated by the model prior to sampling. The exact
              effect will vary per model, but values between -1 and 1 should decrease or
              increase likelihood of selection; values like -100 or 100 should result in a ban
              or exclusive selection of the relevant token.

          logprobs: Whether to return log probabilities of the output tokens or not. If true,
              returns the log probabilities of each output token returned in the content of
              message.

          max_completion_tokens: Maximum number of tokens to generate in the completion

          max_tokens: The maximum number of tokens that can be generated.

              The token count of your prompt plus max_tokens cannot exceed the model's context
              length.

          memory_strategy: The memory strategy to use for the conversation. A memory strategy is a way to
              prevent the underlying LLM's context limit from being exceeded. Only the
              `last_k` memory strategy is supported at this time.

          modalities: List of modalities for the chat completion

          n: How many completions to generate for each prompt.

              Note: Because this parameter generates many completions, it can quickly consume
              your token quota. Use carefully and ensure that you have reasonable settings for
              max_tokens and stop.

          parallel_tool_calls: Currently only supported for OpenAI models.Enables calling tools in parallel.

          prediction: Configure a predicted output to reduce latency

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

          response_format: An object specifying the format that the model must output

          seed: If specified, our system will make a best effort to sample deterministically,
              such that repeated requests with the same seed and parameters should return the
              same result.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream_options: Customize streaming behavior

          suffix: The suffix that comes after a completion of inserted text.This parameter is only
              supported for gpt-3.5-turbo-instruct.

          temperature: The sampling temperature to use for the completion. Higher values mean the model
              will take more risks.

          tool_choice: Currently only supported for OpenAI and Anthropic models.Controls which (if any)
              tool is called by the model.

          tools: Currently only supported for OpenAI and Anthropic models.A list of tools the
              model may call.Currently, only functions are supported as a tool.Use this to
              provide a list of functions the model may generate JSON inputs for.

          top_k: Only sample from the top K options for each subsequent token

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability. logprobs
              must be set to true if this parameter is used.

          top_p: An alternative to sampling with temperature, called nucleus sampling, where the
              model considers the results of the tokens with top_p probability mass. So 0.1
              means only the tokens comprising the top 10% probability mass are considered.

              It is generally recommended to alter this or temperature but not both.

          user: A unique identifier representing your end-user.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["messages", "model"], ["messages", "model", "stream"])
    def create(
        self,
        *,
        messages: Iterable[completion_create_params.Message],
        model: str,
        audio: completion_create_params.Audio | NotGiven = NOT_GIVEN,
        best_of: int | NotGiven = NOT_GIVEN,
        chat_template: str | NotGiven = NOT_GIVEN,
        chat_template_kwargs: object | NotGiven = NOT_GIVEN,
        frequency_penalty: float | NotGiven = NOT_GIVEN,
        guided_choice: List[str] | NotGiven = NOT_GIVEN,
        guided_decoding_backend: str | NotGiven = NOT_GIVEN,
        guided_grammar: str | NotGiven = NOT_GIVEN,
        guided_json: object | NotGiven = NOT_GIVEN,
        guided_regex: str | NotGiven = NOT_GIVEN,
        guided_whitespace_pattern: str | NotGiven = NOT_GIVEN,
        include_stop_str_in_output: bool | NotGiven = NOT_GIVEN,
        inference_extra_headers: object | NotGiven = NOT_GIVEN,
        inference_extra_params: object | NotGiven = NOT_GIVEN,
        inference_timeout: Union[float, str] | NotGiven = NOT_GIVEN,
        logit_bias: Dict[str, int] | NotGiven = NOT_GIVEN,
        logprobs: bool | NotGiven = NOT_GIVEN,
        max_completion_tokens: int | NotGiven = NOT_GIVEN,
        max_tokens: int | NotGiven = NOT_GIVEN,
        memory_strategy: completion_create_params.MemoryStrategy | NotGiven = NOT_GIVEN,
        modalities: List[Literal["text", "audio"]] | NotGiven = NOT_GIVEN,
        n: int | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: object | NotGiven = NOT_GIVEN,
        presence_penalty: float | NotGiven = NOT_GIVEN,
        response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: int | NotGiven = NOT_GIVEN,
        stop: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        stream: Literal[False] | Literal[True] | NotGiven = NOT_GIVEN,
        stream_options: object | NotGiven = NOT_GIVEN,
        suffix: str | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        tool_choice: completion_create_params.ToolChoice | NotGiven = NOT_GIVEN,
        tools: Iterable[completion_create_params.Tool] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_logprobs: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompletionCreateResponse | Stream[ChatCompletionChunk]:
        return cast(
            CompletionCreateResponse,
            self._post(
                "/v4/beta/chat/completions",
                body=maybe_transform(
                    {
                        "messages": messages,
                        "model": model,
                        "audio": audio,
                        "best_of": best_of,
                        "chat_template": chat_template,
                        "chat_template_kwargs": chat_template_kwargs,
                        "frequency_penalty": frequency_penalty,
                        "guided_choice": guided_choice,
                        "guided_decoding_backend": guided_decoding_backend,
                        "guided_grammar": guided_grammar,
                        "guided_json": guided_json,
                        "guided_regex": guided_regex,
                        "guided_whitespace_pattern": guided_whitespace_pattern,
                        "include_stop_str_in_output": include_stop_str_in_output,
                        "inference_extra_headers": inference_extra_headers,
                        "inference_extra_params": inference_extra_params,
                        "inference_timeout": inference_timeout,
                        "logit_bias": logit_bias,
                        "logprobs": logprobs,
                        "max_completion_tokens": max_completion_tokens,
                        "max_tokens": max_tokens,
                        "memory_strategy": memory_strategy,
                        "modalities": modalities,
                        "n": n,
                        "parallel_tool_calls": parallel_tool_calls,
                        "prediction": prediction,
                        "presence_penalty": presence_penalty,
                        "response_format": type_to_response_format_param(response_format),
                        "seed": seed,
                        "stop": stop,
                        "stream": stream,
                        "stream_options": stream_options,
                        "suffix": suffix,
                        "temperature": temperature,
                        "tool_choice": tool_choice,
                        "tools": tools,
                        "top_k": top_k,
                        "top_logprobs": top_logprobs,
                        "top_p": top_p,
                        "user": user,
                    },
                    completion_create_params.CompletionCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, CompletionCreateResponse
                ),  # Union types cannot be passed in as arguments in the type system
                stream=stream or False,
                stream_cls=Stream[ChatCompletionChunk],
            ),
        )


class AsyncCompletionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCompletionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCompletionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCompletionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncCompletionsResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        *,
        messages: Iterable[completion_create_params.Message],
        model: str,
        audio: completion_create_params.Audio | NotGiven = NOT_GIVEN,
        best_of: int | NotGiven = NOT_GIVEN,
        chat_template: str | NotGiven = NOT_GIVEN,
        chat_template_kwargs: object | NotGiven = NOT_GIVEN,
        frequency_penalty: float | NotGiven = NOT_GIVEN,
        guided_choice: List[str] | NotGiven = NOT_GIVEN,
        guided_decoding_backend: str | NotGiven = NOT_GIVEN,
        guided_grammar: str | NotGiven = NOT_GIVEN,
        guided_json: object | NotGiven = NOT_GIVEN,
        guided_regex: str | NotGiven = NOT_GIVEN,
        guided_whitespace_pattern: str | NotGiven = NOT_GIVEN,
        include_stop_str_in_output: bool | NotGiven = NOT_GIVEN,
        inference_extra_headers: object | NotGiven = NOT_GIVEN,
        inference_extra_params: object | NotGiven = NOT_GIVEN,
        inference_timeout: Union[float, str] | NotGiven = NOT_GIVEN,
        logit_bias: Dict[str, int] | NotGiven = NOT_GIVEN,
        logprobs: bool | NotGiven = NOT_GIVEN,
        max_completion_tokens: int | NotGiven = NOT_GIVEN,
        max_tokens: int | NotGiven = NOT_GIVEN,
        memory_strategy: completion_create_params.MemoryStrategy | NotGiven = NOT_GIVEN,
        modalities: List[Literal["text", "audio"]] | NotGiven = NOT_GIVEN,
        n: int | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: object | NotGiven = NOT_GIVEN,
        presence_penalty: float | NotGiven = NOT_GIVEN,
        response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: int | NotGiven = NOT_GIVEN,
        stop: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        stream: Literal[False] | NotGiven = NOT_GIVEN,
        stream_options: object | NotGiven = NOT_GIVEN,
        suffix: str | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        tool_choice: completion_create_params.ToolChoice | NotGiven = NOT_GIVEN,
        tools: Iterable[completion_create_params.Tool] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_logprobs: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompletionCreateResponse:
        """### Description

        Interact with the LLM model using a chat completions interface.

        The LLM model
        will respond with an assistant message.

        ```json
        {
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "You are a name generator. Do not generate anything else than names"
            },
            { "role": "user", "content": "Generate 5 names" }
          ]
        }
        ```

        Args:
          messages: The list of messages in the conversation.

              Expand each message type to see how it works and when to use it. Most
              conversations should begin with a single `user` message.

          model: The name of the model.

              Should be formatted as `vendor/model_name` or `vendor/model_name/deployment`
              (ie: `openai/gpt-3.5-turbo`).

          audio: Audio-related parameters for chat completion

          best_of: Generates best_of completions server-side and returns the `best` (the one with
              the highest log probability per token). Results cannot be streamed.

          chat_template: A Jinja template to use for this conversion. As of transformers v4.44, default
              chat template is no longer allowed, so you must provide a chat template if the
              model's tokenizer does not define one and no override template is given

          chat_template_kwargs: Additional kwargs to pass to the template renderer. Will be accessible by the
              chat template.

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

          guided_choice: Choices for guided decoding. Only supported in vllm.

          guided_decoding_backend: If specified, will override the default guided decoding backend of the server
              for this specific request. If set, must be either 'outlines' /
              'lm-format-enforcer'

          guided_grammar: Context-free grammar for guided decoding. Only supported in vllm.

          guided_json: JSON schema for guided decoding. Only supported in vllm.

          guided_regex: Regex for guided decoding. Only supported in vllm.

          guided_whitespace_pattern: If specified, will override the default whitespace pattern for guided json
              decoding.

          include_stop_str_in_output: Whether to include the stop string in the output.

          inference_extra_headers: Additional headers to be included in the API request

          inference_extra_params: Additional params to be included in the API request

          inference_timeout: Timeout for the API request

          logit_bias: Modify the likelihood of specified tokens appearing in the completion.

              Accepts a JSON object that maps tokens (specified by their token ID in the
              tokenizer) to an associated bias value from -100 to 100. Mathematically, the
              bias is added to the logits generated by the model prior to sampling. The exact
              effect will vary per model, but values between -1 and 1 should decrease or
              increase likelihood of selection; values like -100 or 100 should result in a ban
              or exclusive selection of the relevant token.

          logprobs: Whether to return log probabilities of the output tokens or not. If true,
              returns the log probabilities of each output token returned in the content of
              message.

          max_completion_tokens: Maximum number of tokens to generate in the completion

          max_tokens: The maximum number of tokens that can be generated.

              The token count of your prompt plus max_tokens cannot exceed the model's context
              length.

          memory_strategy: The memory strategy to use for the conversation. A memory strategy is a way to
              prevent the underlying LLM's context limit from being exceeded. Only the
              `last_k` memory strategy is supported at this time.

          modalities: List of modalities for the chat completion

          n: How many completions to generate for each prompt.

              Note: Because this parameter generates many completions, it can quickly consume
              your token quota. Use carefully and ensure that you have reasonable settings for
              max_tokens and stop.

          parallel_tool_calls: Currently only supported for OpenAI models.Enables calling tools in parallel.

          prediction: Configure a predicted output to reduce latency

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

          response_format: An object specifying the format that the model must output

          seed: If specified, our system will make a best effort to sample deterministically,
              such that repeated requests with the same seed and parameters should return the
              same result.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream: Whether or not to stream the response.

              Setting this to True will stream the response in real-time.

          stream_options: Customize streaming behavior

          suffix: The suffix that comes after a completion of inserted text.This parameter is only
              supported for gpt-3.5-turbo-instruct.

          temperature: The sampling temperature to use for the completion. Higher values mean the model
              will take more risks.

          tool_choice: Currently only supported for OpenAI and Anthropic models.Controls which (if any)
              tool is called by the model.

          tools: Currently only supported for OpenAI and Anthropic models.A list of tools the
              model may call.Currently, only functions are supported as a tool.Use this to
              provide a list of functions the model may generate JSON inputs for.

          top_k: Only sample from the top K options for each subsequent token

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability. logprobs
              must be set to true if this parameter is used.

          top_p: An alternative to sampling with temperature, called nucleus sampling, where the
              model considers the results of the tokens with top_p probability mass. So 0.1
              means only the tokens comprising the top 10% probability mass are considered.

              It is generally recommended to alter this or temperature but not both.

          user: A unique identifier representing your end-user.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        messages: Iterable[completion_create_params.Message],
        model: str,
        stream: Literal[True],
        audio: completion_create_params.Audio | NotGiven = NOT_GIVEN,
        best_of: int | NotGiven = NOT_GIVEN,
        chat_template: str | NotGiven = NOT_GIVEN,
        chat_template_kwargs: object | NotGiven = NOT_GIVEN,
        frequency_penalty: float | NotGiven = NOT_GIVEN,
        guided_choice: List[str] | NotGiven = NOT_GIVEN,
        guided_decoding_backend: str | NotGiven = NOT_GIVEN,
        guided_grammar: str | NotGiven = NOT_GIVEN,
        guided_json: object | NotGiven = NOT_GIVEN,
        guided_regex: str | NotGiven = NOT_GIVEN,
        guided_whitespace_pattern: str | NotGiven = NOT_GIVEN,
        include_stop_str_in_output: bool | NotGiven = NOT_GIVEN,
        inference_extra_headers: object | NotGiven = NOT_GIVEN,
        inference_extra_params: object | NotGiven = NOT_GIVEN,
        inference_timeout: Union[float, str] | NotGiven = NOT_GIVEN,
        logit_bias: Dict[str, int] | NotGiven = NOT_GIVEN,
        logprobs: bool | NotGiven = NOT_GIVEN,
        max_completion_tokens: int | NotGiven = NOT_GIVEN,
        max_tokens: int | NotGiven = NOT_GIVEN,
        memory_strategy: completion_create_params.MemoryStrategy | NotGiven = NOT_GIVEN,
        modalities: List[Literal["text", "audio"]] | NotGiven = NOT_GIVEN,
        n: int | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: object | NotGiven = NOT_GIVEN,
        presence_penalty: float | NotGiven = NOT_GIVEN,
        response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: int | NotGiven = NOT_GIVEN,
        stop: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        stream_options: object | NotGiven = NOT_GIVEN,
        suffix: str | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        tool_choice: completion_create_params.ToolChoice | NotGiven = NOT_GIVEN,
        tools: Iterable[completion_create_params.Tool] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_logprobs: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncStream[ChatCompletionChunk]:
        """### Description

        Interact with the LLM model using a chat completions interface.

        The LLM model
        will respond with an assistant message.

        ```json
        {
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "You are a name generator. Do not generate anything else than names"
            },
            { "role": "user", "content": "Generate 5 names" }
          ]
        }
        ```

        Args:
          messages: The list of messages in the conversation.

              Expand each message type to see how it works and when to use it. Most
              conversations should begin with a single `user` message.

          model: The name of the model.

              Should be formatted as `vendor/model_name` or `vendor/model_name/deployment`
              (ie: `openai/gpt-3.5-turbo`).

          stream: Whether or not to stream the response.

              Setting this to True will stream the response in real-time.

          audio: Audio-related parameters for chat completion

          best_of: Generates best_of completions server-side and returns the `best` (the one with
              the highest log probability per token). Results cannot be streamed.

          chat_template: A Jinja template to use for this conversion. As of transformers v4.44, default
              chat template is no longer allowed, so you must provide a chat template if the
              model's tokenizer does not define one and no override template is given

          chat_template_kwargs: Additional kwargs to pass to the template renderer. Will be accessible by the
              chat template.

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

          guided_choice: Choices for guided decoding. Only supported in vllm.

          guided_decoding_backend: If specified, will override the default guided decoding backend of the server
              for this specific request. If set, must be either 'outlines' /
              'lm-format-enforcer'

          guided_grammar: Context-free grammar for guided decoding. Only supported in vllm.

          guided_json: JSON schema for guided decoding. Only supported in vllm.

          guided_regex: Regex for guided decoding. Only supported in vllm.

          guided_whitespace_pattern: If specified, will override the default whitespace pattern for guided json
              decoding.

          include_stop_str_in_output: Whether to include the stop string in the output.

          inference_extra_headers: Additional headers to be included in the API request

          inference_extra_params: Additional params to be included in the API request

          inference_timeout: Timeout for the API request

          logit_bias: Modify the likelihood of specified tokens appearing in the completion.

              Accepts a JSON object that maps tokens (specified by their token ID in the
              tokenizer) to an associated bias value from -100 to 100. Mathematically, the
              bias is added to the logits generated by the model prior to sampling. The exact
              effect will vary per model, but values between -1 and 1 should decrease or
              increase likelihood of selection; values like -100 or 100 should result in a ban
              or exclusive selection of the relevant token.

          logprobs: Whether to return log probabilities of the output tokens or not. If true,
              returns the log probabilities of each output token returned in the content of
              message.

          max_completion_tokens: Maximum number of tokens to generate in the completion

          max_tokens: The maximum number of tokens that can be generated.

              The token count of your prompt plus max_tokens cannot exceed the model's context
              length.

          memory_strategy: The memory strategy to use for the conversation. A memory strategy is a way to
              prevent the underlying LLM's context limit from being exceeded. Only the
              `last_k` memory strategy is supported at this time.

          modalities: List of modalities for the chat completion

          n: How many completions to generate for each prompt.

              Note: Because this parameter generates many completions, it can quickly consume
              your token quota. Use carefully and ensure that you have reasonable settings for
              max_tokens and stop.

          parallel_tool_calls: Currently only supported for OpenAI models.Enables calling tools in parallel.

          prediction: Configure a predicted output to reduce latency

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

          response_format: An object specifying the format that the model must output

          seed: If specified, our system will make a best effort to sample deterministically,
              such that repeated requests with the same seed and parameters should return the
              same result.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream_options: Customize streaming behavior

          suffix: The suffix that comes after a completion of inserted text.This parameter is only
              supported for gpt-3.5-turbo-instruct.

          temperature: The sampling temperature to use for the completion. Higher values mean the model
              will take more risks.

          tool_choice: Currently only supported for OpenAI and Anthropic models.Controls which (if any)
              tool is called by the model.

          tools: Currently only supported for OpenAI and Anthropic models.A list of tools the
              model may call.Currently, only functions are supported as a tool.Use this to
              provide a list of functions the model may generate JSON inputs for.

          top_k: Only sample from the top K options for each subsequent token

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability. logprobs
              must be set to true if this parameter is used.

          top_p: An alternative to sampling with temperature, called nucleus sampling, where the
              model considers the results of the tokens with top_p probability mass. So 0.1
              means only the tokens comprising the top 10% probability mass are considered.

              It is generally recommended to alter this or temperature but not both.

          user: A unique identifier representing your end-user.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        messages: Iterable[completion_create_params.Message],
        model: str,
        stream: bool,
        audio: completion_create_params.Audio | NotGiven = NOT_GIVEN,
        best_of: int | NotGiven = NOT_GIVEN,
        chat_template: str | NotGiven = NOT_GIVEN,
        chat_template_kwargs: object | NotGiven = NOT_GIVEN,
        frequency_penalty: float | NotGiven = NOT_GIVEN,
        guided_choice: List[str] | NotGiven = NOT_GIVEN,
        guided_decoding_backend: str | NotGiven = NOT_GIVEN,
        guided_grammar: str | NotGiven = NOT_GIVEN,
        guided_json: object | NotGiven = NOT_GIVEN,
        guided_regex: str | NotGiven = NOT_GIVEN,
        guided_whitespace_pattern: str | NotGiven = NOT_GIVEN,
        include_stop_str_in_output: bool | NotGiven = NOT_GIVEN,
        inference_extra_headers: object | NotGiven = NOT_GIVEN,
        inference_extra_params: object | NotGiven = NOT_GIVEN,
        inference_timeout: Union[float, str] | NotGiven = NOT_GIVEN,
        logit_bias: Dict[str, int] | NotGiven = NOT_GIVEN,
        logprobs: bool | NotGiven = NOT_GIVEN,
        max_completion_tokens: int | NotGiven = NOT_GIVEN,
        max_tokens: int | NotGiven = NOT_GIVEN,
        memory_strategy: completion_create_params.MemoryStrategy | NotGiven = NOT_GIVEN,
        modalities: List[Literal["text", "audio"]] | NotGiven = NOT_GIVEN,
        n: int | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: object | NotGiven = NOT_GIVEN,
        presence_penalty: float | NotGiven = NOT_GIVEN,
        response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: int | NotGiven = NOT_GIVEN,
        stop: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        stream_options: object | NotGiven = NOT_GIVEN,
        suffix: str | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        tool_choice: completion_create_params.ToolChoice | NotGiven = NOT_GIVEN,
        tools: Iterable[completion_create_params.Tool] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_logprobs: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompletionCreateResponse | AsyncStream[ChatCompletionChunk]:
        """### Description

        Interact with the LLM model using a chat completions interface.

        The LLM model
        will respond with an assistant message.

        ```json
        {
          "model": "gpt-4o",
          "messages": [
            {
              "role": "system",
              "content": "You are a name generator. Do not generate anything else than names"
            },
            { "role": "user", "content": "Generate 5 names" }
          ]
        }
        ```

        Args:
          messages: The list of messages in the conversation.

              Expand each message type to see how it works and when to use it. Most
              conversations should begin with a single `user` message.

          model: The name of the model.

              Should be formatted as `vendor/model_name` or `vendor/model_name/deployment`
              (ie: `openai/gpt-3.5-turbo`).

          stream: Whether or not to stream the response.

              Setting this to True will stream the response in real-time.

          audio: Audio-related parameters for chat completion

          best_of: Generates best_of completions server-side and returns the `best` (the one with
              the highest log probability per token). Results cannot be streamed.

          chat_template: A Jinja template to use for this conversion. As of transformers v4.44, default
              chat template is no longer allowed, so you must provide a chat template if the
              model's tokenizer does not define one and no override template is given

          chat_template_kwargs: Additional kwargs to pass to the template renderer. Will be accessible by the
              chat template.

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

          guided_choice: Choices for guided decoding. Only supported in vllm.

          guided_decoding_backend: If specified, will override the default guided decoding backend of the server
              for this specific request. If set, must be either 'outlines' /
              'lm-format-enforcer'

          guided_grammar: Context-free grammar for guided decoding. Only supported in vllm.

          guided_json: JSON schema for guided decoding. Only supported in vllm.

          guided_regex: Regex for guided decoding. Only supported in vllm.

          guided_whitespace_pattern: If specified, will override the default whitespace pattern for guided json
              decoding.

          include_stop_str_in_output: Whether to include the stop string in the output.

          inference_extra_headers: Additional headers to be included in the API request

          inference_extra_params: Additional params to be included in the API request

          inference_timeout: Timeout for the API request

          logit_bias: Modify the likelihood of specified tokens appearing in the completion.

              Accepts a JSON object that maps tokens (specified by their token ID in the
              tokenizer) to an associated bias value from -100 to 100. Mathematically, the
              bias is added to the logits generated by the model prior to sampling. The exact
              effect will vary per model, but values between -1 and 1 should decrease or
              increase likelihood of selection; values like -100 or 100 should result in a ban
              or exclusive selection of the relevant token.

          logprobs: Whether to return log probabilities of the output tokens or not. If true,
              returns the log probabilities of each output token returned in the content of
              message.

          max_completion_tokens: Maximum number of tokens to generate in the completion

          max_tokens: The maximum number of tokens that can be generated.

              The token count of your prompt plus max_tokens cannot exceed the model's context
              length.

          memory_strategy: The memory strategy to use for the conversation. A memory strategy is a way to
              prevent the underlying LLM's context limit from being exceeded. Only the
              `last_k` memory strategy is supported at this time.

          modalities: List of modalities for the chat completion

          n: How many completions to generate for each prompt.

              Note: Because this parameter generates many completions, it can quickly consume
              your token quota. Use carefully and ensure that you have reasonable settings for
              max_tokens and stop.

          parallel_tool_calls: Currently only supported for OpenAI models.Enables calling tools in parallel.

          prediction: Configure a predicted output to reduce latency

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

          response_format: An object specifying the format that the model must output

          seed: If specified, our system will make a best effort to sample deterministically,
              such that repeated requests with the same seed and parameters should return the
              same result.

          stop: Up to 4 sequences where the API will stop generating further tokens.

          stream_options: Customize streaming behavior

          suffix: The suffix that comes after a completion of inserted text.This parameter is only
              supported for gpt-3.5-turbo-instruct.

          temperature: The sampling temperature to use for the completion. Higher values mean the model
              will take more risks.

          tool_choice: Currently only supported for OpenAI and Anthropic models.Controls which (if any)
              tool is called by the model.

          tools: Currently only supported for OpenAI and Anthropic models.A list of tools the
              model may call.Currently, only functions are supported as a tool.Use this to
              provide a list of functions the model may generate JSON inputs for.

          top_k: Only sample from the top K options for each subsequent token

          top_logprobs: An integer between 0 and 20 specifying the number of most likely tokens to
              return at each token position, each with an associated log probability. logprobs
              must be set to true if this parameter is used.

          top_p: An alternative to sampling with temperature, called nucleus sampling, where the
              model considers the results of the tokens with top_p probability mass. So 0.1
              means only the tokens comprising the top 10% probability mass are considered.

              It is generally recommended to alter this or temperature but not both.

          user: A unique identifier representing your end-user.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["messages", "model"], ["messages", "model", "stream"])
    async def create(
        self,
        *,
        messages: Iterable[completion_create_params.Message],
        model: str,
        audio: completion_create_params.Audio | NotGiven = NOT_GIVEN,
        best_of: int | NotGiven = NOT_GIVEN,
        chat_template: str | NotGiven = NOT_GIVEN,
        chat_template_kwargs: object | NotGiven = NOT_GIVEN,
        frequency_penalty: float | NotGiven = NOT_GIVEN,
        guided_choice: List[str] | NotGiven = NOT_GIVEN,
        guided_decoding_backend: str | NotGiven = NOT_GIVEN,
        guided_grammar: str | NotGiven = NOT_GIVEN,
        guided_json: object | NotGiven = NOT_GIVEN,
        guided_regex: str | NotGiven = NOT_GIVEN,
        guided_whitespace_pattern: str | NotGiven = NOT_GIVEN,
        include_stop_str_in_output: bool | NotGiven = NOT_GIVEN,
        inference_extra_headers: object | NotGiven = NOT_GIVEN,
        inference_extra_params: object | NotGiven = NOT_GIVEN,
        inference_timeout: Union[float, str] | NotGiven = NOT_GIVEN,
        logit_bias: Dict[str, int] | NotGiven = NOT_GIVEN,
        logprobs: bool | NotGiven = NOT_GIVEN,
        max_completion_tokens: int | NotGiven = NOT_GIVEN,
        max_tokens: int | NotGiven = NOT_GIVEN,
        memory_strategy: completion_create_params.MemoryStrategy | NotGiven = NOT_GIVEN,
        modalities: List[Literal["text", "audio"]] | NotGiven = NOT_GIVEN,
        n: int | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: object | NotGiven = NOT_GIVEN,
        presence_penalty: float | NotGiven = NOT_GIVEN,
        response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: int | NotGiven = NOT_GIVEN,
        stop: Union[str, List[str]] | NotGiven = NOT_GIVEN,
        stream: Literal[False] | Literal[True] | NotGiven = NOT_GIVEN,
        stream_options: object | NotGiven = NOT_GIVEN,
        suffix: str | NotGiven = NOT_GIVEN,
        temperature: float | NotGiven = NOT_GIVEN,
        tool_choice: completion_create_params.ToolChoice | NotGiven = NOT_GIVEN,
        tools: Iterable[completion_create_params.Tool] | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        top_logprobs: int | NotGiven = NOT_GIVEN,
        top_p: float | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompletionCreateResponse | AsyncStream[ChatCompletionChunk]:
        return cast(
            CompletionCreateResponse,
            await self._post(
                "/v4/beta/chat/completions",
                body=await async_maybe_transform(
                    {
                        "messages": messages,
                        "model": model,
                        "audio": audio,
                        "best_of": best_of,
                        "chat_template": chat_template,
                        "chat_template_kwargs": chat_template_kwargs,
                        "frequency_penalty": frequency_penalty,
                        "guided_choice": guided_choice,
                        "guided_decoding_backend": guided_decoding_backend,
                        "guided_grammar": guided_grammar,
                        "guided_json": guided_json,
                        "guided_regex": guided_regex,
                        "guided_whitespace_pattern": guided_whitespace_pattern,
                        "include_stop_str_in_output": include_stop_str_in_output,
                        "inference_extra_headers": inference_extra_headers,
                        "inference_extra_params": inference_extra_params,
                        "inference_timeout": inference_timeout,
                        "logit_bias": logit_bias,
                        "logprobs": logprobs,
                        "max_completion_tokens": max_completion_tokens,
                        "max_tokens": max_tokens,
                        "memory_strategy": memory_strategy,
                        "modalities": modalities,
                        "n": n,
                        "parallel_tool_calls": parallel_tool_calls,
                        "prediction": prediction,
                        "presence_penalty": presence_penalty,
                        "response_format": response_format,
                        "seed": seed,
                        "stop": stop,
                        "stream": stream,
                        "stream_options": stream_options,
                        "suffix": suffix,
                        "temperature": temperature,
                        "tool_choice": tool_choice,
                        "tools": tools,
                        "top_k": top_k,
                        "top_logprobs": top_logprobs,
                        "top_p": top_p,
                        "user": user,
                    },
                    completion_create_params.CompletionCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, CompletionCreateResponse
                ),  # Union types cannot be passed in as arguments in the type system
                stream=stream or False,
                stream_cls=AsyncStream[ChatCompletionChunk],
            ),
        )


class CompletionsResourceWithRawResponse:
    def __init__(self, completions: CompletionsResource) -> None:
        self._completions = completions

        self.create = to_raw_response_wrapper(
            completions.create,
        )


class AsyncCompletionsResourceWithRawResponse:
    def __init__(self, completions: AsyncCompletionsResource) -> None:
        self._completions = completions

        self.create = async_to_raw_response_wrapper(
            completions.create,
        )


class CompletionsResourceWithStreamingResponse:
    def __init__(self, completions: CompletionsResource) -> None:
        self._completions = completions

        self.create = to_streamed_response_wrapper(
            completions.create,
        )


class AsyncCompletionsResourceWithStreamingResponse:
    def __init__(self, completions: AsyncCompletionsResource) -> None:
        self._completions = completions

        self.create = async_to_streamed_response_wrapper(
            completions.create,
        )
