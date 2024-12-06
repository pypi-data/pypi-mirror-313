# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ListListParams"]


class ListListParams(TypedDict, total=False):
    authorization: Required[Annotated[str, PropertyInfo(alias="Authorization")]]

    name: str
    """List name"""

    page: str
    """The page of results to be returned"""
