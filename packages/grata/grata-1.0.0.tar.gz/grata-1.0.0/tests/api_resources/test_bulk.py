# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from grata import Grata, AsyncGrata
from tests.utils import assert_matches_type
from grata.types.shared import CompanyDetailed

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBulk:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_enrich(self, client: Grata) -> None:
        bulk = client.bulk.enrich(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )
        assert_matches_type(CompanyDetailed, bulk, path=["response"])

    @parametrize
    def test_method_enrich_with_all_params(self, client: Grata) -> None:
        bulk = client.bulk.enrich(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
            company_uids=["GAGRYBUR", "UFFY5AZY"],
            domains=["okta.com", "slack.com"],
        )
        assert_matches_type(CompanyDetailed, bulk, path=["response"])

    @parametrize
    def test_raw_response_enrich(self, client: Grata) -> None:
        response = client.bulk.with_raw_response.enrich(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bulk = response.parse()
        assert_matches_type(CompanyDetailed, bulk, path=["response"])

    @parametrize
    def test_streaming_response_enrich(self, client: Grata) -> None:
        with client.bulk.with_streaming_response.enrich(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bulk = response.parse()
            assert_matches_type(CompanyDetailed, bulk, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncBulk:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_enrich(self, async_client: AsyncGrata) -> None:
        bulk = await async_client.bulk.enrich(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )
        assert_matches_type(CompanyDetailed, bulk, path=["response"])

    @parametrize
    async def test_method_enrich_with_all_params(self, async_client: AsyncGrata) -> None:
        bulk = await async_client.bulk.enrich(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
            company_uids=["GAGRYBUR", "UFFY5AZY"],
            domains=["okta.com", "slack.com"],
        )
        assert_matches_type(CompanyDetailed, bulk, path=["response"])

    @parametrize
    async def test_raw_response_enrich(self, async_client: AsyncGrata) -> None:
        response = await async_client.bulk.with_raw_response.enrich(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bulk = await response.parse()
        assert_matches_type(CompanyDetailed, bulk, path=["response"])

    @parametrize
    async def test_streaming_response_enrich(self, async_client: AsyncGrata) -> None:
        async with async_client.bulk.with_streaming_response.enrich(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bulk = await response.parse()
            assert_matches_type(CompanyDetailed, bulk, path=["response"])

        assert cast(Any, response.is_closed) is True
