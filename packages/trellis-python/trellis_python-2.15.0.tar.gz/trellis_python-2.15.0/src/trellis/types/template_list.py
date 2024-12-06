# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["TemplateList", "Data"]


class Data(BaseModel):
    id: str

    description: str

    listing_status: Literal["not_reviewed", "in_review", "approved"]
    """An enumeration."""

    name: str

    proj_id: str

    visibility: Literal["public", "unlisted", "private"]
    """An enumeration."""

    category_ids: Optional[List[str]] = None

    image_url: Optional[str] = None


class TemplateList(BaseModel):
    data: List[Data]

    message: str
