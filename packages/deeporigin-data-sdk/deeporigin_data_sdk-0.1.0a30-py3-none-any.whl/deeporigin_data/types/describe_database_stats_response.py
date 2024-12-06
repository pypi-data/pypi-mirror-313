# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["DescribeDatabaseStatsResponse", "Data"]


class Data(BaseModel):
    row_count: float = FieldInfo(alias="rowCount")


class DescribeDatabaseStatsResponse(BaseModel):
    data: Data
