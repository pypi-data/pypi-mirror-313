# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._compat import PYDANTIC_V2
from ..._models import BaseModel

__all__ = ["RowFilterJoin"]


class RowFilterJoin(BaseModel):
    conditions: List["Condition"]

    filter_type: Literal["join"] = FieldInfo(alias="filterType")

    join_type: Literal["and", "or"] = FieldInfo(alias="joinType")


from .condition import Condition

if PYDANTIC_V2:
    RowFilterJoin.model_rebuild()
else:
    RowFilterJoin.update_forward_refs()  # type: ignore
