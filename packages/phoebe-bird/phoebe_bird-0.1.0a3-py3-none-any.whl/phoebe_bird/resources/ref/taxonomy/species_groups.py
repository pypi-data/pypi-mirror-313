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
from ....types.ref.taxonomy import species_group_list_params
from ....types.ref.taxonomy.species_group_list_response import SpeciesGroupListResponse

__all__ = ["SpeciesGroupsResource", "AsyncSpeciesGroupsResource"]


class SpeciesGroupsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SpeciesGroupsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return SpeciesGroupsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SpeciesGroupsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return SpeciesGroupsResourceWithStreamingResponse(self)

    def list(
        self,
        species_grouping: Literal["merlin", "ebird"],
        *,
        group_name_locale: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SpeciesGroupListResponse:
        """Get the list of species groups, e.g.

        terns, finches, etc. #### Notes Merlin puts
        like birds together, with Falcons next to Hawks, whereas eBird follows taxonomic
        order.

        Args:
          species_grouping: The order in which groups are returned.

          group_name_locale: Locale for species group names. English names are returned for any non-listed
              locale or any non-translated group name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not species_grouping:
            raise ValueError(f"Expected a non-empty value for `species_grouping` but received {species_grouping!r}")
        return self._get(
            f"/ref/sppgroup/{species_grouping}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"group_name_locale": group_name_locale}, species_group_list_params.SpeciesGroupListParams
                ),
            ),
            cast_to=SpeciesGroupListResponse,
        )


class AsyncSpeciesGroupsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSpeciesGroupsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSpeciesGroupsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSpeciesGroupsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncSpeciesGroupsResourceWithStreamingResponse(self)

    async def list(
        self,
        species_grouping: Literal["merlin", "ebird"],
        *,
        group_name_locale: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SpeciesGroupListResponse:
        """Get the list of species groups, e.g.

        terns, finches, etc. #### Notes Merlin puts
        like birds together, with Falcons next to Hawks, whereas eBird follows taxonomic
        order.

        Args:
          species_grouping: The order in which groups are returned.

          group_name_locale: Locale for species group names. English names are returned for any non-listed
              locale or any non-translated group name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not species_grouping:
            raise ValueError(f"Expected a non-empty value for `species_grouping` but received {species_grouping!r}")
        return await self._get(
            f"/ref/sppgroup/{species_grouping}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"group_name_locale": group_name_locale}, species_group_list_params.SpeciesGroupListParams
                ),
            ),
            cast_to=SpeciesGroupListResponse,
        )


class SpeciesGroupsResourceWithRawResponse:
    def __init__(self, species_groups: SpeciesGroupsResource) -> None:
        self._species_groups = species_groups

        self.list = to_raw_response_wrapper(
            species_groups.list,
        )


class AsyncSpeciesGroupsResourceWithRawResponse:
    def __init__(self, species_groups: AsyncSpeciesGroupsResource) -> None:
        self._species_groups = species_groups

        self.list = async_to_raw_response_wrapper(
            species_groups.list,
        )


class SpeciesGroupsResourceWithStreamingResponse:
    def __init__(self, species_groups: SpeciesGroupsResource) -> None:
        self._species_groups = species_groups

        self.list = to_streamed_response_wrapper(
            species_groups.list,
        )


class AsyncSpeciesGroupsResourceWithStreamingResponse:
    def __init__(self, species_groups: AsyncSpeciesGroupsResource) -> None:
        self._species_groups = species_groups

        self.list = async_to_streamed_response_wrapper(
            species_groups.list,
        )
