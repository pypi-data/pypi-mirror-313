# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from ..._models import BaseModel

__all__ = ["SourceMetadata"]


class SourceMetadata(BaseModel):
    id: str

    created_at: datetime

    file_mod_time: datetime

    file_name: str

    file_path: str

    file_size: str

    source_id: str

    updated_at: datetime
