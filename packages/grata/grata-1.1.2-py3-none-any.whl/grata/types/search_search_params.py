# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal, TypedDict

__all__ = [
    "SearchSearchParams",
    "Headquarters",
    "HeadquartersExclude",
    "HeadquartersInclude",
    "IndustryClassifications",
    "Lists",
    "TermsInclude",
    "TermsIncludeGroup",
]


class SearchSearchParams(TypedDict, total=False):
    business_models: List[
        Literal[
            "software",
            "software_enabled",
            "services",
            "hardware",
            "content_and_publishing",
            "investment_banks_and_business_brokers",
            "education",
            "directory",
            "job_site",
            "staffing_and_recruiting",
            "private_equity_and_venture_capital",
            "private_schools",
            "retailer",
            "manufacturer",
            "distributor",
            "producer",
            "marketplace",
            "hospitals_and_medical_centers",
            "colleges_and_universities",
            "government",
            "us_federal_agencies",
            "nonprofit_and_associations",
            "religious_institutions",
        ]
    ]

    employees_change: Iterable[float]

    employees_change_time: Literal["month", "quarter", "six_month", "annual"]

    employees_on_professional_networks_range: Iterable[float]

    end_customer: List[
        Literal[
            "b2b",
            "b2c",
            "information_technology",
            "professional_services",
            "electronics",
            "commercial_and_residential_services",
            "hospitality_and_leisure",
            "media",
            "finance",
            "industrials",
            "transportation",
            "education",
            "agriculture",
            "healthcare",
            "government",
            "consumer_product_and_retail",
        ]
    ]

    funding_size: Iterable[float]

    funding_stage: List[
        Literal[
            "early_stage_funding", "late_stage_funding", "private_equity_backed", "other_funding", "pre_ipo_funding"
        ]
    ]

    grata_employees_estimates_range: Iterable[float]

    group_operator: Literal["any", "all"]

    headquarters: Headquarters

    industry_classifications: IndustryClassifications
    """Industry classification codes."""

    is_funded: bool
    """Indicates whether the company has received outside funding."""

    lists: Lists
    """Grata list IDs to search within."""

    ownership: List[
        Literal[
            "bootstrapped",
            "investor_backed",
            "public",
            "public_subsidiary",
            "private_subsidiary",
            "private_equity",
            "private_equity_add_on",
        ]
    ]

    page_token: str
    """Page token used for pagination."""

    terms_exclude: List[str]

    terms_include: TermsInclude

    year_founded: Iterable[float]


class HeadquartersExclude(TypedDict, total=False):
    city: str

    country: str

    state: str


class HeadquartersInclude(TypedDict, total=False):
    city: str

    country: str

    state: str


class Headquarters(TypedDict, total=False):
    exclude: Iterable[HeadquartersExclude]

    include: Iterable[HeadquartersInclude]


class IndustryClassifications(TypedDict, total=False):
    exclude: Iterable[float]

    include: Iterable[float]


class Lists(TypedDict, total=False):
    exclude: List[str]

    include: List[str]


class TermsIncludeGroup(TypedDict, total=False):
    terms: List[str]

    terms_depth: Literal["core", "mention"]

    terms_operator: Literal["any", "all"]


class TermsInclude(TypedDict, total=False):
    groups: Iterable[TermsIncludeGroup]
