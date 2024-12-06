# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["Jobs", "Data"]


class Data(BaseModel):
    id: str

    action_type: Literal["refresh_transform", "run_extraction", "send_webhook"]
    """An enumeration."""

    created_at: datetime

    event_type: Literal["asset_extracted", "asset_uploaded", "transform_completed"]
    """An enumeration."""

    status: Literal["processing", "completed", "failed"]
    """An enumeration."""

    transform_id: Optional[str] = None


class Jobs(BaseModel):
    message: str

    data: Optional[List[Data]] = None
