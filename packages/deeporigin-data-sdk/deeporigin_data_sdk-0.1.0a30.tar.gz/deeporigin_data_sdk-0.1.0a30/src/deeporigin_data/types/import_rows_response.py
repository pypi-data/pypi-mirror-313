# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from pydantic import Field as FieldInfo

from .._models import BaseModel
from .shared.database import Database

__all__ = ["ImportRowsResponse", "Data"]


class Data(BaseModel):
    database: Database

    import_row_count: float = FieldInfo(alias="importRowCount")


class ImportRowsResponse(BaseModel):
    data: Data
