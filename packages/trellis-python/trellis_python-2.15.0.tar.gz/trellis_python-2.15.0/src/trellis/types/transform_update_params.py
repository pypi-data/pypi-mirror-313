# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

__all__ = ["TransformUpdateParams"]


class TransformUpdateParams(TypedDict, total=False):
    asset_ids: List[str]
    """List of asset ids to refresh."""

    include_reference: bool
