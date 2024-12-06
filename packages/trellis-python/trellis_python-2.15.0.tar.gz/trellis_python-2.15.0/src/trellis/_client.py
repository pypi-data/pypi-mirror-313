# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import resources, _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import (
    is_given,
    get_async_library,
)
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import TrellisError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "resources",
    "Trellis",
    "AsyncTrellis",
    "Client",
    "AsyncClient",
]


class Trellis(SyncAPIClient):
    transforms: resources.TransformsResource
    customers: resources.CustomersResource
    projects: resources.ProjectsResource
    assets: resources.AssetsResource
    assets_extract: resources.AssetsExtractResource
    events: resources.EventsResource
    templates: resources.TemplatesResource
    data_sources: resources.DataSourcesResource
    with_raw_response: TrellisWithRawResponse
    with_streaming_response: TrellisWithStreamedResponse

    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous trellis client instance.

        This automatically infers the `api_key` argument from the `AUTHORIZATION_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("AUTHORIZATION_KEY")
        if api_key is None:
            raise TrellisError(
                "The api_key client option must be set either by passing api_key to the client or by setting the AUTHORIZATION_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("TRELLIS_BASE_URL")
        if base_url is None:
            base_url = f"https://api.runtrellis.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.transforms = resources.TransformsResource(self)
        self.customers = resources.CustomersResource(self)
        self.projects = resources.ProjectsResource(self)
        self.assets = resources.AssetsResource(self)
        self.assets_extract = resources.AssetsExtractResource(self)
        self.events = resources.EventsResource(self)
        self.templates = resources.TemplatesResource(self)
        self.data_sources = resources.DataSourcesResource(self)
        self.with_raw_response = TrellisWithRawResponse(self)
        self.with_streaming_response = TrellisWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncTrellis(AsyncAPIClient):
    transforms: resources.AsyncTransformsResource
    customers: resources.AsyncCustomersResource
    projects: resources.AsyncProjectsResource
    assets: resources.AsyncAssetsResource
    assets_extract: resources.AsyncAssetsExtractResource
    events: resources.AsyncEventsResource
    templates: resources.AsyncTemplatesResource
    data_sources: resources.AsyncDataSourcesResource
    with_raw_response: AsyncTrellisWithRawResponse
    with_streaming_response: AsyncTrellisWithStreamedResponse

    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async trellis client instance.

        This automatically infers the `api_key` argument from the `AUTHORIZATION_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("AUTHORIZATION_KEY")
        if api_key is None:
            raise TrellisError(
                "The api_key client option must be set either by passing api_key to the client or by setting the AUTHORIZATION_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("TRELLIS_BASE_URL")
        if base_url is None:
            base_url = f"https://api.runtrellis.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.transforms = resources.AsyncTransformsResource(self)
        self.customers = resources.AsyncCustomersResource(self)
        self.projects = resources.AsyncProjectsResource(self)
        self.assets = resources.AsyncAssetsResource(self)
        self.assets_extract = resources.AsyncAssetsExtractResource(self)
        self.events = resources.AsyncEventsResource(self)
        self.templates = resources.AsyncTemplatesResource(self)
        self.data_sources = resources.AsyncDataSourcesResource(self)
        self.with_raw_response = AsyncTrellisWithRawResponse(self)
        self.with_streaming_response = AsyncTrellisWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class TrellisWithRawResponse:
    def __init__(self, client: Trellis) -> None:
        self.transforms = resources.TransformsResourceWithRawResponse(client.transforms)
        self.customers = resources.CustomersResourceWithRawResponse(client.customers)
        self.projects = resources.ProjectsResourceWithRawResponse(client.projects)
        self.assets = resources.AssetsResourceWithRawResponse(client.assets)
        self.assets_extract = resources.AssetsExtractResourceWithRawResponse(client.assets_extract)
        self.events = resources.EventsResourceWithRawResponse(client.events)
        self.templates = resources.TemplatesResourceWithRawResponse(client.templates)
        self.data_sources = resources.DataSourcesResourceWithRawResponse(client.data_sources)


class AsyncTrellisWithRawResponse:
    def __init__(self, client: AsyncTrellis) -> None:
        self.transforms = resources.AsyncTransformsResourceWithRawResponse(client.transforms)
        self.customers = resources.AsyncCustomersResourceWithRawResponse(client.customers)
        self.projects = resources.AsyncProjectsResourceWithRawResponse(client.projects)
        self.assets = resources.AsyncAssetsResourceWithRawResponse(client.assets)
        self.assets_extract = resources.AsyncAssetsExtractResourceWithRawResponse(client.assets_extract)
        self.events = resources.AsyncEventsResourceWithRawResponse(client.events)
        self.templates = resources.AsyncTemplatesResourceWithRawResponse(client.templates)
        self.data_sources = resources.AsyncDataSourcesResourceWithRawResponse(client.data_sources)


class TrellisWithStreamedResponse:
    def __init__(self, client: Trellis) -> None:
        self.transforms = resources.TransformsResourceWithStreamingResponse(client.transforms)
        self.customers = resources.CustomersResourceWithStreamingResponse(client.customers)
        self.projects = resources.ProjectsResourceWithStreamingResponse(client.projects)
        self.assets = resources.AssetsResourceWithStreamingResponse(client.assets)
        self.assets_extract = resources.AssetsExtractResourceWithStreamingResponse(client.assets_extract)
        self.events = resources.EventsResourceWithStreamingResponse(client.events)
        self.templates = resources.TemplatesResourceWithStreamingResponse(client.templates)
        self.data_sources = resources.DataSourcesResourceWithStreamingResponse(client.data_sources)


class AsyncTrellisWithStreamedResponse:
    def __init__(self, client: AsyncTrellis) -> None:
        self.transforms = resources.AsyncTransformsResourceWithStreamingResponse(client.transforms)
        self.customers = resources.AsyncCustomersResourceWithStreamingResponse(client.customers)
        self.projects = resources.AsyncProjectsResourceWithStreamingResponse(client.projects)
        self.assets = resources.AsyncAssetsResourceWithStreamingResponse(client.assets)
        self.assets_extract = resources.AsyncAssetsExtractResourceWithStreamingResponse(client.assets_extract)
        self.events = resources.AsyncEventsResourceWithStreamingResponse(client.events)
        self.templates = resources.AsyncTemplatesResourceWithStreamingResponse(client.templates)
        self.data_sources = resources.AsyncDataSourcesResourceWithStreamingResponse(client.data_sources)


Client = Trellis

AsyncClient = AsyncTrellis
