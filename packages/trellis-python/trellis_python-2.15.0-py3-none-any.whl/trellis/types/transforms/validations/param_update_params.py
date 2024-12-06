# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

__all__ = ["ParamUpdateParams"]


class ParamUpdateParams(TypedDict, total=False):
    transform_id: Required[str]

    validation_columns: Required[List[str]]
    """The columns to be used in validation"""

    validation_name: Required[str]
    """The name of the validation operation"""

    validation_endpoint: str
    """The URL of the validation API.

    If not provided, the validation_rule will be ran directly.
    """

    validation_rule: str
    """The rules to be applied to the column"""
