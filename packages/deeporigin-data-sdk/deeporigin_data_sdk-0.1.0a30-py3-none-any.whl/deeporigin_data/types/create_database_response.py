# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel
from .shared.database import Database

__all__ = ["CreateDatabaseResponse"]


class CreateDatabaseResponse(BaseModel):
    data: Database
