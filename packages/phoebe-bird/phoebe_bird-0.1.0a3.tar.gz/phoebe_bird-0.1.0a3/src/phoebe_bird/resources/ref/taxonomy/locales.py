# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import strip_not_given
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.ref.taxonomy.locale_list_response import LocaleListResponse

__all__ = ["LocalesResource", "AsyncLocalesResource"]


class LocalesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> LocalesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return LocalesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> LocalesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return LocalesResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        accept_language: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LocaleListResponse:
        """
        Returns the list of supported locale codes and names for species common names,
        with the last time they were updated. Use the accept-language header to get
        translated language names when available.

        NOTE: The locale codes and names are stable but the other fields in this result
        are not yet finalized and should be used with caution.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"Accept-Language": accept_language}), **(extra_headers or {})}
        return self._get(
            "/ref/taxa-locales/ebird",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LocaleListResponse,
        )


class AsyncLocalesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncLocalesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncLocalesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncLocalesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncLocalesResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        accept_language: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LocaleListResponse:
        """
        Returns the list of supported locale codes and names for species common names,
        with the last time they were updated. Use the accept-language header to get
        translated language names when available.

        NOTE: The locale codes and names are stable but the other fields in this result
        are not yet finalized and should be used with caution.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {**strip_not_given({"Accept-Language": accept_language}), **(extra_headers or {})}
        return await self._get(
            "/ref/taxa-locales/ebird",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LocaleListResponse,
        )


class LocalesResourceWithRawResponse:
    def __init__(self, locales: LocalesResource) -> None:
        self._locales = locales

        self.list = to_raw_response_wrapper(
            locales.list,
        )


class AsyncLocalesResourceWithRawResponse:
    def __init__(self, locales: AsyncLocalesResource) -> None:
        self._locales = locales

        self.list = async_to_raw_response_wrapper(
            locales.list,
        )


class LocalesResourceWithStreamingResponse:
    def __init__(self, locales: LocalesResource) -> None:
        self._locales = locales

        self.list = to_streamed_response_wrapper(
            locales.list,
        )


class AsyncLocalesResourceWithStreamingResponse:
    def __init__(self, locales: AsyncLocalesResource) -> None:
        self._locales = locales

        self.list = async_to_streamed_response_wrapper(
            locales.list,
        )
