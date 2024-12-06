# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from trellis import Trellis, AsyncTrellis
from tests.utils import assert_matches_type
from trellis.types.transforms import (
    ResultExportResponse,
    ResultUpdateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestResults:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_update(self, client: Trellis) -> None:
        result = client.transforms.results.update(
            result_id="result_id",
            transform_id="transform_id",
            body={},
        )
        assert_matches_type(ResultUpdateResponse, result, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Trellis) -> None:
        response = client.transforms.results.with_raw_response.update(
            result_id="result_id",
            transform_id="transform_id",
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        result = response.parse()
        assert_matches_type(ResultUpdateResponse, result, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Trellis) -> None:
        with client.transforms.results.with_streaming_response.update(
            result_id="result_id",
            transform_id="transform_id",
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            result = response.parse()
            assert_matches_type(ResultUpdateResponse, result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            client.transforms.results.with_raw_response.update(
                result_id="result_id",
                transform_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `result_id` but received ''"):
            client.transforms.results.with_raw_response.update(
                result_id="",
                transform_id="transform_id",
                body={},
            )

    @parametrize
    def test_method_export(self, client: Trellis) -> None:
        result = client.transforms.results.export(
            transform_id="transform_id",
            file_type="excel",
        )
        assert_matches_type(ResultExportResponse, result, path=["response"])

    @parametrize
    def test_method_export_with_all_params(self, client: Trellis) -> None:
        result = client.transforms.results.export(
            transform_id="transform_id",
            file_type="excel",
            auth_key="auth_key",
        )
        assert_matches_type(ResultExportResponse, result, path=["response"])

    @parametrize
    def test_raw_response_export(self, client: Trellis) -> None:
        response = client.transforms.results.with_raw_response.export(
            transform_id="transform_id",
            file_type="excel",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        result = response.parse()
        assert_matches_type(ResultExportResponse, result, path=["response"])

    @parametrize
    def test_streaming_response_export(self, client: Trellis) -> None:
        with client.transforms.results.with_streaming_response.export(
            transform_id="transform_id",
            file_type="excel",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            result = response.parse()
            assert_matches_type(ResultExportResponse, result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_export(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            client.transforms.results.with_raw_response.export(
                transform_id="",
                file_type="excel",
            )


class TestAsyncResults:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_update(self, async_client: AsyncTrellis) -> None:
        result = await async_client.transforms.results.update(
            result_id="result_id",
            transform_id="transform_id",
            body={},
        )
        assert_matches_type(ResultUpdateResponse, result, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncTrellis) -> None:
        response = await async_client.transforms.results.with_raw_response.update(
            result_id="result_id",
            transform_id="transform_id",
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        result = await response.parse()
        assert_matches_type(ResultUpdateResponse, result, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncTrellis) -> None:
        async with async_client.transforms.results.with_streaming_response.update(
            result_id="result_id",
            transform_id="transform_id",
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            result = await response.parse()
            assert_matches_type(ResultUpdateResponse, result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            await async_client.transforms.results.with_raw_response.update(
                result_id="result_id",
                transform_id="",
                body={},
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `result_id` but received ''"):
            await async_client.transforms.results.with_raw_response.update(
                result_id="",
                transform_id="transform_id",
                body={},
            )

    @parametrize
    async def test_method_export(self, async_client: AsyncTrellis) -> None:
        result = await async_client.transforms.results.export(
            transform_id="transform_id",
            file_type="excel",
        )
        assert_matches_type(ResultExportResponse, result, path=["response"])

    @parametrize
    async def test_method_export_with_all_params(self, async_client: AsyncTrellis) -> None:
        result = await async_client.transforms.results.export(
            transform_id="transform_id",
            file_type="excel",
            auth_key="auth_key",
        )
        assert_matches_type(ResultExportResponse, result, path=["response"])

    @parametrize
    async def test_raw_response_export(self, async_client: AsyncTrellis) -> None:
        response = await async_client.transforms.results.with_raw_response.export(
            transform_id="transform_id",
            file_type="excel",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        result = await response.parse()
        assert_matches_type(ResultExportResponse, result, path=["response"])

    @parametrize
    async def test_streaming_response_export(self, async_client: AsyncTrellis) -> None:
        async with async_client.transforms.results.with_streaming_response.export(
            transform_id="transform_id",
            file_type="excel",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            result = await response.parse()
            assert_matches_type(ResultExportResponse, result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_export(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            await async_client.transforms.results.with_raw_response.export(
                transform_id="",
                file_type="excel",
            )
