# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from grata import Grata, AsyncGrata
from tests.utils import assert_matches_type
from grata.types.shared import CompanyDetailed

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestLists:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Grata) -> None:
        list_ = client.lists.create(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Grata) -> None:
        list_ = client.lists.create(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
            name="New List",
        )
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Grata) -> None:
        response = client.lists.with_raw_response.create(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        list_ = response.parse()
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Grata) -> None:
        with client.lists.with_streaming_response.create(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            list_ = response.parse()
            assert_matches_type(CompanyDetailed, list_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Grata) -> None:
        list_ = client.lists.retrieve(
            list_uid="ZTZGNNT7",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Grata) -> None:
        response = client.lists.with_raw_response.retrieve(
            list_uid="ZTZGNNT7",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        list_ = response.parse()
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Grata) -> None:
        with client.lists.with_streaming_response.retrieve(
            list_uid="ZTZGNNT7",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            list_ = response.parse()
            assert_matches_type(CompanyDetailed, list_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Grata) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `list_uid` but received ''"):
            client.lists.with_raw_response.retrieve(
                list_uid="",
                authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
            )

    @parametrize
    def test_method_update(self, client: Grata) -> None:
        list_ = client.lists.update(
            list_uid="XY2Z8V23",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: Grata) -> None:
        list_ = client.lists.update(
            list_uid="XY2Z8V23",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
            name="New List Name",
        )
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: Grata) -> None:
        response = client.lists.with_raw_response.update(
            list_uid="XY2Z8V23",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        list_ = response.parse()
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: Grata) -> None:
        with client.lists.with_streaming_response.update(
            list_uid="XY2Z8V23",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            list_ = response.parse()
            assert_matches_type(CompanyDetailed, list_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: Grata) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `list_uid` but received ''"):
            client.lists.with_raw_response.update(
                list_uid="",
                authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
            )

    @parametrize
    def test_method_list(self, client: Grata) -> None:
        list_ = client.lists.list(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Grata) -> None:
        list_ = client.lists.list(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
            name="name=List%20A",
            page="page=2",
        )
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Grata) -> None:
        response = client.lists.with_raw_response.list(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        list_ = response.parse()
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Grata) -> None:
        with client.lists.with_streaming_response.list(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            list_ = response.parse()
            assert_matches_type(CompanyDetailed, list_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Grata) -> None:
        list_ = client.lists.delete(
            list_uid="XY2Z8V23",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )
        assert list_ is None

    @parametrize
    def test_raw_response_delete(self, client: Grata) -> None:
        response = client.lists.with_raw_response.delete(
            list_uid="XY2Z8V23",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        list_ = response.parse()
        assert list_ is None

    @parametrize
    def test_streaming_response_delete(self, client: Grata) -> None:
        with client.lists.with_streaming_response.delete(
            list_uid="XY2Z8V23",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            list_ = response.parse()
            assert list_ is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Grata) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `list_uid` but received ''"):
            client.lists.with_raw_response.delete(
                list_uid="",
                authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
            )

    @parametrize
    def test_method_companies(self, client: Grata) -> None:
        list_ = client.lists.companies(
            list_uid="XYZ12345",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    def test_method_companies_with_all_params(self, client: Grata) -> None:
        list_ = client.lists.companies(
            list_uid="XYZ12345",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
            action="add",
            domains=["grata.com"],
            uids=["XYZ12356"],
        )
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    def test_raw_response_companies(self, client: Grata) -> None:
        response = client.lists.with_raw_response.companies(
            list_uid="XYZ12345",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        list_ = response.parse()
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    def test_streaming_response_companies(self, client: Grata) -> None:
        with client.lists.with_streaming_response.companies(
            list_uid="XYZ12345",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            list_ = response.parse()
            assert_matches_type(CompanyDetailed, list_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_companies(self, client: Grata) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `list_uid` but received ''"):
            client.lists.with_raw_response.companies(
                list_uid="",
                authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
            )


class TestAsyncLists:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncGrata) -> None:
        list_ = await async_client.lists.create(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncGrata) -> None:
        list_ = await async_client.lists.create(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
            name="New List",
        )
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncGrata) -> None:
        response = await async_client.lists.with_raw_response.create(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        list_ = await response.parse()
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncGrata) -> None:
        async with async_client.lists.with_streaming_response.create(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            list_ = await response.parse()
            assert_matches_type(CompanyDetailed, list_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncGrata) -> None:
        list_ = await async_client.lists.retrieve(
            list_uid="ZTZGNNT7",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncGrata) -> None:
        response = await async_client.lists.with_raw_response.retrieve(
            list_uid="ZTZGNNT7",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        list_ = await response.parse()
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncGrata) -> None:
        async with async_client.lists.with_streaming_response.retrieve(
            list_uid="ZTZGNNT7",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            list_ = await response.parse()
            assert_matches_type(CompanyDetailed, list_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncGrata) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `list_uid` but received ''"):
            await async_client.lists.with_raw_response.retrieve(
                list_uid="",
                authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncGrata) -> None:
        list_ = await async_client.lists.update(
            list_uid="XY2Z8V23",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncGrata) -> None:
        list_ = await async_client.lists.update(
            list_uid="XY2Z8V23",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
            name="New List Name",
        )
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncGrata) -> None:
        response = await async_client.lists.with_raw_response.update(
            list_uid="XY2Z8V23",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        list_ = await response.parse()
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncGrata) -> None:
        async with async_client.lists.with_streaming_response.update(
            list_uid="XY2Z8V23",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            list_ = await response.parse()
            assert_matches_type(CompanyDetailed, list_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncGrata) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `list_uid` but received ''"):
            await async_client.lists.with_raw_response.update(
                list_uid="",
                authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncGrata) -> None:
        list_ = await async_client.lists.list(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncGrata) -> None:
        list_ = await async_client.lists.list(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
            name="name=List%20A",
            page="page=2",
        )
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncGrata) -> None:
        response = await async_client.lists.with_raw_response.list(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        list_ = await response.parse()
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncGrata) -> None:
        async with async_client.lists.with_streaming_response.list(
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            list_ = await response.parse()
            assert_matches_type(CompanyDetailed, list_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncGrata) -> None:
        list_ = await async_client.lists.delete(
            list_uid="XY2Z8V23",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )
        assert list_ is None

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncGrata) -> None:
        response = await async_client.lists.with_raw_response.delete(
            list_uid="XY2Z8V23",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        list_ = await response.parse()
        assert list_ is None

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncGrata) -> None:
        async with async_client.lists.with_streaming_response.delete(
            list_uid="XY2Z8V23",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            list_ = await response.parse()
            assert list_ is None

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncGrata) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `list_uid` but received ''"):
            await async_client.lists.with_raw_response.delete(
                list_uid="",
                authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
            )

    @parametrize
    async def test_method_companies(self, async_client: AsyncGrata) -> None:
        list_ = await async_client.lists.companies(
            list_uid="XYZ12345",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    async def test_method_companies_with_all_params(self, async_client: AsyncGrata) -> None:
        list_ = await async_client.lists.companies(
            list_uid="XYZ12345",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
            action="add",
            domains=["grata.com"],
            uids=["XYZ12356"],
        )
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    async def test_raw_response_companies(self, async_client: AsyncGrata) -> None:
        response = await async_client.lists.with_raw_response.companies(
            list_uid="XYZ12345",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        list_ = await response.parse()
        assert_matches_type(CompanyDetailed, list_, path=["response"])

    @parametrize
    async def test_streaming_response_companies(self, async_client: AsyncGrata) -> None:
        async with async_client.lists.with_streaming_response.companies(
            list_uid="XYZ12345",
            authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            list_ = await response.parse()
            assert_matches_type(CompanyDetailed, list_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_companies(self, async_client: AsyncGrata) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `list_uid` but received ''"):
            await async_client.lists.with_raw_response.companies(
                list_uid="",
                authorization="Token 840cda398b02093940807af4885853500c1cf5bb",
            )
