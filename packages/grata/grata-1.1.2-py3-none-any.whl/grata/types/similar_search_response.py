# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .company import Company
from .._models import BaseModel

__all__ = ["SimilarSearchResponse"]


class SimilarSearchResponse(BaseModel):
    company: Company

    count: int
    """Total number of items."""

    page_token: str
    """Token for pagination."""

    results: List[Company]
