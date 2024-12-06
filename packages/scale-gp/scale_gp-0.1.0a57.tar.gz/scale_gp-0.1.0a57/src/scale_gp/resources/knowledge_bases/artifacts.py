# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
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
from ...types.knowledge_bases import (
    artifact_list_params,
    artifact_update_params,
    artifact_retrieve_params,
    artifact_batch_delete_params,
)
from ...types.knowledge_bases.artifact import Artifact
from ...types.knowledge_bases.artifact_list_response import ArtifactListResponse
from ...types.knowledge_bases.artifact_delete_response import ArtifactDeleteResponse
from ...types.knowledge_bases.artifact_update_response import ArtifactUpdateResponse
from ...types.knowledge_bases.artifact_batch_delete_response import ArtifactBatchDeleteResponse

__all__ = ["ArtifactsResource", "AsyncArtifactsResource"]


class ArtifactsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ArtifactsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ArtifactsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ArtifactsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ArtifactsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        artifact_id: str,
        *,
        knowledge_base_id: str,
        status_filter: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Artifact:
        """
        ### Description

        Gets the details of an artifact tracked by a knowledge base.

        ### Details

        This API can be used to get information about a single artifact by ID. This
        response will contain much more detail about the artifact than show in the
        [List Artifacts API](https://scale-egp.readme.io/reference/list_knowledge_base_artifacts_v2)
        call. To use this API, pass in the `knowledge_base_id` and `artifact_id` that
        were returned from your
        [List Artifacts API](https://scale-egp.readme.io/reference/list_knowledge_base_artifacts_v2)
        call as path parameters.

        #### Compatibility with V1

        V2 and V1 Knowledge Bases are entirely separate and not backwards compatible.
        Users who have existing V1 knowledge bases will need to migrate their data to V2
        knowledge bases.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not artifact_id:
            raise ValueError(f"Expected a non-empty value for `artifact_id` but received {artifact_id!r}")
        return self._get(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"status_filter": status_filter}, artifact_retrieve_params.ArtifactRetrieveParams
                ),
            ),
            cast_to=Artifact,
        )

    def update(
        self,
        artifact_id: str,
        *,
        knowledge_base_id: str,
        tags: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ArtifactUpdateResponse:
        """Patch Artifact Information

        Args:
          tags: Tags to associate with the artifact.

        Will overwrite existing tags.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not artifact_id:
            raise ValueError(f"Expected a non-empty value for `artifact_id` but received {artifact_id!r}")
        return self._patch(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}",
            body=maybe_transform({"tags": tags}, artifact_update_params.ArtifactUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ArtifactUpdateResponse,
        )

    def list(
        self,
        knowledge_base_id: str,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        status: Optional[Literal["Pending", "Completed", "Failed", "Uploading", "Deleting"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncPageResponse[ArtifactListResponse]:
        """
        ### Description

        List all artifacts tracked by a knowledge base.

        ### Details

        This API can be used to list all artifacts that are currently tracked in a
        knowledge base. This API will return the details of all artifacts including
        their IDs, names, the source they originated from, their current upload
        statuses, and the timestamps for their creation and last-updated time.

        This list should be consistent with the state of the data source at the time of
        start of the latest upload. If the state is not consistent, create a new upload
        to update the knowledge base to reflect the latest state of the data source.

        Args:
          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          status: Get artifacts only with the specified status. Accepted values are: Pending,
              Completed, Failed, Uploading, Deleting

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        return self._get_api_list(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts",
            page=SyncPageResponse[ArtifactListResponse],
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
                    artifact_list_params.ArtifactListParams,
                ),
            ),
            model=ArtifactListResponse,
        )

    def delete(
        self,
        artifact_id: str,
        *,
        knowledge_base_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ArtifactDeleteResponse:
        """
        Delete Locally Stored Artifact

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not artifact_id:
            raise ValueError(f"Expected a non-empty value for `artifact_id` but received {artifact_id!r}")
        return self._delete(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ArtifactDeleteResponse,
        )

    def batch_delete(
        self,
        knowledge_base_id: str,
        *,
        artifact_ids: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ArtifactBatchDeleteResponse:
        """
        Batch Delete Locally Stored Artifacts

        Args:
          artifact_ids: List of artifact ids to delete

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        return self._post(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts/batch-delete",
            body=maybe_transform(
                {"artifact_ids": artifact_ids}, artifact_batch_delete_params.ArtifactBatchDeleteParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ArtifactBatchDeleteResponse,
        )


class AsyncArtifactsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncArtifactsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncArtifactsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncArtifactsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncArtifactsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        artifact_id: str,
        *,
        knowledge_base_id: str,
        status_filter: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Artifact:
        """
        ### Description

        Gets the details of an artifact tracked by a knowledge base.

        ### Details

        This API can be used to get information about a single artifact by ID. This
        response will contain much more detail about the artifact than show in the
        [List Artifacts API](https://scale-egp.readme.io/reference/list_knowledge_base_artifacts_v2)
        call. To use this API, pass in the `knowledge_base_id` and `artifact_id` that
        were returned from your
        [List Artifacts API](https://scale-egp.readme.io/reference/list_knowledge_base_artifacts_v2)
        call as path parameters.

        #### Compatibility with V1

        V2 and V1 Knowledge Bases are entirely separate and not backwards compatible.
        Users who have existing V1 knowledge bases will need to migrate their data to V2
        knowledge bases.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not artifact_id:
            raise ValueError(f"Expected a non-empty value for `artifact_id` but received {artifact_id!r}")
        return await self._get(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"status_filter": status_filter}, artifact_retrieve_params.ArtifactRetrieveParams
                ),
            ),
            cast_to=Artifact,
        )

    async def update(
        self,
        artifact_id: str,
        *,
        knowledge_base_id: str,
        tags: object | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ArtifactUpdateResponse:
        """Patch Artifact Information

        Args:
          tags: Tags to associate with the artifact.

        Will overwrite existing tags.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not artifact_id:
            raise ValueError(f"Expected a non-empty value for `artifact_id` but received {artifact_id!r}")
        return await self._patch(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}",
            body=await async_maybe_transform({"tags": tags}, artifact_update_params.ArtifactUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ArtifactUpdateResponse,
        )

    def list(
        self,
        knowledge_base_id: str,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        page: int | NotGiven = NOT_GIVEN,
        status: Optional[Literal["Pending", "Completed", "Failed", "Uploading", "Deleting"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[ArtifactListResponse, AsyncPageResponse[ArtifactListResponse]]:
        """
        ### Description

        List all artifacts tracked by a knowledge base.

        ### Details

        This API can be used to list all artifacts that are currently tracked in a
        knowledge base. This API will return the details of all artifacts including
        their IDs, names, the source they originated from, their current upload
        statuses, and the timestamps for their creation and last-updated time.

        This list should be consistent with the state of the data source at the time of
        start of the latest upload. If the state is not consistent, create a new upload
        to update the knowledge base to reflect the latest state of the data source.

        Args:
          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          status: Get artifacts only with the specified status. Accepted values are: Pending,
              Completed, Failed, Uploading, Deleting

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        return self._get_api_list(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts",
            page=AsyncPageResponse[ArtifactListResponse],
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
                    artifact_list_params.ArtifactListParams,
                ),
            ),
            model=ArtifactListResponse,
        )

    async def delete(
        self,
        artifact_id: str,
        *,
        knowledge_base_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ArtifactDeleteResponse:
        """
        Delete Locally Stored Artifact

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not artifact_id:
            raise ValueError(f"Expected a non-empty value for `artifact_id` but received {artifact_id!r}")
        return await self._delete(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ArtifactDeleteResponse,
        )

    async def batch_delete(
        self,
        knowledge_base_id: str,
        *,
        artifact_ids: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ArtifactBatchDeleteResponse:
        """
        Batch Delete Locally Stored Artifacts

        Args:
          artifact_ids: List of artifact ids to delete

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        return await self._post(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts/batch-delete",
            body=await async_maybe_transform(
                {"artifact_ids": artifact_ids}, artifact_batch_delete_params.ArtifactBatchDeleteParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ArtifactBatchDeleteResponse,
        )


class ArtifactsResourceWithRawResponse:
    def __init__(self, artifacts: ArtifactsResource) -> None:
        self._artifacts = artifacts

        self.retrieve = to_raw_response_wrapper(
            artifacts.retrieve,
        )
        self.update = to_raw_response_wrapper(
            artifacts.update,
        )
        self.list = to_raw_response_wrapper(
            artifacts.list,
        )
        self.delete = to_raw_response_wrapper(
            artifacts.delete,
        )
        self.batch_delete = to_raw_response_wrapper(
            artifacts.batch_delete,
        )


class AsyncArtifactsResourceWithRawResponse:
    def __init__(self, artifacts: AsyncArtifactsResource) -> None:
        self._artifacts = artifacts

        self.retrieve = async_to_raw_response_wrapper(
            artifacts.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            artifacts.update,
        )
        self.list = async_to_raw_response_wrapper(
            artifacts.list,
        )
        self.delete = async_to_raw_response_wrapper(
            artifacts.delete,
        )
        self.batch_delete = async_to_raw_response_wrapper(
            artifacts.batch_delete,
        )


class ArtifactsResourceWithStreamingResponse:
    def __init__(self, artifacts: ArtifactsResource) -> None:
        self._artifacts = artifacts

        self.retrieve = to_streamed_response_wrapper(
            artifacts.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            artifacts.update,
        )
        self.list = to_streamed_response_wrapper(
            artifacts.list,
        )
        self.delete = to_streamed_response_wrapper(
            artifacts.delete,
        )
        self.batch_delete = to_streamed_response_wrapper(
            artifacts.batch_delete,
        )


class AsyncArtifactsResourceWithStreamingResponse:
    def __init__(self, artifacts: AsyncArtifactsResource) -> None:
        self._artifacts = artifacts

        self.retrieve = async_to_streamed_response_wrapper(
            artifacts.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            artifacts.update,
        )
        self.list = async_to_streamed_response_wrapper(
            artifacts.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            artifacts.delete,
        )
        self.batch_delete = async_to_streamed_response_wrapper(
            artifacts.batch_delete,
        )
