# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["TemplateImage", "Data"]


class Data(BaseModel):
    template_id: str

    image_url: Optional[str] = None


class TemplateImage(BaseModel):
    data: Data

    message: str
