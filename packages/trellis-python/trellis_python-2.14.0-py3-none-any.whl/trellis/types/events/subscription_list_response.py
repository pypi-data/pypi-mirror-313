# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["SubscriptionListResponse", "Data", "DataAction"]


class DataAction(BaseModel):
    id: str

    created_at: datetime

    type: Literal["refresh_transform", "run_extraction", "send_webhook"]
    """An enumeration."""

    transform_id: Optional[str] = None


class Data(BaseModel):
    id: str

    actions: List[DataAction]

    created_at: datetime

    event_type: Literal["asset_extracted", "asset_uploaded", "transform_completed"]
    """An enumeration."""

    proj_id: str


class SubscriptionListResponse(BaseModel):
    message: str

    data: Optional[List[Data]] = None
