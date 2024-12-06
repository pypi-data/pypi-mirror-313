# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

__all__ = ["TransformSummarizeParams"]


class TransformSummarizeParams(TypedDict, total=False):
    operation_ids: Required[List[str]]
    """List of operation IDs to summarize"""

    filters: object
    """Optional filters to apply when summarizing results"""

    prompt_details: str
    """Optional additional details or requirements for the summary"""

    result_ids: List[str]
    """List of result IDs to summarize"""
