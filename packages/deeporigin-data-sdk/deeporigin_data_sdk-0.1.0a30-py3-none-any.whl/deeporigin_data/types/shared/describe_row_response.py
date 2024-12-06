# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from .database import Database
from ..._models import BaseModel
from .workspace import Workspace
from .database_row import DatabaseRow

__all__ = ["DescribeRowResponse", "Data"]

Data: TypeAlias = Annotated[Union[Database, DatabaseRow, Workspace], PropertyInfo(discriminator="type")]


class DescribeRowResponse(BaseModel):
    data: Data
