# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["AssetListParams"]


class AssetListParams(TypedDict, total=False):
    asset_ids: List[str]
    """List of asset IDs to retrieve."""

    limit: int

    offset: int

    order: Literal["asc", "desc"]
    """An enumeration."""

    order_by: Literal["updated_at", "created_at", "id"]
    """An enumeration."""

    proj_id: str
    """The id of the project."""

    status: Literal["uploaded", "failed_upload", "processing", "not_processed", "processed"]
    """An enumeration."""
