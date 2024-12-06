# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["TransformCreateParams", "TransformParams", "TransformParamsOperation", "TransformParamsTablePreferences"]


class TransformCreateParams(TypedDict, total=False):
    proj_id: Required[str]

    transform_params: Required[TransformParams]

    transform_name: str
    """
    The transform_name parameter is an optional parameter that provides a
    human-readable name or description for the transformation, which can be useful
    for identifying and referencing transformations. If provided, the transform_name
    parameter should be a string. If not provided, the value of transform_name will
    be None.
    """


class TransformParamsOperation(TypedDict, total=False):
    column_name: Required[str]
    """Name of the column to be transformed.

    Any alphanumeric characters are allowed. Must be unique.
    """

    column_type: Required[
        Literal[
            "text",
            "integer",
            "numeric",
            "boolean",
            "list",
            "object",
            "string",
            "number",
            "time",
            "date",
            "text[]",
            "jsonb",
        ]
    ]
    """An enumeration."""

    task_description: Required[str]
    """Description of the task to be performed"""

    transform_type: Required[Literal["extraction", "classification", "generation", "manual"]]
    """An enumeration."""

    default_value: object
    """
    The default value to use if has_default is true and no value is found in the
    document. The value you should return is stored under the 'value' key.
    """

    has_default: bool
    """If true, use the default value specified in default_value.

    If false, return null if no value found.
    """

    operations: Iterable[object]
    """Required when column_type is `object` or `list`.

    Defines the structure of object or list operations. If column_type is `list`,
    then operations should only be of length 1 since `list` can only be of one type.
    If column_type is `object`, then operations can be longer of length one (and
    optionally be nested.)
    """

    output_values: Dict[str, str]
    """NOTE: only valid with classification tasks.

    Output values of the transformation operation.
    """


class TransformParamsTablePreferences(TypedDict, total=False):
    advanced_reasoning: bool
    """Using advanced reasoning when extracting rows from the tables.

    Transformation becomes slower and more computationally intensive
    """

    included_table_names: List[str]
    """Parameter that specifies the table names to be included for table transforms."""


class TransformParams(TypedDict, total=False):
    model: Required[str]
    """The model to be used for the transformation.

    Must be one of 'trellis-scale', 'trellis-premium', or 'trellis-vertix'
    """

    mode: str
    """The mode to be used for the transformation.

    Must be one of 'document' or 'table'
    """

    operations: Iterable[TransformParamsOperation]

    table_preferences: TransformParamsTablePreferences
    """Applicable for table transform mode only.

    Optional parameter that specifies the table names to be included for table
    transforms.
    """
