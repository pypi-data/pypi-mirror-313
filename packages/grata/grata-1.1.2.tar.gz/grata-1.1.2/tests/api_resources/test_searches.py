# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from grata import Grata, AsyncGrata
from grata.types import SearchResponse, SimilarSearchResponse
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSearches:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_search(self, client: Grata) -> None:
        search = client.searches.search()
        assert_matches_type(SearchResponse, search, path=["response"])

    @parametrize
    def test_method_search_with_all_params(self, client: Grata) -> None:
        search = client.searches.search(
            business_models=["software"],
            employees_change=[-50],
            employees_change_time="month",
            employees_on_professional_networks_range=[0],
            end_customer=["b2b"],
            funding_size=[0, 0],
            funding_stage=["early_stage_funding"],
            grata_employees_estimates_range=[0],
            group_operator="any",
            headquarters={
                "exclude": [
                    {
                        "city": "city",
                        "country": "country",
                        "state": "state",
                    }
                ],
                "include": [
                    {
                        "city": "city",
                        "country": "country",
                        "state": "state",
                    }
                ],
            },
            industry_classifications={
                "exclude": [0],
                "include": [0],
            },
            is_funded=True,
            lists={
                "exclude": ["string"],
                "include": ["string"],
            },
            ownership=["bootstrapped"],
            page_token="page_token",
            terms_exclude=["string"],
            terms_include={
                "groups": [
                    {
                        "terms": ["string"],
                        "terms_depth": "core",
                        "terms_operator": "any",
                    }
                ]
            },
            year_founded=[1959],
        )
        assert_matches_type(SearchResponse, search, path=["response"])

    @parametrize
    def test_raw_response_search(self, client: Grata) -> None:
        response = client.searches.with_raw_response.search()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(SearchResponse, search, path=["response"])

    @parametrize
    def test_streaming_response_search(self, client: Grata) -> None:
        with client.searches.with_streaming_response.search() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(SearchResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_search_similar(self, client: Grata) -> None:
        search = client.searches.search_similar()
        assert_matches_type(SimilarSearchResponse, search, path=["response"])

    @parametrize
    def test_method_search_similar_with_all_params(self, client: Grata) -> None:
        search = client.searches.search_similar(
            business_models=["software"],
            company_uid="company_uid",
            domain="domain",
            employees_change=[-50],
            employees_change_time="month",
            employees_on_professional_networks_range=[0],
            end_customer=["b2b"],
            funding_size=[0, 0],
            funding_stage=["early_stage_funding"],
            grata_employees_estimates_range=[0],
            group_operator="any",
            headquarters={
                "exclude": [
                    {
                        "city": "city",
                        "country": "country",
                        "state": "state",
                    }
                ],
                "include": [
                    {
                        "city": "city",
                        "country": "country",
                        "state": "state",
                    }
                ],
            },
            industry_classifications={
                "exclude": [0],
                "include": [0],
            },
            is_funded=True,
            lists={
                "exclude": ["string"],
                "include": ["string"],
            },
            ownership=["bootstrapped"],
            page_token="page_token",
            terms_exclude=["string"],
            terms_include={
                "groups": [
                    {
                        "terms": ["string"],
                        "terms_depth": "core",
                        "terms_operator": "any",
                    }
                ]
            },
            year_founded=[1959],
        )
        assert_matches_type(SimilarSearchResponse, search, path=["response"])

    @parametrize
    def test_raw_response_search_similar(self, client: Grata) -> None:
        response = client.searches.with_raw_response.search_similar()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(SimilarSearchResponse, search, path=["response"])

    @parametrize
    def test_streaming_response_search_similar(self, client: Grata) -> None:
        with client.searches.with_streaming_response.search_similar() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(SimilarSearchResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSearches:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_search(self, async_client: AsyncGrata) -> None:
        search = await async_client.searches.search()
        assert_matches_type(SearchResponse, search, path=["response"])

    @parametrize
    async def test_method_search_with_all_params(self, async_client: AsyncGrata) -> None:
        search = await async_client.searches.search(
            business_models=["software"],
            employees_change=[-50],
            employees_change_time="month",
            employees_on_professional_networks_range=[0],
            end_customer=["b2b"],
            funding_size=[0, 0],
            funding_stage=["early_stage_funding"],
            grata_employees_estimates_range=[0],
            group_operator="any",
            headquarters={
                "exclude": [
                    {
                        "city": "city",
                        "country": "country",
                        "state": "state",
                    }
                ],
                "include": [
                    {
                        "city": "city",
                        "country": "country",
                        "state": "state",
                    }
                ],
            },
            industry_classifications={
                "exclude": [0],
                "include": [0],
            },
            is_funded=True,
            lists={
                "exclude": ["string"],
                "include": ["string"],
            },
            ownership=["bootstrapped"],
            page_token="page_token",
            terms_exclude=["string"],
            terms_include={
                "groups": [
                    {
                        "terms": ["string"],
                        "terms_depth": "core",
                        "terms_operator": "any",
                    }
                ]
            },
            year_founded=[1959],
        )
        assert_matches_type(SearchResponse, search, path=["response"])

    @parametrize
    async def test_raw_response_search(self, async_client: AsyncGrata) -> None:
        response = await async_client.searches.with_raw_response.search()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(SearchResponse, search, path=["response"])

    @parametrize
    async def test_streaming_response_search(self, async_client: AsyncGrata) -> None:
        async with async_client.searches.with_streaming_response.search() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(SearchResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_search_similar(self, async_client: AsyncGrata) -> None:
        search = await async_client.searches.search_similar()
        assert_matches_type(SimilarSearchResponse, search, path=["response"])

    @parametrize
    async def test_method_search_similar_with_all_params(self, async_client: AsyncGrata) -> None:
        search = await async_client.searches.search_similar(
            business_models=["software"],
            company_uid="company_uid",
            domain="domain",
            employees_change=[-50],
            employees_change_time="month",
            employees_on_professional_networks_range=[0],
            end_customer=["b2b"],
            funding_size=[0, 0],
            funding_stage=["early_stage_funding"],
            grata_employees_estimates_range=[0],
            group_operator="any",
            headquarters={
                "exclude": [
                    {
                        "city": "city",
                        "country": "country",
                        "state": "state",
                    }
                ],
                "include": [
                    {
                        "city": "city",
                        "country": "country",
                        "state": "state",
                    }
                ],
            },
            industry_classifications={
                "exclude": [0],
                "include": [0],
            },
            is_funded=True,
            lists={
                "exclude": ["string"],
                "include": ["string"],
            },
            ownership=["bootstrapped"],
            page_token="page_token",
            terms_exclude=["string"],
            terms_include={
                "groups": [
                    {
                        "terms": ["string"],
                        "terms_depth": "core",
                        "terms_operator": "any",
                    }
                ]
            },
            year_founded=[1959],
        )
        assert_matches_type(SimilarSearchResponse, search, path=["response"])

    @parametrize
    async def test_raw_response_search_similar(self, async_client: AsyncGrata) -> None:
        response = await async_client.searches.with_raw_response.search_similar()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(SimilarSearchResponse, search, path=["response"])

    @parametrize
    async def test_streaming_response_search_similar(self, async_client: AsyncGrata) -> None:
        async with async_client.searches.with_streaming_response.search_similar() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(SimilarSearchResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True
