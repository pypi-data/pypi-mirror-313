# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = [
    "TransformListResponse",
    "GetTransformsWithTransformParamsResponse",
    "GetTransformsWithTransformParamsResponseData",
    "GetTransformsWithTransformParamsResponseDataParams",
    "GetTransformsResponse",
    "GetTransformsResponseData",
]


class GetTransformsWithTransformParamsResponseDataParams(BaseModel):
    transform_params: object


class GetTransformsWithTransformParamsResponseData(BaseModel):
    id: str

    created_at: datetime

    params: GetTransformsWithTransformParamsResponseDataParams

    proj_id: str

    status: Literal["running", "failed", "completed", "not_started"]
    """An enumeration."""

    updated_at: datetime

    last_ran_at: Optional[datetime] = None

    name: Optional[str] = None


class GetTransformsWithTransformParamsResponse(BaseModel):
    data: List[GetTransformsWithTransformParamsResponseData]

    message: str


class GetTransformsResponseData(BaseModel):
    id: str

    created_at: datetime

    proj_id: str

    status: Literal["running", "failed", "completed", "not_started"]
    """An enumeration."""

    updated_at: datetime

    last_ran_at: Optional[datetime] = None

    name: Optional[str] = None


class GetTransformsResponse(BaseModel):
    data: List[GetTransformsResponseData]

    message: str


TransformListResponse: TypeAlias = Union[GetTransformsWithTransformParamsResponse, GetTransformsResponse]
