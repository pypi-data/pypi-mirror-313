# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from trellis import Trellis, AsyncTrellis
from tests.utils import assert_matches_type
from trellis.types.templates import TemplateImage, ImageDeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestImage:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_update(self, client: Trellis) -> None:
        image = client.templates.image.update(
            template_id="template_id",
            image=b"raw file contents",
        )
        assert_matches_type(TemplateImage, image, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Trellis) -> None:
        response = client.templates.image.with_raw_response.update(
            template_id="template_id",
            image=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        image = response.parse()
        assert_matches_type(TemplateImage, image, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Trellis) -> None:
        with client.templates.image.with_streaming_response.update(
            template_id="template_id",
            image=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            image = response.parse()
            assert_matches_type(TemplateImage, image, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `template_id` but received ''"):
            client.templates.image.with_raw_response.update(
                template_id="",
                image=b"raw file contents",
            )

    @parametrize
    def test_method_delete(self, client: Trellis) -> None:
        image = client.templates.image.delete(
            "template_id",
        )
        assert_matches_type(ImageDeleteResponse, image, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Trellis) -> None:
        response = client.templates.image.with_raw_response.delete(
            "template_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        image = response.parse()
        assert_matches_type(ImageDeleteResponse, image, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Trellis) -> None:
        with client.templates.image.with_streaming_response.delete(
            "template_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            image = response.parse()
            assert_matches_type(ImageDeleteResponse, image, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `template_id` but received ''"):
            client.templates.image.with_raw_response.delete(
                "",
            )


class TestAsyncImage:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_update(self, async_client: AsyncTrellis) -> None:
        image = await async_client.templates.image.update(
            template_id="template_id",
            image=b"raw file contents",
        )
        assert_matches_type(TemplateImage, image, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncTrellis) -> None:
        response = await async_client.templates.image.with_raw_response.update(
            template_id="template_id",
            image=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        image = await response.parse()
        assert_matches_type(TemplateImage, image, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncTrellis) -> None:
        async with async_client.templates.image.with_streaming_response.update(
            template_id="template_id",
            image=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            image = await response.parse()
            assert_matches_type(TemplateImage, image, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `template_id` but received ''"):
            await async_client.templates.image.with_raw_response.update(
                template_id="",
                image=b"raw file contents",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncTrellis) -> None:
        image = await async_client.templates.image.delete(
            "template_id",
        )
        assert_matches_type(ImageDeleteResponse, image, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncTrellis) -> None:
        response = await async_client.templates.image.with_raw_response.delete(
            "template_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        image = await response.parse()
        assert_matches_type(ImageDeleteResponse, image, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncTrellis) -> None:
        async with async_client.templates.image.with_streaming_response.delete(
            "template_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            image = await response.parse()
            assert_matches_type(ImageDeleteResponse, image, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `template_id` but received ''"):
            await async_client.templates.image.with_raw_response.delete(
                "",
            )
