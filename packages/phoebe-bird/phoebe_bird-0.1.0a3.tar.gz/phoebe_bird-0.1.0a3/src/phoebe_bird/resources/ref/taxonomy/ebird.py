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
from ....types.ref.taxonomy import ebird_retrieve_params
from ....types.ref.taxonomy.ebird_retrieve_response import EbirdRetrieveResponse

__all__ = ["EbirdResource", "AsyncEbirdResource"]


class EbirdResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EbirdResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return EbirdResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EbirdResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return EbirdResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        cat: str | NotGiven = NOT_GIVEN,
        fmt: Literal["csv", "json"] | NotGiven = NOT_GIVEN,
        locale: str | NotGiven = NOT_GIVEN,
        species: str | NotGiven = NOT_GIVEN,
        version: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EbirdRetrieveResponse:
        """Get the taxonomy used by eBird.

        #### Notes Each entry in the taxonomy contains a
        species code for example, barswa for Barn Swallow. You can download the taxonomy
        for selected species using the _species_ query parameter with a comma separating
        each code. Otherwise the full taxonomy is downloaded.

        Args:
          cat: Only fetch records from these taxonomic categories.

          fmt: Fetch the records in CSV or JSON format.

          locale: Use this language for common names.

          species: Only fetch records for these species.

          version: Fetch a specific version of the taxonomy.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/ref/taxonomy/ebird",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cat": cat,
                        "fmt": fmt,
                        "locale": locale,
                        "species": species,
                        "version": version,
                    },
                    ebird_retrieve_params.EbirdRetrieveParams,
                ),
            ),
            cast_to=EbirdRetrieveResponse,
        )


class AsyncEbirdResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEbirdResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEbirdResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEbirdResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncEbirdResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        cat: str | NotGiven = NOT_GIVEN,
        fmt: Literal["csv", "json"] | NotGiven = NOT_GIVEN,
        locale: str | NotGiven = NOT_GIVEN,
        species: str | NotGiven = NOT_GIVEN,
        version: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EbirdRetrieveResponse:
        """Get the taxonomy used by eBird.

        #### Notes Each entry in the taxonomy contains a
        species code for example, barswa for Barn Swallow. You can download the taxonomy
        for selected species using the _species_ query parameter with a comma separating
        each code. Otherwise the full taxonomy is downloaded.

        Args:
          cat: Only fetch records from these taxonomic categories.

          fmt: Fetch the records in CSV or JSON format.

          locale: Use this language for common names.

          species: Only fetch records for these species.

          version: Fetch a specific version of the taxonomy.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/ref/taxonomy/ebird",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "cat": cat,
                        "fmt": fmt,
                        "locale": locale,
                        "species": species,
                        "version": version,
                    },
                    ebird_retrieve_params.EbirdRetrieveParams,
                ),
            ),
            cast_to=EbirdRetrieveResponse,
        )


class EbirdResourceWithRawResponse:
    def __init__(self, ebird: EbirdResource) -> None:
        self._ebird = ebird

        self.retrieve = to_raw_response_wrapper(
            ebird.retrieve,
        )


class AsyncEbirdResourceWithRawResponse:
    def __init__(self, ebird: AsyncEbirdResource) -> None:
        self._ebird = ebird

        self.retrieve = async_to_raw_response_wrapper(
            ebird.retrieve,
        )


class EbirdResourceWithStreamingResponse:
    def __init__(self, ebird: EbirdResource) -> None:
        self._ebird = ebird

        self.retrieve = to_streamed_response_wrapper(
            ebird.retrieve,
        )


class AsyncEbirdResourceWithStreamingResponse:
    def __init__(self, ebird: AsyncEbirdResource) -> None:
        self._ebird = ebird

        self.retrieve = async_to_streamed_response_wrapper(
            ebird.retrieve,
        )
