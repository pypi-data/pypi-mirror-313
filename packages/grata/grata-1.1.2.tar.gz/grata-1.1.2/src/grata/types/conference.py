# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import date

from .._models import BaseModel

__all__ = ["Conference"]


class Conference(BaseModel):
    company_count: int
    """Total count of companies attending the conference."""

    end_date: date
    """End date of the conference (YYYY-MM-DD)."""

    location: str
    """Location of the conference."""

    name: str
    """Name of the conference."""

    start_date: date
    """Start date of the conference (YYYY-MM-DD)."""

    url: str
    """Link to the conference."""
