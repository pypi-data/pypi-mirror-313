# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

__all__ = ["TemplateUpdateParams"]


class TemplateUpdateParams(TypedDict, total=False):
    description: Required[str]

    name: Required[str]

    visibility: Required[Literal["public", "unlisted", "private"]]
    """An enumeration."""

    category_ids: List[str]
