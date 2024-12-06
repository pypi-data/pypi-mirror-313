# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel

__all__ = ["SubscriptionDeleteResponse", "Data"]


class Data(BaseModel):
    ids: List[str]

    is_deleted: bool


class SubscriptionDeleteResponse(BaseModel):
    data: Data

    message: str
