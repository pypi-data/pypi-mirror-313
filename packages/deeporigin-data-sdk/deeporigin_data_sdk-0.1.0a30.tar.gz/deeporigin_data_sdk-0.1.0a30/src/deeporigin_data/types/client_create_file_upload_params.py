# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ClientCreateFileUploadParams"]


class ClientCreateFileUploadParams(TypedDict, total=False):
    content_length: Required[Annotated[str, PropertyInfo(alias="contentLength")]]

    name: Required[str]

    checksum_sha256: Annotated[str, PropertyInfo(alias="checksumSha256")]
    """Base64 encoded SHA256 checksum of the file."""

    content_type: Annotated[str, PropertyInfo(alias="contentType")]
