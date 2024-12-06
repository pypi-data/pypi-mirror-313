# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from trellis import Trellis, AsyncTrellis
from tests.utils import assert_matches_type
from trellis.types import (
    ProjectListResponse,
    ProjectCreateResponse,
    ProjectDeleteResponse,
    ProjectTransferResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestProjects:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Trellis) -> None:
        project = client.projects.create(
            name="name",
        )
        assert_matches_type(ProjectCreateResponse, project, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Trellis) -> None:
        response = client.projects.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = response.parse()
        assert_matches_type(ProjectCreateResponse, project, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Trellis) -> None:
        with client.projects.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = response.parse()
            assert_matches_type(ProjectCreateResponse, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: Trellis) -> None:
        project = client.projects.list()
        assert_matches_type(ProjectListResponse, project, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Trellis) -> None:
        project = client.projects.list(
            limit=0,
            offset=0,
            order="asc",
            order_by="updated_at",
            proj_ids=["string"],
            search_term="search_term",
        )
        assert_matches_type(ProjectListResponse, project, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Trellis) -> None:
        response = client.projects.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = response.parse()
        assert_matches_type(ProjectListResponse, project, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Trellis) -> None:
        with client.projects.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = response.parse()
            assert_matches_type(ProjectListResponse, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Trellis) -> None:
        project = client.projects.delete(
            "proj_id",
        )
        assert_matches_type(ProjectDeleteResponse, project, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Trellis) -> None:
        response = client.projects.with_raw_response.delete(
            "proj_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = response.parse()
        assert_matches_type(ProjectDeleteResponse, project, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Trellis) -> None:
        with client.projects.with_streaming_response.delete(
            "proj_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = response.parse()
            assert_matches_type(ProjectDeleteResponse, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `proj_id` but received ''"):
            client.projects.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_transfer(self, client: Trellis) -> None:
        project = client.projects.transfer(
            proj_id="proj_id",
            to_email="to_email",
        )
        assert_matches_type(ProjectTransferResponse, project, path=["response"])

    @parametrize
    def test_method_transfer_with_all_params(self, client: Trellis) -> None:
        project = client.projects.transfer(
            proj_id="proj_id",
            to_email="to_email",
            copy=True,
        )
        assert_matches_type(ProjectTransferResponse, project, path=["response"])

    @parametrize
    def test_raw_response_transfer(self, client: Trellis) -> None:
        response = client.projects.with_raw_response.transfer(
            proj_id="proj_id",
            to_email="to_email",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = response.parse()
        assert_matches_type(ProjectTransferResponse, project, path=["response"])

    @parametrize
    def test_streaming_response_transfer(self, client: Trellis) -> None:
        with client.projects.with_streaming_response.transfer(
            proj_id="proj_id",
            to_email="to_email",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = response.parse()
            assert_matches_type(ProjectTransferResponse, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_transfer(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `proj_id` but received ''"):
            client.projects.with_raw_response.transfer(
                proj_id="",
                to_email="to_email",
            )


class TestAsyncProjects:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncTrellis) -> None:
        project = await async_client.projects.create(
            name="name",
        )
        assert_matches_type(ProjectCreateResponse, project, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncTrellis) -> None:
        response = await async_client.projects.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = await response.parse()
        assert_matches_type(ProjectCreateResponse, project, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncTrellis) -> None:
        async with async_client.projects.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = await response.parse()
            assert_matches_type(ProjectCreateResponse, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncTrellis) -> None:
        project = await async_client.projects.list()
        assert_matches_type(ProjectListResponse, project, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncTrellis) -> None:
        project = await async_client.projects.list(
            limit=0,
            offset=0,
            order="asc",
            order_by="updated_at",
            proj_ids=["string"],
            search_term="search_term",
        )
        assert_matches_type(ProjectListResponse, project, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncTrellis) -> None:
        response = await async_client.projects.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = await response.parse()
        assert_matches_type(ProjectListResponse, project, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncTrellis) -> None:
        async with async_client.projects.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = await response.parse()
            assert_matches_type(ProjectListResponse, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncTrellis) -> None:
        project = await async_client.projects.delete(
            "proj_id",
        )
        assert_matches_type(ProjectDeleteResponse, project, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncTrellis) -> None:
        response = await async_client.projects.with_raw_response.delete(
            "proj_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = await response.parse()
        assert_matches_type(ProjectDeleteResponse, project, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncTrellis) -> None:
        async with async_client.projects.with_streaming_response.delete(
            "proj_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = await response.parse()
            assert_matches_type(ProjectDeleteResponse, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `proj_id` but received ''"):
            await async_client.projects.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_transfer(self, async_client: AsyncTrellis) -> None:
        project = await async_client.projects.transfer(
            proj_id="proj_id",
            to_email="to_email",
        )
        assert_matches_type(ProjectTransferResponse, project, path=["response"])

    @parametrize
    async def test_method_transfer_with_all_params(self, async_client: AsyncTrellis) -> None:
        project = await async_client.projects.transfer(
            proj_id="proj_id",
            to_email="to_email",
            copy=True,
        )
        assert_matches_type(ProjectTransferResponse, project, path=["response"])

    @parametrize
    async def test_raw_response_transfer(self, async_client: AsyncTrellis) -> None:
        response = await async_client.projects.with_raw_response.transfer(
            proj_id="proj_id",
            to_email="to_email",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        project = await response.parse()
        assert_matches_type(ProjectTransferResponse, project, path=["response"])

    @parametrize
    async def test_streaming_response_transfer(self, async_client: AsyncTrellis) -> None:
        async with async_client.projects.with_streaming_response.transfer(
            proj_id="proj_id",
            to_email="to_email",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            project = await response.parse()
            assert_matches_type(ProjectTransferResponse, project, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_transfer(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `proj_id` but received ''"):
            await async_client.projects.with_raw_response.transfer(
                proj_id="",
                to_email="to_email",
            )
