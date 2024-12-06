# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["AssetExtractResponse", "Data"]


class Data(BaseModel):
    asset_id: str

    extraction: str


class AssetExtractResponse(BaseModel):
    data: Data

    message: str
