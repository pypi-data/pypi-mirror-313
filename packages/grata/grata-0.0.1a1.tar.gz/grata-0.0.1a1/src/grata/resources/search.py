# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal

import httpx

from ..types import search_create_params, search_similar_params
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
from ..types.company_basic import CompanyBasic

__all__ = ["SearchResource", "AsyncSearchResource"]


class SearchResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SearchResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TJC-LP/grata-python#accessing-raw-response-data-eg-headers
        """
        return SearchResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SearchResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TJC-LP/grata-python#with_streaming_response
        """
        return SearchResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        authorization: str,
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
        headquarters: search_create_params.Headquarters | NotGiven = NOT_GIVEN,
        industry_classifications: search_create_params.IndustryClassifications | NotGiven = NOT_GIVEN,
        is_funded: bool | NotGiven = NOT_GIVEN,
        lists: search_create_params.Lists | NotGiven = NOT_GIVEN,
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
        terms_include: search_create_params.TermsInclude | NotGiven = NOT_GIVEN,
        year_founded: Iterable[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyBasic:
        """Returns Grata-powered search results based on an input search query.

        If you're
        using any of the filters in the UI that are not presented below, the results may
        differ.

        Args:
          business_models: Business models to search on.

          company_uid: Alphanumeric Grata ID for the company (case-sensitive).

          domain: Domain of the company for similar search. Protocol and path can be included. If
              both the domain and company_uid are specified, domain will be referenced.

          employees_change: Range of % employee growth.

          employees_change_time: The interval for employee growth rate.

          employees_on_professional_networks_range: The range of employee counts listed on professional networks. Inputting 100,001
              as the maximum value will search for all employee sizes above the minimum.
              [100,100001] will search for all companies with 100 or more employees

          end_customer: End vertical that the company sells to.

          funding_size: Range of funding the company has received in USD. Ranges can only start and
              begin with the following values: 0, 5000000, 10000000, 20000000, 50000000,
              100000000, 200000000, 500000000, 500000001. 500000001 equates to maximum.

          grata_employees_estimates_range: The range of employee counts based on Grata Employee estimates. Inputting
              100,001 as the maximum value will search for all employee sizes above the
              minimum. [100,100001] will search for all companies with 100 or more employees

          headquarters: Headquarter locations supports all countries and US city/states. State cannot be
              left blank if city is populated. Country cannot be other than United States if
              searching for city/state.

          industry_classifications: Industry classification code for the company. Pass the industry NAICS code or
              Grata's specific software industry code listed in the mapping doc -
              https://grata.stoplight.io/docs/grata/branches/v1.3/42ptq2xej8i5j-software-industry-code-mapping

          is_funded: Indicates whether or not the company has received outside funding.

          lists: Grata list IDs to search within. Default logic for include is "or", default
              logic for exclude is "and."

          ownership: Ownership types to search and sort on.

          terms_exclude: Keywords to exclude from the search.

          terms_include: String used for keyword search. This is an array of keywords

          year_founded: Range of founding years.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Authorization": authorization, **(extra_headers or {})}
        return self._post(
            "/api/v1.4/search/",
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
                search_create_params.SearchCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyBasic,
        )

    def similar(
        self,
        *,
        authorization: str,
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
        headquarters: search_similar_params.Headquarters | NotGiven = NOT_GIVEN,
        industry_classifications: search_similar_params.IndustryClassifications | NotGiven = NOT_GIVEN,
        is_funded: bool | NotGiven = NOT_GIVEN,
        lists: search_similar_params.Lists | NotGiven = NOT_GIVEN,
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
        terms_include: search_similar_params.TermsInclude | NotGiven = NOT_GIVEN,
        year_founded: Iterable[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyBasic:
        """Returns Grata-powered search results based on an input search query.

        If you're
        using any of the filters in the UI that are not presented below, the results may
        differ.

        Args:
          business_models: Business models to search on.

          company_uid: Alphanumeric Grata ID for the company (case-sensitive).

          domain: Domain of the company for similar search. Protocol and path can be included. If
              both the domain and company_uid are specified, domain will be referenced.

          employees_change: Range of % employee growth.

          employees_change_time: The interval for employee growth rate.

          employees_on_professional_networks_range: The range of employee counts listed on professional networks. Inputting 100,001
              as the maximum value will search for all employee sizes above the minimum.
              [100,100001] will search for all companies with 100 or more employees

          end_customer: End vertical that the company sells to.

          funding_size: Range of funding the company has received in USD. Ranges can only start and
              begin with the following values: 0, 5000000, 10000000, 20000000, 50000000,
              100000000, 200000000, 500000000, 500000001. 500000001 equates to maximum.

          grata_employees_estimates_range: The range of employee counts based on Grata Employee estimates. Inputting
              100,001 as the maximum value will search for all employee sizes above the
              minimum. [100,100001] will search for all companies with 100 or more employees

          headquarters: Headquarter locations supports all countries and US city/states. State cannot be
              left blank if city is populated. Country cannot be other than United States if
              searching for city/state.

          industry_classifications: Industry classification code for the company. Pass the industry NAICS code or
              Grata's specific software industry code listed in the mapping doc -
              https://grata.stoplight.io/docs/grata/branches/v1.3/42ptq2xej8i5j-software-industry-code-mapping

          is_funded: Indicates whether or not the company has received outside funding.

          lists: Grata list IDs to search within. Default logic for include is "or", default
              logic for exclude is "and."

          ownership: Ownership types to search and sort on.

          terms_exclude: Keywords to exclude from the search.

          terms_include: String used for keyword search. This is an array of keywords

          year_founded: Range of founding years.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Authorization": authorization, **(extra_headers or {})}
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
                search_similar_params.SearchSimilarParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyBasic,
        )


class AsyncSearchResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSearchResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TJC-LP/grata-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSearchResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSearchResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TJC-LP/grata-python#with_streaming_response
        """
        return AsyncSearchResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        authorization: str,
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
        headquarters: search_create_params.Headquarters | NotGiven = NOT_GIVEN,
        industry_classifications: search_create_params.IndustryClassifications | NotGiven = NOT_GIVEN,
        is_funded: bool | NotGiven = NOT_GIVEN,
        lists: search_create_params.Lists | NotGiven = NOT_GIVEN,
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
        terms_include: search_create_params.TermsInclude | NotGiven = NOT_GIVEN,
        year_founded: Iterable[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyBasic:
        """Returns Grata-powered search results based on an input search query.

        If you're
        using any of the filters in the UI that are not presented below, the results may
        differ.

        Args:
          business_models: Business models to search on.

          company_uid: Alphanumeric Grata ID for the company (case-sensitive).

          domain: Domain of the company for similar search. Protocol and path can be included. If
              both the domain and company_uid are specified, domain will be referenced.

          employees_change: Range of % employee growth.

          employees_change_time: The interval for employee growth rate.

          employees_on_professional_networks_range: The range of employee counts listed on professional networks. Inputting 100,001
              as the maximum value will search for all employee sizes above the minimum.
              [100,100001] will search for all companies with 100 or more employees

          end_customer: End vertical that the company sells to.

          funding_size: Range of funding the company has received in USD. Ranges can only start and
              begin with the following values: 0, 5000000, 10000000, 20000000, 50000000,
              100000000, 200000000, 500000000, 500000001. 500000001 equates to maximum.

          grata_employees_estimates_range: The range of employee counts based on Grata Employee estimates. Inputting
              100,001 as the maximum value will search for all employee sizes above the
              minimum. [100,100001] will search for all companies with 100 or more employees

          headquarters: Headquarter locations supports all countries and US city/states. State cannot be
              left blank if city is populated. Country cannot be other than United States if
              searching for city/state.

          industry_classifications: Industry classification code for the company. Pass the industry NAICS code or
              Grata's specific software industry code listed in the mapping doc -
              https://grata.stoplight.io/docs/grata/branches/v1.3/42ptq2xej8i5j-software-industry-code-mapping

          is_funded: Indicates whether or not the company has received outside funding.

          lists: Grata list IDs to search within. Default logic for include is "or", default
              logic for exclude is "and."

          ownership: Ownership types to search and sort on.

          terms_exclude: Keywords to exclude from the search.

          terms_include: String used for keyword search. This is an array of keywords

          year_founded: Range of founding years.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Authorization": authorization, **(extra_headers or {})}
        return await self._post(
            "/api/v1.4/search/",
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
                search_create_params.SearchCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyBasic,
        )

    async def similar(
        self,
        *,
        authorization: str,
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
        headquarters: search_similar_params.Headquarters | NotGiven = NOT_GIVEN,
        industry_classifications: search_similar_params.IndustryClassifications | NotGiven = NOT_GIVEN,
        is_funded: bool | NotGiven = NOT_GIVEN,
        lists: search_similar_params.Lists | NotGiven = NOT_GIVEN,
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
        terms_include: search_similar_params.TermsInclude | NotGiven = NOT_GIVEN,
        year_founded: Iterable[float] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyBasic:
        """Returns Grata-powered search results based on an input search query.

        If you're
        using any of the filters in the UI that are not presented below, the results may
        differ.

        Args:
          business_models: Business models to search on.

          company_uid: Alphanumeric Grata ID for the company (case-sensitive).

          domain: Domain of the company for similar search. Protocol and path can be included. If
              both the domain and company_uid are specified, domain will be referenced.

          employees_change: Range of % employee growth.

          employees_change_time: The interval for employee growth rate.

          employees_on_professional_networks_range: The range of employee counts listed on professional networks. Inputting 100,001
              as the maximum value will search for all employee sizes above the minimum.
              [100,100001] will search for all companies with 100 or more employees

          end_customer: End vertical that the company sells to.

          funding_size: Range of funding the company has received in USD. Ranges can only start and
              begin with the following values: 0, 5000000, 10000000, 20000000, 50000000,
              100000000, 200000000, 500000000, 500000001. 500000001 equates to maximum.

          grata_employees_estimates_range: The range of employee counts based on Grata Employee estimates. Inputting
              100,001 as the maximum value will search for all employee sizes above the
              minimum. [100,100001] will search for all companies with 100 or more employees

          headquarters: Headquarter locations supports all countries and US city/states. State cannot be
              left blank if city is populated. Country cannot be other than United States if
              searching for city/state.

          industry_classifications: Industry classification code for the company. Pass the industry NAICS code or
              Grata's specific software industry code listed in the mapping doc -
              https://grata.stoplight.io/docs/grata/branches/v1.3/42ptq2xej8i5j-software-industry-code-mapping

          is_funded: Indicates whether or not the company has received outside funding.

          lists: Grata list IDs to search within. Default logic for include is "or", default
              logic for exclude is "and."

          ownership: Ownership types to search and sort on.

          terms_exclude: Keywords to exclude from the search.

          terms_include: String used for keyword search. This is an array of keywords

          year_founded: Range of founding years.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Authorization": authorization, **(extra_headers or {})}
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
                search_similar_params.SearchSimilarParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyBasic,
        )


class SearchResourceWithRawResponse:
    def __init__(self, search: SearchResource) -> None:
        self._search = search

        self.create = to_raw_response_wrapper(
            search.create,
        )
        self.similar = to_raw_response_wrapper(
            search.similar,
        )


class AsyncSearchResourceWithRawResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.create = async_to_raw_response_wrapper(
            search.create,
        )
        self.similar = async_to_raw_response_wrapper(
            search.similar,
        )


class SearchResourceWithStreamingResponse:
    def __init__(self, search: SearchResource) -> None:
        self._search = search

        self.create = to_streamed_response_wrapper(
            search.create,
        )
        self.similar = to_streamed_response_wrapper(
            search.similar,
        )


class AsyncSearchResourceWithStreamingResponse:
    def __init__(self, search: AsyncSearchResource) -> None:
        self._search = search

        self.create = async_to_streamed_response_wrapper(
            search.create,
        )
        self.similar = async_to_streamed_response_wrapper(
            search.similar,
        )
