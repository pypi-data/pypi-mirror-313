# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["CompanyBasic", "Company", "Result"]


class Company(BaseModel):
    company_uid: Optional[str] = None
    """Unique alphanumeric Grata ID for the company (case-sensitive)."""

    description: Optional[str] = None
    """Description of the company."""

    domain: Optional[str] = None
    """Domain of the company."""

    name: Optional[str] = None
    """Name of the company."""

    url: Optional[str] = None
    """URL to the company's Grata profile."""


class Result(BaseModel):
    company_uid: Optional[str] = None
    """Unique alphanumeric Grata ID for the company (case-sensitive)."""

    description: Optional[str] = None
    """Description of the company."""

    domain: Optional[str] = None
    """Domain of the company."""

    name: Optional[str] = None
    """Name of the company."""

    url: Optional[str] = None
    """URL to the company's Grata profile."""


class CompanyBasic(BaseModel):
    company: Optional[Company] = None

    count: Optional[float] = None
    """Total number of companies in the search."""

    page_token: Optional[str] = None
    """Page token used for pagination."""

    results: Optional[List[Result]] = None
