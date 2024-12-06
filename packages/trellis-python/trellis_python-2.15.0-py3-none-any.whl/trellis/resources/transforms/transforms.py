# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, List, cast
from typing_extensions import Literal

import httpx

from ...types import (
    transform_list_params,
    transform_create_params,
    transform_update_params,
    transform_reference_params,
    transform_summarize_params,
)
from .results import (
    ResultsResource,
    AsyncResultsResource,
    ResultsResourceWithRawResponse,
    AsyncResultsResourceWithRawResponse,
    ResultsResourceWithStreamingResponse,
    AsyncResultsResourceWithStreamingResponse,
)
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
from .validations import (
    ValidationsResource,
    AsyncValidationsResource,
    ValidationsResourceWithRawResponse,
    AsyncValidationsResourceWithRawResponse,
    ValidationsResourceWithStreamingResponse,
    AsyncValidationsResourceWithStreamingResponse,
)
from ..._base_client import make_request_options
from .validations.validations import ValidationsResource, AsyncValidationsResource
from ...types.transform_list_response import TransformListResponse
from ...types.transform_create_response import TransformCreateResponse
from ...types.transform_delete_response import TransformDeleteResponse
from ...types.transform_update_response import TransformUpdateResponse
from ...types.transform_duplicate_response import TransformDuplicateResponse
from ...types.transform_reference_response import TransformReferenceResponse
from ...types.transform_summarize_response import TransformSummarizeResponse
from ...types.transform_autoschema_response import TransformAutoschemaResponse

__all__ = ["TransformsResource", "AsyncTransformsResource"]


class TransformsResource(SyncAPIResource):
    @cached_property
    def results(self) -> ResultsResource:
        return ResultsResource(self._client)

    @cached_property
    def validations(self) -> ValidationsResource:
        return ValidationsResource(self._client)

    @cached_property
    def with_raw_response(self) -> TransformsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#accessing-raw-response-data-eg-headers
        """
        return TransformsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TransformsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#with_streaming_response
        """
        return TransformsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        proj_id: str,
        transform_params: transform_create_params.TransformParams,
        transform_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransformCreateResponse:
        """
        Run the transformation defined in transformation params for all the assets in
        the project

        Args: transform_id (str): The ID of the transformation to run.

        Returns: {"message": "Transformation initiated", "transform_id": transform_id}

        Args:
          transform_name: The transform_name parameter is an optional parameter that provides a
              human-readable name or description for the transformation, which can be useful
              for identifying and referencing transformations. If provided, the transform_name
              parameter should be a string. If not provided, the value of transform_name will
              be None.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/transforms/create",
            body=maybe_transform(
                {
                    "proj_id": proj_id,
                    "transform_params": transform_params,
                    "transform_name": transform_name,
                },
                transform_create_params.TransformCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransformCreateResponse,
        )

    def update(
        self,
        transform_id: str,
        *,
        asset_ids: List[str] | NotGiven = NOT_GIVEN,
        include_reference: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransformUpdateResponse:
        """
        Run a transformation on specified assets or on data that have been added since
        the last run.

        Args: transform_id (str): The ID of the transformation.

        Returns: ReRunTransformResponse: Response indicating the initiation status of
        the transformation.

        Args:
          asset_ids: List of asset ids to refresh.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        return self._patch(
            f"/v1/transforms/{transform_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "asset_ids": asset_ids,
                        "include_reference": include_reference,
                    },
                    transform_update_params.TransformUpdateParams,
                ),
            ),
            cast_to=TransformUpdateResponse,
        )

    def list(
        self,
        *,
        include_transform_params: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: Literal["asc", "desc"] | NotGiven = NOT_GIVEN,
        order_by: Literal["updated_at", "created_at", "id"] | NotGiven = NOT_GIVEN,
        proj_ids: List[str] | NotGiven = NOT_GIVEN,
        search_term: str | NotGiven = NOT_GIVEN,
        transform_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransformListResponse:
        """
        Retrieve all transformation associated with you.

        Parameters:

        - transform_ids (list, optional): The IDs of the transformations to retrieve.
        - proj_ids (list, optional): The ids of the projects to retrieve transformations
          from.
        - include_params (bool, optional): Include metadata in the response such as the
          transform_params and validation_params. Defaults to false.

        Returns:

        - dict: A dict containing all the transformations associated with you.

        Args:
          include_transform_params: Boolean flag to include transform params, which includes the operations.

          order: An enumeration.

          order_by: An enumeration.

          proj_ids: List of project ids to retrieve transformations from.

          search_term: Search term to filter transformations against their id and name.

          transform_ids: List of transform IDs to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            TransformListResponse,
            self._get(
                "/v1/transforms",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=maybe_transform(
                        {
                            "include_transform_params": include_transform_params,
                            "limit": limit,
                            "offset": offset,
                            "order": order,
                            "order_by": order_by,
                            "proj_ids": proj_ids,
                            "search_term": search_term,
                            "transform_ids": transform_ids,
                        },
                        transform_list_params.TransformListParams,
                    ),
                ),
                cast_to=cast(
                    Any, TransformListResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def delete(
        self,
        transform_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransformDeleteResponse:
        """
        Delete Transform

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        return self._delete(
            f"/v1/transforms/{transform_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransformDeleteResponse,
        )

    def autoschema(
        self,
        transform_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransformAutoschemaResponse:
        """
        Create Autoschema

        Args:
          transform_id: The transform_id to get the autoschema for

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        return self._get(
            f"/v1/transforms/{transform_id}/autoschema",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransformAutoschemaResponse,
        )

    def duplicate(
        self,
        transform_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransformDuplicateResponse:
        """
        Duplicate a transformation for a given transform_id and customer.

        This endpoint creates a copy of the specified transformation, including its
        operations and other metadata, but does not run it.

        Args: transform_id (str): The ID of the transformation to duplicate.

        Returns: CreateTransformResponse: Response indicating the creation status of the
        new transformation.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        return self._post(
            f"/v1/transforms/{transform_id}/duplicate",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransformDuplicateResponse,
        )

    def reference(
        self,
        *,
        transform_id: str,
        column_name: str | NotGiven = NOT_GIVEN,
        result_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransformReferenceResponse:
        """
        Get Result Reference

        Args:
          column_name: column name to get reference for

          result_id: result id to get reference for

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/transforms/reference",
            body=maybe_transform(
                {
                    "transform_id": transform_id,
                    "column_name": column_name,
                    "result_id": result_id,
                },
                transform_reference_params.TransformReferenceParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransformReferenceResponse,
        )

    def summarize(
        self,
        transform_id: str,
        *,
        operation_ids: List[str],
        filters: object | NotGiven = NOT_GIVEN,
        prompt_details: str | NotGiven = NOT_GIVEN,
        result_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransformSummarizeResponse:
        """
        Summarize Transform

        Args:
          transform_id: The id of the transformation to summarize

          operation_ids: List of operation IDs to summarize

          filters: Optional filters to apply when summarizing results

          prompt_details: Optional additional details or requirements for the summary

          result_ids: List of result IDs to summarize

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        return self._post(
            f"/v1/transforms/{transform_id}/summarize",
            body=maybe_transform(
                {
                    "operation_ids": operation_ids,
                    "filters": filters,
                    "prompt_details": prompt_details,
                    "result_ids": result_ids,
                },
                transform_summarize_params.TransformSummarizeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransformSummarizeResponse,
        )

    def wake_up(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """This call is of fire and forget type. It will add the task in the background."""
        return self._get(
            "/v1/transforms/wake_up",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncTransformsResource(AsyncAPIResource):
    @cached_property
    def results(self) -> AsyncResultsResource:
        return AsyncResultsResource(self._client)

    @cached_property
    def validations(self) -> AsyncValidationsResource:
        return AsyncValidationsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTransformsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncTransformsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTransformsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#with_streaming_response
        """
        return AsyncTransformsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        proj_id: str,
        transform_params: transform_create_params.TransformParams,
        transform_name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransformCreateResponse:
        """
        Run the transformation defined in transformation params for all the assets in
        the project

        Args: transform_id (str): The ID of the transformation to run.

        Returns: {"message": "Transformation initiated", "transform_id": transform_id}

        Args:
          transform_name: The transform_name parameter is an optional parameter that provides a
              human-readable name or description for the transformation, which can be useful
              for identifying and referencing transformations. If provided, the transform_name
              parameter should be a string. If not provided, the value of transform_name will
              be None.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/transforms/create",
            body=await async_maybe_transform(
                {
                    "proj_id": proj_id,
                    "transform_params": transform_params,
                    "transform_name": transform_name,
                },
                transform_create_params.TransformCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransformCreateResponse,
        )

    async def update(
        self,
        transform_id: str,
        *,
        asset_ids: List[str] | NotGiven = NOT_GIVEN,
        include_reference: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransformUpdateResponse:
        """
        Run a transformation on specified assets or on data that have been added since
        the last run.

        Args: transform_id (str): The ID of the transformation.

        Returns: ReRunTransformResponse: Response indicating the initiation status of
        the transformation.

        Args:
          asset_ids: List of asset ids to refresh.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        return await self._patch(
            f"/v1/transforms/{transform_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "asset_ids": asset_ids,
                        "include_reference": include_reference,
                    },
                    transform_update_params.TransformUpdateParams,
                ),
            ),
            cast_to=TransformUpdateResponse,
        )

    async def list(
        self,
        *,
        include_transform_params: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: Literal["asc", "desc"] | NotGiven = NOT_GIVEN,
        order_by: Literal["updated_at", "created_at", "id"] | NotGiven = NOT_GIVEN,
        proj_ids: List[str] | NotGiven = NOT_GIVEN,
        search_term: str | NotGiven = NOT_GIVEN,
        transform_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransformListResponse:
        """
        Retrieve all transformation associated with you.

        Parameters:

        - transform_ids (list, optional): The IDs of the transformations to retrieve.
        - proj_ids (list, optional): The ids of the projects to retrieve transformations
          from.
        - include_params (bool, optional): Include metadata in the response such as the
          transform_params and validation_params. Defaults to false.

        Returns:

        - dict: A dict containing all the transformations associated with you.

        Args:
          include_transform_params: Boolean flag to include transform params, which includes the operations.

          order: An enumeration.

          order_by: An enumeration.

          proj_ids: List of project ids to retrieve transformations from.

          search_term: Search term to filter transformations against their id and name.

          transform_ids: List of transform IDs to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            TransformListResponse,
            await self._get(
                "/v1/transforms",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=await async_maybe_transform(
                        {
                            "include_transform_params": include_transform_params,
                            "limit": limit,
                            "offset": offset,
                            "order": order,
                            "order_by": order_by,
                            "proj_ids": proj_ids,
                            "search_term": search_term,
                            "transform_ids": transform_ids,
                        },
                        transform_list_params.TransformListParams,
                    ),
                ),
                cast_to=cast(
                    Any, TransformListResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def delete(
        self,
        transform_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransformDeleteResponse:
        """
        Delete Transform

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        return await self._delete(
            f"/v1/transforms/{transform_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransformDeleteResponse,
        )

    async def autoschema(
        self,
        transform_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransformAutoschemaResponse:
        """
        Create Autoschema

        Args:
          transform_id: The transform_id to get the autoschema for

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        return await self._get(
            f"/v1/transforms/{transform_id}/autoschema",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransformAutoschemaResponse,
        )

    async def duplicate(
        self,
        transform_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransformDuplicateResponse:
        """
        Duplicate a transformation for a given transform_id and customer.

        This endpoint creates a copy of the specified transformation, including its
        operations and other metadata, but does not run it.

        Args: transform_id (str): The ID of the transformation to duplicate.

        Returns: CreateTransformResponse: Response indicating the creation status of the
        new transformation.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        return await self._post(
            f"/v1/transforms/{transform_id}/duplicate",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransformDuplicateResponse,
        )

    async def reference(
        self,
        *,
        transform_id: str,
        column_name: str | NotGiven = NOT_GIVEN,
        result_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransformReferenceResponse:
        """
        Get Result Reference

        Args:
          column_name: column name to get reference for

          result_id: result id to get reference for

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/transforms/reference",
            body=await async_maybe_transform(
                {
                    "transform_id": transform_id,
                    "column_name": column_name,
                    "result_id": result_id,
                },
                transform_reference_params.TransformReferenceParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransformReferenceResponse,
        )

    async def summarize(
        self,
        transform_id: str,
        *,
        operation_ids: List[str],
        filters: object | NotGiven = NOT_GIVEN,
        prompt_details: str | NotGiven = NOT_GIVEN,
        result_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TransformSummarizeResponse:
        """
        Summarize Transform

        Args:
          transform_id: The id of the transformation to summarize

          operation_ids: List of operation IDs to summarize

          filters: Optional filters to apply when summarizing results

          prompt_details: Optional additional details or requirements for the summary

          result_ids: List of result IDs to summarize

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        return await self._post(
            f"/v1/transforms/{transform_id}/summarize",
            body=await async_maybe_transform(
                {
                    "operation_ids": operation_ids,
                    "filters": filters,
                    "prompt_details": prompt_details,
                    "result_ids": result_ids,
                },
                transform_summarize_params.TransformSummarizeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TransformSummarizeResponse,
        )

    async def wake_up(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """This call is of fire and forget type. It will add the task in the background."""
        return await self._get(
            "/v1/transforms/wake_up",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class TransformsResourceWithRawResponse:
    def __init__(self, transforms: TransformsResource) -> None:
        self._transforms = transforms

        self.create = to_raw_response_wrapper(
            transforms.create,
        )
        self.update = to_raw_response_wrapper(
            transforms.update,
        )
        self.list = to_raw_response_wrapper(
            transforms.list,
        )
        self.delete = to_raw_response_wrapper(
            transforms.delete,
        )
        self.autoschema = to_raw_response_wrapper(
            transforms.autoschema,
        )
        self.duplicate = to_raw_response_wrapper(
            transforms.duplicate,
        )
        self.reference = to_raw_response_wrapper(
            transforms.reference,
        )
        self.summarize = to_raw_response_wrapper(
            transforms.summarize,
        )
        self.wake_up = to_raw_response_wrapper(
            transforms.wake_up,
        )

    @cached_property
    def results(self) -> ResultsResourceWithRawResponse:
        return ResultsResourceWithRawResponse(self._transforms.results)

    @cached_property
    def validations(self) -> ValidationsResourceWithRawResponse:
        return ValidationsResourceWithRawResponse(self._transforms.validations)


class AsyncTransformsResourceWithRawResponse:
    def __init__(self, transforms: AsyncTransformsResource) -> None:
        self._transforms = transforms

        self.create = async_to_raw_response_wrapper(
            transforms.create,
        )
        self.update = async_to_raw_response_wrapper(
            transforms.update,
        )
        self.list = async_to_raw_response_wrapper(
            transforms.list,
        )
        self.delete = async_to_raw_response_wrapper(
            transforms.delete,
        )
        self.autoschema = async_to_raw_response_wrapper(
            transforms.autoschema,
        )
        self.duplicate = async_to_raw_response_wrapper(
            transforms.duplicate,
        )
        self.reference = async_to_raw_response_wrapper(
            transforms.reference,
        )
        self.summarize = async_to_raw_response_wrapper(
            transforms.summarize,
        )
        self.wake_up = async_to_raw_response_wrapper(
            transforms.wake_up,
        )

    @cached_property
    def results(self) -> AsyncResultsResourceWithRawResponse:
        return AsyncResultsResourceWithRawResponse(self._transforms.results)

    @cached_property
    def validations(self) -> AsyncValidationsResourceWithRawResponse:
        return AsyncValidationsResourceWithRawResponse(self._transforms.validations)


class TransformsResourceWithStreamingResponse:
    def __init__(self, transforms: TransformsResource) -> None:
        self._transforms = transforms

        self.create = to_streamed_response_wrapper(
            transforms.create,
        )
        self.update = to_streamed_response_wrapper(
            transforms.update,
        )
        self.list = to_streamed_response_wrapper(
            transforms.list,
        )
        self.delete = to_streamed_response_wrapper(
            transforms.delete,
        )
        self.autoschema = to_streamed_response_wrapper(
            transforms.autoschema,
        )
        self.duplicate = to_streamed_response_wrapper(
            transforms.duplicate,
        )
        self.reference = to_streamed_response_wrapper(
            transforms.reference,
        )
        self.summarize = to_streamed_response_wrapper(
            transforms.summarize,
        )
        self.wake_up = to_streamed_response_wrapper(
            transforms.wake_up,
        )

    @cached_property
    def results(self) -> ResultsResourceWithStreamingResponse:
        return ResultsResourceWithStreamingResponse(self._transforms.results)

    @cached_property
    def validations(self) -> ValidationsResourceWithStreamingResponse:
        return ValidationsResourceWithStreamingResponse(self._transforms.validations)


class AsyncTransformsResourceWithStreamingResponse:
    def __init__(self, transforms: AsyncTransformsResource) -> None:
        self._transforms = transforms

        self.create = async_to_streamed_response_wrapper(
            transforms.create,
        )
        self.update = async_to_streamed_response_wrapper(
            transforms.update,
        )
        self.list = async_to_streamed_response_wrapper(
            transforms.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            transforms.delete,
        )
        self.autoschema = async_to_streamed_response_wrapper(
            transforms.autoschema,
        )
        self.duplicate = async_to_streamed_response_wrapper(
            transforms.duplicate,
        )
        self.reference = async_to_streamed_response_wrapper(
            transforms.reference,
        )
        self.summarize = async_to_streamed_response_wrapper(
            transforms.summarize,
        )
        self.wake_up = async_to_streamed_response_wrapper(
            transforms.wake_up,
        )

    @cached_property
    def results(self) -> AsyncResultsResourceWithStreamingResponse:
        return AsyncResultsResourceWithStreamingResponse(self._transforms.results)

    @cached_property
    def validations(self) -> AsyncValidationsResourceWithStreamingResponse:
        return AsyncValidationsResourceWithStreamingResponse(self._transforms.validations)
