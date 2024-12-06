# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["DataSourceCreateParams", "Credentials"]


class DataSourceCreateParams(TypedDict, total=False):
    credentials: Required[Credentials]

    name: Required[str]

    proj_id: Required[str]

    type: Required[Literal["s3"]]
    """An enumeration."""


class Credentials(TypedDict, total=False):
    access_key: Required[str]

    path: Required[str]

    region: Required[str]

    secret_key: Required[str]

    session_token: Required[str]
