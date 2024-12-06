# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "ClientListRowsParams",
    "Filter",
    "FilterParent",
    "FilterParentParent",
    "FilterParentParentID",
    "FilterParentParentIsRoot",
    "FilterRowType",
    "FilterIsInlineDatabase",
]


class ClientListRowsParams(TypedDict, total=False):
    filters: Required[Iterable[Filter]]


class FilterParentParentID(TypedDict, total=False):
    id: Required[str]


class FilterParentParentIsRoot(TypedDict, total=False):
    is_root: Required[Annotated[bool, PropertyInfo(alias="isRoot")]]


FilterParentParent: TypeAlias = Union[FilterParentParentID, FilterParentParentIsRoot]


class FilterParent(TypedDict, total=False):
    parent: Required[FilterParentParent]


class FilterRowType(TypedDict, total=False):
    row_type: Required[Annotated[str, PropertyInfo(alias="rowType")]]


class FilterIsInlineDatabase(TypedDict, total=False):
    is_inline_database: Required[Annotated[bool, PropertyInfo(alias="isInlineDatabase")]]


Filter: TypeAlias = Union[FilterParent, FilterRowType, FilterIsInlineDatabase]
