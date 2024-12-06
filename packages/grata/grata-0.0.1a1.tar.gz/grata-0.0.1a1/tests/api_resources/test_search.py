# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from grata import Grata, AsyncGrata
from grata.types import CompanyBasic
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSearch:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Grata) -> None:
        search = client.search.create(
            authorization="Authorization",
        )
        assert_matches_type(CompanyBasic, search, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Grata) -> None:
        search = client.search.create(
            authorization="Authorization",
            business_models=["software"],
            company_uid="26AJRCR2",
            domain="slack.com",
            employees_change=[-50],
            employees_change_time="month",
            employees_on_professional_networks_range=[0],
            end_customer=["b2b", "b2c"],
            funding_size=[0, 100000000],
            funding_stage=["early_stage_funding"],
            grata_employees_estimates_range=[10, 100],
            headquarters={
                "exclude": [
                    {
                        "city": "New York",
                        "country": "United States",
                        "state": "New York",
                    }
                ],
                "include": [
                    {
                        "city": "Los Angeles ",
                        "country": "United States",
                        "state": "California",
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
            page_token="",
            terms_exclude=["string"],
            terms_include={
                "group_operator": "any",
                "groups": [
                    {
                        "terms": ["messaging"],
                        "terms_depth": "core",
                        "terms_operator": "any",
                    }
                ],
            },
            year_founded=[1970, 2018],
        )
        assert_matches_type(CompanyBasic, search, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Grata) -> None:
        response = client.search.with_raw_response.create(
            authorization="Authorization",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(CompanyBasic, search, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Grata) -> None:
        with client.search.with_streaming_response.create(
            authorization="Authorization",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(CompanyBasic, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_similar(self, client: Grata) -> None:
        search = client.search.similar(
            authorization="Authorization",
        )
        assert_matches_type(CompanyBasic, search, path=["response"])

    @parametrize
    def test_method_similar_with_all_params(self, client: Grata) -> None:
        search = client.search.similar(
            authorization="Authorization",
            business_models=["software"],
            company_uid="26AJRCR2",
            domain="slack.com",
            employees_change=[-50],
            employees_change_time="month",
            employees_on_professional_networks_range=[0],
            end_customer=["b2b", "b2c"],
            funding_size=[0, 100000000],
            funding_stage=["early_stage_funding"],
            grata_employees_estimates_range=[10, 100],
            headquarters={
                "exclude": [
                    {
                        "city": "New York",
                        "country": "United States",
                        "state": "New York",
                    }
                ],
                "include": [
                    {
                        "city": "Los Angeles ",
                        "country": "United States",
                        "state": "California",
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
            page_token="",
            terms_exclude=["string"],
            terms_include={
                "group_operator": "any",
                "groups": [
                    {
                        "terms": ["messaging"],
                        "terms_depth": "core",
                        "terms_operator": "any",
                    }
                ],
            },
            year_founded=[1970, 2018],
        )
        assert_matches_type(CompanyBasic, search, path=["response"])

    @parametrize
    def test_raw_response_similar(self, client: Grata) -> None:
        response = client.search.with_raw_response.similar(
            authorization="Authorization",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(CompanyBasic, search, path=["response"])

    @parametrize
    def test_streaming_response_similar(self, client: Grata) -> None:
        with client.search.with_streaming_response.similar(
            authorization="Authorization",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(CompanyBasic, search, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSearch:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncGrata) -> None:
        search = await async_client.search.create(
            authorization="Authorization",
        )
        assert_matches_type(CompanyBasic, search, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncGrata) -> None:
        search = await async_client.search.create(
            authorization="Authorization",
            business_models=["software"],
            company_uid="26AJRCR2",
            domain="slack.com",
            employees_change=[-50],
            employees_change_time="month",
            employees_on_professional_networks_range=[0],
            end_customer=["b2b", "b2c"],
            funding_size=[0, 100000000],
            funding_stage=["early_stage_funding"],
            grata_employees_estimates_range=[10, 100],
            headquarters={
                "exclude": [
                    {
                        "city": "New York",
                        "country": "United States",
                        "state": "New York",
                    }
                ],
                "include": [
                    {
                        "city": "Los Angeles ",
                        "country": "United States",
                        "state": "California",
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
            page_token="",
            terms_exclude=["string"],
            terms_include={
                "group_operator": "any",
                "groups": [
                    {
                        "terms": ["messaging"],
                        "terms_depth": "core",
                        "terms_operator": "any",
                    }
                ],
            },
            year_founded=[1970, 2018],
        )
        assert_matches_type(CompanyBasic, search, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncGrata) -> None:
        response = await async_client.search.with_raw_response.create(
            authorization="Authorization",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(CompanyBasic, search, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncGrata) -> None:
        async with async_client.search.with_streaming_response.create(
            authorization="Authorization",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(CompanyBasic, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_similar(self, async_client: AsyncGrata) -> None:
        search = await async_client.search.similar(
            authorization="Authorization",
        )
        assert_matches_type(CompanyBasic, search, path=["response"])

    @parametrize
    async def test_method_similar_with_all_params(self, async_client: AsyncGrata) -> None:
        search = await async_client.search.similar(
            authorization="Authorization",
            business_models=["software"],
            company_uid="26AJRCR2",
            domain="slack.com",
            employees_change=[-50],
            employees_change_time="month",
            employees_on_professional_networks_range=[0],
            end_customer=["b2b", "b2c"],
            funding_size=[0, 100000000],
            funding_stage=["early_stage_funding"],
            grata_employees_estimates_range=[10, 100],
            headquarters={
                "exclude": [
                    {
                        "city": "New York",
                        "country": "United States",
                        "state": "New York",
                    }
                ],
                "include": [
                    {
                        "city": "Los Angeles ",
                        "country": "United States",
                        "state": "California",
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
            page_token="",
            terms_exclude=["string"],
            terms_include={
                "group_operator": "any",
                "groups": [
                    {
                        "terms": ["messaging"],
                        "terms_depth": "core",
                        "terms_operator": "any",
                    }
                ],
            },
            year_founded=[1970, 2018],
        )
        assert_matches_type(CompanyBasic, search, path=["response"])

    @parametrize
    async def test_raw_response_similar(self, async_client: AsyncGrata) -> None:
        response = await async_client.search.with_raw_response.similar(
            authorization="Authorization",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(CompanyBasic, search, path=["response"])

    @parametrize
    async def test_streaming_response_similar(self, async_client: AsyncGrata) -> None:
        async with async_client.search.with_streaming_response.similar(
            authorization="Authorization",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(CompanyBasic, search, path=["response"])

        assert cast(Any, response.is_closed) is True
