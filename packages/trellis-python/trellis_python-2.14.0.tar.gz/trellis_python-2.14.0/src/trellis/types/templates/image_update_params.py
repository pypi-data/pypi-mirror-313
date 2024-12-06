# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..._types import FileTypes

__all__ = ["ImageUpdateParams"]


class ImageUpdateParams(TypedDict, total=False):
    image: Required[FileTypes]
    """Image file to upload.

    Allowed types are: image/jpeg, image/png, image/webp, image/avif
    """
