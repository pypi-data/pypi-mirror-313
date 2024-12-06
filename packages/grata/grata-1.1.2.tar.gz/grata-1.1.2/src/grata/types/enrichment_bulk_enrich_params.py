# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

__all__ = ["EnrichmentBulkEnrichParams"]


class EnrichmentBulkEnrichParams(TypedDict, total=False):
    company_uids: Required[List[str]]
    """An array of unique alphanumeric Grata IDs for the companies."""

    domains: Required[List[str]]
    """An array of domains for the companies being enriched."""
