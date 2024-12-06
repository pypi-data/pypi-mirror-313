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
from ....types.ref.hotspot import geo_retrieve_params
from ....types.ref.hotspot.geo_retrieve_response import GeoRetrieveResponse

__all__ = ["GeoResource", "AsyncGeoResource"]


class GeoResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> GeoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return GeoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> GeoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return GeoResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        lat: float,
        lng: float,
        back: int | NotGiven = NOT_GIVEN,
        dist: int | NotGiven = NOT_GIVEN,
        fmt: Literal["csv", "json"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GeoRetrieveResponse:
        """
        Get the list of hotspots, within a radius of up to 50 kilometers, from a given
        set of coordinates.

        Args:
          back: The number of days back to fetch hotspots.

          dist: The search radius from the given position, in kilometers.

          fmt: Fetch the records in CSV or JSON format.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/ref/hotspot/geo",
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
                        "dist": dist,
                        "fmt": fmt,
                    },
                    geo_retrieve_params.GeoRetrieveParams,
                ),
            ),
            cast_to=GeoRetrieveResponse,
        )


class AsyncGeoResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncGeoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncGeoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncGeoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncGeoResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        lat: float,
        lng: float,
        back: int | NotGiven = NOT_GIVEN,
        dist: int | NotGiven = NOT_GIVEN,
        fmt: Literal["csv", "json"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GeoRetrieveResponse:
        """
        Get the list of hotspots, within a radius of up to 50 kilometers, from a given
        set of coordinates.

        Args:
          back: The number of days back to fetch hotspots.

          dist: The search radius from the given position, in kilometers.

          fmt: Fetch the records in CSV or JSON format.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/ref/hotspot/geo",
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
                        "dist": dist,
                        "fmt": fmt,
                    },
                    geo_retrieve_params.GeoRetrieveParams,
                ),
            ),
            cast_to=GeoRetrieveResponse,
        )


class GeoResourceWithRawResponse:
    def __init__(self, geo: GeoResource) -> None:
        self._geo = geo

        self.retrieve = to_raw_response_wrapper(
            geo.retrieve,
        )


class AsyncGeoResourceWithRawResponse:
    def __init__(self, geo: AsyncGeoResource) -> None:
        self._geo = geo

        self.retrieve = async_to_raw_response_wrapper(
            geo.retrieve,
        )


class GeoResourceWithStreamingResponse:
    def __init__(self, geo: GeoResource) -> None:
        self._geo = geo

        self.retrieve = to_streamed_response_wrapper(
            geo.retrieve,
        )


class AsyncGeoResourceWithStreamingResponse:
    def __init__(self, geo: AsyncGeoResource) -> None:
        self._geo = geo

        self.retrieve = async_to_streamed_response_wrapper(
            geo.retrieve,
        )
