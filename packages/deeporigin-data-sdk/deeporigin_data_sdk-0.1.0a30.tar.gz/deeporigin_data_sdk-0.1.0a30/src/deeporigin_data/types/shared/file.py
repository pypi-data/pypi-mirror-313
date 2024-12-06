# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["File"]


class File(BaseModel):
    id: str
    """Deep Origin system ID."""

    content_length: float = FieldInfo(alias="contentLength")

    date_created: str = FieldInfo(alias="dateCreated")

    name: str

    status: Literal["ready", "archived"]

    uri: str

    content_type: Optional[str] = FieldInfo(alias="contentType", default=None)

    created_by_user_drn: Optional[str] = FieldInfo(alias="createdByUserDrn", default=None)

    date_updated: Optional[str] = FieldInfo(alias="dateUpdated", default=None)
