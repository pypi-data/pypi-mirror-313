# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Literal, overload

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    required_args,
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncPageResponse, AsyncPageResponse
from ..._base_client import AsyncPaginator, make_request_options
from ...types.knowledge_bases import upload_list_params, upload_create_params, upload_retrieve_params
from ...types.local_chunks_source_config_param import LocalChunksSourceConfigParam
from ...types.knowledge_bases.upload_list_response import UploadListResponse
from ...types.knowledge_bases.knowledge_base_upload import KnowledgeBaseUpload
from ...types.knowledge_bases.cancel_knowledge_base_upload_response import CancelKnowledgeBaseUploadResponse
from ...types.knowledge_bases.create_knowledge_base_upload_response import CreateKnowledgeBaseUploadResponse

__all__ = ["UploadsResource", "AsyncUploadsResource"]


class UploadsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UploadsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return UploadsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UploadsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return UploadsResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        knowledge_base_id: str,
        *,
        data_source_config: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceConfig,
        chunking_strategy_config: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfig
        | NotGiven = NOT_GIVEN,
        data_source_auth_config: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceAuthConfig
        | NotGiven = NOT_GIVEN,
        force_reupload: bool | NotGiven = NOT_GIVEN,
        tagging_information: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformation
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateKnowledgeBaseUploadResponse:
        """
        Submit Upload Job

        Args:
          data_source_config: Configuration for the data source which describes where to find the data.

          chunking_strategy_config: Configuration for the chunking strategy which describes how to chunk the data.

          data_source_auth_config: Configuration for the data source which describes how to authenticate to the
              data source.

          force_reupload: Force reingest, regardless the change of the source file.

          tagging_information: A dictionary of tags to apply to all artifacts added from the data source.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        knowledge_base_id: str,
        *,
        data_source_config: LocalChunksSourceConfigParam,
        chunks: Iterable[upload_create_params.CreateKnowledgeBaseV2UploadFromLocalChunksRequestChunk]
        | NotGiven = NOT_GIVEN,
        force_reupload: bool | NotGiven = NOT_GIVEN,
        tagging_information: upload_create_params.CreateKnowledgeBaseV2UploadFromLocalChunksRequestTaggingInformation
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateKnowledgeBaseUploadResponse:
        """
        Submit Upload Job

        Args:
          data_source_config: Configuration for the data source which describes where to find the data.

          chunks: List of chunks.

          force_reupload: Force reingest, regardless the change of the source file.

          tagging_information: A dictionary of tags to apply to all artifacts added from the data source.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        knowledge_base_id: str,
        *,
        chunking_strategy_config: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceIDRequestChunkingStrategyConfig,
        data_source_id: str,
        force_reupload: bool | NotGiven = NOT_GIVEN,
        tagging_information: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceIDRequestTaggingInformation
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateKnowledgeBaseUploadResponse:
        """
        Submit Upload Job

        Args:
          chunking_strategy_config: Configuration for the chunking strategy which describes how to chunk the data.

          data_source_id: Id of the data source to fetch.

          force_reupload: Force reingest, regardless the change of the source file.

          tagging_information: A dictionary of tags to apply to all artifacts added from the data source.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["data_source_config"], ["chunking_strategy_config", "data_source_id"])
    def create(
        self,
        knowledge_base_id: str,
        *,
        data_source_config: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceConfig
        | LocalChunksSourceConfigParam
        | NotGiven = NOT_GIVEN,
        chunking_strategy_config: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfig
        | NotGiven = NOT_GIVEN,
        data_source_auth_config: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceAuthConfig
        | NotGiven = NOT_GIVEN,
        force_reupload: bool | NotGiven = NOT_GIVEN,
        tagging_information: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformation
        | NotGiven = NOT_GIVEN,
        chunks: Iterable[upload_create_params.CreateKnowledgeBaseV2UploadFromLocalChunksRequestChunk]
        | NotGiven = NOT_GIVEN,
        data_source_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateKnowledgeBaseUploadResponse:
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        return self._post(
            f"/v4/knowledge-bases/{knowledge_base_id}/uploads",
            body=maybe_transform(
                {
                    "data_source_config": data_source_config,
                    "chunking_strategy_config": chunking_strategy_config,
                    "data_source_auth_config": data_source_auth_config,
                    "force_reupload": force_reupload,
                    "tagging_information": tagging_information,
                    "chunks": chunks,
                    "data_source_id": data_source_id,
                },
                upload_create_params.UploadCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CreateKnowledgeBaseUploadResponse,
        )

    def retrieve(
        self,
        upload_id: str,
        *,
        knowledge_base_id: str,
        include_artifact_list: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> KnowledgeBaseUpload:
        """
        Get Upload Job

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not upload_id:
            raise ValueError(f"Expected a non-empty value for `upload_id` but received {upload_id!r}")
        return self._get(
            f"/v4/knowledge-bases/{knowledge_base_id}/uploads/{upload_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"include_artifact_list": include_artifact_list}, upload_retrieve_params.UploadRetrieveParams
                ),
            ),
            cast_to=KnowledgeBaseUpload,
        )

    def list(
        self,
        knowledge_base_id: str,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        status: Optional[Literal["Running", "Completed", "Failed", "Canceled"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncPageResponse[UploadListResponse]:
        """
        ### Description

        List all uploads for a knowledge base.

        ### Details

        This API can be used to list all uploads that have been created for a knowledge
        base. This API will return the details of all uploads including their IDs, their
        statuses, the data source configs they use, the chunking strategy configs they
        use, and the timestamps for their creation and last-updated time.

        #### Backwards Compatibility

        V2 and V1 Knowledge Bases are entirely separate and not backwards compatible.
        Users who have existing V1 knowledge bases will need to migrate their data to V2
        knowledge bases.

        Args:
          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        return self._get_api_list(
            f"/v4/knowledge-bases/{knowledge_base_id}/uploads",
            page=SyncPageResponse[UploadListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                        "status": status,
                    },
                    upload_list_params.UploadListParams,
                ),
            ),
            model=UploadListResponse,
        )

    def cancel(
        self,
        upload_id: str,
        *,
        knowledge_base_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CancelKnowledgeBaseUploadResponse:
        """
        Cancel Upload Job

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not upload_id:
            raise ValueError(f"Expected a non-empty value for `upload_id` but received {upload_id!r}")
        return self._post(
            f"/v4/knowledge-bases/{knowledge_base_id}/uploads/{upload_id}/cancel",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CancelKnowledgeBaseUploadResponse,
        )


class AsyncUploadsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUploadsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncUploadsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUploadsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncUploadsResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        knowledge_base_id: str,
        *,
        data_source_config: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceConfig,
        chunking_strategy_config: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfig
        | NotGiven = NOT_GIVEN,
        data_source_auth_config: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceAuthConfig
        | NotGiven = NOT_GIVEN,
        force_reupload: bool | NotGiven = NOT_GIVEN,
        tagging_information: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformation
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateKnowledgeBaseUploadResponse:
        """
        Submit Upload Job

        Args:
          data_source_config: Configuration for the data source which describes where to find the data.

          chunking_strategy_config: Configuration for the chunking strategy which describes how to chunk the data.

          data_source_auth_config: Configuration for the data source which describes how to authenticate to the
              data source.

          force_reupload: Force reingest, regardless the change of the source file.

          tagging_information: A dictionary of tags to apply to all artifacts added from the data source.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        knowledge_base_id: str,
        *,
        data_source_config: LocalChunksSourceConfigParam,
        chunks: Iterable[upload_create_params.CreateKnowledgeBaseV2UploadFromLocalChunksRequestChunk]
        | NotGiven = NOT_GIVEN,
        force_reupload: bool | NotGiven = NOT_GIVEN,
        tagging_information: upload_create_params.CreateKnowledgeBaseV2UploadFromLocalChunksRequestTaggingInformation
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateKnowledgeBaseUploadResponse:
        """
        Submit Upload Job

        Args:
          data_source_config: Configuration for the data source which describes where to find the data.

          chunks: List of chunks.

          force_reupload: Force reingest, regardless the change of the source file.

          tagging_information: A dictionary of tags to apply to all artifacts added from the data source.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        knowledge_base_id: str,
        *,
        chunking_strategy_config: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceIDRequestChunkingStrategyConfig,
        data_source_id: str,
        force_reupload: bool | NotGiven = NOT_GIVEN,
        tagging_information: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceIDRequestTaggingInformation
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateKnowledgeBaseUploadResponse:
        """
        Submit Upload Job

        Args:
          chunking_strategy_config: Configuration for the chunking strategy which describes how to chunk the data.

          data_source_id: Id of the data source to fetch.

          force_reupload: Force reingest, regardless the change of the source file.

          tagging_information: A dictionary of tags to apply to all artifacts added from the data source.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["data_source_config"], ["chunking_strategy_config", "data_source_id"])
    async def create(
        self,
        knowledge_base_id: str,
        *,
        data_source_config: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceConfig
        | LocalChunksSourceConfigParam
        | NotGiven = NOT_GIVEN,
        chunking_strategy_config: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceRequestChunkingStrategyConfig
        | NotGiven = NOT_GIVEN,
        data_source_auth_config: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceRequestDataSourceAuthConfig
        | NotGiven = NOT_GIVEN,
        force_reupload: bool | NotGiven = NOT_GIVEN,
        tagging_information: upload_create_params.CreateKnowledgeBaseV2UploadFromDataSourceRequestTaggingInformation
        | NotGiven = NOT_GIVEN,
        chunks: Iterable[upload_create_params.CreateKnowledgeBaseV2UploadFromLocalChunksRequestChunk]
        | NotGiven = NOT_GIVEN,
        data_source_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CreateKnowledgeBaseUploadResponse:
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        return await self._post(
            f"/v4/knowledge-bases/{knowledge_base_id}/uploads",
            body=await async_maybe_transform(
                {
                    "data_source_config": data_source_config,
                    "chunking_strategy_config": chunking_strategy_config,
                    "data_source_auth_config": data_source_auth_config,
                    "force_reupload": force_reupload,
                    "tagging_information": tagging_information,
                    "chunks": chunks,
                    "data_source_id": data_source_id,
                },
                upload_create_params.UploadCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CreateKnowledgeBaseUploadResponse,
        )

    async def retrieve(
        self,
        upload_id: str,
        *,
        knowledge_base_id: str,
        include_artifact_list: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> KnowledgeBaseUpload:
        """
        Get Upload Job

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not upload_id:
            raise ValueError(f"Expected a non-empty value for `upload_id` but received {upload_id!r}")
        return await self._get(
            f"/v4/knowledge-bases/{knowledge_base_id}/uploads/{upload_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"include_artifact_list": include_artifact_list}, upload_retrieve_params.UploadRetrieveParams
                ),
            ),
            cast_to=KnowledgeBaseUpload,
        )

    def list(
        self,
        knowledge_base_id: str,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        status: Optional[Literal["Running", "Completed", "Failed", "Canceled"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[UploadListResponse, AsyncPageResponse[UploadListResponse]]:
        """
        ### Description

        List all uploads for a knowledge base.

        ### Details

        This API can be used to list all uploads that have been created for a knowledge
        base. This API will return the details of all uploads including their IDs, their
        statuses, the data source configs they use, the chunking strategy configs they
        use, and the timestamps for their creation and last-updated time.

        #### Backwards Compatibility

        V2 and V1 Knowledge Bases are entirely separate and not backwards compatible.
        Users who have existing V1 knowledge bases will need to migrate their data to V2
        knowledge bases.

        Args:
          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        return self._get_api_list(
            f"/v4/knowledge-bases/{knowledge_base_id}/uploads",
            page=AsyncPageResponse[UploadListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "page": page,
                        "status": status,
                    },
                    upload_list_params.UploadListParams,
                ),
            ),
            model=UploadListResponse,
        )

    async def cancel(
        self,
        upload_id: str,
        *,
        knowledge_base_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CancelKnowledgeBaseUploadResponse:
        """
        Cancel Upload Job

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not upload_id:
            raise ValueError(f"Expected a non-empty value for `upload_id` but received {upload_id!r}")
        return await self._post(
            f"/v4/knowledge-bases/{knowledge_base_id}/uploads/{upload_id}/cancel",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CancelKnowledgeBaseUploadResponse,
        )


class UploadsResourceWithRawResponse:
    def __init__(self, uploads: UploadsResource) -> None:
        self._uploads = uploads

        self.create = to_raw_response_wrapper(
            uploads.create,
        )
        self.retrieve = to_raw_response_wrapper(
            uploads.retrieve,
        )
        self.list = to_raw_response_wrapper(
            uploads.list,
        )
        self.cancel = to_raw_response_wrapper(
            uploads.cancel,
        )


class AsyncUploadsResourceWithRawResponse:
    def __init__(self, uploads: AsyncUploadsResource) -> None:
        self._uploads = uploads

        self.create = async_to_raw_response_wrapper(
            uploads.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            uploads.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            uploads.list,
        )
        self.cancel = async_to_raw_response_wrapper(
            uploads.cancel,
        )


class UploadsResourceWithStreamingResponse:
    def __init__(self, uploads: UploadsResource) -> None:
        self._uploads = uploads

        self.create = to_streamed_response_wrapper(
            uploads.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            uploads.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            uploads.list,
        )
        self.cancel = to_streamed_response_wrapper(
            uploads.cancel,
        )


class AsyncUploadsResourceWithStreamingResponse:
    def __init__(self, uploads: AsyncUploadsResource) -> None:
        self._uploads = uploads

        self.create = async_to_streamed_response_wrapper(
            uploads.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            uploads.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            uploads.list,
        )
        self.cancel = async_to_streamed_response_wrapper(
            uploads.cancel,
        )
