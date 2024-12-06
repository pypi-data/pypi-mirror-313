# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ....._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ....._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....._base_client import make_request_options
from .....types.data.observations.nearest import geo_specie_list_params
from .....types.data.observations.nearest.geo_specie_list_response import GeoSpecieListResponse

__all__ = ["GeoSpeciesResource", "AsyncGeoSpeciesResource"]


class GeoSpeciesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> GeoSpeciesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return GeoSpeciesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> GeoSpeciesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return GeoSpeciesResourceWithStreamingResponse(self)

    def list(
        self,
        species_code: str,
        *,
        lat: float,
        lng: float,
        back: int | NotGiven = NOT_GIVEN,
        dist: int | NotGiven = NOT_GIVEN,
        hotspot: bool | NotGiven = NOT_GIVEN,
        include_provisional: bool | NotGiven = NOT_GIVEN,
        max_results: int | NotGiven = NOT_GIVEN,
        spp_locale: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GeoSpecieListResponse:
        """Find the nearest locations where a species has been seen recently.

        #### Notes
        The species code is typically a 6-letter code, e.g. barswa for Barn Swallow. You
        can get complete set of species code from the GET eBird Taxonomy end-point.

        Args:
          back: The number of days back to fetch observations.

          dist: Only fetch observations within this distance of the provided lat/lng

          hotspot: Only fetch observations from hotspots

          include_provisional: Include observations which have not yet been reviewed.

          max_results: Only fetch up to this number of observations

          spp_locale: Use this language for species common names

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not species_code:
            raise ValueError(f"Expected a non-empty value for `species_code` but received {species_code!r}")
        return self._get(
            f"/data/nearest/geo/recent/{species_code}",
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
                        "hotspot": hotspot,
                        "include_provisional": include_provisional,
                        "max_results": max_results,
                        "spp_locale": spp_locale,
                    },
                    geo_specie_list_params.GeoSpecieListParams,
                ),
            ),
            cast_to=GeoSpecieListResponse,
        )


class AsyncGeoSpeciesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncGeoSpeciesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncGeoSpeciesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncGeoSpeciesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncGeoSpeciesResourceWithStreamingResponse(self)

    async def list(
        self,
        species_code: str,
        *,
        lat: float,
        lng: float,
        back: int | NotGiven = NOT_GIVEN,
        dist: int | NotGiven = NOT_GIVEN,
        hotspot: bool | NotGiven = NOT_GIVEN,
        include_provisional: bool | NotGiven = NOT_GIVEN,
        max_results: int | NotGiven = NOT_GIVEN,
        spp_locale: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> GeoSpecieListResponse:
        """Find the nearest locations where a species has been seen recently.

        #### Notes
        The species code is typically a 6-letter code, e.g. barswa for Barn Swallow. You
        can get complete set of species code from the GET eBird Taxonomy end-point.

        Args:
          back: The number of days back to fetch observations.

          dist: Only fetch observations within this distance of the provided lat/lng

          hotspot: Only fetch observations from hotspots

          include_provisional: Include observations which have not yet been reviewed.

          max_results: Only fetch up to this number of observations

          spp_locale: Use this language for species common names

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not species_code:
            raise ValueError(f"Expected a non-empty value for `species_code` but received {species_code!r}")
        return await self._get(
            f"/data/nearest/geo/recent/{species_code}",
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
                        "hotspot": hotspot,
                        "include_provisional": include_provisional,
                        "max_results": max_results,
                        "spp_locale": spp_locale,
                    },
                    geo_specie_list_params.GeoSpecieListParams,
                ),
            ),
            cast_to=GeoSpecieListResponse,
        )


class GeoSpeciesResourceWithRawResponse:
    def __init__(self, geo_species: GeoSpeciesResource) -> None:
        self._geo_species = geo_species

        self.list = to_raw_response_wrapper(
            geo_species.list,
        )


class AsyncGeoSpeciesResourceWithRawResponse:
    def __init__(self, geo_species: AsyncGeoSpeciesResource) -> None:
        self._geo_species = geo_species

        self.list = async_to_raw_response_wrapper(
            geo_species.list,
        )


class GeoSpeciesResourceWithStreamingResponse:
    def __init__(self, geo_species: GeoSpeciesResource) -> None:
        self._geo_species = geo_species

        self.list = to_streamed_response_wrapper(
            geo_species.list,
        )


class AsyncGeoSpeciesResourceWithStreamingResponse:
    def __init__(self, geo_species: AsyncGeoSpeciesResource) -> None:
        self._geo_species = geo_species

        self.list = async_to_streamed_response_wrapper(
            geo_species.list,
        )
