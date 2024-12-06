# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from ..._compat import PYDANTIC_V2
from ..._models import BaseModel

__all__ = [
    "Condition",
    "RowFilterText",
    "RowFilterNumber",
    "RowFilterBoolean",
    "RowFilterNullity",
    "RowFilterSet",
    "RowFilterSubstructure",
]


class RowFilterText(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    filter_type: Literal["text"] = FieldInfo(alias="filterType")

    filter_value: str = FieldInfo(alias="filterValue")

    operator: Literal["equals", "notEqual", "contains", "notContains", "startsWith", "endsWith"]


class RowFilterNumber(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    filter_type: Literal["number"] = FieldInfo(alias="filterType")

    filter_value: float = FieldInfo(alias="filterValue")

    operator: Literal["equals", "notEqual", "lessThan", "lessThanOrEqual", "greaterThan", "greaterThanOrEqual"]


class RowFilterBoolean(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    filter_type: Literal["boolean"] = FieldInfo(alias="filterType")

    filter_value: bool = FieldInfo(alias="filterValue")

    operator: Literal["equals", "notEqual"]


class RowFilterNullity(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    filter_type: Literal["nullity"] = FieldInfo(alias="filterType")

    operator: Literal["isNull", "isNotNull"]


class RowFilterSet(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    filter_type: Literal["set"] = FieldInfo(alias="filterType")

    operator: Literal["in", "notIn"]

    values: List[None]


class RowFilterSubstructure(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    filter_type: Literal["substructure"] = FieldInfo(alias="filterType")

    substructure: str
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

if PYDANTIC_V2:
    RowFilterText.model_rebuild()
    RowFilterNumber.model_rebuild()
    RowFilterBoolean.model_rebuild()
    RowFilterNullity.model_rebuild()
    RowFilterSet.model_rebuild()
    RowFilterSubstructure.model_rebuild()
else:
    RowFilterText.update_forward_refs()  # type: ignore
    RowFilterNumber.update_forward_refs()  # type: ignore
    RowFilterBoolean.update_forward_refs()  # type: ignore
    RowFilterNullity.update_forward_refs()  # type: ignore
    RowFilterSet.update_forward_refs()  # type: ignore
    RowFilterSubstructure.update_forward_refs()  # type: ignore
