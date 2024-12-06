# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

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
from ......types.data.observations.geo.recent import specie_list_params
from ......types.data.observations.geo.recent.specie_list_response import SpecieListResponse

__all__ = ["SpeciesResource", "AsyncSpeciesResource"]


class SpeciesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SpeciesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return SpeciesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SpeciesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return SpeciesResourceWithStreamingResponse(self)

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
    ) -> SpecieListResponse:
        """
        Get all observations of a species, seen up to 30 days ago, at any location
        within a radius of up to 50 kilometers, from a given set of coordinates. Results
        include only the most recent observation from each location in the region
        specified.

        #### URL parameters

        | Name        | Description             |
        | ----------- | ----------------------- |
        | speciesCode | The eBird species code. |

        #### Notes

        The species code is typically a 6-letter code, e.g. horlar for Horned Lark. You
        can get complete set of species code from the GET eBird Taxonomy end-point.

        Args:
          back: The number of days back to fetch observations.

          dist: The search radius from the given position, in kilometers.

          hotspot: Only fetch observations from hotspots

          include_provisional: Include observations which have not yet been reviewed.

          max_results: Only fetch this number of observations

          spp_locale: Use this language for species common names

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not species_code:
            raise ValueError(f"Expected a non-empty value for `species_code` but received {species_code!r}")
        return self._get(
            f"/data/obs/geo/recent/{species_code}",
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
                    specie_list_params.SpecieListParams,
                ),
            ),
            cast_to=SpecieListResponse,
        )


class AsyncSpeciesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSpeciesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSpeciesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSpeciesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncSpeciesResourceWithStreamingResponse(self)

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
    ) -> SpecieListResponse:
        """
        Get all observations of a species, seen up to 30 days ago, at any location
        within a radius of up to 50 kilometers, from a given set of coordinates. Results
        include only the most recent observation from each location in the region
        specified.

        #### URL parameters

        | Name        | Description             |
        | ----------- | ----------------------- |
        | speciesCode | The eBird species code. |

        #### Notes

        The species code is typically a 6-letter code, e.g. horlar for Horned Lark. You
        can get complete set of species code from the GET eBird Taxonomy end-point.

        Args:
          back: The number of days back to fetch observations.

          dist: The search radius from the given position, in kilometers.

          hotspot: Only fetch observations from hotspots

          include_provisional: Include observations which have not yet been reviewed.

          max_results: Only fetch this number of observations

          spp_locale: Use this language for species common names

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not species_code:
            raise ValueError(f"Expected a non-empty value for `species_code` but received {species_code!r}")
        return await self._get(
            f"/data/obs/geo/recent/{species_code}",
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
                    specie_list_params.SpecieListParams,
                ),
            ),
            cast_to=SpecieListResponse,
        )


class SpeciesResourceWithRawResponse:
    def __init__(self, species: SpeciesResource) -> None:
        self._species = species

        self.list = to_raw_response_wrapper(
            species.list,
        )


class AsyncSpeciesResourceWithRawResponse:
    def __init__(self, species: AsyncSpeciesResource) -> None:
        self._species = species

        self.list = async_to_raw_response_wrapper(
            species.list,
        )


class SpeciesResourceWithStreamingResponse:
    def __init__(self, species: SpeciesResource) -> None:
        self._species = species

        self.list = to_streamed_response_wrapper(
            species.list,
        )


class AsyncSpeciesResourceWithStreamingResponse:
    def __init__(self, species: AsyncSpeciesResource) -> None:
        self._species = species

        self.list = async_to_streamed_response_wrapper(
            species.list,
        )
