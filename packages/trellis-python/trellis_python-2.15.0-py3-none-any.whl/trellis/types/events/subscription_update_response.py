# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["SubscriptionUpdateResponse", "Data"]


class Data(BaseModel):
    id: str

    event_type: Literal["asset_extracted", "asset_uploaded", "transform_completed"]
    """An enumeration."""

    proj_name: str


class SubscriptionUpdateResponse(BaseModel):
    data: Data

    message: str
