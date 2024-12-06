# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.product import top100_retrieve_params
from ...types.product.top100_retrieve_response import Top100RetrieveResponse

__all__ = ["Top100Resource", "AsyncTop100Resource"]


class Top100Resource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> Top100ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return Top100ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> Top100ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return Top100ResourceWithStreamingResponse(self)

    def retrieve(
        self,
        d: int,
        *,
        region_code: str,
        y: int,
        m: int,
        max_results: int | NotGiven = NOT_GIVEN,
        ranked_by: Literal["spp", "cl"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Top100RetrieveResponse:
        """
        Get the top 100 contributors on a given date for a country or region.

        #### Notes

        The results are updated every 15 minutes.

        When ordering by the number of completed checklists, the number of species seen
        will always be zero. Similarly when ordering by the number of species seen the
        number of completed checklists will always be zero. <b>Selected Response Field
        Notes</b>

        profileHandle - if a user has enabled their profile, this is the handle to reach
        it via ebird.org/ebird/profile/{profileHandle}

        numSpecies - always zero when checklistSort parameter is true. Invalid
        observations ARE included in this total numCompleteChecklists - always zero when
        checklistSort parameter is false

        Args:
          max_results: Only fetch this number of contributors.

          ranked_by: Order by number of complete checklists (cl) or by number of species seen (spp).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not region_code:
            raise ValueError(f"Expected a non-empty value for `region_code` but received {region_code!r}")
        return self._get(
            f"/product/top100/{region_code}/{y}/{m}/{d}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "max_results": max_results,
                        "ranked_by": ranked_by,
                    },
                    top100_retrieve_params.Top100RetrieveParams,
                ),
            ),
            cast_to=Top100RetrieveResponse,
        )


class AsyncTop100Resource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTop100ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTop100ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTop100ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncTop100ResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        d: int,
        *,
        region_code: str,
        y: int,
        m: int,
        max_results: int | NotGiven = NOT_GIVEN,
        ranked_by: Literal["spp", "cl"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Top100RetrieveResponse:
        """
        Get the top 100 contributors on a given date for a country or region.

        #### Notes

        The results are updated every 15 minutes.

        When ordering by the number of completed checklists, the number of species seen
        will always be zero. Similarly when ordering by the number of species seen the
        number of completed checklists will always be zero. <b>Selected Response Field
        Notes</b>

        profileHandle - if a user has enabled their profile, this is the handle to reach
        it via ebird.org/ebird/profile/{profileHandle}

        numSpecies - always zero when checklistSort parameter is true. Invalid
        observations ARE included in this total numCompleteChecklists - always zero when
        checklistSort parameter is false

        Args:
          max_results: Only fetch this number of contributors.

          ranked_by: Order by number of complete checklists (cl) or by number of species seen (spp).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not region_code:
            raise ValueError(f"Expected a non-empty value for `region_code` but received {region_code!r}")
        return await self._get(
            f"/product/top100/{region_code}/{y}/{m}/{d}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "max_results": max_results,
                        "ranked_by": ranked_by,
                    },
                    top100_retrieve_params.Top100RetrieveParams,
                ),
            ),
            cast_to=Top100RetrieveResponse,
        )


class Top100ResourceWithRawResponse:
    def __init__(self, top100: Top100Resource) -> None:
        self._top100 = top100

        self.retrieve = to_raw_response_wrapper(
            top100.retrieve,
        )


class AsyncTop100ResourceWithRawResponse:
    def __init__(self, top100: AsyncTop100Resource) -> None:
        self._top100 = top100

        self.retrieve = async_to_raw_response_wrapper(
            top100.retrieve,
        )


class Top100ResourceWithStreamingResponse:
    def __init__(self, top100: Top100Resource) -> None:
        self._top100 = top100

        self.retrieve = to_streamed_response_wrapper(
            top100.retrieve,
        )


class AsyncTop100ResourceWithStreamingResponse:
    def __init__(self, top100: AsyncTop100Resource) -> None:
        self._top100 = top100

        self.retrieve = async_to_streamed_response_wrapper(
            top100.retrieve,
        )
