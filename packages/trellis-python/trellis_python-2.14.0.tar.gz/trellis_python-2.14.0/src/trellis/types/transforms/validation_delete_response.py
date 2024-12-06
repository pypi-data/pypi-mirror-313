# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from ..._models import BaseModel

__all__ = ["ValidationDeleteResponse", "Data"]


class Data(BaseModel):
    is_deleted: bool


class ValidationDeleteResponse(BaseModel):
    data: Data

    message: str
