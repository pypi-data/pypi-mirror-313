# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from ..._models import BaseModel

__all__ = ["CategoryDeleteResponse", "Data"]


class Data(BaseModel):
    is_deleted: bool


class CategoryDeleteResponse(BaseModel):
    data: Data

    message: str
