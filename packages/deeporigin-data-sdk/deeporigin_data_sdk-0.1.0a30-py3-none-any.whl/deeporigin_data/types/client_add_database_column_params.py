# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo
from .shared_params.add_column_base import AddColumnBase
from .shared_params.add_column_union import AddColumnUnion

__all__ = [
    "ClientAddDatabaseColumnParams",
    "Column",
    "ColumnAddColumnDate",
    "ColumnAddColumnEditor",
    "ColumnAddColumnExpression",
    "ColumnAddColumnFile",
    "ColumnAddColumnFileConfigFile",
    "ColumnAddColumnFloat",
    "ColumnAddColumnFloatConfigNumeric",
    "ColumnAddColumnInteger",
    "ColumnAddColumnIntegerConfigNumeric",
    "ColumnAddColumnReference",
    "ColumnAddColumnSelect",
    "ColumnAddColumnSelectConfigSelect",
    "ColumnAddColumnText",
    "ColumnAddColumnURL",
    "ColumnAddColumnUser",
]


class ClientAddDatabaseColumnParams(TypedDict, total=False):
    column: Required[Column]

    database_id: Required[Annotated[str, PropertyInfo(alias="databaseId")]]


class ColumnAddColumnDate(TypedDict, total=False):
    cardinality: Required[Literal["one", "many"]]

    name: Required[str]

    type: Required[Literal["date"]]

    cell_json_schema: Annotated[object, PropertyInfo(alias="cellJsonSchema")]

    enabled_viewers: Annotated[
        List[Literal["code", "html", "image", "molecule", "notebook", "sequence", "smiles", "spreadsheet"]],
        PropertyInfo(alias="enabledViewers"),
    ]

    inline_viewer: Annotated[Literal["molecule2d"], PropertyInfo(alias="inlineViewer")]

    is_required: Annotated[bool, PropertyInfo(alias="isRequired")]

    system_type: Annotated[Literal["name", "bodyDocument"], PropertyInfo(alias="systemType")]


class ColumnAddColumnEditor(TypedDict, total=False):
    cardinality: Required[Literal["one", "many"]]

    name: Required[str]

    type: Required[Literal["editor"]]

    cell_json_schema: Annotated[object, PropertyInfo(alias="cellJsonSchema")]

    enabled_viewers: Annotated[
        List[Literal["code", "html", "image", "molecule", "notebook", "sequence", "smiles", "spreadsheet"]],
        PropertyInfo(alias="enabledViewers"),
    ]

    inline_viewer: Annotated[Literal["molecule2d"], PropertyInfo(alias="inlineViewer")]

    is_required: Annotated[bool, PropertyInfo(alias="isRequired")]

    system_type: Annotated[Literal["name", "bodyDocument"], PropertyInfo(alias="systemType")]


class ColumnAddColumnExpression(TypedDict, total=False):
    cardinality: Required[Literal["one", "many"]]

    expression_code: Required[Annotated[str, PropertyInfo(alias="expressionCode")]]

    expression_return_type: Required[
        Annotated[Literal["text", "float", "integer"], PropertyInfo(alias="expressionReturnType")]
    ]

    name: Required[str]

    type: Required[Literal["expression"]]

    cell_json_schema: Annotated[object, PropertyInfo(alias="cellJsonSchema")]

    enabled_viewers: Annotated[
        List[Literal["code", "html", "image", "molecule", "notebook", "sequence", "smiles", "spreadsheet"]],
        PropertyInfo(alias="enabledViewers"),
    ]

    inline_viewer: Annotated[Literal["molecule2d"], PropertyInfo(alias="inlineViewer")]

    is_required: Annotated[bool, PropertyInfo(alias="isRequired")]

    system_type: Annotated[Literal["name", "bodyDocument"], PropertyInfo(alias="systemType")]


class ColumnAddColumnFileConfigFile(TypedDict, total=False):
    allowed_extensions: Annotated[List[str], PropertyInfo(alias="allowedExtensions")]


class ColumnAddColumnFile(TypedDict, total=False):
    cardinality: Required[Literal["one", "many"]]

    name: Required[str]

    type: Required[Literal["file"]]

    cell_json_schema: Annotated[object, PropertyInfo(alias="cellJsonSchema")]

    config_file: Annotated[ColumnAddColumnFileConfigFile, PropertyInfo(alias="configFile")]

    enabled_viewers: Annotated[
        List[Literal["code", "html", "image", "molecule", "notebook", "sequence", "smiles", "spreadsheet"]],
        PropertyInfo(alias="enabledViewers"),
    ]

    inline_viewer: Annotated[Literal["molecule2d"], PropertyInfo(alias="inlineViewer")]

    is_required: Annotated[bool, PropertyInfo(alias="isRequired")]

    system_type: Annotated[Literal["name", "bodyDocument"], PropertyInfo(alias="systemType")]


class ColumnAddColumnFloatConfigNumeric(TypedDict, total=False):
    unit: str


class ColumnAddColumnFloat(TypedDict, total=False):
    cardinality: Required[Literal["one", "many"]]

    name: Required[str]

    type: Required[Literal["float"]]

    cell_json_schema: Annotated[object, PropertyInfo(alias="cellJsonSchema")]

    config_numeric: Annotated[ColumnAddColumnFloatConfigNumeric, PropertyInfo(alias="configNumeric")]

    enabled_viewers: Annotated[
        List[Literal["code", "html", "image", "molecule", "notebook", "sequence", "smiles", "spreadsheet"]],
        PropertyInfo(alias="enabledViewers"),
    ]

    inline_viewer: Annotated[Literal["molecule2d"], PropertyInfo(alias="inlineViewer")]

    is_required: Annotated[bool, PropertyInfo(alias="isRequired")]

    system_type: Annotated[Literal["name", "bodyDocument"], PropertyInfo(alias="systemType")]


class ColumnAddColumnIntegerConfigNumeric(TypedDict, total=False):
    unit: str


class ColumnAddColumnInteger(TypedDict, total=False):
    cardinality: Required[Literal["one", "many"]]

    name: Required[str]

    type: Required[Literal["integer"]]

    cell_json_schema: Annotated[object, PropertyInfo(alias="cellJsonSchema")]

    config_numeric: Annotated[ColumnAddColumnIntegerConfigNumeric, PropertyInfo(alias="configNumeric")]

    enabled_viewers: Annotated[
        List[Literal["code", "html", "image", "molecule", "notebook", "sequence", "smiles", "spreadsheet"]],
        PropertyInfo(alias="enabledViewers"),
    ]

    inline_viewer: Annotated[Literal["molecule2d"], PropertyInfo(alias="inlineViewer")]

    is_required: Annotated[bool, PropertyInfo(alias="isRequired")]

    system_type: Annotated[Literal["name", "bodyDocument"], PropertyInfo(alias="systemType")]


class ColumnAddColumnReference(TypedDict, total=False):
    cardinality: Required[Literal["one", "many"]]

    name: Required[str]

    reference_database_row_id: Required[Annotated[str, PropertyInfo(alias="referenceDatabaseRowId")]]

    type: Required[Literal["reference"]]

    cell_json_schema: Annotated[object, PropertyInfo(alias="cellJsonSchema")]

    enabled_viewers: Annotated[
        List[Literal["code", "html", "image", "molecule", "notebook", "sequence", "smiles", "spreadsheet"]],
        PropertyInfo(alias="enabledViewers"),
    ]

    inline_viewer: Annotated[Literal["molecule2d"], PropertyInfo(alias="inlineViewer")]

    is_required: Annotated[bool, PropertyInfo(alias="isRequired")]

    system_type: Annotated[Literal["name", "bodyDocument"], PropertyInfo(alias="systemType")]


class ColumnAddColumnSelectConfigSelect(TypedDict, total=False):
    options: Required[List[str]]

    can_create: Annotated[bool, PropertyInfo(alias="canCreate")]


class ColumnAddColumnSelect(TypedDict, total=False):
    cardinality: Required[Literal["one", "many"]]

    config_select: Required[Annotated[ColumnAddColumnSelectConfigSelect, PropertyInfo(alias="configSelect")]]

    name: Required[str]

    type: Required[Literal["select"]]

    cell_json_schema: Annotated[object, PropertyInfo(alias="cellJsonSchema")]

    enabled_viewers: Annotated[
        List[Literal["code", "html", "image", "molecule", "notebook", "sequence", "smiles", "spreadsheet"]],
        PropertyInfo(alias="enabledViewers"),
    ]

    inline_viewer: Annotated[Literal["molecule2d"], PropertyInfo(alias="inlineViewer")]

    is_required: Annotated[bool, PropertyInfo(alias="isRequired")]

    system_type: Annotated[Literal["name", "bodyDocument"], PropertyInfo(alias="systemType")]


class ColumnAddColumnText(TypedDict, total=False):
    cardinality: Required[Literal["one", "many"]]

    name: Required[str]

    type: Required[Literal["text"]]

    cell_json_schema: Annotated[object, PropertyInfo(alias="cellJsonSchema")]

    enabled_viewers: Annotated[
        List[Literal["code", "html", "image", "molecule", "notebook", "sequence", "smiles", "spreadsheet"]],
        PropertyInfo(alias="enabledViewers"),
    ]

    inline_viewer: Annotated[Literal["molecule2d"], PropertyInfo(alias="inlineViewer")]

    is_required: Annotated[bool, PropertyInfo(alias="isRequired")]

    system_type: Annotated[Literal["name", "bodyDocument"], PropertyInfo(alias="systemType")]


class ColumnAddColumnURL(TypedDict, total=False):
    cardinality: Required[Literal["one", "many"]]

    name: Required[str]

    type: Required[Literal["url"]]

    cell_json_schema: Annotated[object, PropertyInfo(alias="cellJsonSchema")]

    enabled_viewers: Annotated[
        List[Literal["code", "html", "image", "molecule", "notebook", "sequence", "smiles", "spreadsheet"]],
        PropertyInfo(alias="enabledViewers"),
    ]

    inline_viewer: Annotated[Literal["molecule2d"], PropertyInfo(alias="inlineViewer")]

    is_required: Annotated[bool, PropertyInfo(alias="isRequired")]

    system_type: Annotated[Literal["name", "bodyDocument"], PropertyInfo(alias="systemType")]


class ColumnAddColumnUser(TypedDict, total=False):
    cardinality: Required[Literal["one", "many"]]

    name: Required[str]

    type: Required[Literal["user"]]

    cell_json_schema: Annotated[object, PropertyInfo(alias="cellJsonSchema")]

    enabled_viewers: Annotated[
        List[Literal["code", "html", "image", "molecule", "notebook", "sequence", "smiles", "spreadsheet"]],
        PropertyInfo(alias="enabledViewers"),
    ]

    inline_viewer: Annotated[Literal["molecule2d"], PropertyInfo(alias="inlineViewer")]

    is_required: Annotated[bool, PropertyInfo(alias="isRequired")]

    system_type: Annotated[Literal["name", "bodyDocument"], PropertyInfo(alias="systemType")]


Column: TypeAlias = Union[
    AddColumnBase,
    AddColumnUnion,
    ColumnAddColumnDate,
    ColumnAddColumnEditor,
    ColumnAddColumnExpression,
    ColumnAddColumnFile,
    ColumnAddColumnFloat,
    ColumnAddColumnInteger,
    ColumnAddColumnReference,
    ColumnAddColumnSelect,
    ColumnAddColumnText,
    ColumnAddColumnURL,
    ColumnAddColumnUser,
]
