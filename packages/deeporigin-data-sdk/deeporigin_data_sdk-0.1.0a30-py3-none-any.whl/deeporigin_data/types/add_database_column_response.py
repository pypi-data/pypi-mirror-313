# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel
from .shared.database import Database

__all__ = ["AddDatabaseColumnResponse", "Data", "DataColumn"]


class DataColumn:
    pass


class Data(BaseModel):
    column: DataColumn

    database: Database


class AddDatabaseColumnResponse(BaseModel):
    data: Data
