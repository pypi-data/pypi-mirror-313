# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

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
from .....types.data.observations.recent import historic_list_params
from .....types.data.observations.recent.historic_list_response import HistoricListResponse

__all__ = ["HistoricResource", "AsyncHistoricResource"]


class HistoricResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> HistoricResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return HistoricResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> HistoricResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return HistoricResourceWithStreamingResponse(self)

    def list(
        self,
        d: int,
        *,
        region_code: str,
        y: int,
        m: int,
        cat: Literal["species", "slash", "issf", "spuh", "hybrid", "domestic", "form", "intergrade"]
        | NotGiven = NOT_GIVEN,
        detail: Literal["simple", "full"] | NotGiven = NOT_GIVEN,
        hotspot: bool | NotGiven = NOT_GIVEN,
        include_provisional: bool | NotGiven = NOT_GIVEN,
        max_results: int | NotGiven = NOT_GIVEN,
        r: List[str] | NotGiven = NOT_GIVEN,
        rank: Literal["mrec", "create"] | NotGiven = NOT_GIVEN,
        spp_locale: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> HistoricListResponse:
        """
        Get a list of all taxa seen in a country, region or location on a specific date,
        with the specific observations determined by the "rank" parameter (defaults to
        latest observation on the date).

        #### Notes Responses may be cached for 30 minutes

        Args:
          cat: Only fetch observations from these taxonomic categories

          detail: Include a subset (simple), or all (full), of the fields available.

          hotspot: Only fetch observations from hotspots

          include_provisional: Include observations which have not yet been reviewed.

          max_results: Only fetch this number of observations

          r: Fetch observations from up to 50 locations

          rank: Include latest observation of the day, or the first added

          spp_locale: Use this language for species common names

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not region_code:
            raise ValueError(f"Expected a non-empty value for `region_code` but received {region_code!r}")
        return self._get(
            f"/data/obs/{region_code}/historic/{y}/{m}/{d}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cat": cat,
                        "detail": detail,
                        "hotspot": hotspot,
                        "include_provisional": include_provisional,
                        "max_results": max_results,
                        "r": r,
                        "rank": rank,
                        "spp_locale": spp_locale,
                    },
                    historic_list_params.HistoricListParams,
                ),
            ),
            cast_to=HistoricListResponse,
        )


class AsyncHistoricResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncHistoricResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncHistoricResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncHistoricResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncHistoricResourceWithStreamingResponse(self)

    async def list(
        self,
        d: int,
        *,
        region_code: str,
        y: int,
        m: int,
        cat: Literal["species", "slash", "issf", "spuh", "hybrid", "domestic", "form", "intergrade"]
        | NotGiven = NOT_GIVEN,
        detail: Literal["simple", "full"] | NotGiven = NOT_GIVEN,
        hotspot: bool | NotGiven = NOT_GIVEN,
        include_provisional: bool | NotGiven = NOT_GIVEN,
        max_results: int | NotGiven = NOT_GIVEN,
        r: List[str] | NotGiven = NOT_GIVEN,
        rank: Literal["mrec", "create"] | NotGiven = NOT_GIVEN,
        spp_locale: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> HistoricListResponse:
        """
        Get a list of all taxa seen in a country, region or location on a specific date,
        with the specific observations determined by the "rank" parameter (defaults to
        latest observation on the date).

        #### Notes Responses may be cached for 30 minutes

        Args:
          cat: Only fetch observations from these taxonomic categories

          detail: Include a subset (simple), or all (full), of the fields available.

          hotspot: Only fetch observations from hotspots

          include_provisional: Include observations which have not yet been reviewed.

          max_results: Only fetch this number of observations

          r: Fetch observations from up to 50 locations

          rank: Include latest observation of the day, or the first added

          spp_locale: Use this language for species common names

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not region_code:
            raise ValueError(f"Expected a non-empty value for `region_code` but received {region_code!r}")
        return await self._get(
            f"/data/obs/{region_code}/historic/{y}/{m}/{d}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "cat": cat,
                        "detail": detail,
                        "hotspot": hotspot,
                        "include_provisional": include_provisional,
                        "max_results": max_results,
                        "r": r,
                        "rank": rank,
                        "spp_locale": spp_locale,
                    },
                    historic_list_params.HistoricListParams,
                ),
            ),
            cast_to=HistoricListResponse,
        )


class HistoricResourceWithRawResponse:
    def __init__(self, historic: HistoricResource) -> None:
        self._historic = historic

        self.list = to_raw_response_wrapper(
            historic.list,
        )


class AsyncHistoricResourceWithRawResponse:
    def __init__(self, historic: AsyncHistoricResource) -> None:
        self._historic = historic

        self.list = async_to_raw_response_wrapper(
            historic.list,
        )


class HistoricResourceWithStreamingResponse:
    def __init__(self, historic: HistoricResource) -> None:
        self._historic = historic

        self.list = to_streamed_response_wrapper(
            historic.list,
        )


class AsyncHistoricResourceWithStreamingResponse:
    def __init__(self, historic: AsyncHistoricResource) -> None:
        self._historic = historic

        self.list = async_to_streamed_response_wrapper(
            historic.list,
        )
