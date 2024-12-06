# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["ProjectTransferResponse", "Data"]


class Data(BaseModel):
    proj_name: Optional[str] = None


class ProjectTransferResponse(BaseModel):
    data: Data

    message: str
