# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["CompanyDetailed", "Result"]


class Result(BaseModel):
    company_count: Optional[float] = None
    """Number of companies in the list"""

    created_date: Optional[str] = None
    """Date the list was created"""

    list_uid: Optional[str] = None
    """UID of list"""

    name: Optional[str] = None
    """List name"""

    updated_date: Optional[str] = None
    """Date the list was last updated"""


class CompanyDetailed(BaseModel):
    count: Optional[float] = None
    """Number of lists in the results"""

    page: Optional[float] = None
    """Current page of results"""

    pages: Optional[float] = None
    """Number of pages of results"""

    results: Optional[List[Result]] = None
