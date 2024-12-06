# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from pydantic import Field as FieldInfo

from ..._utils import PropertyInfo
from ..._models import BaseModel

__all__ = [
    "DatabaseRow",
    "Field",
    "FieldFieldText",
    "FieldFieldTextInvalidData",
    "FieldFieldInteger",
    "FieldFieldIntegerInvalidData",
    "FieldFieldFloat",
    "FieldFieldFloatInvalidData",
    "FieldFieldBoolean",
    "FieldFieldBooleanInvalidData",
    "FieldFieldReference",
    "FieldFieldReferenceInvalidData",
    "FieldFieldReferenceValue",
    "FieldFieldEditor",
    "FieldFieldEditorInvalidData",
    "FieldFieldEditorValue",
    "FieldFieldFile",
    "FieldFieldFileInvalidData",
    "FieldFieldFileValue",
    "FieldFieldSelect",
    "FieldFieldSelectInvalidData",
    "FieldFieldSelectValue",
    "FieldFieldDate",
    "FieldFieldDateInvalidData",
    "FieldFieldURL",
    "FieldFieldURLInvalidData",
    "FieldFieldURLValue",
    "FieldFieldURLValueURL",
    "FieldFieldUser",
    "FieldFieldUserInvalidData",
    "FieldFieldUserValue",
    "FieldFieldExpression",
    "FieldFieldExpressionValue",
    "FieldFieldExpressionInvalidData",
    "FieldFieldLookup",
    "FieldFieldLookupInvalidData",
    "FieldFieldLookupValue",
    "FieldFieldLookupValueFieldText",
    "FieldFieldLookupValueFieldTextInvalidData",
    "FieldFieldLookupValueFieldInteger",
    "FieldFieldLookupValueFieldIntegerInvalidData",
    "FieldFieldLookupValueFieldFloat",
    "FieldFieldLookupValueFieldFloatInvalidData",
    "FieldFieldLookupValueFieldBoolean",
    "FieldFieldLookupValueFieldBooleanInvalidData",
    "FieldFieldLookupValueFieldReference",
    "FieldFieldLookupValueFieldReferenceInvalidData",
    "FieldFieldLookupValueFieldReferenceValue",
    "FieldFieldLookupValueFieldEditor",
    "FieldFieldLookupValueFieldEditorInvalidData",
    "FieldFieldLookupValueFieldEditorValue",
    "FieldFieldLookupValueFieldFile",
    "FieldFieldLookupValueFieldFileInvalidData",
    "FieldFieldLookupValueFieldFileValue",
    "FieldFieldLookupValueFieldSelect",
    "FieldFieldLookupValueFieldSelectInvalidData",
    "FieldFieldLookupValueFieldSelectValue",
    "FieldFieldLookupValueFieldDate",
    "FieldFieldLookupValueFieldDateInvalidData",
    "FieldFieldLookupValueFieldURL",
    "FieldFieldLookupValueFieldURLInvalidData",
    "FieldFieldLookupValueFieldURLValue",
    "FieldFieldLookupValueFieldURLValueURL",
    "FieldFieldLookupValueFieldUser",
    "FieldFieldLookupValueFieldUserInvalidData",
    "FieldFieldLookupValueFieldUserValue",
]


class FieldFieldTextInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldText(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["text"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldTextInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class FieldFieldIntegerInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldInteger(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["integer"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldIntegerInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[int] = None

    version: Optional[float] = None


class FieldFieldFloatInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldFloat(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["float"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldFloatInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[float] = None

    version: Optional[float] = None


class FieldFieldBooleanInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldBoolean(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["boolean"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldBooleanInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[bool] = None

    version: Optional[float] = None


class FieldFieldReferenceInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldReferenceValue(BaseModel):
    row_ids: List[str] = FieldInfo(alias="rowIds")


class FieldFieldReference(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["reference"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldReferenceInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldFieldReferenceValue] = None

    version: Optional[float] = None


class FieldFieldEditorInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldEditorValue(BaseModel):
    top_level_blocks: List[object] = FieldInfo(alias="topLevelBlocks")


class FieldFieldEditor(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["editor"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldEditorInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldFieldEditorValue] = None

    version: Optional[float] = None


class FieldFieldFileInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldFileValue(BaseModel):
    file_ids: List[str] = FieldInfo(alias="fileIds")


class FieldFieldFile(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["file"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldFileInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldFieldFileValue] = None

    version: Optional[float] = None


class FieldFieldSelectInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldSelectValue(BaseModel):
    selected_options: List[str] = FieldInfo(alias="selectedOptions")


class FieldFieldSelect(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["select"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldSelectInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldFieldSelectValue] = None

    version: Optional[float] = None


class FieldFieldDateInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldDate(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["date"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldDateInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class FieldFieldURLInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldURLValueURL(BaseModel):
    url: str

    title: Optional[str] = None


class FieldFieldURLValue(BaseModel):
    urls: List[FieldFieldURLValueURL]


class FieldFieldURL(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["url"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldURLInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldFieldURLValue] = None

    version: Optional[float] = None


class FieldFieldUserInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldUserValue(BaseModel):
    user_drns: List[str] = FieldInfo(alias="userDrns")


class FieldFieldUser(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["user"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldUserInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldFieldUserValue] = None

    version: Optional[float] = None


class FieldFieldExpressionValue(BaseModel):
    error_message: Optional[str] = FieldInfo(alias="errorMessage", default=None)
    """The error message from executing the expression, if one occurred."""

    invalid_result: Optional[object] = FieldInfo(alias="invalidResult", default=None)
    """Expression result that is not a valid return value type."""

    result: Union[str, float, None] = None
    """The return value from executing the expression."""


class FieldFieldExpressionInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldExpression(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["expression"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    value: FieldFieldExpressionValue

    invalid_data: Optional[FieldFieldExpressionInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    version: Optional[float] = None


class FieldFieldLookupInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldLookupValueFieldTextInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldLookupValueFieldText(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["text"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldLookupValueFieldTextInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class FieldFieldLookupValueFieldIntegerInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldLookupValueFieldInteger(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["integer"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldLookupValueFieldIntegerInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[int] = None

    version: Optional[float] = None


class FieldFieldLookupValueFieldFloatInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldLookupValueFieldFloat(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["float"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldLookupValueFieldFloatInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[float] = None

    version: Optional[float] = None


class FieldFieldLookupValueFieldBooleanInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldLookupValueFieldBoolean(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["boolean"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldLookupValueFieldBooleanInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[bool] = None

    version: Optional[float] = None


class FieldFieldLookupValueFieldReferenceInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldLookupValueFieldReferenceValue(BaseModel):
    row_ids: List[str] = FieldInfo(alias="rowIds")


class FieldFieldLookupValueFieldReference(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["reference"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldLookupValueFieldReferenceInvalidData] = FieldInfo(
        alias="invalidData", default=None
    )

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldFieldLookupValueFieldReferenceValue] = None

    version: Optional[float] = None


class FieldFieldLookupValueFieldEditorInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldLookupValueFieldEditorValue(BaseModel):
    top_level_blocks: List[object] = FieldInfo(alias="topLevelBlocks")


class FieldFieldLookupValueFieldEditor(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["editor"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldLookupValueFieldEditorInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldFieldLookupValueFieldEditorValue] = None

    version: Optional[float] = None


class FieldFieldLookupValueFieldFileInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldLookupValueFieldFileValue(BaseModel):
    file_ids: List[str] = FieldInfo(alias="fileIds")


class FieldFieldLookupValueFieldFile(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["file"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldLookupValueFieldFileInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldFieldLookupValueFieldFileValue] = None

    version: Optional[float] = None


class FieldFieldLookupValueFieldSelectInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldLookupValueFieldSelectValue(BaseModel):
    selected_options: List[str] = FieldInfo(alias="selectedOptions")


class FieldFieldLookupValueFieldSelect(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["select"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldLookupValueFieldSelectInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldFieldLookupValueFieldSelectValue] = None

    version: Optional[float] = None


class FieldFieldLookupValueFieldDateInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldLookupValueFieldDate(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["date"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldLookupValueFieldDateInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[str] = None

    version: Optional[float] = None


class FieldFieldLookupValueFieldURLInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldLookupValueFieldURLValueURL(BaseModel):
    url: str

    title: Optional[str] = None


class FieldFieldLookupValueFieldURLValue(BaseModel):
    urls: List[FieldFieldLookupValueFieldURLValueURL]


class FieldFieldLookupValueFieldURL(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["url"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldLookupValueFieldURLInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldFieldLookupValueFieldURLValue] = None

    version: Optional[float] = None


class FieldFieldLookupValueFieldUserInvalidData(BaseModel):
    message: Optional[str] = None


class FieldFieldLookupValueFieldUserValue(BaseModel):
    user_drns: List[str] = FieldInfo(alias="userDrns")


class FieldFieldLookupValueFieldUser(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["user"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldLookupValueFieldUserInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldFieldLookupValueFieldUserValue] = None

    version: Optional[float] = None


FieldFieldLookupValue: TypeAlias = Union[
    FieldFieldLookupValueFieldText,
    FieldFieldLookupValueFieldInteger,
    FieldFieldLookupValueFieldFloat,
    FieldFieldLookupValueFieldBoolean,
    FieldFieldLookupValueFieldReference,
    FieldFieldLookupValueFieldEditor,
    FieldFieldLookupValueFieldFile,
    FieldFieldLookupValueFieldSelect,
    FieldFieldLookupValueFieldDate,
    FieldFieldLookupValueFieldURL,
    FieldFieldLookupValueFieldUser,
]


class FieldFieldLookup(BaseModel):
    column_id: str = FieldInfo(alias="columnId")

    type: Literal["lookup"]

    validation_status: Literal["valid", "invalid"] = FieldInfo(alias="validationStatus")

    invalid_data: Optional[FieldFieldLookupInvalidData] = FieldInfo(alias="invalidData", default=None)

    system_type: Optional[Literal["name", "bodyDocument"]] = FieldInfo(alias="systemType", default=None)

    value: Optional[FieldFieldLookupValue] = None

    version: Optional[float] = None


Field: TypeAlias = Annotated[
    Union[
        FieldFieldText,
        FieldFieldInteger,
        FieldFieldFloat,
        FieldFieldBoolean,
        FieldFieldReference,
        FieldFieldEditor,
        FieldFieldFile,
        FieldFieldSelect,
        FieldFieldDate,
        FieldFieldURL,
        FieldFieldUser,
        FieldFieldExpression,
        FieldFieldLookup,
    ],
    PropertyInfo(discriminator="type"),
]


class DatabaseRow(BaseModel):
    id: str
    """Deep Origin system ID."""

    date_created: str = FieldInfo(alias="dateCreated")

    hid: str

    type: Literal["row"]

    created_by_user_drn: Optional[str] = FieldInfo(alias="createdByUserDrn", default=None)

    creation_block_id: Optional[str] = FieldInfo(alias="creationBlockId", default=None)

    creation_parent_id: Optional[str] = FieldInfo(alias="creationParentId", default=None)

    date_updated: Optional[str] = FieldInfo(alias="dateUpdated", default=None)

    edited_by_user_drn: Optional[str] = FieldInfo(alias="editedByUserDrn", default=None)

    fields: Optional[List[Field]] = None

    is_template: Optional[bool] = FieldInfo(alias="isTemplate", default=None)

    name: Optional[str] = None

    parent_hid: Optional[str] = FieldInfo(alias="parentHid", default=None)

    parent_id: Optional[str] = FieldInfo(alias="parentId", default=None)

    validation_status: Optional[Literal["valid", "invalid"]] = FieldInfo(alias="validationStatus", default=None)
