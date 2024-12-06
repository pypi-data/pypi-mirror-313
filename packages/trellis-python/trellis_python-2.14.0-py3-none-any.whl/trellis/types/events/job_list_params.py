# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["JobListParams"]


class JobListParams(TypedDict, total=False):
    status: Literal["processing", "completed", "failed"]
    """An enumeration."""
