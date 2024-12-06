# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from .._models import BaseModel

__all__ = ["List"]


class List(BaseModel):
    company_count: int
    """Number of companies in the list."""

    created_date: datetime
    """Date the list was created."""

    list_uid: str
    """UID of the list."""

    name: str
    """Name of the list."""

    updated_date: datetime
    """Date the list was last updated."""
