# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import list_list_params, list_create_params, list_update_params, list_companies_params
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
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
from ..types.shared.company_detailed import CompanyDetailed

__all__ = ["ListsResource", "AsyncListsResource"]


class ListsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ListsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TJC-LP/grata-python#accessing-raw-response-data-eg-headers
        """
        return ListsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ListsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TJC-LP/grata-python#with_streaming_response
        """
        return ListsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        authorization: str,
        name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyDetailed:
        """The create call will allow users to create a list in Grata.

        The list visibility
        will be set to organization and it will be visible in the Grata UI for all users
        within the account to view.

        Args:
          name: Name of list being created

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Authorization": authorization, **(extra_headers or {})}
        return self._post(
            "/api/v1.4/lists/",
            body=maybe_transform({"name": name}, list_create_params.ListCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyDetailed,
        )

    def retrieve(
        self,
        list_uid: str,
        *,
        authorization: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyDetailed:
        """
        Grata's List Details API returns details about the lists in your organization.
        Private lists will not be returned with this call.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not list_uid:
            raise ValueError(f"Expected a non-empty value for `list_uid` but received {list_uid!r}")
        extra_headers = {"Authorization": authorization, **(extra_headers or {})}
        return self._get(
            f"/api/v1.4/lists/{list_uid}/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyDetailed,
        )

    def update(
        self,
        list_uid: str,
        *,
        authorization: str,
        name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyDetailed:
        """Grata's List Name API updates the name of a list.

        Private lists are not eligible
        to be updated with this call.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not list_uid:
            raise ValueError(f"Expected a non-empty value for `list_uid` but received {list_uid!r}")
        extra_headers = {"Authorization": authorization, **(extra_headers or {})}
        return self._patch(
            f"/api/v1.4/lists/{list_uid}/",
            body=maybe_transform({"name": name}, list_update_params.ListUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyDetailed,
        )

    def list(
        self,
        *,
        authorization: str,
        name: str | NotGiven = NOT_GIVEN,
        page: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyDetailed:
        """
        Grata's Search Lists API enables you to search for and return details about the
        lists in your organization. Private lists will not be returned with this call.

        Args:
          name: List name

          page: The page of results to be returned

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Authorization": authorization, **(extra_headers or {})}
        return self._get(
            "/api/v1.4/lists/",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "name": name,
                        "page": page,
                    },
                    list_list_params.ListListParams,
                ),
            ),
            cast_to=CompanyDetailed,
        )

    def delete(
        self,
        list_uid: str,
        *,
        authorization: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete List

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not list_uid:
            raise ValueError(f"Expected a non-empty value for `list_uid` but received {list_uid!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"Authorization": authorization})
        return self._delete(
            f"/api/v1.4/lists/{list_uid}/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def companies(
        self,
        list_uid: str,
        *,
        authorization: str,
        action: Literal["add", "remove"] | NotGiven = NOT_GIVEN,
        domains: List[str] | NotGiven = NOT_GIVEN,
        uids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyDetailed:
        """
        The modify call will allow users to add or remove companies from an exisiting
        list. Private lists are not eligible to be updated with this call.

        Args:
          domains: Domains to add or remove from a list (max of 500 permitted per call).

          uids: Grata company UIDs to add or remove from a list (max of 500 permitted per call).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not list_uid:
            raise ValueError(f"Expected a non-empty value for `list_uid` but received {list_uid!r}")
        extra_headers = {"Authorization": authorization, **(extra_headers or {})}
        return self._post(
            f"/api/v1.4/lists/{list_uid}/companies/",
            body=maybe_transform(
                {
                    "action": action,
                    "domains": domains,
                    "uids": uids,
                },
                list_companies_params.ListCompaniesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyDetailed,
        )


class AsyncListsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncListsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/TJC-LP/grata-python#accessing-raw-response-data-eg-headers
        """
        return AsyncListsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncListsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/TJC-LP/grata-python#with_streaming_response
        """
        return AsyncListsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        authorization: str,
        name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyDetailed:
        """The create call will allow users to create a list in Grata.

        The list visibility
        will be set to organization and it will be visible in the Grata UI for all users
        within the account to view.

        Args:
          name: Name of list being created

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Authorization": authorization, **(extra_headers or {})}
        return await self._post(
            "/api/v1.4/lists/",
            body=await async_maybe_transform({"name": name}, list_create_params.ListCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyDetailed,
        )

    async def retrieve(
        self,
        list_uid: str,
        *,
        authorization: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyDetailed:
        """
        Grata's List Details API returns details about the lists in your organization.
        Private lists will not be returned with this call.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not list_uid:
            raise ValueError(f"Expected a non-empty value for `list_uid` but received {list_uid!r}")
        extra_headers = {"Authorization": authorization, **(extra_headers or {})}
        return await self._get(
            f"/api/v1.4/lists/{list_uid}/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyDetailed,
        )

    async def update(
        self,
        list_uid: str,
        *,
        authorization: str,
        name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyDetailed:
        """Grata's List Name API updates the name of a list.

        Private lists are not eligible
        to be updated with this call.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not list_uid:
            raise ValueError(f"Expected a non-empty value for `list_uid` but received {list_uid!r}")
        extra_headers = {"Authorization": authorization, **(extra_headers or {})}
        return await self._patch(
            f"/api/v1.4/lists/{list_uid}/",
            body=await async_maybe_transform({"name": name}, list_update_params.ListUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyDetailed,
        )

    async def list(
        self,
        *,
        authorization: str,
        name: str | NotGiven = NOT_GIVEN,
        page: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyDetailed:
        """
        Grata's Search Lists API enables you to search for and return details about the
        lists in your organization. Private lists will not be returned with this call.

        Args:
          name: List name

          page: The page of results to be returned

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Authorization": authorization, **(extra_headers or {})}
        return await self._get(
            "/api/v1.4/lists/",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "name": name,
                        "page": page,
                    },
                    list_list_params.ListListParams,
                ),
            ),
            cast_to=CompanyDetailed,
        )

    async def delete(
        self,
        list_uid: str,
        *,
        authorization: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete List

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not list_uid:
            raise ValueError(f"Expected a non-empty value for `list_uid` but received {list_uid!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        extra_headers.update({"Authorization": authorization})
        return await self._delete(
            f"/api/v1.4/lists/{list_uid}/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def companies(
        self,
        list_uid: str,
        *,
        authorization: str,
        action: Literal["add", "remove"] | NotGiven = NOT_GIVEN,
        domains: List[str] | NotGiven = NOT_GIVEN,
        uids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CompanyDetailed:
        """
        The modify call will allow users to add or remove companies from an exisiting
        list. Private lists are not eligible to be updated with this call.

        Args:
          domains: Domains to add or remove from a list (max of 500 permitted per call).

          uids: Grata company UIDs to add or remove from a list (max of 500 permitted per call).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not list_uid:
            raise ValueError(f"Expected a non-empty value for `list_uid` but received {list_uid!r}")
        extra_headers = {"Authorization": authorization, **(extra_headers or {})}
        return await self._post(
            f"/api/v1.4/lists/{list_uid}/companies/",
            body=await async_maybe_transform(
                {
                    "action": action,
                    "domains": domains,
                    "uids": uids,
                },
                list_companies_params.ListCompaniesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompanyDetailed,
        )


class ListsResourceWithRawResponse:
    def __init__(self, lists: ListsResource) -> None:
        self._lists = lists

        self.create = to_raw_response_wrapper(
            lists.create,
        )
        self.retrieve = to_raw_response_wrapper(
            lists.retrieve,
        )
        self.update = to_raw_response_wrapper(
            lists.update,
        )
        self.list = to_raw_response_wrapper(
            lists.list,
        )
        self.delete = to_raw_response_wrapper(
            lists.delete,
        )
        self.companies = to_raw_response_wrapper(
            lists.companies,
        )


class AsyncListsResourceWithRawResponse:
    def __init__(self, lists: AsyncListsResource) -> None:
        self._lists = lists

        self.create = async_to_raw_response_wrapper(
            lists.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            lists.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            lists.update,
        )
        self.list = async_to_raw_response_wrapper(
            lists.list,
        )
        self.delete = async_to_raw_response_wrapper(
            lists.delete,
        )
        self.companies = async_to_raw_response_wrapper(
            lists.companies,
        )


class ListsResourceWithStreamingResponse:
    def __init__(self, lists: ListsResource) -> None:
        self._lists = lists

        self.create = to_streamed_response_wrapper(
            lists.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            lists.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            lists.update,
        )
        self.list = to_streamed_response_wrapper(
            lists.list,
        )
        self.delete = to_streamed_response_wrapper(
            lists.delete,
        )
        self.companies = to_streamed_response_wrapper(
            lists.companies,
        )


class AsyncListsResourceWithStreamingResponse:
    def __init__(self, lists: AsyncListsResource) -> None:
        self._lists = lists

        self.create = async_to_streamed_response_wrapper(
            lists.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            lists.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            lists.update,
        )
        self.list = async_to_streamed_response_wrapper(
            lists.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            lists.delete,
        )
        self.companies = async_to_streamed_response_wrapper(
            lists.companies,
        )
