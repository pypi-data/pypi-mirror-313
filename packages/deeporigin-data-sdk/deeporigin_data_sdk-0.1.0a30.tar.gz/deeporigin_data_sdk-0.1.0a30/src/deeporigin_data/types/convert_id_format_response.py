# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["ConvertIDFormatResponse", "Data"]


class Data(BaseModel):
    id: str
    """Deep Origin system ID."""

    hid: str


class ConvertIDFormatResponse(BaseModel):
    data: List[Data]
