# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

__all__ = ["TemplateListParams"]


class TemplateListParams(TypedDict, total=False):
    category_id: str
    """Category id (optional)"""

    owned_only: bool
    """Include only templates owned by you.

    If false, only templates from others are included.
    """

    template_ids: List[str]
    """List of template ids (optional). Takes priority over category_id"""
