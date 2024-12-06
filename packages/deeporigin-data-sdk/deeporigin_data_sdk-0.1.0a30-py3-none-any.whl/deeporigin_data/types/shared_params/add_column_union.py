# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["AddColumnUnion"]


class AddColumnUnion(TypedDict, total=False):
    cardinality: Required[Literal["one", "many"]]

    name: Required[str]

    type: Required[Literal["boolean"]]

    cell_json_schema: Annotated[object, PropertyInfo(alias="cellJsonSchema")]

    enabled_viewers: Annotated[
        List[Literal["code", "html", "image", "molecule", "notebook", "sequence", "smiles", "spreadsheet"]],
        PropertyInfo(alias="enabledViewers"),
    ]

    inline_viewer: Annotated[Literal["molecule2d"], PropertyInfo(alias="inlineViewer")]

    is_required: Annotated[bool, PropertyInfo(alias="isRequired")]

    system_type: Annotated[Literal["name", "bodyDocument"], PropertyInfo(alias="systemType")]
