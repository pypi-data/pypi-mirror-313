# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["TemplateCopyResponse", "Data"]


class Data(BaseModel):
    id: str

    proj_id: str


class TemplateCopyResponse(BaseModel):
    data: Data

    message: str
