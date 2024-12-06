# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from trellis import Trellis, AsyncTrellis
from tests.utils import assert_matches_type
from trellis.types.events import (
    EventSubscription,
    SubscriptionListResponse,
    SubscriptionDeleteResponse,
    SubscriptionUpdateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSubscriptions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Trellis) -> None:
        subscription = client.events.subscriptions.create(
            event_type="asset_extracted",
        )
        assert_matches_type(EventSubscription, subscription, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Trellis) -> None:
        subscription = client.events.subscriptions.create(
            event_type="asset_extracted",
            proj_id="proj_id",
            transform_id="transform_id",
        )
        assert_matches_type(EventSubscription, subscription, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Trellis) -> None:
        response = client.events.subscriptions.with_raw_response.create(
            event_type="asset_extracted",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = response.parse()
        assert_matches_type(EventSubscription, subscription, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Trellis) -> None:
        with client.events.subscriptions.with_streaming_response.create(
            event_type="asset_extracted",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = response.parse()
            assert_matches_type(EventSubscription, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update(self, client: Trellis) -> None:
        subscription = client.events.subscriptions.update(
            event_subscription_id="event_subscription_id",
            event_type="asset_extracted",
        )
        assert_matches_type(SubscriptionUpdateResponse, subscription, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Trellis) -> None:
        subscription = client.events.subscriptions.update(
            event_subscription_id="event_subscription_id",
            event_type="asset_extracted",
            proj_id="proj_id",
            transform_id="transform_id",
        )
        assert_matches_type(SubscriptionUpdateResponse, subscription, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Trellis) -> None:
        response = client.events.subscriptions.with_raw_response.update(
            event_subscription_id="event_subscription_id",
            event_type="asset_extracted",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = response.parse()
        assert_matches_type(SubscriptionUpdateResponse, subscription, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Trellis) -> None:
        with client.events.subscriptions.with_streaming_response.update(
            event_subscription_id="event_subscription_id",
            event_type="asset_extracted",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = response.parse()
            assert_matches_type(SubscriptionUpdateResponse, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `event_subscription_id` but received ''"):
            client.events.subscriptions.with_raw_response.update(
                event_subscription_id="",
                event_type="asset_extracted",
            )

    @parametrize
    def test_method_list(self, client: Trellis) -> None:
        subscription = client.events.subscriptions.list()
        assert_matches_type(SubscriptionListResponse, subscription, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Trellis) -> None:
        subscription = client.events.subscriptions.list(
            ids=["string"],
            proj_id="proj_id",
        )
        assert_matches_type(SubscriptionListResponse, subscription, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Trellis) -> None:
        response = client.events.subscriptions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = response.parse()
        assert_matches_type(SubscriptionListResponse, subscription, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Trellis) -> None:
        with client.events.subscriptions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = response.parse()
            assert_matches_type(SubscriptionListResponse, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Trellis) -> None:
        subscription = client.events.subscriptions.delete()
        assert_matches_type(SubscriptionDeleteResponse, subscription, path=["response"])

    @parametrize
    def test_method_delete_with_all_params(self, client: Trellis) -> None:
        subscription = client.events.subscriptions.delete(
            ids=["string"],
        )
        assert_matches_type(SubscriptionDeleteResponse, subscription, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Trellis) -> None:
        response = client.events.subscriptions.with_raw_response.delete()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = response.parse()
        assert_matches_type(SubscriptionDeleteResponse, subscription, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Trellis) -> None:
        with client.events.subscriptions.with_streaming_response.delete() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = response.parse()
            assert_matches_type(SubscriptionDeleteResponse, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSubscriptions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncTrellis) -> None:
        subscription = await async_client.events.subscriptions.create(
            event_type="asset_extracted",
        )
        assert_matches_type(EventSubscription, subscription, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncTrellis) -> None:
        subscription = await async_client.events.subscriptions.create(
            event_type="asset_extracted",
            proj_id="proj_id",
            transform_id="transform_id",
        )
        assert_matches_type(EventSubscription, subscription, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncTrellis) -> None:
        response = await async_client.events.subscriptions.with_raw_response.create(
            event_type="asset_extracted",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = await response.parse()
        assert_matches_type(EventSubscription, subscription, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncTrellis) -> None:
        async with async_client.events.subscriptions.with_streaming_response.create(
            event_type="asset_extracted",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = await response.parse()
            assert_matches_type(EventSubscription, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update(self, async_client: AsyncTrellis) -> None:
        subscription = await async_client.events.subscriptions.update(
            event_subscription_id="event_subscription_id",
            event_type="asset_extracted",
        )
        assert_matches_type(SubscriptionUpdateResponse, subscription, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncTrellis) -> None:
        subscription = await async_client.events.subscriptions.update(
            event_subscription_id="event_subscription_id",
            event_type="asset_extracted",
            proj_id="proj_id",
            transform_id="transform_id",
        )
        assert_matches_type(SubscriptionUpdateResponse, subscription, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncTrellis) -> None:
        response = await async_client.events.subscriptions.with_raw_response.update(
            event_subscription_id="event_subscription_id",
            event_type="asset_extracted",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = await response.parse()
        assert_matches_type(SubscriptionUpdateResponse, subscription, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncTrellis) -> None:
        async with async_client.events.subscriptions.with_streaming_response.update(
            event_subscription_id="event_subscription_id",
            event_type="asset_extracted",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = await response.parse()
            assert_matches_type(SubscriptionUpdateResponse, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `event_subscription_id` but received ''"):
            await async_client.events.subscriptions.with_raw_response.update(
                event_subscription_id="",
                event_type="asset_extracted",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncTrellis) -> None:
        subscription = await async_client.events.subscriptions.list()
        assert_matches_type(SubscriptionListResponse, subscription, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncTrellis) -> None:
        subscription = await async_client.events.subscriptions.list(
            ids=["string"],
            proj_id="proj_id",
        )
        assert_matches_type(SubscriptionListResponse, subscription, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncTrellis) -> None:
        response = await async_client.events.subscriptions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = await response.parse()
        assert_matches_type(SubscriptionListResponse, subscription, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncTrellis) -> None:
        async with async_client.events.subscriptions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = await response.parse()
            assert_matches_type(SubscriptionListResponse, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncTrellis) -> None:
        subscription = await async_client.events.subscriptions.delete()
        assert_matches_type(SubscriptionDeleteResponse, subscription, path=["response"])

    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncTrellis) -> None:
        subscription = await async_client.events.subscriptions.delete(
            ids=["string"],
        )
        assert_matches_type(SubscriptionDeleteResponse, subscription, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncTrellis) -> None:
        response = await async_client.events.subscriptions.with_raw_response.delete()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        subscription = await response.parse()
        assert_matches_type(SubscriptionDeleteResponse, subscription, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncTrellis) -> None:
        async with async_client.events.subscriptions.with_streaming_response.delete() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            subscription = await response.parse()
            assert_matches_type(SubscriptionDeleteResponse, subscription, path=["response"])

        assert cast(Any, response.is_closed) is True
