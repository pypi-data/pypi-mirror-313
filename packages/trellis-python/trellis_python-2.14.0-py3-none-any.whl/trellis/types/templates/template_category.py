# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from ..._models import BaseModel

__all__ = ["TemplateCategory", "Data"]


class Data(BaseModel):
    id: str

    description: str

    name: str


class TemplateCategory(BaseModel):
    data: Data

    message: str
