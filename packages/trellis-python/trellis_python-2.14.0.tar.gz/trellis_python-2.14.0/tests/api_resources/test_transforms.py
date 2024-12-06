# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from trellis import Trellis, AsyncTrellis
from tests.utils import assert_matches_type
from trellis.types import (
    TransformListResponse,
    TransformCreateResponse,
    TransformDeleteResponse,
    TransformUpdateResponse,
    TransformDuplicateResponse,
    TransformReferenceResponse,
    TransformSummarizeResponse,
    TransformAutoschemaResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTransforms:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Trellis) -> None:
        transform = client.transforms.create(
            proj_id="proj_id",
            transform_params={"model": "model"},
        )
        assert_matches_type(TransformCreateResponse, transform, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Trellis) -> None:
        transform = client.transforms.create(
            proj_id="proj_id",
            transform_params={
                "model": "model",
                "mode": "document",
                "operations": [
                    {
                        "column_name": "column_name",
                        "column_type": "text",
                        "task_description": "task_description",
                        "transform_type": "extraction",
                        "default_value": {},
                        "has_default": True,
                        "operations": [{}],
                        "output_values": {"foo": "string"},
                    }
                ],
                "table_preferences": {
                    "advanced_reasoning": True,
                    "included_table_names": ["string"],
                },
            },
            transform_name="transform_name",
        )
        assert_matches_type(TransformCreateResponse, transform, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Trellis) -> None:
        response = client.transforms.with_raw_response.create(
            proj_id="proj_id",
            transform_params={"model": "model"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transform = response.parse()
        assert_matches_type(TransformCreateResponse, transform, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Trellis) -> None:
        with client.transforms.with_streaming_response.create(
            proj_id="proj_id",
            transform_params={"model": "model"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transform = response.parse()
            assert_matches_type(TransformCreateResponse, transform, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update(self, client: Trellis) -> None:
        transform = client.transforms.update(
            transform_id="transform_id",
        )
        assert_matches_type(TransformUpdateResponse, transform, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Trellis) -> None:
        transform = client.transforms.update(
            transform_id="transform_id",
            asset_ids=["string"],
            include_reference=True,
        )
        assert_matches_type(TransformUpdateResponse, transform, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Trellis) -> None:
        response = client.transforms.with_raw_response.update(
            transform_id="transform_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transform = response.parse()
        assert_matches_type(TransformUpdateResponse, transform, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Trellis) -> None:
        with client.transforms.with_streaming_response.update(
            transform_id="transform_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transform = response.parse()
            assert_matches_type(TransformUpdateResponse, transform, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            client.transforms.with_raw_response.update(
                transform_id="",
            )

    @parametrize
    def test_method_list(self, client: Trellis) -> None:
        transform = client.transforms.list()
        assert_matches_type(TransformListResponse, transform, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Trellis) -> None:
        transform = client.transforms.list(
            include_transform_params=True,
            limit=0,
            offset=0,
            order="asc",
            order_by="updated_at",
            proj_ids=["string"],
            search_term="search_term",
            transform_ids=["string"],
        )
        assert_matches_type(TransformListResponse, transform, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Trellis) -> None:
        response = client.transforms.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transform = response.parse()
        assert_matches_type(TransformListResponse, transform, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Trellis) -> None:
        with client.transforms.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transform = response.parse()
            assert_matches_type(TransformListResponse, transform, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Trellis) -> None:
        transform = client.transforms.delete(
            "transform_id",
        )
        assert_matches_type(TransformDeleteResponse, transform, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Trellis) -> None:
        response = client.transforms.with_raw_response.delete(
            "transform_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transform = response.parse()
        assert_matches_type(TransformDeleteResponse, transform, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Trellis) -> None:
        with client.transforms.with_streaming_response.delete(
            "transform_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transform = response.parse()
            assert_matches_type(TransformDeleteResponse, transform, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            client.transforms.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_autoschema(self, client: Trellis) -> None:
        transform = client.transforms.autoschema(
            "transform_id",
        )
        assert_matches_type(TransformAutoschemaResponse, transform, path=["response"])

    @parametrize
    def test_raw_response_autoschema(self, client: Trellis) -> None:
        response = client.transforms.with_raw_response.autoschema(
            "transform_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transform = response.parse()
        assert_matches_type(TransformAutoschemaResponse, transform, path=["response"])

    @parametrize
    def test_streaming_response_autoschema(self, client: Trellis) -> None:
        with client.transforms.with_streaming_response.autoschema(
            "transform_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transform = response.parse()
            assert_matches_type(TransformAutoschemaResponse, transform, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_autoschema(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            client.transforms.with_raw_response.autoschema(
                "",
            )

    @parametrize
    def test_method_duplicate(self, client: Trellis) -> None:
        transform = client.transforms.duplicate(
            "transform_id",
        )
        assert_matches_type(TransformDuplicateResponse, transform, path=["response"])

    @parametrize
    def test_raw_response_duplicate(self, client: Trellis) -> None:
        response = client.transforms.with_raw_response.duplicate(
            "transform_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transform = response.parse()
        assert_matches_type(TransformDuplicateResponse, transform, path=["response"])

    @parametrize
    def test_streaming_response_duplicate(self, client: Trellis) -> None:
        with client.transforms.with_streaming_response.duplicate(
            "transform_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transform = response.parse()
            assert_matches_type(TransformDuplicateResponse, transform, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_duplicate(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            client.transforms.with_raw_response.duplicate(
                "",
            )

    @parametrize
    def test_method_reference(self, client: Trellis) -> None:
        transform = client.transforms.reference(
            transform_id="transform_id",
        )
        assert_matches_type(TransformReferenceResponse, transform, path=["response"])

    @parametrize
    def test_method_reference_with_all_params(self, client: Trellis) -> None:
        transform = client.transforms.reference(
            transform_id="transform_id",
            column_name="column_name",
            result_id="result_id",
        )
        assert_matches_type(TransformReferenceResponse, transform, path=["response"])

    @parametrize
    def test_raw_response_reference(self, client: Trellis) -> None:
        response = client.transforms.with_raw_response.reference(
            transform_id="transform_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transform = response.parse()
        assert_matches_type(TransformReferenceResponse, transform, path=["response"])

    @parametrize
    def test_streaming_response_reference(self, client: Trellis) -> None:
        with client.transforms.with_streaming_response.reference(
            transform_id="transform_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transform = response.parse()
            assert_matches_type(TransformReferenceResponse, transform, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_summarize(self, client: Trellis) -> None:
        transform = client.transforms.summarize(
            transform_id="transform_id",
            operation_ids=["string"],
        )
        assert_matches_type(TransformSummarizeResponse, transform, path=["response"])

    @parametrize
    def test_method_summarize_with_all_params(self, client: Trellis) -> None:
        transform = client.transforms.summarize(
            transform_id="transform_id",
            operation_ids=["string"],
            filters={},
            prompt_details="prompt_details",
            result_ids=["string"],
        )
        assert_matches_type(TransformSummarizeResponse, transform, path=["response"])

    @parametrize
    def test_raw_response_summarize(self, client: Trellis) -> None:
        response = client.transforms.with_raw_response.summarize(
            transform_id="transform_id",
            operation_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transform = response.parse()
        assert_matches_type(TransformSummarizeResponse, transform, path=["response"])

    @parametrize
    def test_streaming_response_summarize(self, client: Trellis) -> None:
        with client.transforms.with_streaming_response.summarize(
            transform_id="transform_id",
            operation_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transform = response.parse()
            assert_matches_type(TransformSummarizeResponse, transform, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_summarize(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            client.transforms.with_raw_response.summarize(
                transform_id="",
                operation_ids=["string"],
            )

    @parametrize
    def test_method_wake_up(self, client: Trellis) -> None:
        transform = client.transforms.wake_up()
        assert_matches_type(object, transform, path=["response"])

    @parametrize
    def test_raw_response_wake_up(self, client: Trellis) -> None:
        response = client.transforms.with_raw_response.wake_up()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transform = response.parse()
        assert_matches_type(object, transform, path=["response"])

    @parametrize
    def test_streaming_response_wake_up(self, client: Trellis) -> None:
        with client.transforms.with_streaming_response.wake_up() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transform = response.parse()
            assert_matches_type(object, transform, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTransforms:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncTrellis) -> None:
        transform = await async_client.transforms.create(
            proj_id="proj_id",
            transform_params={"model": "model"},
        )
        assert_matches_type(TransformCreateResponse, transform, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncTrellis) -> None:
        transform = await async_client.transforms.create(
            proj_id="proj_id",
            transform_params={
                "model": "model",
                "mode": "document",
                "operations": [
                    {
                        "column_name": "column_name",
                        "column_type": "text",
                        "task_description": "task_description",
                        "transform_type": "extraction",
                        "default_value": {},
                        "has_default": True,
                        "operations": [{}],
                        "output_values": {"foo": "string"},
                    }
                ],
                "table_preferences": {
                    "advanced_reasoning": True,
                    "included_table_names": ["string"],
                },
            },
            transform_name="transform_name",
        )
        assert_matches_type(TransformCreateResponse, transform, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncTrellis) -> None:
        response = await async_client.transforms.with_raw_response.create(
            proj_id="proj_id",
            transform_params={"model": "model"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transform = await response.parse()
        assert_matches_type(TransformCreateResponse, transform, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncTrellis) -> None:
        async with async_client.transforms.with_streaming_response.create(
            proj_id="proj_id",
            transform_params={"model": "model"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transform = await response.parse()
            assert_matches_type(TransformCreateResponse, transform, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update(self, async_client: AsyncTrellis) -> None:
        transform = await async_client.transforms.update(
            transform_id="transform_id",
        )
        assert_matches_type(TransformUpdateResponse, transform, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncTrellis) -> None:
        transform = await async_client.transforms.update(
            transform_id="transform_id",
            asset_ids=["string"],
            include_reference=True,
        )
        assert_matches_type(TransformUpdateResponse, transform, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncTrellis) -> None:
        response = await async_client.transforms.with_raw_response.update(
            transform_id="transform_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transform = await response.parse()
        assert_matches_type(TransformUpdateResponse, transform, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncTrellis) -> None:
        async with async_client.transforms.with_streaming_response.update(
            transform_id="transform_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transform = await response.parse()
            assert_matches_type(TransformUpdateResponse, transform, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            await async_client.transforms.with_raw_response.update(
                transform_id="",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncTrellis) -> None:
        transform = await async_client.transforms.list()
        assert_matches_type(TransformListResponse, transform, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncTrellis) -> None:
        transform = await async_client.transforms.list(
            include_transform_params=True,
            limit=0,
            offset=0,
            order="asc",
            order_by="updated_at",
            proj_ids=["string"],
            search_term="search_term",
            transform_ids=["string"],
        )
        assert_matches_type(TransformListResponse, transform, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncTrellis) -> None:
        response = await async_client.transforms.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transform = await response.parse()
        assert_matches_type(TransformListResponse, transform, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncTrellis) -> None:
        async with async_client.transforms.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transform = await response.parse()
            assert_matches_type(TransformListResponse, transform, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncTrellis) -> None:
        transform = await async_client.transforms.delete(
            "transform_id",
        )
        assert_matches_type(TransformDeleteResponse, transform, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncTrellis) -> None:
        response = await async_client.transforms.with_raw_response.delete(
            "transform_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transform = await response.parse()
        assert_matches_type(TransformDeleteResponse, transform, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncTrellis) -> None:
        async with async_client.transforms.with_streaming_response.delete(
            "transform_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transform = await response.parse()
            assert_matches_type(TransformDeleteResponse, transform, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            await async_client.transforms.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_autoschema(self, async_client: AsyncTrellis) -> None:
        transform = await async_client.transforms.autoschema(
            "transform_id",
        )
        assert_matches_type(TransformAutoschemaResponse, transform, path=["response"])

    @parametrize
    async def test_raw_response_autoschema(self, async_client: AsyncTrellis) -> None:
        response = await async_client.transforms.with_raw_response.autoschema(
            "transform_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transform = await response.parse()
        assert_matches_type(TransformAutoschemaResponse, transform, path=["response"])

    @parametrize
    async def test_streaming_response_autoschema(self, async_client: AsyncTrellis) -> None:
        async with async_client.transforms.with_streaming_response.autoschema(
            "transform_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transform = await response.parse()
            assert_matches_type(TransformAutoschemaResponse, transform, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_autoschema(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            await async_client.transforms.with_raw_response.autoschema(
                "",
            )

    @parametrize
    async def test_method_duplicate(self, async_client: AsyncTrellis) -> None:
        transform = await async_client.transforms.duplicate(
            "transform_id",
        )
        assert_matches_type(TransformDuplicateResponse, transform, path=["response"])

    @parametrize
    async def test_raw_response_duplicate(self, async_client: AsyncTrellis) -> None:
        response = await async_client.transforms.with_raw_response.duplicate(
            "transform_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transform = await response.parse()
        assert_matches_type(TransformDuplicateResponse, transform, path=["response"])

    @parametrize
    async def test_streaming_response_duplicate(self, async_client: AsyncTrellis) -> None:
        async with async_client.transforms.with_streaming_response.duplicate(
            "transform_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transform = await response.parse()
            assert_matches_type(TransformDuplicateResponse, transform, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_duplicate(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            await async_client.transforms.with_raw_response.duplicate(
                "",
            )

    @parametrize
    async def test_method_reference(self, async_client: AsyncTrellis) -> None:
        transform = await async_client.transforms.reference(
            transform_id="transform_id",
        )
        assert_matches_type(TransformReferenceResponse, transform, path=["response"])

    @parametrize
    async def test_method_reference_with_all_params(self, async_client: AsyncTrellis) -> None:
        transform = await async_client.transforms.reference(
            transform_id="transform_id",
            column_name="column_name",
            result_id="result_id",
        )
        assert_matches_type(TransformReferenceResponse, transform, path=["response"])

    @parametrize
    async def test_raw_response_reference(self, async_client: AsyncTrellis) -> None:
        response = await async_client.transforms.with_raw_response.reference(
            transform_id="transform_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transform = await response.parse()
        assert_matches_type(TransformReferenceResponse, transform, path=["response"])

    @parametrize
    async def test_streaming_response_reference(self, async_client: AsyncTrellis) -> None:
        async with async_client.transforms.with_streaming_response.reference(
            transform_id="transform_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transform = await response.parse()
            assert_matches_type(TransformReferenceResponse, transform, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_summarize(self, async_client: AsyncTrellis) -> None:
        transform = await async_client.transforms.summarize(
            transform_id="transform_id",
            operation_ids=["string"],
        )
        assert_matches_type(TransformSummarizeResponse, transform, path=["response"])

    @parametrize
    async def test_method_summarize_with_all_params(self, async_client: AsyncTrellis) -> None:
        transform = await async_client.transforms.summarize(
            transform_id="transform_id",
            operation_ids=["string"],
            filters={},
            prompt_details="prompt_details",
            result_ids=["string"],
        )
        assert_matches_type(TransformSummarizeResponse, transform, path=["response"])

    @parametrize
    async def test_raw_response_summarize(self, async_client: AsyncTrellis) -> None:
        response = await async_client.transforms.with_raw_response.summarize(
            transform_id="transform_id",
            operation_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transform = await response.parse()
        assert_matches_type(TransformSummarizeResponse, transform, path=["response"])

    @parametrize
    async def test_streaming_response_summarize(self, async_client: AsyncTrellis) -> None:
        async with async_client.transforms.with_streaming_response.summarize(
            transform_id="transform_id",
            operation_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transform = await response.parse()
            assert_matches_type(TransformSummarizeResponse, transform, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_summarize(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `transform_id` but received ''"):
            await async_client.transforms.with_raw_response.summarize(
                transform_id="",
                operation_ids=["string"],
            )

    @parametrize
    async def test_method_wake_up(self, async_client: AsyncTrellis) -> None:
        transform = await async_client.transforms.wake_up()
        assert_matches_type(object, transform, path=["response"])

    @parametrize
    async def test_raw_response_wake_up(self, async_client: AsyncTrellis) -> None:
        response = await async_client.transforms.with_raw_response.wake_up()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        transform = await response.parse()
        assert_matches_type(object, transform, path=["response"])

    @parametrize
    async def test_streaming_response_wake_up(self, async_client: AsyncTrellis) -> None:
        async with async_client.transforms.with_streaming_response.wake_up() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            transform = await response.parse()
            assert_matches_type(object, transform, path=["response"])

        assert cast(Any, response.is_closed) is True
