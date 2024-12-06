# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ValidationRetrieveParams"]


class ValidationRetrieveParams(TypedDict, total=False):
    precedence: bool

    result_id: str
    """The ID of the result to get the validation for (optional)"""
