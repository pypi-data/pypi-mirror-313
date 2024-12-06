# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable, Optional
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "SearchSimilarParams",
    "Headquarters",
    "HeadquartersExclude",
    "HeadquartersInclude",
    "IndustryClassifications",
    "Lists",
    "TermsInclude",
    "TermsIncludeGroup",
]


class SearchSimilarParams(TypedDict, total=False):
    authorization: Required[Annotated[str, PropertyInfo(alias="Authorization")]]

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
    """Business models to search on."""

    company_uid: str
    """Alphanumeric Grata ID for the company (case-sensitive)."""

    domain: str
    """Domain of the company for similar search.

    Protocol and path can be included. If both the domain and company_uid are
    specified, domain will be referenced.
    """

    employees_change: Iterable[float]
    """Range of % employee growth."""

    employees_change_time: Literal["month", "quarter", "six_month", "annual"]
    """The interval for employee growth rate."""

    employees_on_professional_networks_range: Iterable[float]
    """The range of employee counts listed on professional networks.

    Inputting 100,001 as the maximum value will search for all employee sizes above
    the minimum. [100,100001] will search for all companies with 100 or more
    employees
    """

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
    """End vertical that the company sells to."""

    funding_size: Iterable[float]
    """Range of funding the company has received in USD.

    Ranges can only start and begin with the following values: 0, 5000000, 10000000,
    20000000, 50000000, 100000000, 200000000, 500000000, 500000001. 500000001
    equates to maximum.
    """

    funding_stage: List[
        Literal[
            "early_stage_funding", "late_stage_funding", "private_equity_backed", "other_funding", "pre_ipo_funding"
        ]
    ]

    grata_employees_estimates_range: Iterable[float]
    """The range of employee counts based on Grata Employee estimates.

    Inputting 100,001 as the maximum value will search for all employee sizes above
    the minimum. [100,100001] will search for all companies with 100 or more
    employees
    """

    headquarters: Headquarters
    """Headquarter locations supports all countries and US city/states.

    State cannot be left blank if city is populated. Country cannot be other than
    United States if searching for city/state.
    """

    industry_classifications: IndustryClassifications
    """Industry classification code for the company.

    Pass the industry NAICS code or Grata's specific software industry code listed
    in the mapping doc -
    https://grata.stoplight.io/docs/grata/branches/v1.3/42ptq2xej8i5j-software-industry-code-mapping
    """

    is_funded: bool
    """Indicates whether or not the company has received outside funding."""

    lists: Lists
    """Grata list IDs to search within.

    Default logic for include is "or", default logic for exclude is "and."
    """

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
    """Ownership types to search and sort on."""

    page_token: str

    terms_exclude: List[str]
    """Keywords to exclude from the search."""

    terms_include: TermsInclude
    """String used for keyword search. This is an array of keywords"""

    year_founded: Iterable[float]
    """Range of founding years."""


class HeadquartersExclude(TypedDict, total=False):
    city: Optional[str]

    country: str

    state: Optional[str]


class HeadquartersInclude(TypedDict, total=False):
    city: Optional[str]

    country: str

    state: Optional[str]


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
    group_operator: Literal["any", "all"]

    groups: Iterable[TermsIncludeGroup]
