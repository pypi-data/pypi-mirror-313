# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["ListRowBackReferencesResponse", "Data", "DataRow"]


class DataRow:
    pass


class Data(BaseModel):
    rows: List[DataRow]


class ListRowBackReferencesResponse(BaseModel):
    data: Data
