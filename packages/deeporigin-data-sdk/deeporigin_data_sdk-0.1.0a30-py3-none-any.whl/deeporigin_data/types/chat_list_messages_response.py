# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "ChatListMessagesResponse",
    "Data",
    "DataMessage",
    "DataMessageContent",
    "DataMessageContentText",
    "DataMessageContentTextText",
    "DataMessageContentImageFile",
    "DataMessageContentImageFileImageFile",
    "DataMessageContentImageURL",
    "DataMessageContentImageURLImageURL",
    "DataMessageContentRefusal",
]


class DataMessageContentTextText(BaseModel):
    value: str


class DataMessageContentText(BaseModel):
    text: DataMessageContentTextText

    type: Literal["text"]


class DataMessageContentImageFileImageFile(BaseModel):
    file_id: str


class DataMessageContentImageFile(BaseModel):
    image_file: DataMessageContentImageFileImageFile

    type: Literal["image_file"]


class DataMessageContentImageURLImageURL(BaseModel):
    url: str


class DataMessageContentImageURL(BaseModel):
    image_url: DataMessageContentImageURLImageURL

    type: Literal["image_url"]


class DataMessageContentRefusal(BaseModel):
    refusal: str

    type: Literal["refusal"]


DataMessageContent: TypeAlias = Annotated[
    Union[DataMessageContentText, DataMessageContentImageFile, DataMessageContentImageURL, DataMessageContentRefusal],
    PropertyInfo(discriminator="type"),
]


class DataMessage(BaseModel):
    id: str
    """Deep Origin system ID."""

    role: Literal["user", "assistant"]

    content: Optional[List[DataMessageContent]] = None


class Data(BaseModel):
    messages: List[DataMessage]


class ChatListMessagesResponse(BaseModel):
    data: Data
