# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestApplicationThreads:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="prisma failure")
    @parametrize
    def test_method_process(self, client: SGPClient) -> None:
        application_thread = client.application_threads.process(
            thread_id="thread_id",
            application_variant_id="application_variant_id",
            inputs={},
        )
        assert_matches_type(object, application_thread, path=["response"])

    @pytest.mark.skip(reason="prisma failure")
    @parametrize
    def test_method_process_with_all_params(self, client: SGPClient) -> None:
        application_thread = client.application_threads.process(
            thread_id="thread_id",
            application_variant_id="application_variant_id",
            inputs={},
            history=[
                {
                    "request": "request",
                    "response": "response",
                    "session_data": {},
                }
            ],
            operation_metadata={},
            overrides={
                "foo": {
                    "artifact_ids_filter": ["string"],
                    "artifact_name_regex": ["string"],
                    "type": "knowledge_base_schema",
                }
            },
            stream=True,
        )
        assert_matches_type(object, application_thread, path=["response"])

    @pytest.mark.skip(reason="prisma failure")
    @parametrize
    def test_raw_response_process(self, client: SGPClient) -> None:
        response = client.application_threads.with_raw_response.process(
            thread_id="thread_id",
            application_variant_id="application_variant_id",
            inputs={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_thread = response.parse()
        assert_matches_type(object, application_thread, path=["response"])

    @pytest.mark.skip(reason="prisma failure")
    @parametrize
    def test_streaming_response_process(self, client: SGPClient) -> None:
        with client.application_threads.with_streaming_response.process(
            thread_id="thread_id",
            application_variant_id="application_variant_id",
            inputs={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_thread = response.parse()
            assert_matches_type(object, application_thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prisma failure")
    @parametrize
    def test_path_params_process(self, client: SGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            client.application_threads.with_raw_response.process(
                thread_id="thread_id",
                application_variant_id="",
                inputs={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            client.application_threads.with_raw_response.process(
                thread_id="",
                application_variant_id="application_variant_id",
                inputs={},
            )


class TestAsyncApplicationThreads:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="prisma failure")
    @parametrize
    async def test_method_process(self, async_client: AsyncSGPClient) -> None:
        application_thread = await async_client.application_threads.process(
            thread_id="thread_id",
            application_variant_id="application_variant_id",
            inputs={},
        )
        assert_matches_type(object, application_thread, path=["response"])

    @pytest.mark.skip(reason="prisma failure")
    @parametrize
    async def test_method_process_with_all_params(self, async_client: AsyncSGPClient) -> None:
        application_thread = await async_client.application_threads.process(
            thread_id="thread_id",
            application_variant_id="application_variant_id",
            inputs={},
            history=[
                {
                    "request": "request",
                    "response": "response",
                    "session_data": {},
                }
            ],
            operation_metadata={},
            overrides={
                "foo": {
                    "artifact_ids_filter": ["string"],
                    "artifact_name_regex": ["string"],
                    "type": "knowledge_base_schema",
                }
            },
            stream=True,
        )
        assert_matches_type(object, application_thread, path=["response"])

    @pytest.mark.skip(reason="prisma failure")
    @parametrize
    async def test_raw_response_process(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.application_threads.with_raw_response.process(
            thread_id="thread_id",
            application_variant_id="application_variant_id",
            inputs={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_thread = await response.parse()
        assert_matches_type(object, application_thread, path=["response"])

    @pytest.mark.skip(reason="prisma failure")
    @parametrize
    async def test_streaming_response_process(self, async_client: AsyncSGPClient) -> None:
        async with async_client.application_threads.with_streaming_response.process(
            thread_id="thread_id",
            application_variant_id="application_variant_id",
            inputs={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_thread = await response.parse()
            assert_matches_type(object, application_thread, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="prisma failure")
    @parametrize
    async def test_path_params_process(self, async_client: AsyncSGPClient) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_variant_id` but received ''"
        ):
            await async_client.application_threads.with_raw_response.process(
                thread_id="thread_id",
                application_variant_id="",
                inputs={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `thread_id` but received ''"):
            await async_client.application_threads.with_raw_response.process(
                thread_id="",
                application_variant_id="application_variant_id",
                inputs={},
            )
