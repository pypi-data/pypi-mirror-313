# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.ref.region.adjacent_list_response import AdjacentListResponse

__all__ = ["AdjacentResource", "AsyncAdjacentResource"]


class AdjacentResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AdjacentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AdjacentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AdjacentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AdjacentResourceWithStreamingResponse(self)

    def list(
        self,
        region_code: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AdjacentListResponse:
        """Get the list of countries or regions that share a border with this one.

        ####
        Notes Only subnational2 codes in the United States, New Zealand, or Mexico are
        currently supported

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not region_code:
            raise ValueError(f"Expected a non-empty value for `region_code` but received {region_code!r}")
        return self._get(
            f"/ref/adjacent/{region_code}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AdjacentListResponse,
        )


class AsyncAdjacentResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAdjacentResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAdjacentResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAdjacentResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncAdjacentResourceWithStreamingResponse(self)

    async def list(
        self,
        region_code: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AdjacentListResponse:
        """Get the list of countries or regions that share a border with this one.

        ####
        Notes Only subnational2 codes in the United States, New Zealand, or Mexico are
        currently supported

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not region_code:
            raise ValueError(f"Expected a non-empty value for `region_code` but received {region_code!r}")
        return await self._get(
            f"/ref/adjacent/{region_code}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AdjacentListResponse,
        )


class AdjacentResourceWithRawResponse:
    def __init__(self, adjacent: AdjacentResource) -> None:
        self._adjacent = adjacent

        self.list = to_raw_response_wrapper(
            adjacent.list,
        )


class AsyncAdjacentResourceWithRawResponse:
    def __init__(self, adjacent: AsyncAdjacentResource) -> None:
        self._adjacent = adjacent

        self.list = async_to_raw_response_wrapper(
            adjacent.list,
        )


class AdjacentResourceWithStreamingResponse:
    def __init__(self, adjacent: AdjacentResource) -> None:
        self._adjacent = adjacent

        self.list = to_streamed_response_wrapper(
            adjacent.list,
        )


class AsyncAdjacentResourceWithStreamingResponse:
    def __init__(self, adjacent: AsyncAdjacentResource) -> None:
        self._adjacent = adjacent

        self.list = async_to_streamed_response_wrapper(
            adjacent.list,
        )
