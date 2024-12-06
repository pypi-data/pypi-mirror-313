# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..types import chunk_rank_params, chunk_synthesis_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.shared_params.chunk import Chunk
from ..types.ranked_chunks_response import RankedChunksResponse
from ..types.synthesize_chunks_response import SynthesizeChunksResponse

__all__ = ["ChunksResource", "AsyncChunksResource"]


class ChunksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ChunksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ChunksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChunksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ChunksResourceWithStreamingResponse(self)

    def rank(
        self,
        *,
        query: str,
        rank_strategy: chunk_rank_params.RankStrategy,
        relevant_chunks: Iterable[Chunk],
        account_id: str | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> RankedChunksResponse:
        """
        ### Description

        Sorts a list of text chunks by similarity against a given query string.

        ### Details

        Use this API endpoint to rank which text chunks provide the most relevant
        responses to a given a query string.

        This is useful for stuffing chunks into a prompt where order may matter or for
        filtering out less relevant chunks according to the ranking strategy. For
        example, this API may be useful when doing retrieval augment generation (RAG).
        Sometimes vector store
        [similarity search](https://scale-egp.readme.io/reference/query_vector_store)
        does not always return the best ranking of text chunks, since this is heavily
        dependent on embedding generation. This API endpoint can act as a
        post-processing step to re-sort the given chunks using more complex strategies
        that may outperform vector search, and then filter only the top-k most relevant
        chunks to stuff into the prompt for RAG.

        ### Restrictions and Limits

        Ranking can be a very intensive and slow process depending on methodology where
        duration scales with number of chunks. For best performance, we recommend
        ranking less than 640 chunks at a time, and you may see a decrease in
        performance as the number of chunks ranked increases.

        Args:
          query: Natural language query to re-rank chunks against. If a vector store query was
              originally used to retrieve these chunks, please use the same query for this
              ranking

          rank_strategy: The ranking strategy to use.

              Rank strategies determine how the ranking is done, They consist of the ranking
              method name and additional params needed to compute the ranking.

              Use the built-in `cross_encoder` or `rouge` strategies or create a custom one
              with the Models API.

          relevant_chunks: List of chunks to rank

          account_id: Account to rank chunks with. If you have access to more than one account, you
              must specify an account_id

          top_k: Number of chunks to return. Must be greater than 0 if specified. If not
              specified, all chunks will be returned.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v4/chunks/rank",
            body=maybe_transform(
                {
                    "query": query,
                    "rank_strategy": rank_strategy,
                    "relevant_chunks": relevant_chunks,
                    "account_id": account_id,
                    "top_k": top_k,
                },
                chunk_rank_params.ChunkRankParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RankedChunksResponse,
        )

    def synthesis(
        self,
        *,
        chunks: Iterable[Chunk],
        query: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SynthesizeChunksResponse:
        """
        ### Description

        Synthesizes a response to the given query using the given chunks as context.

        ### Details

        This API operates on "chunks," which are the result of
        [querying a vector store](https://scale-egp.readme.io/reference/query_vector_store).
        A chunk is simply a fragment of a larger document. It can optionally have its
        own metadata or ID. You can also construct your own chunks from scratch so long
        as you provide the text pertaining to each chunk.

        Synthesizing chunks can be thought of as the final step in a retrieval augmented
        generation ( RAG) system, after querying for chunks and potentially
        [ranking them](https://scale-egp.readme.io/reference/rank_chunks). Once you have
        the relevant chunks to use to respond to the user, you'll want to synthesize a
        readable natural language answer. During this synthesis step, we prompt an LLM
        with instructions and a set of (possibly transformed) chunks to guide it toward
        synthesizing a natural language response to the user query.

        There are several synthesis strategies, whose difference become more apparent as
        the number of chunks increases. Currently, EGP supports the `compact` strategy
        by default: stuff as many chunks into the synthesis LLM as possible, produce a
        best-effort answer, then continue to stuff and answer the next set of chunks.
        The answer is passed through and gradually refined with each iteration of chunk
        scanning. This continues until all chunks have been scanned and a final answer
        is synthesized. More synthesis strategies are currently in development!

        ### Restrictions and Limits

        Generally, chunk synthesis increases its token consumption linearly the number
        of chunk-tokens. The `compact` strategy attempts to be as token-efficient as
        possible by stuffing tokens into each round of chunk scanning. Other strategies
        (in development!) may produce better summaries or more precise answers at the
        expense of more tokens consumed.

        Broadly, we recommend keeping the number of chunks to under 100, or the total
        number of tokens across all chunks under around 10,000.

        Args:
          chunks: List of chunks to use to synthesize the response.

          query: Natural language query to resolve using the supplied chunks.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v4/chunks/synthesis",
            body=maybe_transform(
                {
                    "chunks": chunks,
                    "query": query,
                },
                chunk_synthesis_params.ChunkSynthesisParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SynthesizeChunksResponse,
        )


class AsyncChunksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncChunksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncChunksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChunksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncChunksResourceWithStreamingResponse(self)

    async def rank(
        self,
        *,
        query: str,
        rank_strategy: chunk_rank_params.RankStrategy,
        relevant_chunks: Iterable[Chunk],
        account_id: str | NotGiven = NOT_GIVEN,
        top_k: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> RankedChunksResponse:
        """
        ### Description

        Sorts a list of text chunks by similarity against a given query string.

        ### Details

        Use this API endpoint to rank which text chunks provide the most relevant
        responses to a given a query string.

        This is useful for stuffing chunks into a prompt where order may matter or for
        filtering out less relevant chunks according to the ranking strategy. For
        example, this API may be useful when doing retrieval augment generation (RAG).
        Sometimes vector store
        [similarity search](https://scale-egp.readme.io/reference/query_vector_store)
        does not always return the best ranking of text chunks, since this is heavily
        dependent on embedding generation. This API endpoint can act as a
        post-processing step to re-sort the given chunks using more complex strategies
        that may outperform vector search, and then filter only the top-k most relevant
        chunks to stuff into the prompt for RAG.

        ### Restrictions and Limits

        Ranking can be a very intensive and slow process depending on methodology where
        duration scales with number of chunks. For best performance, we recommend
        ranking less than 640 chunks at a time, and you may see a decrease in
        performance as the number of chunks ranked increases.

        Args:
          query: Natural language query to re-rank chunks against. If a vector store query was
              originally used to retrieve these chunks, please use the same query for this
              ranking

          rank_strategy: The ranking strategy to use.

              Rank strategies determine how the ranking is done, They consist of the ranking
              method name and additional params needed to compute the ranking.

              Use the built-in `cross_encoder` or `rouge` strategies or create a custom one
              with the Models API.

          relevant_chunks: List of chunks to rank

          account_id: Account to rank chunks with. If you have access to more than one account, you
              must specify an account_id

          top_k: Number of chunks to return. Must be greater than 0 if specified. If not
              specified, all chunks will be returned.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v4/chunks/rank",
            body=await async_maybe_transform(
                {
                    "query": query,
                    "rank_strategy": rank_strategy,
                    "relevant_chunks": relevant_chunks,
                    "account_id": account_id,
                    "top_k": top_k,
                },
                chunk_rank_params.ChunkRankParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RankedChunksResponse,
        )

    async def synthesis(
        self,
        *,
        chunks: Iterable[Chunk],
        query: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SynthesizeChunksResponse:
        """
        ### Description

        Synthesizes a response to the given query using the given chunks as context.

        ### Details

        This API operates on "chunks," which are the result of
        [querying a vector store](https://scale-egp.readme.io/reference/query_vector_store).
        A chunk is simply a fragment of a larger document. It can optionally have its
        own metadata or ID. You can also construct your own chunks from scratch so long
        as you provide the text pertaining to each chunk.

        Synthesizing chunks can be thought of as the final step in a retrieval augmented
        generation ( RAG) system, after querying for chunks and potentially
        [ranking them](https://scale-egp.readme.io/reference/rank_chunks). Once you have
        the relevant chunks to use to respond to the user, you'll want to synthesize a
        readable natural language answer. During this synthesis step, we prompt an LLM
        with instructions and a set of (possibly transformed) chunks to guide it toward
        synthesizing a natural language response to the user query.

        There are several synthesis strategies, whose difference become more apparent as
        the number of chunks increases. Currently, EGP supports the `compact` strategy
        by default: stuff as many chunks into the synthesis LLM as possible, produce a
        best-effort answer, then continue to stuff and answer the next set of chunks.
        The answer is passed through and gradually refined with each iteration of chunk
        scanning. This continues until all chunks have been scanned and a final answer
        is synthesized. More synthesis strategies are currently in development!

        ### Restrictions and Limits

        Generally, chunk synthesis increases its token consumption linearly the number
        of chunk-tokens. The `compact` strategy attempts to be as token-efficient as
        possible by stuffing tokens into each round of chunk scanning. Other strategies
        (in development!) may produce better summaries or more precise answers at the
        expense of more tokens consumed.

        Broadly, we recommend keeping the number of chunks to under 100, or the total
        number of tokens across all chunks under around 10,000.

        Args:
          chunks: List of chunks to use to synthesize the response.

          query: Natural language query to resolve using the supplied chunks.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v4/chunks/synthesis",
            body=await async_maybe_transform(
                {
                    "chunks": chunks,
                    "query": query,
                },
                chunk_synthesis_params.ChunkSynthesisParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SynthesizeChunksResponse,
        )


class ChunksResourceWithRawResponse:
    def __init__(self, chunks: ChunksResource) -> None:
        self._chunks = chunks

        self.rank = to_raw_response_wrapper(
            chunks.rank,
        )
        self.synthesis = to_raw_response_wrapper(
            chunks.synthesis,
        )


class AsyncChunksResourceWithRawResponse:
    def __init__(self, chunks: AsyncChunksResource) -> None:
        self._chunks = chunks

        self.rank = async_to_raw_response_wrapper(
            chunks.rank,
        )
        self.synthesis = async_to_raw_response_wrapper(
            chunks.synthesis,
        )


class ChunksResourceWithStreamingResponse:
    def __init__(self, chunks: ChunksResource) -> None:
        self._chunks = chunks

        self.rank = to_streamed_response_wrapper(
            chunks.rank,
        )
        self.synthesis = to_streamed_response_wrapper(
            chunks.synthesis,
        )


class AsyncChunksResourceWithStreamingResponse:
    def __init__(self, chunks: AsyncChunksResource) -> None:
        self._chunks = chunks

        self.rank = async_to_streamed_response_wrapper(
            chunks.rank,
        )
        self.synthesis = async_to_streamed_response_wrapper(
            chunks.synthesis,
        )
