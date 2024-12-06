# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo
from .shared_params.add_column_base import AddColumnBase
from .shared_params.add_column_union import AddColumnUnion

__all__ = [
    "ClientImportRowsParams",
    "AddColumn",
    "AddColumnAddColumnDate",
    "AddColumnAddColumnEditor",
    "AddColumnAddColumnExpression",
    "AddColumnAddColumnFile",
    "AddColumnAddColumnFileConfigFile",
    "AddColumnAddColumnFloat",
    "AddColumnAddColumnFloatConfigNumeric",
    "AddColumnAddColumnInteger",
    "AddColumnAddColumnIntegerConfigNumeric",
    "AddColumnAddColumnReference",
    "AddColumnAddColumnSelect",
    "AddColumnAddColumnSelectConfigSelect",
    "AddColumnAddColumnText",
    "AddColumnAddColumnURL",
    "AddColumnAddColumnUser",
]


class ClientImportRowsParams(TypedDict, total=False):
    database_id: Required[Annotated[str, PropertyInfo(alias="databaseId")]]

    add_columns: Annotated[Iterable[AddColumn], PropertyInfo(alias="addColumns")]
    """Optionally add additional columns to the database during import."""

    creation_block_id: Annotated[str, PropertyInfo(alias="creationBlockId")]

    creation_parent_id: Annotated[str, PropertyInfo(alias="creationParentId")]


class AddColumnAddColumnDate(TypedDict, total=False):
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


class AddColumnAddColumnEditor(TypedDict, total=False):
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


class AddColumnAddColumnExpression(TypedDict, total=False):
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


class AddColumnAddColumnFileConfigFile(TypedDict, total=False):
    allowed_extensions: Annotated[List[str], PropertyInfo(alias="allowedExtensions")]


class AddColumnAddColumnFile(TypedDict, total=False):
    cardinality: Required[Literal["one", "many"]]

    name: Required[str]

    type: Required[Literal["file"]]

    cell_json_schema: Annotated[object, PropertyInfo(alias="cellJsonSchema")]

    config_file: Annotated[AddColumnAddColumnFileConfigFile, PropertyInfo(alias="configFile")]

    enabled_viewers: Annotated[
        List[Literal["code", "html", "image", "molecule", "notebook", "sequence", "smiles", "spreadsheet"]],
        PropertyInfo(alias="enabledViewers"),
    ]

    inline_viewer: Annotated[Literal["molecule2d"], PropertyInfo(alias="inlineViewer")]

    is_required: Annotated[bool, PropertyInfo(alias="isRequired")]

    system_type: Annotated[Literal["name", "bodyDocument"], PropertyInfo(alias="systemType")]


class AddColumnAddColumnFloatConfigNumeric(TypedDict, total=False):
    unit: str


class AddColumnAddColumnFloat(TypedDict, total=False):
    cardinality: Required[Literal["one", "many"]]

    name: Required[str]

    type: Required[Literal["float"]]

    cell_json_schema: Annotated[object, PropertyInfo(alias="cellJsonSchema")]

    config_numeric: Annotated[AddColumnAddColumnFloatConfigNumeric, PropertyInfo(alias="configNumeric")]

    enabled_viewers: Annotated[
        List[Literal["code", "html", "image", "molecule", "notebook", "sequence", "smiles", "spreadsheet"]],
        PropertyInfo(alias="enabledViewers"),
    ]

    inline_viewer: Annotated[Literal["molecule2d"], PropertyInfo(alias="inlineViewer")]

    is_required: Annotated[bool, PropertyInfo(alias="isRequired")]

    system_type: Annotated[Literal["name", "bodyDocument"], PropertyInfo(alias="systemType")]


class AddColumnAddColumnIntegerConfigNumeric(TypedDict, total=False):
    unit: str


class AddColumnAddColumnInteger(TypedDict, total=False):
    cardinality: Required[Literal["one", "many"]]

    name: Required[str]

    type: Required[Literal["integer"]]

    cell_json_schema: Annotated[object, PropertyInfo(alias="cellJsonSchema")]

    config_numeric: Annotated[AddColumnAddColumnIntegerConfigNumeric, PropertyInfo(alias="configNumeric")]

    enabled_viewers: Annotated[
        List[Literal["code", "html", "image", "molecule", "notebook", "sequence", "smiles", "spreadsheet"]],
        PropertyInfo(alias="enabledViewers"),
    ]

    inline_viewer: Annotated[Literal["molecule2d"], PropertyInfo(alias="inlineViewer")]

    is_required: Annotated[bool, PropertyInfo(alias="isRequired")]

    system_type: Annotated[Literal["name", "bodyDocument"], PropertyInfo(alias="systemType")]


class AddColumnAddColumnReference(TypedDict, total=False):
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


class AddColumnAddColumnSelectConfigSelect(TypedDict, total=False):
    options: Required[List[str]]

    can_create: Annotated[bool, PropertyInfo(alias="canCreate")]


class AddColumnAddColumnSelect(TypedDict, total=False):
    cardinality: Required[Literal["one", "many"]]

    config_select: Required[Annotated[AddColumnAddColumnSelectConfigSelect, PropertyInfo(alias="configSelect")]]

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


class AddColumnAddColumnText(TypedDict, total=False):
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


class AddColumnAddColumnURL(TypedDict, total=False):
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


class AddColumnAddColumnUser(TypedDict, total=False):
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


AddColumn: TypeAlias = Union[
    AddColumnBase,
    AddColumnUnion,
    AddColumnAddColumnDate,
    AddColumnAddColumnEditor,
    AddColumnAddColumnExpression,
    AddColumnAddColumnFile,
    AddColumnAddColumnFloat,
    AddColumnAddColumnInteger,
    AddColumnAddColumnReference,
    AddColumnAddColumnSelect,
    AddColumnAddColumnText,
    AddColumnAddColumnURL,
    AddColumnAddColumnUser,
]
