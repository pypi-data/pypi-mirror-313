# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from trellis import Trellis, AsyncTrellis
from tests.utils import assert_matches_type
from trellis.types.events.subscriptions import EventSubscriptionAction

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestActions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Trellis) -> None:
        action = client.events.subscriptions.actions.create(
            event_subscription_id="event_subscription_id",
            actions=[{"type": "refresh_transform"}],
        )
        assert_matches_type(EventSubscriptionAction, action, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Trellis) -> None:
        response = client.events.subscriptions.actions.with_raw_response.create(
            event_subscription_id="event_subscription_id",
            actions=[{"type": "refresh_transform"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = response.parse()
        assert_matches_type(EventSubscriptionAction, action, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Trellis) -> None:
        with client.events.subscriptions.actions.with_streaming_response.create(
            event_subscription_id="event_subscription_id",
            actions=[{"type": "refresh_transform"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = response.parse()
            assert_matches_type(EventSubscriptionAction, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: Trellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `event_subscription_id` but received ''"):
            client.events.subscriptions.actions.with_raw_response.create(
                event_subscription_id="",
                actions=[{"type": "refresh_transform"}],
            )


class TestAsyncActions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncTrellis) -> None:
        action = await async_client.events.subscriptions.actions.create(
            event_subscription_id="event_subscription_id",
            actions=[{"type": "refresh_transform"}],
        )
        assert_matches_type(EventSubscriptionAction, action, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncTrellis) -> None:
        response = await async_client.events.subscriptions.actions.with_raw_response.create(
            event_subscription_id="event_subscription_id",
            actions=[{"type": "refresh_transform"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        action = await response.parse()
        assert_matches_type(EventSubscriptionAction, action, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncTrellis) -> None:
        async with async_client.events.subscriptions.actions.with_streaming_response.create(
            event_subscription_id="event_subscription_id",
            actions=[{"type": "refresh_transform"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            action = await response.parse()
            assert_matches_type(EventSubscriptionAction, action, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncTrellis) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `event_subscription_id` but received ''"):
            await async_client.events.subscriptions.actions.with_raw_response.create(
                event_subscription_id="",
                actions=[{"type": "refresh_transform"}],
            )
