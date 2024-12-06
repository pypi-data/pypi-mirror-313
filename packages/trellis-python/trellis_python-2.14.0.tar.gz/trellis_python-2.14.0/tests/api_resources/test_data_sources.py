# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from trellis import Trellis, AsyncTrellis
from tests.utils import assert_matches_type
from trellis.types import Source, DataSourceRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDataSources:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Trellis) -> None:
        data_source = client.data_sources.create(
            credentials={
                "access_key": "access_key",
                "path": "path",
                "region": "region",
                "secret_key": "secret_key",
                "session_token": "session_token",
            },
            name="name",
            proj_id="proj_id",
            type="s3",
        )
        assert_matches_type(Source, data_source, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Trellis) -> None:
        response = client.data_sources.with_raw_response.create(
            credentials={
                "access_key": "access_key",
                "path": "path",
                "region": "region",
                "secret_key": "secret_key",
                "session_token": "session_token",
            },
            name="name",
            proj_id="proj_id",
            type="s3",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        data_source = response.parse()
        assert_matches_type(Source, data_source, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Trellis) -> None:
        with client.data_sources.with_streaming_response.create(
            credentials={
                "access_key": "access_key",
                "path": "path",
                "region": "region",
                "secret_key": "secret_key",
                "session_token": "session_token",
            },
            name="name",
            proj_id="proj_id",
            type="s3",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            data_source = response.parse()
            assert_matches_type(Source, data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Trellis) -> None:
        data_source = client.data_sources.retrieve()
        assert_matches_type(DataSourceRetrieveResponse, data_source, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Trellis) -> None:
        data_source = client.data_sources.retrieve(
            limit=0,
            offset=0,
            order="asc",
            order_by="updated_at",
            proj_id="proj_id",
        )
        assert_matches_type(DataSourceRetrieveResponse, data_source, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Trellis) -> None:
        response = client.data_sources.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        data_source = response.parse()
        assert_matches_type(DataSourceRetrieveResponse, data_source, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Trellis) -> None:
        with client.data_sources.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            data_source = response.parse()
            assert_matches_type(DataSourceRetrieveResponse, data_source, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDataSources:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncTrellis) -> None:
        data_source = await async_client.data_sources.create(
            credentials={
                "access_key": "access_key",
                "path": "path",
                "region": "region",
                "secret_key": "secret_key",
                "session_token": "session_token",
            },
            name="name",
            proj_id="proj_id",
            type="s3",
        )
        assert_matches_type(Source, data_source, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncTrellis) -> None:
        response = await async_client.data_sources.with_raw_response.create(
            credentials={
                "access_key": "access_key",
                "path": "path",
                "region": "region",
                "secret_key": "secret_key",
                "session_token": "session_token",
            },
            name="name",
            proj_id="proj_id",
            type="s3",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        data_source = await response.parse()
        assert_matches_type(Source, data_source, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncTrellis) -> None:
        async with async_client.data_sources.with_streaming_response.create(
            credentials={
                "access_key": "access_key",
                "path": "path",
                "region": "region",
                "secret_key": "secret_key",
                "session_token": "session_token",
            },
            name="name",
            proj_id="proj_id",
            type="s3",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            data_source = await response.parse()
            assert_matches_type(Source, data_source, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncTrellis) -> None:
        data_source = await async_client.data_sources.retrieve()
        assert_matches_type(DataSourceRetrieveResponse, data_source, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncTrellis) -> None:
        data_source = await async_client.data_sources.retrieve(
            limit=0,
            offset=0,
            order="asc",
            order_by="updated_at",
            proj_id="proj_id",
        )
        assert_matches_type(DataSourceRetrieveResponse, data_source, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncTrellis) -> None:
        response = await async_client.data_sources.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        data_source = await response.parse()
        assert_matches_type(DataSourceRetrieveResponse, data_source, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncTrellis) -> None:
        async with async_client.data_sources.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            data_source = await response.parse()
            assert_matches_type(DataSourceRetrieveResponse, data_source, path=["response"])

        assert cast(Any, response.is_closed) is True
