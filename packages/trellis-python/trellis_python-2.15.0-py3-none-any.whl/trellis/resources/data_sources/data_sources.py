# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ...types import data_source_create_params, data_source_retrieve_params
from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .metadata import (
    MetadataResource,
    AsyncMetadataResource,
    MetadataResourceWithRawResponse,
    AsyncMetadataResourceWithRawResponse,
    MetadataResourceWithStreamingResponse,
    AsyncMetadataResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.source import Source
from ...types.data_source_retrieve_response import DataSourceRetrieveResponse

__all__ = ["DataSourcesResource", "AsyncDataSourcesResource"]


class DataSourcesResource(SyncAPIResource):
    @cached_property
    def metadata(self) -> MetadataResource:
        return MetadataResource(self._client)

    @cached_property
    def with_raw_response(self) -> DataSourcesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#accessing-raw-response-data-eg-headers
        """
        return DataSourcesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DataSourcesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#with_streaming_response
        """
        return DataSourcesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        credentials: data_source_create_params.Credentials,
        name: str,
        proj_id: str,
        type: Literal["s3"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Source:
        """
        Create Data Source

        Args:
          type: An enumeration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/data_source",
            body=maybe_transform(
                {
                    "credentials": credentials,
                    "name": name,
                    "proj_id": proj_id,
                    "type": type,
                },
                data_source_create_params.DataSourceCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Source,
        )

    def retrieve(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: Literal["asc", "desc"] | NotGiven = NOT_GIVEN,
        order_by: Literal["updated_at", "created_at", "id"] | NotGiven = NOT_GIVEN,
        proj_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DataSourceRetrieveResponse:
        """
        Get Source

        Args:
          order: An enumeration.

          order_by: An enumeration.

          proj_id: The id of the project.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/data_source",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "order": order,
                        "order_by": order_by,
                        "proj_id": proj_id,
                    },
                    data_source_retrieve_params.DataSourceRetrieveParams,
                ),
            ),
            cast_to=DataSourceRetrieveResponse,
        )


class AsyncDataSourcesResource(AsyncAPIResource):
    @cached_property
    def metadata(self) -> AsyncMetadataResource:
        return AsyncMetadataResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDataSourcesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncDataSourcesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDataSourcesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#with_streaming_response
        """
        return AsyncDataSourcesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        credentials: data_source_create_params.Credentials,
        name: str,
        proj_id: str,
        type: Literal["s3"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Source:
        """
        Create Data Source

        Args:
          type: An enumeration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/data_source",
            body=await async_maybe_transform(
                {
                    "credentials": credentials,
                    "name": name,
                    "proj_id": proj_id,
                    "type": type,
                },
                data_source_create_params.DataSourceCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Source,
        )

    async def retrieve(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: Literal["asc", "desc"] | NotGiven = NOT_GIVEN,
        order_by: Literal["updated_at", "created_at", "id"] | NotGiven = NOT_GIVEN,
        proj_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DataSourceRetrieveResponse:
        """
        Get Source

        Args:
          order: An enumeration.

          order_by: An enumeration.

          proj_id: The id of the project.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/data_source",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "order": order,
                        "order_by": order_by,
                        "proj_id": proj_id,
                    },
                    data_source_retrieve_params.DataSourceRetrieveParams,
                ),
            ),
            cast_to=DataSourceRetrieveResponse,
        )


class DataSourcesResourceWithRawResponse:
    def __init__(self, data_sources: DataSourcesResource) -> None:
        self._data_sources = data_sources

        self.create = to_raw_response_wrapper(
            data_sources.create,
        )
        self.retrieve = to_raw_response_wrapper(
            data_sources.retrieve,
        )

    @cached_property
    def metadata(self) -> MetadataResourceWithRawResponse:
        return MetadataResourceWithRawResponse(self._data_sources.metadata)


class AsyncDataSourcesResourceWithRawResponse:
    def __init__(self, data_sources: AsyncDataSourcesResource) -> None:
        self._data_sources = data_sources

        self.create = async_to_raw_response_wrapper(
            data_sources.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            data_sources.retrieve,
        )

    @cached_property
    def metadata(self) -> AsyncMetadataResourceWithRawResponse:
        return AsyncMetadataResourceWithRawResponse(self._data_sources.metadata)


class DataSourcesResourceWithStreamingResponse:
    def __init__(self, data_sources: DataSourcesResource) -> None:
        self._data_sources = data_sources

        self.create = to_streamed_response_wrapper(
            data_sources.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            data_sources.retrieve,
        )

    @cached_property
    def metadata(self) -> MetadataResourceWithStreamingResponse:
        return MetadataResourceWithStreamingResponse(self._data_sources.metadata)


class AsyncDataSourcesResourceWithStreamingResponse:
    def __init__(self, data_sources: AsyncDataSourcesResource) -> None:
        self._data_sources = data_sources

        self.create = async_to_streamed_response_wrapper(
            data_sources.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            data_sources.retrieve,
        )

    @cached_property
    def metadata(self) -> AsyncMetadataResourceWithStreamingResponse:
        return AsyncMetadataResourceWithStreamingResponse(self._data_sources.metadata)
