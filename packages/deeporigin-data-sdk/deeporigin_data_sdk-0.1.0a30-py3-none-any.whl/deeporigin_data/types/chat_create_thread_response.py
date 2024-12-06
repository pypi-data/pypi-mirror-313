# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ChatCreateThreadResponse", "Data", "DataChatThread"]


class DataChatThread(BaseModel):
    id: str
    """Deep Origin system ID."""

    created_at: str = FieldInfo(alias="createdAt")

    openai_id: str = FieldInfo(alias="openaiId")

    created_by_user_drn: Optional[str] = FieldInfo(alias="createdByUserDrn", default=None)


class Data(BaseModel):
    chat_thread: DataChatThread = FieldInfo(alias="chatThread")


class ChatCreateThreadResponse(BaseModel):
    data: Data
