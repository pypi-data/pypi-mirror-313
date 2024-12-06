# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["TemplateCopyParams"]


class TemplateCopyParams(TypedDict, total=False):
    proj_id: Required[str]

    copy_assets: bool

    copy_transformations: bool
