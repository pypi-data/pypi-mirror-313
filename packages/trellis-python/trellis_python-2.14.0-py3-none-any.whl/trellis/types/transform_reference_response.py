# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["TransformReferenceResponse", "Data"]


class Data(BaseModel):
    asset_id: str

    column_name: str

    result_id: str

    page_num: Optional[int] = None

    x_1: Optional[float] = None
    """The x coordinate of the first point. If it does not exist, make it None."""

    x_2: Optional[float] = None
    """The x coordinate of the second point. If it does not exist, make it None."""

    y_1: Optional[float] = None
    """The y coordinate of the first point. If it does not exist, make it None."""

    y_2: Optional[float] = None
    """The y coordinate of the second point. If it does not exist, make it None."""


class TransformReferenceResponse(BaseModel):
    data: List[Data]

    message: str
