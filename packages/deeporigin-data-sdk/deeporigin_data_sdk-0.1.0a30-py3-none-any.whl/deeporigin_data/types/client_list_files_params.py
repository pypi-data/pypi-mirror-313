# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ClientListFilesParams", "Filter"]


class ClientListFilesParams(TypedDict, total=False):
    filters: Iterable[Filter]


class Filter(TypedDict, total=False):
    assigned_row_ids: Annotated[List[str], PropertyInfo(alias="assignedRowIds")]

    file_ids: Annotated[List[str], PropertyInfo(alias="fileIds")]

    is_unassigned: Annotated[bool, PropertyInfo(alias="isUnassigned")]

    status: List[Literal["ready", "archived"]]
