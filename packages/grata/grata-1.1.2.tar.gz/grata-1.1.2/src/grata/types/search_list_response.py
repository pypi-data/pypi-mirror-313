# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List as TypingList

from .list import List as ListList
from .._models import BaseModel

__all__ = ["SearchListResponse"]


class SearchListResponse(BaseModel):
    count: int
    """Number of lists in the results."""

    page: int
    """Current page of results."""

    pages: int
    """Number of pages of results."""

    results: TypingList[ListList]
