# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["TransformDeleteResponse", "Data"]


class Data(BaseModel):
    transform_id: str

    status: Union[Literal["running", "failed", "completed", "not_started"], str, None] = None
    """An enumeration."""


class TransformDeleteResponse(BaseModel):
    data: Data

    message: str
