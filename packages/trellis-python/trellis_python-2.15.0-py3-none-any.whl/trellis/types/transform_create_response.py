# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["TransformCreateResponse", "Data"]


class Data(BaseModel):
    transform_id: str


class TransformCreateResponse(BaseModel):
    data: Data

    message: str
