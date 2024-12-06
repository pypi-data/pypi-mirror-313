# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .params import (
    ParamsResource,
    AsyncParamsResource,
    ParamsResourceWithRawResponse,
    AsyncParamsResourceWithRawResponse,
    ParamsResourceWithStreamingResponse,
    AsyncParamsResourceWithStreamingResponse,
)
from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.transforms import validation_update_params, validation_retrieve_params
from ....types.transforms.validation_delete_response import ValidationDeleteResponse
from ....types.transforms.validation_update_response import ValidationUpdateResponse
from ....types.transforms.validation_retrieve_response import ValidationRetrieveResponse

__all__ = ["ValidationsResource", "AsyncValidationsResource"]


class ValidationsResource(SyncAPIResource):
    @cached_property
    def params(self) -> ParamsResource:
        return ParamsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ValidationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#accessing-raw-response-data-eg-headers
        """
        return ValidationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ValidationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#with_streaming_response
        """
        return ValidationsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        transform_id: str,
        *,
        precedence: bool | NotGiven = NOT_GIVEN,
        result_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ValidationRetrieveResponse:
        """
        Retrieve the validation results for a given transform_id.

        Args: transform_id (str): The ID of the transformation.

        Returns: dict: A dictionary containing the validation results.

        Args:
          result_id: The ID of the result to get the validation for (optional)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        return self._get(
            f"/v1/transforms/{transform_id}/validations",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "precedence": precedence,
                        "result_id": result_id,
                    },
                    validation_retrieve_params.ValidationRetrieveParams,
                ),
            ),
            cast_to=ValidationRetrieveResponse,
        )

    def update(
        self,
        validation_id: str,
        *,
        result: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ValidationUpdateResponse:
        """
        Override Validation Results

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validation_id:
            raise ValueError(f"Expected a non-empty value for `validation_id` but received {validation_id!r}")
        return self._patch(
            f"/v1/transforms/validations/{validation_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"result": result}, validation_update_params.ValidationUpdateParams),
            ),
            cast_to=ValidationUpdateResponse,
        )

    def delete(
        self,
        validation_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ValidationDeleteResponse:
        """
        Delete Manual Results

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validation_id:
            raise ValueError(f"Expected a non-empty value for `validation_id` but received {validation_id!r}")
        return self._delete(
            f"/v1/transforms/validations/{validation_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ValidationDeleteResponse,
        )


class AsyncValidationsResource(AsyncAPIResource):
    @cached_property
    def params(self) -> AsyncParamsResource:
        return AsyncParamsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncValidationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncValidationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncValidationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#with_streaming_response
        """
        return AsyncValidationsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        transform_id: str,
        *,
        precedence: bool | NotGiven = NOT_GIVEN,
        result_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ValidationRetrieveResponse:
        """
        Retrieve the validation results for a given transform_id.

        Args: transform_id (str): The ID of the transformation.

        Returns: dict: A dictionary containing the validation results.

        Args:
          result_id: The ID of the result to get the validation for (optional)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        return await self._get(
            f"/v1/transforms/{transform_id}/validations",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "precedence": precedence,
                        "result_id": result_id,
                    },
                    validation_retrieve_params.ValidationRetrieveParams,
                ),
            ),
            cast_to=ValidationRetrieveResponse,
        )

    async def update(
        self,
        validation_id: str,
        *,
        result: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ValidationUpdateResponse:
        """
        Override Validation Results

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validation_id:
            raise ValueError(f"Expected a non-empty value for `validation_id` but received {validation_id!r}")
        return await self._patch(
            f"/v1/transforms/validations/{validation_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"result": result}, validation_update_params.ValidationUpdateParams),
            ),
            cast_to=ValidationUpdateResponse,
        )

    async def delete(
        self,
        validation_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ValidationDeleteResponse:
        """
        Delete Manual Results

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not validation_id:
            raise ValueError(f"Expected a non-empty value for `validation_id` but received {validation_id!r}")
        return await self._delete(
            f"/v1/transforms/validations/{validation_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ValidationDeleteResponse,
        )


class ValidationsResourceWithRawResponse:
    def __init__(self, validations: ValidationsResource) -> None:
        self._validations = validations

        self.retrieve = to_raw_response_wrapper(
            validations.retrieve,
        )
        self.update = to_raw_response_wrapper(
            validations.update,
        )
        self.delete = to_raw_response_wrapper(
            validations.delete,
        )

    @cached_property
    def params(self) -> ParamsResourceWithRawResponse:
        return ParamsResourceWithRawResponse(self._validations.params)


class AsyncValidationsResourceWithRawResponse:
    def __init__(self, validations: AsyncValidationsResource) -> None:
        self._validations = validations

        self.retrieve = async_to_raw_response_wrapper(
            validations.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            validations.update,
        )
        self.delete = async_to_raw_response_wrapper(
            validations.delete,
        )

    @cached_property
    def params(self) -> AsyncParamsResourceWithRawResponse:
        return AsyncParamsResourceWithRawResponse(self._validations.params)


class ValidationsResourceWithStreamingResponse:
    def __init__(self, validations: ValidationsResource) -> None:
        self._validations = validations

        self.retrieve = to_streamed_response_wrapper(
            validations.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            validations.update,
        )
        self.delete = to_streamed_response_wrapper(
            validations.delete,
        )

    @cached_property
    def params(self) -> ParamsResourceWithStreamingResponse:
        return ParamsResourceWithStreamingResponse(self._validations.params)


class AsyncValidationsResourceWithStreamingResponse:
    def __init__(self, validations: AsyncValidationsResource) -> None:
        self._validations = validations

        self.retrieve = async_to_streamed_response_wrapper(
            validations.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            validations.update,
        )
        self.delete = async_to_streamed_response_wrapper(
            validations.delete,
        )

    @cached_property
    def params(self) -> AsyncParamsResourceWithStreamingResponse:
        return AsyncParamsResourceWithStreamingResponse(self._validations.params)
