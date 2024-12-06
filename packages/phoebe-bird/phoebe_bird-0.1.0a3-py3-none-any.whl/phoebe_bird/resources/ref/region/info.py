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
from ....types.ref.region import info_retrieve_params
from ....types.ref.region.info_retrieve_response import InfoRetrieveResponse

__all__ = ["InfoResource", "AsyncInfoResource"]


class InfoResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> InfoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return InfoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InfoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return InfoResourceWithStreamingResponse(self)

    def retrieve(
        self,
        region_code: str,
        *,
        delim: str | NotGiven = NOT_GIVEN,
        region_name_format: Literal["detailed", "detailednoqual", "full", "namequal", "nameonly", "revdetailed"]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> InfoRetrieveResponse:
        """
        Get information on the name and geographical area covered by a region.

        #### Notes

        Taking Madison County, New York, USA (location code US-NY-053) as an example the
        various values for the regionNameFormat query parameter work as follows:

        | Value          | Description                                | Result                           |
        | -------------- | ------------------------------------------ | -------------------------------- |
        | detailed       | return a detailed description              | Madison County, New York, US     |
        | detailednoqual | return the name to the subnational1 level  | Madison, New York                |
        | full           | return the full description                | Madison, New York, United States |
        | namequal       | return the qualified name                  | Madison County                   |
        | nameonly       | return only the name of the region         | Madison                          |
        | revdetailed    | return the detailed description in reverse | US, New York, Madison County     |

        Args:
          delim: The characters used to separate elements in the name.

          region_name_format: Control how the name is displayed.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not region_code:
            raise ValueError(f"Expected a non-empty value for `region_code` but received {region_code!r}")
        return self._get(
            f"/ref/region/info/{region_code}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "delim": delim,
                        "region_name_format": region_name_format,
                    },
                    info_retrieve_params.InfoRetrieveParams,
                ),
            ),
            cast_to=InfoRetrieveResponse,
        )


class AsyncInfoResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncInfoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncInfoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInfoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncInfoResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        region_code: str,
        *,
        delim: str | NotGiven = NOT_GIVEN,
        region_name_format: Literal["detailed", "detailednoqual", "full", "namequal", "nameonly", "revdetailed"]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> InfoRetrieveResponse:
        """
        Get information on the name and geographical area covered by a region.

        #### Notes

        Taking Madison County, New York, USA (location code US-NY-053) as an example the
        various values for the regionNameFormat query parameter work as follows:

        | Value          | Description                                | Result                           |
        | -------------- | ------------------------------------------ | -------------------------------- |
        | detailed       | return a detailed description              | Madison County, New York, US     |
        | detailednoqual | return the name to the subnational1 level  | Madison, New York                |
        | full           | return the full description                | Madison, New York, United States |
        | namequal       | return the qualified name                  | Madison County                   |
        | nameonly       | return only the name of the region         | Madison                          |
        | revdetailed    | return the detailed description in reverse | US, New York, Madison County     |

        Args:
          delim: The characters used to separate elements in the name.

          region_name_format: Control how the name is displayed.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not region_code:
            raise ValueError(f"Expected a non-empty value for `region_code` but received {region_code!r}")
        return await self._get(
            f"/ref/region/info/{region_code}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "delim": delim,
                        "region_name_format": region_name_format,
                    },
                    info_retrieve_params.InfoRetrieveParams,
                ),
            ),
            cast_to=InfoRetrieveResponse,
        )


class InfoResourceWithRawResponse:
    def __init__(self, info: InfoResource) -> None:
        self._info = info

        self.retrieve = to_raw_response_wrapper(
            info.retrieve,
        )


class AsyncInfoResourceWithRawResponse:
    def __init__(self, info: AsyncInfoResource) -> None:
        self._info = info

        self.retrieve = async_to_raw_response_wrapper(
            info.retrieve,
        )


class InfoResourceWithStreamingResponse:
    def __init__(self, info: InfoResource) -> None:
        self._info = info

        self.retrieve = to_streamed_response_wrapper(
            info.retrieve,
        )


class AsyncInfoResourceWithStreamingResponse:
    def __init__(self, info: AsyncInfoResource) -> None:
        self._info = info

        self.retrieve = async_to_streamed_response_wrapper(
            info.retrieve,
        )
