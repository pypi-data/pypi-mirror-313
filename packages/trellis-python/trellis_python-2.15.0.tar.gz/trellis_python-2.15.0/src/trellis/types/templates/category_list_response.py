# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel

__all__ = ["CategoryListResponse", "Data"]


class Data(BaseModel):
    id: str

    description: str

    name: str


class CategoryListResponse(BaseModel):
    data: List[Data]

    message: str
