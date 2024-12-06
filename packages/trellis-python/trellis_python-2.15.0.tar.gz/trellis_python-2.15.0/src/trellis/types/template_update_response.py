# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["TemplateUpdateResponse", "Data"]


class Data(BaseModel):
    id: str

    description: str

    name: str

    proj_id: str

    visibility: Literal["public", "unlisted", "private"]
    """An enumeration."""


class TemplateUpdateResponse(BaseModel):
    data: Data

    message: str
