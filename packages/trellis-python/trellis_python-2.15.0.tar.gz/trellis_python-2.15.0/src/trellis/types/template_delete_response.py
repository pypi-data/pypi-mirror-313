# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["TemplateDeleteResponse", "Data"]


class Data(BaseModel):
    is_deleted: bool


class TemplateDeleteResponse(BaseModel):
    data: Data

    message: str
