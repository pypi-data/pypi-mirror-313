# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["SubscriptionUpdateParams"]


class SubscriptionUpdateParams(TypedDict, total=False):
    event_type: Required[Literal["asset_extracted", "asset_uploaded", "transform_completed"]]
    """An enumeration."""

    proj_id: str
    """Project ID for the event subscription.

    Either `proj_id` or `transform_id` must be present, but not both.
    """

    transform_id: str
    """Transformation ID for the event subscription.

    Either `proj_id` or `transform_id` must be present, but not both.
    """
