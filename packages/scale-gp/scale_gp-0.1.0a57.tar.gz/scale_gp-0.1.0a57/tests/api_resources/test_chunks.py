# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from scale_gp import SGPClient, AsyncSGPClient
from tests.utils import assert_matches_type
from scale_gp.types import RankedChunksResponse, SynthesizeChunksResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChunks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_rank(self, client: SGPClient) -> None:
        chunk = client.chunks.rank(
            query="query",
            rank_strategy={},
            relevant_chunks=[
                {
                    "chunk_id": "chunk_id",
                    "score": 0,
                    "text": "text",
                }
            ],
        )
        assert_matches_type(RankedChunksResponse, chunk, path=["response"])

    @parametrize
    def test_method_rank_with_all_params(self, client: SGPClient) -> None:
        chunk = client.chunks.rank(
            query="query",
            rank_strategy={
                "method": "cross_encoder",
                "params": {"cross_encoder_model": "cross-encoder/ms-marco-MiniLM-L-12-v2"},
            },
            relevant_chunks=[
                {
                    "chunk_id": "chunk_id",
                    "score": 0,
                    "text": "text",
                    "attachment_url": "attachment_url",
                    "embedding": [0],
                    "metadata": {},
                    "title": "title",
                    "user_supplied_metadata": {},
                }
            ],
            account_id="account_id",
            top_k=1,
        )
        assert_matches_type(RankedChunksResponse, chunk, path=["response"])

    @parametrize
    def test_raw_response_rank(self, client: SGPClient) -> None:
        response = client.chunks.with_raw_response.rank(
            query="query",
            rank_strategy={},
            relevant_chunks=[
                {
                    "chunk_id": "chunk_id",
                    "score": 0,
                    "text": "text",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chunk = response.parse()
        assert_matches_type(RankedChunksResponse, chunk, path=["response"])

    @parametrize
    def test_streaming_response_rank(self, client: SGPClient) -> None:
        with client.chunks.with_streaming_response.rank(
            query="query",
            rank_strategy={},
            relevant_chunks=[
                {
                    "chunk_id": "chunk_id",
                    "score": 0,
                    "text": "text",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chunk = response.parse()
            assert_matches_type(RankedChunksResponse, chunk, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_synthesis(self, client: SGPClient) -> None:
        chunk = client.chunks.synthesis(
            chunks=[
                {
                    "chunk_id": "chunk_id",
                    "score": 0,
                    "text": "text",
                }
            ],
            query="query",
        )
        assert_matches_type(SynthesizeChunksResponse, chunk, path=["response"])

    @parametrize
    def test_raw_response_synthesis(self, client: SGPClient) -> None:
        response = client.chunks.with_raw_response.synthesis(
            chunks=[
                {
                    "chunk_id": "chunk_id",
                    "score": 0,
                    "text": "text",
                }
            ],
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chunk = response.parse()
        assert_matches_type(SynthesizeChunksResponse, chunk, path=["response"])

    @parametrize
    def test_streaming_response_synthesis(self, client: SGPClient) -> None:
        with client.chunks.with_streaming_response.synthesis(
            chunks=[
                {
                    "chunk_id": "chunk_id",
                    "score": 0,
                    "text": "text",
                }
            ],
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chunk = response.parse()
            assert_matches_type(SynthesizeChunksResponse, chunk, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncChunks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_rank(self, async_client: AsyncSGPClient) -> None:
        chunk = await async_client.chunks.rank(
            query="query",
            rank_strategy={},
            relevant_chunks=[
                {
                    "chunk_id": "chunk_id",
                    "score": 0,
                    "text": "text",
                }
            ],
        )
        assert_matches_type(RankedChunksResponse, chunk, path=["response"])

    @parametrize
    async def test_method_rank_with_all_params(self, async_client: AsyncSGPClient) -> None:
        chunk = await async_client.chunks.rank(
            query="query",
            rank_strategy={
                "method": "cross_encoder",
                "params": {"cross_encoder_model": "cross-encoder/ms-marco-MiniLM-L-12-v2"},
            },
            relevant_chunks=[
                {
                    "chunk_id": "chunk_id",
                    "score": 0,
                    "text": "text",
                    "attachment_url": "attachment_url",
                    "embedding": [0],
                    "metadata": {},
                    "title": "title",
                    "user_supplied_metadata": {},
                }
            ],
            account_id="account_id",
            top_k=1,
        )
        assert_matches_type(RankedChunksResponse, chunk, path=["response"])

    @parametrize
    async def test_raw_response_rank(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.chunks.with_raw_response.rank(
            query="query",
            rank_strategy={},
            relevant_chunks=[
                {
                    "chunk_id": "chunk_id",
                    "score": 0,
                    "text": "text",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chunk = await response.parse()
        assert_matches_type(RankedChunksResponse, chunk, path=["response"])

    @parametrize
    async def test_streaming_response_rank(self, async_client: AsyncSGPClient) -> None:
        async with async_client.chunks.with_streaming_response.rank(
            query="query",
            rank_strategy={},
            relevant_chunks=[
                {
                    "chunk_id": "chunk_id",
                    "score": 0,
                    "text": "text",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chunk = await response.parse()
            assert_matches_type(RankedChunksResponse, chunk, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_synthesis(self, async_client: AsyncSGPClient) -> None:
        chunk = await async_client.chunks.synthesis(
            chunks=[
                {
                    "chunk_id": "chunk_id",
                    "score": 0,
                    "text": "text",
                }
            ],
            query="query",
        )
        assert_matches_type(SynthesizeChunksResponse, chunk, path=["response"])

    @parametrize
    async def test_raw_response_synthesis(self, async_client: AsyncSGPClient) -> None:
        response = await async_client.chunks.with_raw_response.synthesis(
            chunks=[
                {
                    "chunk_id": "chunk_id",
                    "score": 0,
                    "text": "text",
                }
            ],
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chunk = await response.parse()
        assert_matches_type(SynthesizeChunksResponse, chunk, path=["response"])

    @parametrize
    async def test_streaming_response_synthesis(self, async_client: AsyncSGPClient) -> None:
        async with async_client.chunks.with_streaming_response.synthesis(
            chunks=[
                {
                    "chunk_id": "chunk_id",
                    "score": 0,
                    "text": "text",
                }
            ],
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chunk = await response.parse()
            assert_matches_type(SynthesizeChunksResponse, chunk, path=["response"])

        assert cast(Any, response.is_closed) is True
