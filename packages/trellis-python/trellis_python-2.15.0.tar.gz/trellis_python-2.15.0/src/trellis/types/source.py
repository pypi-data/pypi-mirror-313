# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["Source"]


class Source(BaseModel):
    id: str

    name: str

    proj_id: str

    type: str
