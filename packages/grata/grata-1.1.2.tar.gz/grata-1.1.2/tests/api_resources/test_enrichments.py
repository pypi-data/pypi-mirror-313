# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from grata import Grata, AsyncGrata
from grata.types import Company, BulkEnrichResponse
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEnrichments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_bulk_enrich(self, client: Grata) -> None:
        enrichment = client.enrichments.bulk_enrich(
            company_uids=["GAGRYBUR", "UFFY5AZY"],
            domains=["grata.com", "slack.com"],
        )
        assert_matches_type(BulkEnrichResponse, enrichment, path=["response"])

    @parametrize
    def test_raw_response_bulk_enrich(self, client: Grata) -> None:
        response = client.enrichments.with_raw_response.bulk_enrich(
            company_uids=["GAGRYBUR", "UFFY5AZY"],
            domains=["grata.com", "slack.com"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enrichment = response.parse()
        assert_matches_type(BulkEnrichResponse, enrichment, path=["response"])

    @parametrize
    def test_streaming_response_bulk_enrich(self, client: Grata) -> None:
        with client.enrichments.with_streaming_response.bulk_enrich(
            company_uids=["GAGRYBUR", "UFFY5AZY"],
            domains=["grata.com", "slack.com"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enrichment = response.parse()
            assert_matches_type(BulkEnrichResponse, enrichment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_enrich(self, client: Grata) -> None:
        enrichment = client.enrichments.enrich(
            domain="slack.com",
        )
        assert_matches_type(Company, enrichment, path=["response"])

    @parametrize
    def test_method_enrich_with_all_params(self, client: Grata) -> None:
        enrichment = client.enrichments.enrich(
            domain="slack.com",
            company_uid="7W46XUJT",
        )
        assert_matches_type(Company, enrichment, path=["response"])

    @parametrize
    def test_raw_response_enrich(self, client: Grata) -> None:
        response = client.enrichments.with_raw_response.enrich(
            domain="slack.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enrichment = response.parse()
        assert_matches_type(Company, enrichment, path=["response"])

    @parametrize
    def test_streaming_response_enrich(self, client: Grata) -> None:
        with client.enrichments.with_streaming_response.enrich(
            domain="slack.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enrichment = response.parse()
            assert_matches_type(Company, enrichment, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEnrichments:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_bulk_enrich(self, async_client: AsyncGrata) -> None:
        enrichment = await async_client.enrichments.bulk_enrich(
            company_uids=["GAGRYBUR", "UFFY5AZY"],
            domains=["grata.com", "slack.com"],
        )
        assert_matches_type(BulkEnrichResponse, enrichment, path=["response"])

    @parametrize
    async def test_raw_response_bulk_enrich(self, async_client: AsyncGrata) -> None:
        response = await async_client.enrichments.with_raw_response.bulk_enrich(
            company_uids=["GAGRYBUR", "UFFY5AZY"],
            domains=["grata.com", "slack.com"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enrichment = await response.parse()
        assert_matches_type(BulkEnrichResponse, enrichment, path=["response"])

    @parametrize
    async def test_streaming_response_bulk_enrich(self, async_client: AsyncGrata) -> None:
        async with async_client.enrichments.with_streaming_response.bulk_enrich(
            company_uids=["GAGRYBUR", "UFFY5AZY"],
            domains=["grata.com", "slack.com"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enrichment = await response.parse()
            assert_matches_type(BulkEnrichResponse, enrichment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_enrich(self, async_client: AsyncGrata) -> None:
        enrichment = await async_client.enrichments.enrich(
            domain="slack.com",
        )
        assert_matches_type(Company, enrichment, path=["response"])

    @parametrize
    async def test_method_enrich_with_all_params(self, async_client: AsyncGrata) -> None:
        enrichment = await async_client.enrichments.enrich(
            domain="slack.com",
            company_uid="7W46XUJT",
        )
        assert_matches_type(Company, enrichment, path=["response"])

    @parametrize
    async def test_raw_response_enrich(self, async_client: AsyncGrata) -> None:
        response = await async_client.enrichments.with_raw_response.enrich(
            domain="slack.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enrichment = await response.parse()
        assert_matches_type(Company, enrichment, path=["response"])

    @parametrize
    async def test_streaming_response_enrich(self, async_client: AsyncGrata) -> None:
        async with async_client.enrichments.with_streaming_response.enrich(
            domain="slack.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enrichment = await response.parse()
            assert_matches_type(Company, enrichment, path=["response"])

        assert cast(Any, response.is_closed) is True
