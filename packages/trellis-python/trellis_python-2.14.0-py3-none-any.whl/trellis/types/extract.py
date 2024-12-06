# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Extract", "Data"]


class Data(BaseModel):
    asset_id: str

    ext_file_id: str

    ext_file_name: str

    status: Literal["uploaded", "failed_upload", "processing", "not_processed", "processed"]
    """An enumeration."""

    file_type: Optional[str] = None

    url: Optional[str] = None


class Extract(BaseModel):
    data: List[Data]

    message: str
