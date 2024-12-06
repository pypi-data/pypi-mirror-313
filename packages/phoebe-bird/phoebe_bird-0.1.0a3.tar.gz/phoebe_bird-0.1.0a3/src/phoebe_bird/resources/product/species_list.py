# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.product.species_list_list_response import SpeciesListListResponse

__all__ = ["SpeciesListResource", "AsyncSpeciesListResource"]


class SpeciesListResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SpeciesListResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return SpeciesListResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SpeciesListResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return SpeciesListResourceWithStreamingResponse(self)

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
    ) -> SpeciesListListResponse:
        """
        Get a list of species codes ever seen in a region, in taxonomic order (species
        taxa only)

        #### Notes The results are usually updated every 10 seconds for locations, every day for larger regions.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not region_code:
            raise ValueError(f"Expected a non-empty value for `region_code` but received {region_code!r}")
        return self._get(
            f"/product/spplist/{region_code}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SpeciesListListResponse,
        )


class AsyncSpeciesListResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSpeciesListResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSpeciesListResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSpeciesListResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncSpeciesListResourceWithStreamingResponse(self)

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
    ) -> SpeciesListListResponse:
        """
        Get a list of species codes ever seen in a region, in taxonomic order (species
        taxa only)

        #### Notes The results are usually updated every 10 seconds for locations, every day for larger regions.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not region_code:
            raise ValueError(f"Expected a non-empty value for `region_code` but received {region_code!r}")
        return await self._get(
            f"/product/spplist/{region_code}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SpeciesListListResponse,
        )


class SpeciesListResourceWithRawResponse:
    def __init__(self, species_list: SpeciesListResource) -> None:
        self._species_list = species_list

        self.list = to_raw_response_wrapper(
            species_list.list,
        )


class AsyncSpeciesListResourceWithRawResponse:
    def __init__(self, species_list: AsyncSpeciesListResource) -> None:
        self._species_list = species_list

        self.list = async_to_raw_response_wrapper(
            species_list.list,
        )


class SpeciesListResourceWithStreamingResponse:
    def __init__(self, species_list: SpeciesListResource) -> None:
        self._species_list = species_list

        self.list = to_streamed_response_wrapper(
            species_list.list,
        )


class AsyncSpeciesListResourceWithStreamingResponse:
    def __init__(self, species_list: AsyncSpeciesListResource) -> None:
        self._species_list = species_list

        self.list = async_to_streamed_response_wrapper(
            species_list.list,
        )
