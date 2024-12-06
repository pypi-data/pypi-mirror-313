# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from ..._utils import PropertyInfo

__all__ = [
    "Condition",
    "RowFilterText",
    "RowFilterNumber",
    "RowFilterBoolean",
    "RowFilterNullity",
    "RowFilterSet",
    "RowFilterSubstructure",
]


class RowFilterText(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["text"], PropertyInfo(alias="filterType")]]

    filter_value: Required[Annotated[str, PropertyInfo(alias="filterValue")]]

    operator: Required[Literal["equals", "notEqual", "contains", "notContains", "startsWith", "endsWith"]]


class RowFilterNumber(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["number"], PropertyInfo(alias="filterType")]]

    filter_value: Required[Annotated[float, PropertyInfo(alias="filterValue")]]

    operator: Required[
        Literal["equals", "notEqual", "lessThan", "lessThanOrEqual", "greaterThan", "greaterThanOrEqual"]
    ]


class RowFilterBoolean(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["boolean"], PropertyInfo(alias="filterType")]]

    filter_value: Required[Annotated[bool, PropertyInfo(alias="filterValue")]]

    operator: Required[Literal["equals", "notEqual"]]


class RowFilterNullity(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["nullity"], PropertyInfo(alias="filterType")]]

    operator: Required[Literal["isNull", "isNotNull"]]


class RowFilterSet(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["set"], PropertyInfo(alias="filterType")]]

    operator: Required[Literal["in", "notIn"]]

    values: Required[Iterable[None]]


class RowFilterSubstructure(TypedDict, total=False):
    column_id: Required[Annotated[str, PropertyInfo(alias="columnId")]]

    filter_type: Required[Annotated[Literal["substructure"], PropertyInfo(alias="filterType")]]

    substructure: Required[str]
    """A SMARTS or SMILES string to match against."""


Condition: TypeAlias = Union[
    RowFilterText,
    RowFilterNumber,
    RowFilterBoolean,
    RowFilterNullity,
    RowFilterSet,
    RowFilterSubstructure,
    "RowFilterJoin",
]

from .row_filter_join import RowFilterJoin
