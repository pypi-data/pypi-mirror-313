# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ProjectTransferParams"]


class ProjectTransferParams(TypedDict, total=False):
    to_email: Required[str]

    copy: bool
