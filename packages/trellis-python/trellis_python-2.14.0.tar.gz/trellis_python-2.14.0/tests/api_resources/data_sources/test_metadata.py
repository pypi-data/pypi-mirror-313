# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from trellis import Trellis, AsyncTrellis
from tests.utils import assert_matches_type
from trellis.types.data_sources import MetadataRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMetadata:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Trellis) -> None:
        metadata = client.data_sources.metadata.retrieve(
            source_id="source_id",
        )
        assert_matches_type(MetadataRetrieveResponse, metadata, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Trellis) -> None:
        metadata = client.data_sources.metadata.retrieve(
            source_id="source_id",
            limit=0,
            offset=0,
            order="asc",
            order_by="updated_at",
        )
        assert_matches_type(MetadataRetrieveResponse, metadata, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Trellis) -> None:
        response = client.data_sources.metadata.with_raw_response.retrieve(
            source_id="source_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metadata = response.parse()
        assert_matches_type(MetadataRetrieveResponse, metadata, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Trellis) -> None:
        with client.data_sources.metadata.with_streaming_response.retrieve(
            source_id="source_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metadata = response.parse()
            assert_matches_type(MetadataRetrieveResponse, metadata, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `source_id` but received ''"):
            client.data_sources.metadata.with_raw_response.retrieve(
                source_id="",
            )


class TestAsyncMetadata:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncTrellis) -> None:
        metadata = await async_client.data_sources.metadata.retrieve(
            source_id="source_id",
        )
        assert_matches_type(MetadataRetrieveResponse, metadata, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncTrellis) -> None:
        metadata = await async_client.data_sources.metadata.retrieve(
            source_id="source_id",
            limit=0,
            offset=0,
            order="asc",
            order_by="updated_at",
        )
        assert_matches_type(MetadataRetrieveResponse, metadata, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncTrellis) -> None:
        response = await async_client.data_sources.metadata.with_raw_response.retrieve(
            source_id="source_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metadata = await response.parse()
        assert_matches_type(MetadataRetrieveResponse, metadata, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncTrellis) -> None:
        async with async_client.data_sources.metadata.with_streaming_response.retrieve(
            source_id="source_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metadata = await response.parse()
            assert_matches_type(MetadataRetrieveResponse, metadata, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `source_id` but received ''"):
            await async_client.data_sources.metadata.with_raw_response.retrieve(
                source_id="",
            )
