# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["TransformUpdateResponse", "Data"]


class Data(BaseModel):
    status: Literal["running", "failed", "completed", "not_started"]
    """An enumeration."""

    transform_id: str


class TransformUpdateResponse(BaseModel):
    data: Data

    message: str
