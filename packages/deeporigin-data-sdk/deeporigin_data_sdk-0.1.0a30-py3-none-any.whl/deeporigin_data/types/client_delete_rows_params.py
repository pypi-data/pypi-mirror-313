# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ClientDeleteRowsParams"]


class ClientDeleteRowsParams(TypedDict, total=False):
    database_id: Required[Annotated[str, PropertyInfo(alias="databaseId")]]

    delete_all: Annotated[bool, PropertyInfo(alias="deleteAll")]
    """
    When true, deletes all rows in the table except rows with the specified
    `rowIds`.
    """

    row_ids: Annotated[List[str], PropertyInfo(alias="rowIds")]
    """List of row IDs to delete."""
