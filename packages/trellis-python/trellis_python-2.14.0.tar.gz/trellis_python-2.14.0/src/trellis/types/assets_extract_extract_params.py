# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["AssetsExtractExtractParams"]


class AssetsExtractExtractParams(TypedDict, total=False):
    asset_ids: List[str]

    parse_strategy: Literal["optimized", "ocr", "xml", "markdown", "advanced_markdown"]
    """Enum representing different parsing strategies.

    Note that OCR and XML will be deprecated soon.
    """

    proj_id: str

    run_on_all_assets: bool
