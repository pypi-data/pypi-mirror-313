# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["ValidationUpdateResponse", "Data"]


class Data(BaseModel):
    id: str

    created_at: datetime

    result_id: str

    transform_id: str

    deleted_at: Optional[datetime] = None

    overridden_by: Optional[str] = None

    result: Optional[bool] = None

    validation_columns: Optional[List[str]] = None

    validation_endpoint: Optional[str] = None

    validation_name: Optional[str] = None

    validation_param_id: Optional[str] = None

    validation_rule: Optional[str] = None


class ValidationUpdateResponse(BaseModel):
    data: Data

    message: str
