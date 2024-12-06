# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ListListParams"]


class ListListParams(TypedDict, total=False):
    name: str
    """List name"""

    page: str
    """The page of results to be returned"""
