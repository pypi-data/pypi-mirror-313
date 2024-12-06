# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from trellis import Trellis, AsyncTrellis
from tests.utils import assert_matches_type
from trellis.types import Extract

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAssetsExtract:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_extract(self, client: Trellis) -> None:
        assets_extract = client.assets_extract.extract()
        assert_matches_type(Extract, assets_extract, path=["response"])

    @parametrize
    def test_method_extract_with_all_params(self, client: Trellis) -> None:
        assets_extract = client.assets_extract.extract(
            asset_ids=["string"],
            parse_strategy="optimized",
            proj_id="proj_id",
            run_on_all_assets=True,
        )
        assert_matches_type(Extract, assets_extract, path=["response"])

    @parametrize
    def test_raw_response_extract(self, client: Trellis) -> None:
        response = client.assets_extract.with_raw_response.extract()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        assets_extract = response.parse()
        assert_matches_type(Extract, assets_extract, path=["response"])

    @parametrize
    def test_streaming_response_extract(self, client: Trellis) -> None:
        with client.assets_extract.with_streaming_response.extract() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            assets_extract = response.parse()
            assert_matches_type(Extract, assets_extract, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update_status(self, client: Trellis) -> None:
        assets_extract = client.assets_extract.update_status(
            body={},
        )
        assert_matches_type(object, assets_extract, path=["response"])

    @parametrize
    def test_raw_response_update_status(self, client: Trellis) -> None:
        response = client.assets_extract.with_raw_response.update_status(
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        assets_extract = response.parse()
        assert_matches_type(object, assets_extract, path=["response"])

    @parametrize
    def test_streaming_response_update_status(self, client: Trellis) -> None:
        with client.assets_extract.with_streaming_response.update_status(
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            assets_extract = response.parse()
            assert_matches_type(object, assets_extract, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAssetsExtract:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_extract(self, async_client: AsyncTrellis) -> None:
        assets_extract = await async_client.assets_extract.extract()
        assert_matches_type(Extract, assets_extract, path=["response"])

    @parametrize
    async def test_method_extract_with_all_params(self, async_client: AsyncTrellis) -> None:
        assets_extract = await async_client.assets_extract.extract(
            asset_ids=["string"],
            parse_strategy="optimized",
            proj_id="proj_id",
            run_on_all_assets=True,
        )
        assert_matches_type(Extract, assets_extract, path=["response"])

    @parametrize
    async def test_raw_response_extract(self, async_client: AsyncTrellis) -> None:
        response = await async_client.assets_extract.with_raw_response.extract()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        assets_extract = await response.parse()
        assert_matches_type(Extract, assets_extract, path=["response"])

    @parametrize
    async def test_streaming_response_extract(self, async_client: AsyncTrellis) -> None:
        async with async_client.assets_extract.with_streaming_response.extract() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            assets_extract = await response.parse()
            assert_matches_type(Extract, assets_extract, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update_status(self, async_client: AsyncTrellis) -> None:
        assets_extract = await async_client.assets_extract.update_status(
            body={},
        )
        assert_matches_type(object, assets_extract, path=["response"])

    @parametrize
    async def test_raw_response_update_status(self, async_client: AsyncTrellis) -> None:
        response = await async_client.assets_extract.with_raw_response.update_status(
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        assets_extract = await response.parse()
        assert_matches_type(object, assets_extract, path=["response"])

    @parametrize
    async def test_streaming_response_update_status(self, async_client: AsyncTrellis) -> None:
        async with async_client.assets_extract.with_streaming_response.update_status(
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            assets_extract = await response.parse()
            assert_matches_type(object, assets_extract, path=["response"])

        assert cast(Any, response.is_closed) is True
