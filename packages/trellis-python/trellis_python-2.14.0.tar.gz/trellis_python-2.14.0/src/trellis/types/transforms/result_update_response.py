# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ResultUpdateResponse"]


class ResultUpdateResponse(BaseModel):
    message: str

    data: Union[Literal[False], object, None] = None
