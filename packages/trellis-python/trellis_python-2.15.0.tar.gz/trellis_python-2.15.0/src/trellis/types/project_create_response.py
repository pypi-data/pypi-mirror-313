# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["ProjectCreateResponse", "Data"]


class Data(BaseModel):
    proj_id: str


class ProjectCreateResponse(BaseModel):
    data: Data

    message: str
