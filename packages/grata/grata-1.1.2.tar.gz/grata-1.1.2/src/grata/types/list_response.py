# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["ListResponse", "NotProcessed", "Processed", "Result", "ResultCompany"]


class NotProcessed(BaseModel):
    companies: List[str]

    count: int
    """The number of companies processed."""


class Processed(BaseModel):
    companies: List[str]

    count: int
    """The number of companies processed."""


class ResultCompany(BaseModel):
    domain: str
    """The associated domain."""

    uid: str
    """The associated company UID."""


class Result(BaseModel):
    company: ResultCompany

    input: str
    """The inputted domain or UID."""

    processed: bool
    """Indicates whether the domain was processed."""


class ListResponse(BaseModel):
    not_processed: NotProcessed

    processed: Processed

    results: List[Result]
