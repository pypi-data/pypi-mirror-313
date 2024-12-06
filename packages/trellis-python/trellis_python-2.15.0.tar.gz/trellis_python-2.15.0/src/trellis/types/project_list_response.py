# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["ProjectListResponse", "Data"]


class Data(BaseModel):
    id: str

    asset_count: int

    created_at: datetime

    name: str

    transform_count: int

    updated_at: datetime

    template_id: Optional[str] = None


class ProjectListResponse(BaseModel):
    data: List[Data]

    message: str
