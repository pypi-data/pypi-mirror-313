# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

import httpx

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
from ....types.transforms.validations import param_create_params, param_update_params
from ....types.transforms.validations.param_create_response import ParamCreateResponse
from ....types.transforms.validations.param_delete_response import ParamDeleteResponse
from ....types.transforms.validations.param_update_response import ParamUpdateResponse
from ....types.transforms.validations.param_retrieve_response import ParamRetrieveResponse

__all__ = ["ParamsResource", "AsyncParamsResource"]


class ParamsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#accessing-raw-response-data-eg-headers
        """
        return ParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#with_streaming_response
        """
        return ParamsResourceWithStreamingResponse(self)

    def create(
        self,
        transform_id: str,
        *,
        validation_columns: List[str],
        validation_name: str,
        validation_endpoint: str | NotGiven = NOT_GIVEN,
        validation_rule: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ParamCreateResponse:
        """
        Insert Validation Params

        Args:
          validation_columns: The columns to be used in validation

          validation_name: The name of the validation operation

          validation_endpoint: The URL of the validation API. If not provided, the validation_rule will be ran
              directly.

          validation_rule: The rules to be applied to the column

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        return self._post(
            f"/v1/transforms/{transform_id}/validations/params",
            body=maybe_transform(
                {
                    "validation_columns": validation_columns,
                    "validation_name": validation_name,
                    "validation_endpoint": validation_endpoint,
                    "validation_rule": validation_rule,
                },
                param_create_params.ParamCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParamCreateResponse,
        )

    def retrieve(
        self,
        transform_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ParamRetrieveResponse:
        """
        Get All Validation Params

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        return self._get(
            f"/v1/transforms/{transform_id}/validations/params",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParamRetrieveResponse,
        )

    def update(
        self,
        validation_param_id: str,
        *,
        transform_id: str,
        validation_columns: List[str],
        validation_name: str,
        validation_endpoint: str | NotGiven = NOT_GIVEN,
        validation_rule: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ParamUpdateResponse:
        """
        " Update a validation parameter for a given transformation.

        Args: transform_id (str): The ID of the transformation. validation_param_id
        (str): The ID of the validation parameter. validation_param (ValidationParams):
        The updated validation parameter data.

        Returns: dict: A dictionary containing a success message and the updated
        validation parameter data.

        Raises: HTTPException: If the transformation does not exist for the current
        customer, or if an error occurs during the update process.

        Args:
          validation_columns: The columns to be used in validation

          validation_name: The name of the validation operation

          validation_endpoint: The URL of the validation API. If not provided, the validation_rule will be ran
              directly.

          validation_rule: The rules to be applied to the column

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        if not validation_param_id:
            raise ValueError(
                f"Expected a non-empty value for `validation_param_id` but received {validation_param_id!r}"
            )
        return self._put(
            f"/v1/transforms/{transform_id}/validations/params/{validation_param_id}",
            body=maybe_transform(
                {
                    "validation_columns": validation_columns,
                    "validation_name": validation_name,
                    "validation_endpoint": validation_endpoint,
                    "validation_rule": validation_rule,
                },
                param_update_params.ParamUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParamUpdateResponse,
        )

    def delete(
        self,
        validation_param_id: str,
        *,
        transform_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ParamDeleteResponse:
        """
        Delete Validation Params

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        if not validation_param_id:
            raise ValueError(
                f"Expected a non-empty value for `validation_param_id` but received {validation_param_id!r}"
            )
        return self._delete(
            f"/v1/transforms/{transform_id}/validations/params/{validation_param_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParamDeleteResponse,
        )


class AsyncParamsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncParamsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncParamsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncParamsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/Trellis-insights/trellis-python-sdk#with_streaming_response
        """
        return AsyncParamsResourceWithStreamingResponse(self)

    async def create(
        self,
        transform_id: str,
        *,
        validation_columns: List[str],
        validation_name: str,
        validation_endpoint: str | NotGiven = NOT_GIVEN,
        validation_rule: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ParamCreateResponse:
        """
        Insert Validation Params

        Args:
          validation_columns: The columns to be used in validation

          validation_name: The name of the validation operation

          validation_endpoint: The URL of the validation API. If not provided, the validation_rule will be ran
              directly.

          validation_rule: The rules to be applied to the column

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        return await self._post(
            f"/v1/transforms/{transform_id}/validations/params",
            body=await async_maybe_transform(
                {
                    "validation_columns": validation_columns,
                    "validation_name": validation_name,
                    "validation_endpoint": validation_endpoint,
                    "validation_rule": validation_rule,
                },
                param_create_params.ParamCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParamCreateResponse,
        )

    async def retrieve(
        self,
        transform_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ParamRetrieveResponse:
        """
        Get All Validation Params

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        return await self._get(
            f"/v1/transforms/{transform_id}/validations/params",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParamRetrieveResponse,
        )

    async def update(
        self,
        validation_param_id: str,
        *,
        transform_id: str,
        validation_columns: List[str],
        validation_name: str,
        validation_endpoint: str | NotGiven = NOT_GIVEN,
        validation_rule: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ParamUpdateResponse:
        """
        " Update a validation parameter for a given transformation.

        Args: transform_id (str): The ID of the transformation. validation_param_id
        (str): The ID of the validation parameter. validation_param (ValidationParams):
        The updated validation parameter data.

        Returns: dict: A dictionary containing a success message and the updated
        validation parameter data.

        Raises: HTTPException: If the transformation does not exist for the current
        customer, or if an error occurs during the update process.

        Args:
          validation_columns: The columns to be used in validation

          validation_name: The name of the validation operation

          validation_endpoint: The URL of the validation API. If not provided, the validation_rule will be ran
              directly.

          validation_rule: The rules to be applied to the column

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        if not validation_param_id:
            raise ValueError(
                f"Expected a non-empty value for `validation_param_id` but received {validation_param_id!r}"
            )
        return await self._put(
            f"/v1/transforms/{transform_id}/validations/params/{validation_param_id}",
            body=await async_maybe_transform(
                {
                    "validation_columns": validation_columns,
                    "validation_name": validation_name,
                    "validation_endpoint": validation_endpoint,
                    "validation_rule": validation_rule,
                },
                param_update_params.ParamUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParamUpdateResponse,
        )

    async def delete(
        self,
        validation_param_id: str,
        *,
        transform_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ParamDeleteResponse:
        """
        Delete Validation Params

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not transform_id:
            raise ValueError(f"Expected a non-empty value for `transform_id` but received {transform_id!r}")
        if not validation_param_id:
            raise ValueError(
                f"Expected a non-empty value for `validation_param_id` but received {validation_param_id!r}"
            )
        return await self._delete(
            f"/v1/transforms/{transform_id}/validations/params/{validation_param_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ParamDeleteResponse,
        )


class ParamsResourceWithRawResponse:
    def __init__(self, params: ParamsResource) -> None:
        self._params = params

        self.create = to_raw_response_wrapper(
            params.create,
        )
        self.retrieve = to_raw_response_wrapper(
            params.retrieve,
        )
        self.update = to_raw_response_wrapper(
            params.update,
        )
        self.delete = to_raw_response_wrapper(
            params.delete,
        )


class AsyncParamsResourceWithRawResponse:
    def __init__(self, params: AsyncParamsResource) -> None:
        self._params = params

        self.create = async_to_raw_response_wrapper(
            params.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            params.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            params.update,
        )
        self.delete = async_to_raw_response_wrapper(
            params.delete,
        )


class ParamsResourceWithStreamingResponse:
    def __init__(self, params: ParamsResource) -> None:
        self._params = params

        self.create = to_streamed_response_wrapper(
            params.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            params.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            params.update,
        )
        self.delete = to_streamed_response_wrapper(
            params.delete,
        )


class AsyncParamsResourceWithStreamingResponse:
    def __init__(self, params: AsyncParamsResource) -> None:
        self._params = params

        self.create = async_to_streamed_response_wrapper(
            params.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            params.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            params.update,
        )
        self.delete = async_to_streamed_response_wrapper(
            params.delete,
        )
