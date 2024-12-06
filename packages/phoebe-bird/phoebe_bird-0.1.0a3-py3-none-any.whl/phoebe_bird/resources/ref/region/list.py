# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.ref.region import list_list_params
from ....types.ref.region.list_list_response import ListListResponse

__all__ = ["ListResource", "AsyncListResource"]


class ListResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ListResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return ListResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ListResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return ListResourceWithStreamingResponse(self)

    def list(
        self,
        parent_region_code: str,
        *,
        region_type: str,
        fmt: Literal["csv", "json"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListListResponse:
        """Get the list of sub-regions for a given country or region.

        #### Notes Not all
        combinations of region type and region code are valid. You can fetch all the
        subnational1 or subnational2 regions for a country however you can only specify
        a region type of 'country' when using 'world' as a region code.

        Args:
          fmt: Fetch the records in CSV or JSON format.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not region_type:
            raise ValueError(f"Expected a non-empty value for `region_type` but received {region_type!r}")
        if not parent_region_code:
            raise ValueError(f"Expected a non-empty value for `parent_region_code` but received {parent_region_code!r}")
        return self._get(
            f"/ref/region/list/{region_type}/{parent_region_code}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"fmt": fmt}, list_list_params.ListListParams),
            ),
            cast_to=ListListResponse,
        )


class AsyncListResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncListResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncListResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncListResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncListResourceWithStreamingResponse(self)

    async def list(
        self,
        parent_region_code: str,
        *,
        region_type: str,
        fmt: Literal["csv", "json"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ListListResponse:
        """Get the list of sub-regions for a given country or region.

        #### Notes Not all
        combinations of region type and region code are valid. You can fetch all the
        subnational1 or subnational2 regions for a country however you can only specify
        a region type of 'country' when using 'world' as a region code.

        Args:
          fmt: Fetch the records in CSV or JSON format.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not region_type:
            raise ValueError(f"Expected a non-empty value for `region_type` but received {region_type!r}")
        if not parent_region_code:
            raise ValueError(f"Expected a non-empty value for `parent_region_code` but received {parent_region_code!r}")
        return await self._get(
            f"/ref/region/list/{region_type}/{parent_region_code}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"fmt": fmt}, list_list_params.ListListParams),
            ),
            cast_to=ListListResponse,
        )


class ListResourceWithRawResponse:
    def __init__(self, list: ListResource) -> None:
        self._list = list

        self.list = to_raw_response_wrapper(
            list.list,
        )


class AsyncListResourceWithRawResponse:
    def __init__(self, list: AsyncListResource) -> None:
        self._list = list

        self.list = async_to_raw_response_wrapper(
            list.list,
        )


class ListResourceWithStreamingResponse:
    def __init__(self, list: ListResource) -> None:
        self._list = list

        self.list = to_streamed_response_wrapper(
            list.list,
        )


class AsyncListResourceWithStreamingResponse:
    def __init__(self, list: AsyncListResource) -> None:
        self._list = list

        self.list = async_to_streamed_response_wrapper(
            list.list,
        )
