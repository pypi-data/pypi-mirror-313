# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["CustomerUsageParams"]


class CustomerUsageParams(TypedDict, total=False):
    end_date: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """End date (ISO format)"""

    limit: int

    offset: int

    order: Literal["asc", "desc"]
    """An enumeration."""

    order_by: Literal["updated_at", "created_at", "id"]
    """An enumeration."""

    start_date: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """Start date (ISO format)"""
