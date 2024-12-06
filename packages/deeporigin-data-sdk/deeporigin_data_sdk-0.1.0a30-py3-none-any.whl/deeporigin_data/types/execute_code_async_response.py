# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ExecuteCodeAsyncResponse", "Data", "DataCodeExecution"]


class DataCodeExecution(BaseModel):
    id: str
    """Deep Origin system ID."""

    status: Literal["pending", "success", "fail"]

    code: Optional[str] = None

    code_language: Optional[Literal["python"]] = FieldInfo(alias="codeLanguage", default=None)

    created_by_user_drn: Optional[str] = FieldInfo(alias="createdByUserDrn", default=None)

    execution_error_message: Optional[str] = FieldInfo(alias="executionErrorMessage", default=None)

    finished_date: Optional[str] = FieldInfo(alias="finishedDate", default=None)

    result_uri: Optional[str] = FieldInfo(alias="resultUri", default=None)

    start_date: Optional[str] = FieldInfo(alias="startDate", default=None)


class Data(BaseModel):
    code_execution: DataCodeExecution = FieldInfo(alias="codeExecution")


class ExecuteCodeAsyncResponse(BaseModel):
    data: Data
