# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "ClientListDatabaseRowsParams",
    "ColumnSelection",
    "Filter",
    "FilterRowFilterText",
    "FilterRowFilterNumber",
    "FilterRowFilterBoolean",
    "FilterRowFilterNullity",
    "FilterRowFilterSet",
    "FilterRowFilterSubstructure",
    "RowSort",
]


class ClientListDatabaseRowsParams(TypedDict, total=False):
    database_row_id: Required[Annotated[str, PropertyInfo(alias="databaseRowId")]]

    column_selection: Annotated[ColumnSelection, PropertyInfo(alias="columnSelection")]
    """Select columns for inclusion/exclusion."""

    filter: Filter

    limit: int

    offset: int

    row_sort: Annotated[Iterable[RowSort], PropertyInfo(alias="rowSort")]
    """Sort rows by column."""


class ColumnSelection(TypedDict, total=False):
    exclude: List[str]

    include: List[str]


class FilterRowFilterText(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["text"], PropertyInfo(alias="filterType")]]

    filter_value: Required[Annotated[str, PropertyInfo(alias="filterValue")]]

    operator: Required[Literal["equals", "notEqual", "contains", "notContains", "startsWith", "endsWith"]]


class FilterRowFilterNumber(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["number"], PropertyInfo(alias="filterType")]]

    filter_value: Required[Annotated[float, PropertyInfo(alias="filterValue")]]

    operator: Required[
        Literal["equals", "notEqual", "lessThan", "lessThanOrEqual", "greaterThan", "greaterThanOrEqual"]
    ]


class FilterRowFilterBoolean(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["boolean"], PropertyInfo(alias="filterType")]]

    filter_value: Required[Annotated[bool, PropertyInfo(alias="filterValue")]]

    operator: Required[Literal["equals", "notEqual"]]


class FilterRowFilterNullity(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["nullity"], PropertyInfo(alias="filterType")]]

    operator: Required[Literal["isNull", "isNotNull"]]


class FilterRowFilterSet(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["set"], PropertyInfo(alias="filterType")]]

    operator: Required[Literal["in", "notIn"]]

    values: Required[Iterable[None]]


class FilterRowFilterSubstructure(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["substructure"], PropertyInfo(alias="filterType")]]

    substructure: Required[str]
    """A SMARTS or SMILES string to match against."""


Filter: TypeAlias = Union[
    FilterRowFilterText,
    FilterRowFilterNumber,
    FilterRowFilterBoolean,
    FilterRowFilterNullity,
    FilterRowFilterSet,
    FilterRowFilterSubstructure,
    "RowFilterJoin",
]


class RowSort(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    sort: Required[Literal["asc", "desc"]]


from .shared_params.row_filter_join import RowFilterJoin
