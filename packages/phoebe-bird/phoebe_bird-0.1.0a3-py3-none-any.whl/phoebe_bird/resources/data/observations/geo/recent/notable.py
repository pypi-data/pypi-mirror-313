# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ......_types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ......_utils import (
    maybe_transform,
    async_maybe_transform,
)
from ......_compat import cached_property
from ......_resource import SyncAPIResource, AsyncAPIResource
from ......_response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ......_base_client import make_request_options
from ......types.data.observations.geo.recent import notable_list_params
from ......types.data.observations.geo.recent.notable_list_response import NotableListResponse

__all__ = ["NotableResource", "AsyncNotableResource"]


class NotableResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> NotableResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return NotableResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> NotableResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return NotableResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        lat: float,
        lng: float,
        back: int | NotGiven = NOT_GIVEN,
        detail: Literal["simple", "full"] | NotGiven = NOT_GIVEN,
        dist: int | NotGiven = NOT_GIVEN,
        hotspot: bool | NotGiven = NOT_GIVEN,
        max_results: int | NotGiven = NOT_GIVEN,
        spp_locale: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NotableListResponse:
        """
        Get the list of notable observations (up to 30 days ago) of birds seen at
        locations within a radius of up to 50 kilometers, from a given set of
        coordinates. Notable observations can be for locally or nationally rare species
        or are otherwise unusual, for example over-wintering birds in a species which is
        normally only a summer visitor.

        Args:
          back: The number of days back to fetch observations.

          detail: Include a subset (simple), or all (full), of the fields available.

          dist: The search radius from the given position, in kilometers.

          hotspot: Only fetch observations from hotspots

          max_results: Only fetch this number of observations

          spp_locale: Use this language for species common names

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/data/obs/geo/recent/notable",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "lat": lat,
                        "lng": lng,
                        "back": back,
                        "detail": detail,
                        "dist": dist,
                        "hotspot": hotspot,
                        "max_results": max_results,
                        "spp_locale": spp_locale,
                    },
                    notable_list_params.NotableListParams,
                ),
            ),
            cast_to=NotableListResponse,
        )


class AsyncNotableResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncNotableResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncNotableResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncNotableResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncNotableResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        lat: float,
        lng: float,
        back: int | NotGiven = NOT_GIVEN,
        detail: Literal["simple", "full"] | NotGiven = NOT_GIVEN,
        dist: int | NotGiven = NOT_GIVEN,
        hotspot: bool | NotGiven = NOT_GIVEN,
        max_results: int | NotGiven = NOT_GIVEN,
        spp_locale: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NotableListResponse:
        """
        Get the list of notable observations (up to 30 days ago) of birds seen at
        locations within a radius of up to 50 kilometers, from a given set of
        coordinates. Notable observations can be for locally or nationally rare species
        or are otherwise unusual, for example over-wintering birds in a species which is
        normally only a summer visitor.

        Args:
          back: The number of days back to fetch observations.

          detail: Include a subset (simple), or all (full), of the fields available.

          dist: The search radius from the given position, in kilometers.

          hotspot: Only fetch observations from hotspots

          max_results: Only fetch this number of observations

          spp_locale: Use this language for species common names

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/data/obs/geo/recent/notable",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "lat": lat,
                        "lng": lng,
                        "back": back,
                        "detail": detail,
                        "dist": dist,
                        "hotspot": hotspot,
                        "max_results": max_results,
                        "spp_locale": spp_locale,
                    },
                    notable_list_params.NotableListParams,
                ),
            ),
            cast_to=NotableListResponse,
        )


class NotableResourceWithRawResponse:
    def __init__(self, notable: NotableResource) -> None:
        self._notable = notable

        self.list = to_raw_response_wrapper(
            notable.list,
        )


class AsyncNotableResourceWithRawResponse:
    def __init__(self, notable: AsyncNotableResource) -> None:
        self._notable = notable

        self.list = async_to_raw_response_wrapper(
            notable.list,
        )


class NotableResourceWithStreamingResponse:
    def __init__(self, notable: NotableResource) -> None:
        self._notable = notable

        self.list = to_streamed_response_wrapper(
            notable.list,
        )


class AsyncNotableResourceWithStreamingResponse:
    def __init__(self, notable: AsyncNotableResource) -> None:
        self._notable = notable

        self.list = async_to_streamed_response_wrapper(
            notable.list,
        )
