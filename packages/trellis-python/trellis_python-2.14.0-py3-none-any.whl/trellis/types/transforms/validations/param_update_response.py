# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime

from ...._models import BaseModel

__all__ = ["ParamUpdateResponse", "Data"]


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


class ParamUpdateResponse(BaseModel):
    data: Data
    """Represents a validation parameter in the system.

    Attributes: id (str): The ID of the validation parameter. transform_id (str):
    The ID of the associated transform. validation_name (str | None): The name of
    the validation. validation_rule (str | None): The rule for the validation.
    validation_columns (List[str] | None): The list of columns to be validated.
    validation_endpoint (str | None): The endpoint for the validation.
    """

    message: str
