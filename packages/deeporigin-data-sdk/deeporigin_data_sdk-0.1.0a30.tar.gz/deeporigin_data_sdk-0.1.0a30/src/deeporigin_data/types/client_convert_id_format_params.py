# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Required, TypeAlias, TypedDict

__all__ = ["ClientConvertIDFormatParams", "Conversion", "ConversionID", "ConversionHid"]


class ClientConvertIDFormatParams(TypedDict, total=False):
    conversions: Required[Iterable[Conversion]]


class ConversionID(TypedDict, total=False):
    id: Required[str]
    """Deep Origin system ID."""


class ConversionHid(TypedDict, total=False):
    hid: Required[str]


Conversion: TypeAlias = Union[ConversionID, ConversionHid]
