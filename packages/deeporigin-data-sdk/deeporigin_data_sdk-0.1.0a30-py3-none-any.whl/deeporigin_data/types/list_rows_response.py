# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ListRowsResponse", "Data"]


class Data(BaseModel):
    id: str
    """Deep Origin system ID."""

    hid: str

    type: Literal["database", "row", "workspace"]

    name: Optional[str] = None

    parent_id: Optional[str] = FieldInfo(alias="parentId", default=None)


class ListRowsResponse(BaseModel):
    data: List[Data]
