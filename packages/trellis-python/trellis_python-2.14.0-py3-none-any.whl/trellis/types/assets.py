# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["Assets", "Data", "Metadata"]


class Data(BaseModel):
    asset_id: str

    created_at: datetime

    status: Literal["uploaded", "failed_upload", "processing", "not_processed", "processed"]
    """An enumeration."""

    ext_file_id: Optional[str] = None

    ext_file_name: Optional[str] = None

    file_type: Optional[str] = None

    proj_id: Optional[str] = None

    url: Optional[str] = None


class Metadata(BaseModel):
    total_filtered_results_count: int

    total_results_count: int


class Assets(BaseModel):
    data: List[Data]

    message: str

    metadata: Optional[Metadata] = None
