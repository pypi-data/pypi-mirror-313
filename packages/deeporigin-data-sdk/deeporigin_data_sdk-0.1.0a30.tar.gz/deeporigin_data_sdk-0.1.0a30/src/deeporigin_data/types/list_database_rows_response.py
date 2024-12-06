# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .shared.database_row import DatabaseRow

__all__ = ["ListDatabaseRowsResponse"]


class ListDatabaseRowsResponse(BaseModel):
    data: List[DatabaseRow]
