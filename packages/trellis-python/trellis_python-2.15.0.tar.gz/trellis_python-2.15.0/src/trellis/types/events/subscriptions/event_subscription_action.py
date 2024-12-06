# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["EventSubscriptionAction", "Data"]


class Data(BaseModel):
    id: str

    created_at: datetime

    type: Literal["refresh_transform", "run_extraction", "send_webhook"]
    """An enumeration."""

    transform_id: Optional[str] = None


class EventSubscriptionAction(BaseModel):
    data: List[Data]

    message: str
