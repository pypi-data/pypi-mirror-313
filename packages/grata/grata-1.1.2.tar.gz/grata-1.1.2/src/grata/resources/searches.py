# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal

import httpx

from ..types import search_search_params, search_search_similar_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.search_response import SearchResponse
from ..types.similar_search_response import SimilarSearchResponse

__all__ = ["SearchesResource", "AsyncSearchesResource"]


class SearchesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SearchesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TJC-LP/grata-python#accessing-raw-response-data-eg-headers
        """
        return SearchesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SearchesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TJC-LP/grata-python#with_streaming_response
        """
        return SearchesResourceWithStreamingResponse(self)

    def search(
        self,
        *,
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
        | NotGiven = NOT_GIVEN,
        employees_change: Iterable[float] | NotGiven = NOT_GIVEN,
        employees_change_time: Literal["month", "quarter", "six_month", "annual"] | NotGiven = NOT_GIVEN,
        employees_on_professional_networks_range: Iterable[float] | NotGiven = NOT_GIVEN,
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
        | NotGiven = NOT_GIVEN,
        funding_size: Iterable[float] | NotGiven = NOT_GIVEN,
        funding_stage: List[
            Literal[
                "early_stage_funding", "late_stage_funding", "private_equity_backed", "other_funding", "pre_ipo_funding"
            ]
        ]
        | NotGiven = NOT_GIVEN,
        grata_employees_estimates_range: Iterable[float] | NotGiven = NOT_GIVEN,
        group_operator: Literal["any", "all"] | NotGiven = NOT_GIVEN,
        headquarters: search_search_params.Headquarters | NotGiven = NOT_GIVEN,
        industry_classifications: search_search_params.IndustryClassifications | NotGiven = NOT_GIVEN,
        is_funded: bool | NotGiven = NOT_GIVEN,
        lists: search_search_params.Lists | NotGiven = NOT_GIVEN,
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
        | NotGiven = NOT_GIVEN,
        page_token: str | NotGiven = NOT_GIVEN,
        terms_exclude: List[str] | NotGiven = NOT_GIVEN,
        terms_include: search_search_params.TermsInclude | NotGiven = NOT_GIVEN,
        year_founded: Iterable[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchResponse:
        """
        Returns Grata-powered search results based on an input search query.

        Args:
          industry_classifications: Industry classification codes.

          is_funded: Indicates whether the company has received outside funding.

          lists: Grata list IDs to search within.

          page_token: Page token used for pagination.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1.4/search/",
            body=maybe_transform(
                {
                    "business_models": business_models,
                    "employees_change": employees_change,
                    "employees_change_time": employees_change_time,
                    "employees_on_professional_networks_range": employees_on_professional_networks_range,
                    "end_customer": end_customer,
                    "funding_size": funding_size,
                    "funding_stage": funding_stage,
                    "grata_employees_estimates_range": grata_employees_estimates_range,
                    "group_operator": group_operator,
                    "headquarters": headquarters,
                    "industry_classifications": industry_classifications,
                    "is_funded": is_funded,
                    "lists": lists,
                    "ownership": ownership,
                    "page_token": page_token,
                    "terms_exclude": terms_exclude,
                    "terms_include": terms_include,
                    "year_founded": year_founded,
                },
                search_search_params.SearchSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SearchResponse,
        )

    def search_similar(
        self,
        *,
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
        | NotGiven = NOT_GIVEN,
        company_uid: str | NotGiven = NOT_GIVEN,
        domain: str | NotGiven = NOT_GIVEN,
        employees_change: Iterable[float] | NotGiven = NOT_GIVEN,
        employees_change_time: Literal["month", "quarter", "six_month", "annual"] | NotGiven = NOT_GIVEN,
        employees_on_professional_networks_range: Iterable[float] | NotGiven = NOT_GIVEN,
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
        | NotGiven = NOT_GIVEN,
        funding_size: Iterable[float] | NotGiven = NOT_GIVEN,
        funding_stage: List[
            Literal[
                "early_stage_funding", "late_stage_funding", "private_equity_backed", "other_funding", "pre_ipo_funding"
            ]
        ]
        | NotGiven = NOT_GIVEN,
        grata_employees_estimates_range: Iterable[float] | NotGiven = NOT_GIVEN,
        group_operator: Literal["any", "all"] | NotGiven = NOT_GIVEN,
        headquarters: search_search_similar_params.Headquarters | NotGiven = NOT_GIVEN,
        industry_classifications: search_search_similar_params.IndustryClassifications | NotGiven = NOT_GIVEN,
        is_funded: bool | NotGiven = NOT_GIVEN,
        lists: search_search_similar_params.Lists | NotGiven = NOT_GIVEN,
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
        | NotGiven = NOT_GIVEN,
        page_token: str | NotGiven = NOT_GIVEN,
        terms_exclude: List[str] | NotGiven = NOT_GIVEN,
        terms_include: search_search_similar_params.TermsInclude | NotGiven = NOT_GIVEN,
        year_founded: Iterable[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SimilarSearchResponse:
        """
        Returns companies similar to the specified company.

        Args:
          company_uid: Alphanumeric Grata ID for the company (case-sensitive).

          domain: Domain of the company for similar search.

          industry_classifications: Industry classification codes.

          is_funded: Indicates whether the company has received outside funding.

          lists: Grata list IDs to search within.

          page_token: Page token used for pagination.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1.4/search-similar/",
            body=maybe_transform(
                {
                    "business_models": business_models,
                    "company_uid": company_uid,
                    "domain": domain,
                    "employees_change": employees_change,
                    "employees_change_time": employees_change_time,
                    "employees_on_professional_networks_range": employees_on_professional_networks_range,
                    "end_customer": end_customer,
                    "funding_size": funding_size,
                    "funding_stage": funding_stage,
                    "grata_employees_estimates_range": grata_employees_estimates_range,
                    "group_operator": group_operator,
                    "headquarters": headquarters,
                    "industry_classifications": industry_classifications,
                    "is_funded": is_funded,
                    "lists": lists,
                    "ownership": ownership,
                    "page_token": page_token,
                    "terms_exclude": terms_exclude,
                    "terms_include": terms_include,
                    "year_founded": year_founded,
                },
                search_search_similar_params.SearchSearchSimilarParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SimilarSearchResponse,
        )


class AsyncSearchesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSearchesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TJC-LP/grata-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSearchesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSearchesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TJC-LP/grata-python#with_streaming_response
        """
        return AsyncSearchesResourceWithStreamingResponse(self)

    async def search(
        self,
        *,
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
        | NotGiven = NOT_GIVEN,
        employees_change: Iterable[float] | NotGiven = NOT_GIVEN,
        employees_change_time: Literal["month", "quarter", "six_month", "annual"] | NotGiven = NOT_GIVEN,
        employees_on_professional_networks_range: Iterable[float] | NotGiven = NOT_GIVEN,
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
        | NotGiven = NOT_GIVEN,
        funding_size: Iterable[float] | NotGiven = NOT_GIVEN,
        funding_stage: List[
            Literal[
                "early_stage_funding", "late_stage_funding", "private_equity_backed", "other_funding", "pre_ipo_funding"
            ]
        ]
        | NotGiven = NOT_GIVEN,
        grata_employees_estimates_range: Iterable[float] | NotGiven = NOT_GIVEN,
        group_operator: Literal["any", "all"] | NotGiven = NOT_GIVEN,
        headquarters: search_search_params.Headquarters | NotGiven = NOT_GIVEN,
        industry_classifications: search_search_params.IndustryClassifications | NotGiven = NOT_GIVEN,
        is_funded: bool | NotGiven = NOT_GIVEN,
        lists: search_search_params.Lists | NotGiven = NOT_GIVEN,
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
        | NotGiven = NOT_GIVEN,
        page_token: str | NotGiven = NOT_GIVEN,
        terms_exclude: List[str] | NotGiven = NOT_GIVEN,
        terms_include: search_search_params.TermsInclude | NotGiven = NOT_GIVEN,
        year_founded: Iterable[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SearchResponse:
        """
        Returns Grata-powered search results based on an input search query.

        Args:
          industry_classifications: Industry classification codes.

          is_funded: Indicates whether the company has received outside funding.

          lists: Grata list IDs to search within.

          page_token: Page token used for pagination.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1.4/search/",
            body=await async_maybe_transform(
                {
                    "business_models": business_models,
                    "employees_change": employees_change,
                    "employees_change_time": employees_change_time,
                    "employees_on_professional_networks_range": employees_on_professional_networks_range,
                    "end_customer": end_customer,
                    "funding_size": funding_size,
                    "funding_stage": funding_stage,
                    "grata_employees_estimates_range": grata_employees_estimates_range,
                    "group_operator": group_operator,
                    "headquarters": headquarters,
                    "industry_classifications": industry_classifications,
                    "is_funded": is_funded,
                    "lists": lists,
                    "ownership": ownership,
                    "page_token": page_token,
                    "terms_exclude": terms_exclude,
                    "terms_include": terms_include,
                    "year_founded": year_founded,
                },
                search_search_params.SearchSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SearchResponse,
        )

    async def search_similar(
        self,
        *,
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
        | NotGiven = NOT_GIVEN,
        company_uid: str | NotGiven = NOT_GIVEN,
        domain: str | NotGiven = NOT_GIVEN,
        employees_change: Iterable[float] | NotGiven = NOT_GIVEN,
        employees_change_time: Literal["month", "quarter", "six_month", "annual"] | NotGiven = NOT_GIVEN,
        employees_on_professional_networks_range: Iterable[float] | NotGiven = NOT_GIVEN,
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
        | NotGiven = NOT_GIVEN,
        funding_size: Iterable[float] | NotGiven = NOT_GIVEN,
        funding_stage: List[
            Literal[
                "early_stage_funding", "late_stage_funding", "private_equity_backed", "other_funding", "pre_ipo_funding"
            ]
        ]
        | NotGiven = NOT_GIVEN,
        grata_employees_estimates_range: Iterable[float] | NotGiven = NOT_GIVEN,
        group_operator: Literal["any", "all"] | NotGiven = NOT_GIVEN,
        headquarters: search_search_similar_params.Headquarters | NotGiven = NOT_GIVEN,
        industry_classifications: search_search_similar_params.IndustryClassifications | NotGiven = NOT_GIVEN,
        is_funded: bool | NotGiven = NOT_GIVEN,
        lists: search_search_similar_params.Lists | NotGiven = NOT_GIVEN,
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
        | NotGiven = NOT_GIVEN,
        page_token: str | NotGiven = NOT_GIVEN,
        terms_exclude: List[str] | NotGiven = NOT_GIVEN,
        terms_include: search_search_similar_params.TermsInclude | NotGiven = NOT_GIVEN,
        year_founded: Iterable[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SimilarSearchResponse:
        """
        Returns companies similar to the specified company.

        Args:
          company_uid: Alphanumeric Grata ID for the company (case-sensitive).

          domain: Domain of the company for similar search.

          industry_classifications: Industry classification codes.

          is_funded: Indicates whether the company has received outside funding.

          lists: Grata list IDs to search within.

          page_token: Page token used for pagination.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1.4/search-similar/",
            body=await async_maybe_transform(
                {
                    "business_models": business_models,
                    "company_uid": company_uid,
                    "domain": domain,
                    "employees_change": employees_change,
                    "employees_change_time": employees_change_time,
                    "employees_on_professional_networks_range": employees_on_professional_networks_range,
                    "end_customer": end_customer,
                    "funding_size": funding_size,
                    "funding_stage": funding_stage,
                    "grata_employees_estimates_range": grata_employees_estimates_range,
                    "group_operator": group_operator,
                    "headquarters": headquarters,
                    "industry_classifications": industry_classifications,
                    "is_funded": is_funded,
                    "lists": lists,
                    "ownership": ownership,
                    "page_token": page_token,
                    "terms_exclude": terms_exclude,
                    "terms_include": terms_include,
                    "year_founded": year_founded,
                },
                search_search_similar_params.SearchSearchSimilarParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SimilarSearchResponse,
        )


class SearchesResourceWithRawResponse:
    def __init__(self, searches: SearchesResource) -> None:
        self._searches = searches

        self.search = to_raw_response_wrapper(
            searches.search,
        )
        self.search_similar = to_raw_response_wrapper(
            searches.search_similar,
        )


class AsyncSearchesResourceWithRawResponse:
    def __init__(self, searches: AsyncSearchesResource) -> None:
        self._searches = searches

        self.search = async_to_raw_response_wrapper(
            searches.search,
        )
        self.search_similar = async_to_raw_response_wrapper(
            searches.search_similar,
        )


class SearchesResourceWithStreamingResponse:
    def __init__(self, searches: SearchesResource) -> None:
        self._searches = searches

        self.search = to_streamed_response_wrapper(
            searches.search,
        )
        self.search_similar = to_streamed_response_wrapper(
            searches.search_similar,
        )


class AsyncSearchesResourceWithStreamingResponse:
    def __init__(self, searches: AsyncSearchesResource) -> None:
        self._searches = searches

        self.search = async_to_streamed_response_wrapper(
            searches.search,
        )
        self.search_similar = async_to_streamed_response_wrapper(
            searches.search_similar,
        )
