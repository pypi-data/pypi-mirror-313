# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from trellis import Trellis, AsyncTrellis
from tests.utils import assert_matches_type
from trellis.types import (
    Template,
    TemplateList,
    TemplateCopyResponse,
    TemplateDeleteResponse,
    TemplateUpdateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTemplates:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Trellis) -> None:
        template = client.templates.create(
            description="description",
            name="name",
            proj_id="proj_id",
            visibility="public",
        )
        assert_matches_type(Template, template, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Trellis) -> None:
        template = client.templates.create(
            description="description",
            name="name",
            proj_id="proj_id",
            visibility="public",
            category_ids=["string"],
        )
        assert_matches_type(Template, template, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Trellis) -> None:
        response = client.templates.with_raw_response.create(
            description="description",
            name="name",
            proj_id="proj_id",
            visibility="public",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        template = response.parse()
        assert_matches_type(Template, template, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Trellis) -> None:
        with client.templates.with_streaming_response.create(
            description="description",
            name="name",
            proj_id="proj_id",
            visibility="public",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            template = response.parse()
            assert_matches_type(Template, template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update(self, client: Trellis) -> None:
        template = client.templates.update(
            template_id="template_id",
            description="description",
            name="name",
            visibility="public",
        )
        assert_matches_type(TemplateUpdateResponse, template, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Trellis) -> None:
        template = client.templates.update(
            template_id="template_id",
            description="description",
            name="name",
            visibility="public",
            category_ids=["string"],
        )
        assert_matches_type(TemplateUpdateResponse, template, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Trellis) -> None:
        response = client.templates.with_raw_response.update(
            template_id="template_id",
            description="description",
            name="name",
            visibility="public",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        template = response.parse()
        assert_matches_type(TemplateUpdateResponse, template, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Trellis) -> None:
        with client.templates.with_streaming_response.update(
            template_id="template_id",
            description="description",
            name="name",
            visibility="public",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            template = response.parse()
            assert_matches_type(TemplateUpdateResponse, template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `template_id` but received ''"):
            client.templates.with_raw_response.update(
                template_id="",
                description="description",
                name="name",
                visibility="public",
            )

    @parametrize
    def test_method_list(self, client: Trellis) -> None:
        template = client.templates.list()
        assert_matches_type(TemplateList, template, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Trellis) -> None:
        template = client.templates.list(
            category_id="category_id",
            owned_only=True,
            template_ids=["string"],
        )
        assert_matches_type(TemplateList, template, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Trellis) -> None:
        response = client.templates.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        template = response.parse()
        assert_matches_type(TemplateList, template, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Trellis) -> None:
        with client.templates.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            template = response.parse()
            assert_matches_type(TemplateList, template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Trellis) -> None:
        template = client.templates.delete(
            "template_id",
        )
        assert_matches_type(TemplateDeleteResponse, template, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Trellis) -> None:
        response = client.templates.with_raw_response.delete(
            "template_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        template = response.parse()
        assert_matches_type(TemplateDeleteResponse, template, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Trellis) -> None:
        with client.templates.with_streaming_response.delete(
            "template_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            template = response.parse()
            assert_matches_type(TemplateDeleteResponse, template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `template_id` but received ''"):
            client.templates.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_copy(self, client: Trellis) -> None:
        template = client.templates.copy(
            template_id="template_id",
            proj_id="proj_id",
        )
        assert_matches_type(TemplateCopyResponse, template, path=["response"])

    @parametrize
    def test_method_copy_with_all_params(self, client: Trellis) -> None:
        template = client.templates.copy(
            template_id="template_id",
            proj_id="proj_id",
            copy_assets=True,
            copy_transformations=True,
        )
        assert_matches_type(TemplateCopyResponse, template, path=["response"])

    @parametrize
    def test_raw_response_copy(self, client: Trellis) -> None:
        response = client.templates.with_raw_response.copy(
            template_id="template_id",
            proj_id="proj_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        template = response.parse()
        assert_matches_type(TemplateCopyResponse, template, path=["response"])

    @parametrize
    def test_streaming_response_copy(self, client: Trellis) -> None:
        with client.templates.with_streaming_response.copy(
            template_id="template_id",
            proj_id="proj_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            template = response.parse()
            assert_matches_type(TemplateCopyResponse, template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_copy(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `template_id` but received ''"):
            client.templates.with_raw_response.copy(
                template_id="",
                proj_id="proj_id",
            )


class TestAsyncTemplates:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncTrellis) -> None:
        template = await async_client.templates.create(
            description="description",
            name="name",
            proj_id="proj_id",
            visibility="public",
        )
        assert_matches_type(Template, template, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncTrellis) -> None:
        template = await async_client.templates.create(
            description="description",
            name="name",
            proj_id="proj_id",
            visibility="public",
            category_ids=["string"],
        )
        assert_matches_type(Template, template, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncTrellis) -> None:
        response = await async_client.templates.with_raw_response.create(
            description="description",
            name="name",
            proj_id="proj_id",
            visibility="public",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        template = await response.parse()
        assert_matches_type(Template, template, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncTrellis) -> None:
        async with async_client.templates.with_streaming_response.create(
            description="description",
            name="name",
            proj_id="proj_id",
            visibility="public",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            template = await response.parse()
            assert_matches_type(Template, template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update(self, async_client: AsyncTrellis) -> None:
        template = await async_client.templates.update(
            template_id="template_id",
            description="description",
            name="name",
            visibility="public",
        )
        assert_matches_type(TemplateUpdateResponse, template, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncTrellis) -> None:
        template = await async_client.templates.update(
            template_id="template_id",
            description="description",
            name="name",
            visibility="public",
            category_ids=["string"],
        )
        assert_matches_type(TemplateUpdateResponse, template, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncTrellis) -> None:
        response = await async_client.templates.with_raw_response.update(
            template_id="template_id",
            description="description",
            name="name",
            visibility="public",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        template = await response.parse()
        assert_matches_type(TemplateUpdateResponse, template, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncTrellis) -> None:
        async with async_client.templates.with_streaming_response.update(
            template_id="template_id",
            description="description",
            name="name",
            visibility="public",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            template = await response.parse()
            assert_matches_type(TemplateUpdateResponse, template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `template_id` but received ''"):
            await async_client.templates.with_raw_response.update(
                template_id="",
                description="description",
                name="name",
                visibility="public",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncTrellis) -> None:
        template = await async_client.templates.list()
        assert_matches_type(TemplateList, template, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncTrellis) -> None:
        template = await async_client.templates.list(
            category_id="category_id",
            owned_only=True,
            template_ids=["string"],
        )
        assert_matches_type(TemplateList, template, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncTrellis) -> None:
        response = await async_client.templates.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        template = await response.parse()
        assert_matches_type(TemplateList, template, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncTrellis) -> None:
        async with async_client.templates.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            template = await response.parse()
            assert_matches_type(TemplateList, template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncTrellis) -> None:
        template = await async_client.templates.delete(
            "template_id",
        )
        assert_matches_type(TemplateDeleteResponse, template, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncTrellis) -> None:
        response = await async_client.templates.with_raw_response.delete(
            "template_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        template = await response.parse()
        assert_matches_type(TemplateDeleteResponse, template, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncTrellis) -> None:
        async with async_client.templates.with_streaming_response.delete(
            "template_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            template = await response.parse()
            assert_matches_type(TemplateDeleteResponse, template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `template_id` but received ''"):
            await async_client.templates.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_copy(self, async_client: AsyncTrellis) -> None:
        template = await async_client.templates.copy(
            template_id="template_id",
            proj_id="proj_id",
        )
        assert_matches_type(TemplateCopyResponse, template, path=["response"])

    @parametrize
    async def test_method_copy_with_all_params(self, async_client: AsyncTrellis) -> None:
        template = await async_client.templates.copy(
            template_id="template_id",
            proj_id="proj_id",
            copy_assets=True,
            copy_transformations=True,
        )
        assert_matches_type(TemplateCopyResponse, template, path=["response"])

    @parametrize
    async def test_raw_response_copy(self, async_client: AsyncTrellis) -> None:
        response = await async_client.templates.with_raw_response.copy(
            template_id="template_id",
            proj_id="proj_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        template = await response.parse()
        assert_matches_type(TemplateCopyResponse, template, path=["response"])

    @parametrize
    async def test_streaming_response_copy(self, async_client: AsyncTrellis) -> None:
        async with async_client.templates.with_streaming_response.copy(
            template_id="template_id",
            proj_id="proj_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            template = await response.parse()
            assert_matches_type(TemplateCopyResponse, template, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_copy(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `template_id` but received ''"):
            await async_client.templates.with_raw_response.copy(
                template_id="",
                proj_id="proj_id",
            )
