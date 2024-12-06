# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["TransformAutoschemaResponse", "Data", "DataOperation", "Metadata"]


class DataOperation(BaseModel):
    column_name: str
    """Name of the column to be transformed.

    Any alphanumeric characters are allowed. Must be unique.
    """

    column_type: Literal[
        "text", "integer", "numeric", "boolean", "list", "object", "string", "number", "time", "date", "text[]", "jsonb"
    ]
    """An enumeration."""

    task_description: str
    """Description of the task to be performed"""

    transform_type: Literal["extraction", "classification", "generation", "manual"]
    """An enumeration."""

    default_value: Optional[object] = None
    """
    The default value to use if has_default is true and no value is found in the
    document. The value you should return is stored under the 'value' key.
    """

    has_default: Optional[bool] = None
    """If true, use the default value specified in default_value.

    If false, return null if no value found.
    """

    operations: Optional[List[object]] = None
    """Required when column_type is `object` or `list`.

    Defines the structure of object or list operations. If column_type is `list`,
    then operations should only be of length 1 since `list` can only be of one type.
    If column_type is `object`, then operations can be longer of length one (and
    optionally be nested.)
    """

    output_values: Optional[Dict[str, str]] = None
    """NOTE: only valid with classification tasks.

    Output values of the transformation operation.
    """


class Data(BaseModel):
    column_name: str
    """Name of the column to be transformed.

    Any alphanumeric characters are allowed. Must be unique.
    """

    column_type: Literal[
        "text", "integer", "numeric", "boolean", "list", "object", "string", "number", "time", "date", "text[]", "jsonb"
    ]
    """An enumeration."""

    task_description: str
    """Description of the task to be performed"""

    transform_type: Literal["extraction", "classification", "generation", "manual"]
    """An enumeration."""

    id: Optional[str] = None

    default_value: Optional[object] = None
    """
    The default value to use if has_default is true and no value is found in the
    document. The value you should return is stored under the 'value' key.
    """

    has_default: Optional[bool] = None
    """If true, use the default value specified in default_value.

    If false, return null if no value found.
    """

    operations: Optional[List[DataOperation]] = None
    """Required when column_type is `object` or `list`.

    Defines the structure of object or list operations. If column_type is `list`,
    then operations should only be of length 1 since `list` can only be of one type.
    If column_type is `object`, then operations can be longer of length one (and
    optionally be nested.)
    """

    output_values: Optional[Dict[str, str]] = None
    """NOTE: only valid with classification tasks.

    Output values of the transformation operation.
    """


class Metadata(BaseModel):
    total_generated: int


class TransformAutoschemaResponse(BaseModel):
    data: List[Data]

    message: str

    metadata: Metadata
