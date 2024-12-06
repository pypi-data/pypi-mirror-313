# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from trellis import Trellis, AsyncTrellis
from tests.utils import assert_matches_type
from trellis.types import Usage
from trellis._utils import parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCustomers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_usage(self, client: Trellis) -> None:
        customer = client.customers.usage()
        assert_matches_type(Usage, customer, path=["response"])

    @parametrize
    def test_method_usage_with_all_params(self, client: Trellis) -> None:
        customer = client.customers.usage(
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            limit=0,
            offset=0,
            order="asc",
            order_by="updated_at",
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(Usage, customer, path=["response"])

    @parametrize
    def test_raw_response_usage(self, client: Trellis) -> None:
        response = client.customers.with_raw_response.usage()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        customer = response.parse()
        assert_matches_type(Usage, customer, path=["response"])

    @parametrize
    def test_streaming_response_usage(self, client: Trellis) -> None:
        with client.customers.with_streaming_response.usage() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            customer = response.parse()
            assert_matches_type(Usage, customer, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCustomers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_usage(self, async_client: AsyncTrellis) -> None:
        customer = await async_client.customers.usage()
        assert_matches_type(Usage, customer, path=["response"])

    @parametrize
    async def test_method_usage_with_all_params(self, async_client: AsyncTrellis) -> None:
        customer = await async_client.customers.usage(
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            limit=0,
            offset=0,
            order="asc",
            order_by="updated_at",
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(Usage, customer, path=["response"])

    @parametrize
    async def test_raw_response_usage(self, async_client: AsyncTrellis) -> None:
        response = await async_client.customers.with_raw_response.usage()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        customer = await response.parse()
        assert_matches_type(Usage, customer, path=["response"])

    @parametrize
    async def test_streaming_response_usage(self, async_client: AsyncTrellis) -> None:
        async with async_client.customers.with_streaming_response.usage() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            customer = await response.parse()
            assert_matches_type(Usage, customer, path=["response"])

        assert cast(Any, response.is_closed) is True
