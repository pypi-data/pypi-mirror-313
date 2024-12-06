# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["AssetExtractParams"]


class AssetExtractParams(TypedDict, total=False):
    blocking: bool
    """Whether to block until extraction is complete. Defaults to True."""
