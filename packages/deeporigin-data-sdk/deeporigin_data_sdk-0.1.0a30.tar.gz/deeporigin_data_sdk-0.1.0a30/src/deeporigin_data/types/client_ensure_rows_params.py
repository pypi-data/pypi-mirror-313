# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ClientEnsureRowsParams", "Row", "RowCell", "RowRow"]


class ClientEnsureRowsParams(TypedDict, total=False):
    database_id: Required[Annotated[str, PropertyInfo(alias="databaseId")]]

    rows: Required[Iterable[Row]]

    check_previous_value: Annotated[bool, PropertyInfo(alias="checkPreviousValue")]


class RowCell(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]
    """The column's name or system ID."""

    value: Required[object]

    previous_version: Annotated[float, PropertyInfo(alias="previousVersion")]
    """The previous version of the cell.

    When `checkPreviousValue` is true, the insertion will atomically ensure an
    incremental update to `previousVersion`.
    """


class RowRow(TypedDict, total=False):
    creation_block_id: Annotated[str, PropertyInfo(alias="creationBlockId")]

    creation_parent_id: Annotated[str, PropertyInfo(alias="creationParentId")]

    is_template: Annotated[bool, PropertyInfo(alias="isTemplate")]


class Row(TypedDict, total=False):
    cells: Iterable[RowCell]

    row: RowRow

    row_id: Annotated[str, PropertyInfo(alias="rowId")]
