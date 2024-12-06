# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from trellis import Trellis, AsyncTrellis
from tests.utils import assert_matches_type
from trellis.types.transforms.validations import (
    ParamCreateResponse,
    ParamDeleteResponse,
    ParamUpdateResponse,
    ParamRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestParams:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Trellis) -> None:
        param = client.transforms.validations.params.create(
            transform_id="transform_id",
            validation_columns=["string"],
            validation_name="validation_name",
        )
        assert_matches_type(ParamCreateResponse, param, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Trellis) -> None:
        param = client.transforms.validations.params.create(
            transform_id="transform_id",
            validation_columns=["string"],
            validation_name="validation_name",
            validation_endpoint="validation_endpoint",
            validation_rule="validation_rule",
        )
        assert_matches_type(ParamCreateResponse, param, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Trellis) -> None:
        response = client.transforms.validations.params.with_raw_response.create(
            transform_id="transform_id",
            validation_columns=["string"],
            validation_name="validation_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        param = response.parse()
        assert_matches_type(ParamCreateResponse, param, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Trellis) -> None:
        with client.transforms.validations.params.with_streaming_response.create(
            transform_id="transform_id",
            validation_columns=["string"],
            validation_name="validation_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            param = response.parse()
            assert_matches_type(ParamCreateResponse, param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            client.transforms.validations.params.with_raw_response.create(
                transform_id="",
                validation_columns=["string"],
                validation_name="validation_name",
            )

    @parametrize
    def test_method_retrieve(self, client: Trellis) -> None:
        param = client.transforms.validations.params.retrieve(
            "transform_id",
        )
        assert_matches_type(ParamRetrieveResponse, param, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Trellis) -> None:
        response = client.transforms.validations.params.with_raw_response.retrieve(
            "transform_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        param = response.parse()
        assert_matches_type(ParamRetrieveResponse, param, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Trellis) -> None:
        with client.transforms.validations.params.with_streaming_response.retrieve(
            "transform_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            param = response.parse()
            assert_matches_type(ParamRetrieveResponse, param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            client.transforms.validations.params.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: Trellis) -> None:
        param = client.transforms.validations.params.update(
            validation_param_id="validation_param_id",
            transform_id="transform_id",
            validation_columns=["string"],
            validation_name="validation_name",
        )
        assert_matches_type(ParamUpdateResponse, param, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Trellis) -> None:
        param = client.transforms.validations.params.update(
            validation_param_id="validation_param_id",
            transform_id="transform_id",
            validation_columns=["string"],
            validation_name="validation_name",
            validation_endpoint="validation_endpoint",
            validation_rule="validation_rule",
        )
        assert_matches_type(ParamUpdateResponse, param, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Trellis) -> None:
        response = client.transforms.validations.params.with_raw_response.update(
            validation_param_id="validation_param_id",
            transform_id="transform_id",
            validation_columns=["string"],
            validation_name="validation_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        param = response.parse()
        assert_matches_type(ParamUpdateResponse, param, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Trellis) -> None:
        with client.transforms.validations.params.with_streaming_response.update(
            validation_param_id="validation_param_id",
            transform_id="transform_id",
            validation_columns=["string"],
            validation_name="validation_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            param = response.parse()
            assert_matches_type(ParamUpdateResponse, param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            client.transforms.validations.params.with_raw_response.update(
                validation_param_id="validation_param_id",
                transform_id="",
                validation_columns=["string"],
                validation_name="validation_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `validation_param_id` but received ''"):
            client.transforms.validations.params.with_raw_response.update(
                validation_param_id="",
                transform_id="transform_id",
                validation_columns=["string"],
                validation_name="validation_name",
            )

    @parametrize
    def test_method_delete(self, client: Trellis) -> None:
        param = client.transforms.validations.params.delete(
            validation_param_id="validation_param_id",
            transform_id="transform_id",
        )
        assert_matches_type(ParamDeleteResponse, param, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Trellis) -> None:
        response = client.transforms.validations.params.with_raw_response.delete(
            validation_param_id="validation_param_id",
            transform_id="transform_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        param = response.parse()
        assert_matches_type(ParamDeleteResponse, param, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Trellis) -> None:
        with client.transforms.validations.params.with_streaming_response.delete(
            validation_param_id="validation_param_id",
            transform_id="transform_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            param = response.parse()
            assert_matches_type(ParamDeleteResponse, param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            client.transforms.validations.params.with_raw_response.delete(
                validation_param_id="validation_param_id",
                transform_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `validation_param_id` but received ''"):
            client.transforms.validations.params.with_raw_response.delete(
                validation_param_id="",
                transform_id="transform_id",
            )


class TestAsyncParams:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncTrellis) -> None:
        param = await async_client.transforms.validations.params.create(
            transform_id="transform_id",
            validation_columns=["string"],
            validation_name="validation_name",
        )
        assert_matches_type(ParamCreateResponse, param, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncTrellis) -> None:
        param = await async_client.transforms.validations.params.create(
            transform_id="transform_id",
            validation_columns=["string"],
            validation_name="validation_name",
            validation_endpoint="validation_endpoint",
            validation_rule="validation_rule",
        )
        assert_matches_type(ParamCreateResponse, param, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncTrellis) -> None:
        response = await async_client.transforms.validations.params.with_raw_response.create(
            transform_id="transform_id",
            validation_columns=["string"],
            validation_name="validation_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        param = await response.parse()
        assert_matches_type(ParamCreateResponse, param, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncTrellis) -> None:
        async with async_client.transforms.validations.params.with_streaming_response.create(
            transform_id="transform_id",
            validation_columns=["string"],
            validation_name="validation_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            param = await response.parse()
            assert_matches_type(ParamCreateResponse, param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            await async_client.transforms.validations.params.with_raw_response.create(
                transform_id="",
                validation_columns=["string"],
                validation_name="validation_name",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncTrellis) -> None:
        param = await async_client.transforms.validations.params.retrieve(
            "transform_id",
        )
        assert_matches_type(ParamRetrieveResponse, param, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncTrellis) -> None:
        response = await async_client.transforms.validations.params.with_raw_response.retrieve(
            "transform_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        param = await response.parse()
        assert_matches_type(ParamRetrieveResponse, param, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncTrellis) -> None:
        async with async_client.transforms.validations.params.with_streaming_response.retrieve(
            "transform_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            param = await response.parse()
            assert_matches_type(ParamRetrieveResponse, param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            await async_client.transforms.validations.params.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncTrellis) -> None:
        param = await async_client.transforms.validations.params.update(
            validation_param_id="validation_param_id",
            transform_id="transform_id",
            validation_columns=["string"],
            validation_name="validation_name",
        )
        assert_matches_type(ParamUpdateResponse, param, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncTrellis) -> None:
        param = await async_client.transforms.validations.params.update(
            validation_param_id="validation_param_id",
            transform_id="transform_id",
            validation_columns=["string"],
            validation_name="validation_name",
            validation_endpoint="validation_endpoint",
            validation_rule="validation_rule",
        )
        assert_matches_type(ParamUpdateResponse, param, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncTrellis) -> None:
        response = await async_client.transforms.validations.params.with_raw_response.update(
            validation_param_id="validation_param_id",
            transform_id="transform_id",
            validation_columns=["string"],
            validation_name="validation_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        param = await response.parse()
        assert_matches_type(ParamUpdateResponse, param, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncTrellis) -> None:
        async with async_client.transforms.validations.params.with_streaming_response.update(
            validation_param_id="validation_param_id",
            transform_id="transform_id",
            validation_columns=["string"],
            validation_name="validation_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            param = await response.parse()
            assert_matches_type(ParamUpdateResponse, param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            await async_client.transforms.validations.params.with_raw_response.update(
                validation_param_id="validation_param_id",
                transform_id="",
                validation_columns=["string"],
                validation_name="validation_name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `validation_param_id` but received ''"):
            await async_client.transforms.validations.params.with_raw_response.update(
                validation_param_id="",
                transform_id="transform_id",
                validation_columns=["string"],
                validation_name="validation_name",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncTrellis) -> None:
        param = await async_client.transforms.validations.params.delete(
            validation_param_id="validation_param_id",
            transform_id="transform_id",
        )
        assert_matches_type(ParamDeleteResponse, param, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncTrellis) -> None:
        response = await async_client.transforms.validations.params.with_raw_response.delete(
            validation_param_id="validation_param_id",
            transform_id="transform_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        param = await response.parse()
        assert_matches_type(ParamDeleteResponse, param, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncTrellis) -> None:
        async with async_client.transforms.validations.params.with_streaming_response.delete(
            validation_param_id="validation_param_id",
            transform_id="transform_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            param = await response.parse()
            assert_matches_type(ParamDeleteResponse, param, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            await async_client.transforms.validations.params.with_raw_response.delete(
                validation_param_id="validation_param_id",
                transform_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `validation_param_id` but received ''"):
            await async_client.transforms.validations.params.with_raw_response.delete(
                validation_param_id="",
                transform_id="transform_id",
            )
