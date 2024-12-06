# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["ProjectListParams"]


class ProjectListParams(TypedDict, total=False):
    limit: int

    offset: int

    order: Literal["asc", "desc"]
    """An enumeration."""

    order_by: Literal["updated_at", "created_at", "id"]
    """An enumeration."""

    proj_ids: List[str]
    """A list of project ids"""

    search_term: str
    """Search term"""
