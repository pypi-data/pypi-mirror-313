# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["RowFilterJoin"]


class RowFilterJoin(TypedDict, total=False):
    conditions: Required[Iterable["Condition"]]

    filter_type: Required[Annotated[Literal["join"], PropertyInfo(alias="filterType")]]

    join_type: Required[Annotated[Literal["and", "or"], PropertyInfo(alias="joinType")]]


from .condition import Condition
