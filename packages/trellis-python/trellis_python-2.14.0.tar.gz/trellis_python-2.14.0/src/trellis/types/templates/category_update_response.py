# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from ..._models import BaseModel

__all__ = ["CategoryUpdateResponse", "Data"]


class Data(BaseModel):
    id: str

    description: str

    name: str


class CategoryUpdateResponse(BaseModel):
    data: Data

    message: str
