# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict

from .._models import BaseModel

__all__ = ["TransformSummarizeResponse", "Data"]


class Data(BaseModel):
    summary: Dict[str, str]
    """Dictionary of column_name to column_summary"""


class TransformSummarizeResponse(BaseModel):
    data: Data

    message: str
