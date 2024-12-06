# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .shared.file import File

__all__ = ["ListFilesResponse", "Data", "DataAssignment"]


class DataAssignment(BaseModel):
    row_id: str = FieldInfo(alias="rowId")


class Data(BaseModel):
    file: File

    assignments: Optional[List[DataAssignment]] = None


class ListFilesResponse(BaseModel):
    data: List[Data]
