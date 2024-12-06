# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "ClientChatSendMessageParams",
    "Message",
    "Context",
    "ContextDatabase",
    "ContextDatabaseDatabase",
    "ContextDatabaseColumn",
    "ContextDatabaseRow",
]


class ClientChatSendMessageParams(TypedDict, total=False):
    messages: Required[Iterable[Message]]

    thread_id: Required[Annotated[str, PropertyInfo(alias="threadId")]]

    context: Context


class Message(TypedDict, total=False):
    content: Required[str]

    role: Required[Literal["user", "assistant"]]


class ContextDatabaseDatabase(TypedDict, total=False):
    hid: Required[str]
    """ID of the database."""

    hid_prefix: Required[Annotated[str, PropertyInfo(alias="hidPrefix")]]
    """Prefix for rows created in the database."""

    name: Required[str]
    """Display name of the database."""


class ContextDatabaseColumn(TypedDict, total=False):
    name: Required[str]
    """Display name of the column."""


class ContextDatabaseRow(TypedDict, total=False):
    hid: Required[str]
    """ID of the row."""

    name: str
    """Display name of the row."""


class ContextDatabase(TypedDict, total=False):
    database: Required[ContextDatabaseDatabase]
    """The selected database."""

    columns: Iterable[ContextDatabaseColumn]
    """List of columns to filter the dataframe by."""

    rows: Iterable[ContextDatabaseRow]
    """List of rows to filter the dataframe by."""


class Context(TypedDict, total=False):
    databases: Iterable[ContextDatabase]
