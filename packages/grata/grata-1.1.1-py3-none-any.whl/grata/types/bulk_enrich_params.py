# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

__all__ = ["BulkEnrichParams"]


class BulkEnrichParams(TypedDict, total=False):
    company_uids: List[str]
    """An array of unique alphanumeric Grata IDs for the companies."""

    domains: List[str]
    """An array of domains for the companies being enriched."""
