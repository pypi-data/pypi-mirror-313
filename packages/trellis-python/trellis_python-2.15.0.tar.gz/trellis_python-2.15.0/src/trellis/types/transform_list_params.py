# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["TransformListParams"]


class TransformListParams(TypedDict, total=False):
    include_transform_params: bool
    """Boolean flag to include transform params, which includes the operations."""

    limit: int

    offset: int

    order: Literal["asc", "desc"]
    """An enumeration."""

    order_by: Literal["updated_at", "created_at", "id"]
    """An enumeration."""

    proj_ids: List[str]
    """List of project ids to retrieve transformations from."""

    search_term: str
    """Search term to filter transformations against their id and name."""

    transform_ids: List[str]
    """List of transform IDs to retrieve."""
