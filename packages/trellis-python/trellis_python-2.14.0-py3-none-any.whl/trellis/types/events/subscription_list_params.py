# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

__all__ = ["SubscriptionListParams"]


class SubscriptionListParams(TypedDict, total=False):
    ids: List[str]
    """(Optional) Filter to only see event subscriptions by ids.

    This takes precedence over proj_id.
    """

    proj_id: str
    """(Optional) Filter to only see events by project id"""
