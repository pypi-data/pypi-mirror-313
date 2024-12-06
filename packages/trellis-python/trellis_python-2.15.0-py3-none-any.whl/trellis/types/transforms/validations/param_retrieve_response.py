# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime

from ...._models import BaseModel

__all__ = ["ParamRetrieveResponse", "Data"]


class Data(BaseModel):
    transform_id: str

    id: Optional[str] = None

    created_at: Optional[datetime] = None

    deleted_at: Optional[datetime] = None

    updated_at: Optional[datetime] = None

    validation_columns: Union[List[str], str, None] = None

    validation_endpoint: Optional[str] = None

    validation_name: Optional[str] = None

    validation_rule: Optional[str] = None


class ParamRetrieveResponse(BaseModel):
    data: List[Data]

    message: str
