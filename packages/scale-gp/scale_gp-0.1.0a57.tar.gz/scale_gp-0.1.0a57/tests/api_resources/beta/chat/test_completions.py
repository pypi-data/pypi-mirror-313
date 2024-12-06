# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types.beta.chat import CompletionCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCompletions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create_overload_1(self, client: SGPClient) -> None:
        completion = client.beta.chat.completions.create(
            messages=[{"content": "string"}],
            model="model",
        )
        assert_matches_type(CompletionCreateResponse, completion, path=["response"])

    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: SGPClient) -> None:
        completion = client.beta.chat.completions.create(
            messages=[
                {
                    "content": "string",
                    "name": "name",
                    "role": "user",
                }
            ],
            model="model",
            audio={
                "format": "wav",
                "voice": "alloy",
            },
            best_of=0,
            chat_template="chat_template",
            chat_template_kwargs={},
            frequency_penalty=0,
            guided_choice=["string"],
            guided_decoding_backend="guided_decoding_backend",
            guided_grammar="guided_grammar",
            guided_json={},
            guided_regex="guided_regex",
            guided_whitespace_pattern="guided_whitespace_pattern",
            include_stop_str_in_output=True,
            inference_extra_headers={},
            inference_extra_params={},
            inference_timeout=0,
            logit_bias={"foo": 0},
            logprobs=True,
            max_completion_tokens=0,
            max_tokens=0,
            memory_strategy={
                "k": 0,
                "name": "last_k",
            },
            modalities=["text"],
            n=0,
            parallel_tool_calls=True,
            prediction={},
            presence_penalty=0,
            response_format={"type": "text"},
            seed=0,
            stop="string",
            stream=False,
            stream_options={},
            suffix="suffix",
            temperature=0,
            tool_choice="none",
            tools=[
                {
                    "function": {
                        "name": "name",
                        "description": "description",
                        "parameters": {},
                    },
                    "type": "function",
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            top_k=0,
            top_logprobs=0,
            top_p=0,
            user="user",
        )
        assert_matches_type(CompletionCreateResponse, completion, path=["response"])

    @parametrize
    def test_raw_response_create_overload_1(self, client: SGPClient) -> None:
        response = client.beta.chat.completions.with_raw_response.create(
            messages=[{"content": "string"}],
            model="model",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        completion = response.parse()
        assert_matches_type(CompletionCreateResponse, completion, path=["response"])

    @parametrize
    def test_streaming_response_create_overload_1(self, client: SGPClient) -> None:
        with client.beta.chat.completions.with_streaming_response.create(
            messages=[{"content": "string"}],
            model="model",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            completion = response.parse()
            assert_matches_type(CompletionCreateResponse, completion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_create_overload_2(self, client: SGPClient) -> None:
        completion_stream = client.beta.chat.completions.create(
            messages=[{"content": "string"}],
            model="model",
            stream=True,
        )
        completion_stream.response.close()

    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: SGPClient) -> None:
        completion_stream = client.beta.chat.completions.create(
            messages=[
                {
                    "content": "string",
                    "name": "name",
                    "role": "user",
                }
            ],
            model="model",
            stream=True,
            audio={
                "format": "wav",
                "voice": "alloy",
            },
            best_of=0,
            chat_template="chat_template",
            chat_template_kwargs={},
            frequency_penalty=0,
            guided_choice=["string"],
            guided_decoding_backend="guided_decoding_backend",
            guided_grammar="guided_grammar",
            guided_json={},
            guided_regex="guided_regex",
            guided_whitespace_pattern="guided_whitespace_pattern",
            include_stop_str_in_output=True,
            inference_extra_headers={},
            inference_extra_params={},
            inference_timeout=0,
            logit_bias={"foo": 0},
            logprobs=True,
            max_completion_tokens=0,
            max_tokens=0,
            memory_strategy={
                "k": 0,
                "name": "last_k",
            },
            modalities=["text"],
            n=0,
            parallel_tool_calls=True,
            prediction={},
            presence_penalty=0,
            response_format={"type": "text"},
            seed=0,
            stop="string",
            stream_options={},
            suffix="suffix",
            temperature=0,
            tool_choice="none",
            tools=[
                {
                    "function": {
                        "name": "name",
                        "description": "description",
                        "parameters": {},
                    },
                    "type": "function",
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            top_k=0,
            top_logprobs=0,
            top_p=0,
            user="user",
        )
        completion_stream.response.close()

    @parametrize
    def test_raw_response_create_overload_2(self, client: SGPClient) -> None:
        response = client.beta.chat.completions.with_raw_response.create(
            messages=[{"content": "string"}],
            model="model",
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        stream.close()

    @parametrize
    def test_streaming_response_create_overload_2(self, client: SGPClient) -> None:
        with client.beta.chat.completions.with_streaming_response.create(
            messages=[{"content": "string"}],
            model="model",
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True


class TestAsyncCompletions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        completion = await async_client.beta.chat.completions.create(
            messages=[{"content": "string"}],
            model="model",
        )
        assert_matches_type(CompletionCreateResponse, completion, path=["response"])

    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncSGPClient) -> None:
        completion = await async_client.beta.chat.completions.create(
            messages=[
                {
                    "content": "string",
                    "name": "name",
                    "role": "user",
                }
            ],
            model="model",
            audio={
                "format": "wav",
                "voice": "alloy",
            },
            best_of=0,
            chat_template="chat_template",
            chat_template_kwargs={},
            frequency_penalty=0,
            guided_choice=["string"],
            guided_decoding_backend="guided_decoding_backend",
            guided_grammar="guided_grammar",
            guided_json={},
            guided_regex="guided_regex",
            guided_whitespace_pattern="guided_whitespace_pattern",
            include_stop_str_in_output=True,
            inference_extra_headers={},
            inference_extra_params={},
            inference_timeout=0,
            logit_bias={"foo": 0},
            logprobs=True,
            max_completion_tokens=0,
            max_tokens=0,
            memory_strategy={
                "k": 0,
                "name": "last_k",
            },
            modalities=["text"],
            n=0,
            parallel_tool_calls=True,
            prediction={},
            presence_penalty=0,
            response_format={"type": "text"},
            seed=0,
            stop="string",
            stream=False,
            stream_options={},
            suffix="suffix",
            temperature=0,
            tool_choice="none",
            tools=[
                {
                    "function": {
                        "name": "name",
                        "description": "description",
                        "parameters": {},
                    },
                    "type": "function",
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            top_k=0,
            top_logprobs=0,
            top_p=0,
            user="user",
        )
        assert_matches_type(CompletionCreateResponse, completion, path=["response"])

    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.beta.chat.completions.with_raw_response.create(
            messages=[{"content": "string"}],
            model="model",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        completion = await response.parse()
        assert_matches_type(CompletionCreateResponse, completion, path=["response"])

    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncSGPClient) -> None:
        async with async_client.beta.chat.completions.with_streaming_response.create(
            messages=[{"content": "string"}],
            model="model",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            completion = await response.parse()
            assert_matches_type(CompletionCreateResponse, completion, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        completion_stream = await async_client.beta.chat.completions.create(
            messages=[{"content": "string"}],
            model="model",
            stream=True,
        )
        await completion_stream.response.aclose()

    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncSGPClient) -> None:
        completion_stream = await async_client.beta.chat.completions.create(
            messages=[
                {
                    "content": "string",
                    "name": "name",
                    "role": "user",
                }
            ],
            model="model",
            stream=True,
            audio={
                "format": "wav",
                "voice": "alloy",
            },
            best_of=0,
            chat_template="chat_template",
            chat_template_kwargs={},
            frequency_penalty=0,
            guided_choice=["string"],
            guided_decoding_backend="guided_decoding_backend",
            guided_grammar="guided_grammar",
            guided_json={},
            guided_regex="guided_regex",
            guided_whitespace_pattern="guided_whitespace_pattern",
            include_stop_str_in_output=True,
            inference_extra_headers={},
            inference_extra_params={},
            inference_timeout=0,
            logit_bias={"foo": 0},
            logprobs=True,
            max_completion_tokens=0,
            max_tokens=0,
            memory_strategy={
                "k": 0,
                "name": "last_k",
            },
            modalities=["text"],
            n=0,
            parallel_tool_calls=True,
            prediction={},
            presence_penalty=0,
            response_format={"type": "text"},
            seed=0,
            stop="string",
            stream_options={},
            suffix="suffix",
            temperature=0,
            tool_choice="none",
            tools=[
                {
                    "function": {
                        "name": "name",
                        "description": "description",
                        "parameters": {},
                    },
                    "type": "function",
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            top_k=0,
            top_logprobs=0,
            top_p=0,
            user="user",
        )
        await completion_stream.response.aclose()

    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.beta.chat.completions.with_raw_response.create(
            messages=[{"content": "string"}],
            model="model",
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = await response.parse()
        await stream.close()

    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncSGPClient) -> None:
        async with async_client.beta.chat.completions.with_streaming_response.create(
            messages=[{"content": "string"}],
            model="model",
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True
