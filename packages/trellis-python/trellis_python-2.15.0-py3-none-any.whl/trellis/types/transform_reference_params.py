# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["TransformReferenceParams"]


class TransformReferenceParams(TypedDict, total=False):
    transform_id: Required[str]

    column_name: str
    """column name to get reference for"""

    result_id: str
    """result id to get reference for"""
