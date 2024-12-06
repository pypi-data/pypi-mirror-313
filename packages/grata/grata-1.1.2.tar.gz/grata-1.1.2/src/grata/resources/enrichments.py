# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

import httpx

from ..types import enrichment_enrich_params, enrichment_bulk_enrich_params
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
from ..types.company import Company
from ..types.bulk_enrich_response import BulkEnrichResponse

__all__ = ["EnrichmentsResource", "AsyncEnrichmentsResource"]


class EnrichmentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EnrichmentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TJC-LP/grata-python#accessing-raw-response-data-eg-headers
        """
        return EnrichmentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EnrichmentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TJC-LP/grata-python#with_streaming_response
        """
        return EnrichmentsResourceWithStreamingResponse(self)

    def bulk_enrich(
        self,
        *,
        company_uids: List[str],
        domains: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BulkEnrichResponse:
        """
        Provide a set of up to 100 company domains or Grata-specific company IDs to
        return relevant firmographic data on requested companies.

        Args:
          company_uids: An array of unique alphanumeric Grata IDs for the companies.

          domains: An array of domains for the companies being enriched.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1.4/bulk/enrich/",
            body=maybe_transform(
                {
                    "company_uids": company_uids,
                    "domains": domains,
                },
                enrichment_bulk_enrich_params.EnrichmentBulkEnrichParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BulkEnrichResponse,
        )

    def enrich(
        self,
        *,
        domain: str,
        company_uid: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Company:
        """
        Provide a company domain or Grata-specific company ID to return relevant
        firmographic data on a company.

        Args:
          domain: Domain of the company being enriched. Protocol and path can be included. If both
              the domain and company_uid are included, the domain will be used.

          company_uid: Unique alphanumeric Grata ID for the company (case-sensitive).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v1.4/enrich/",
            body=maybe_transform(
                {
                    "domain": domain,
                    "company_uid": company_uid,
                },
                enrichment_enrich_params.EnrichmentEnrichParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Company,
        )


class AsyncEnrichmentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEnrichmentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TJC-LP/grata-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEnrichmentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEnrichmentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TJC-LP/grata-python#with_streaming_response
        """
        return AsyncEnrichmentsResourceWithStreamingResponse(self)

    async def bulk_enrich(
        self,
        *,
        company_uids: List[str],
        domains: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BulkEnrichResponse:
        """
        Provide a set of up to 100 company domains or Grata-specific company IDs to
        return relevant firmographic data on requested companies.

        Args:
          company_uids: An array of unique alphanumeric Grata IDs for the companies.

          domains: An array of domains for the companies being enriched.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1.4/bulk/enrich/",
            body=await async_maybe_transform(
                {
                    "company_uids": company_uids,
                    "domains": domains,
                },
                enrichment_bulk_enrich_params.EnrichmentBulkEnrichParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BulkEnrichResponse,
        )

    async def enrich(
        self,
        *,
        domain: str,
        company_uid: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Company:
        """
        Provide a company domain or Grata-specific company ID to return relevant
        firmographic data on a company.

        Args:
          domain: Domain of the company being enriched. Protocol and path can be included. If both
              the domain and company_uid are included, the domain will be used.

          company_uid: Unique alphanumeric Grata ID for the company (case-sensitive).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v1.4/enrich/",
            body=await async_maybe_transform(
                {
                    "domain": domain,
                    "company_uid": company_uid,
                },
                enrichment_enrich_params.EnrichmentEnrichParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Company,
        )


class EnrichmentsResourceWithRawResponse:
    def __init__(self, enrichments: EnrichmentsResource) -> None:
        self._enrichments = enrichments

        self.bulk_enrich = to_raw_response_wrapper(
            enrichments.bulk_enrich,
        )
        self.enrich = to_raw_response_wrapper(
            enrichments.enrich,
        )


class AsyncEnrichmentsResourceWithRawResponse:
    def __init__(self, enrichments: AsyncEnrichmentsResource) -> None:
        self._enrichments = enrichments

        self.bulk_enrich = async_to_raw_response_wrapper(
            enrichments.bulk_enrich,
        )
        self.enrich = async_to_raw_response_wrapper(
            enrichments.enrich,
        )


class EnrichmentsResourceWithStreamingResponse:
    def __init__(self, enrichments: EnrichmentsResource) -> None:
        self._enrichments = enrichments

        self.bulk_enrich = to_streamed_response_wrapper(
            enrichments.bulk_enrich,
        )
        self.enrich = to_streamed_response_wrapper(
            enrichments.enrich,
        )


class AsyncEnrichmentsResourceWithStreamingResponse:
    def __init__(self, enrichments: AsyncEnrichmentsResource) -> None:
        self._enrichments = enrichments

        self.bulk_enrich = async_to_streamed_response_wrapper(
            enrichments.bulk_enrich,
        )
        self.enrich = async_to_streamed_response_wrapper(
            enrichments.enrich,
        )
