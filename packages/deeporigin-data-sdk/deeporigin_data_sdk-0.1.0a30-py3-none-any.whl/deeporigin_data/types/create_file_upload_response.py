# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from pydantic import Field as FieldInfo

from .._models import BaseModel
from .shared.file import File

__all__ = ["CreateFileUploadResponse", "Data"]


class Data(BaseModel):
    file: File

    upload_url: str = FieldInfo(alias="uploadUrl")


class CreateFileUploadResponse(BaseModel):
    data: Data
