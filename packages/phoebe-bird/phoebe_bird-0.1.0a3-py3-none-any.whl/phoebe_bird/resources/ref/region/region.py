# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .info import (
    InfoResource,
    AsyncInfoResource,
    InfoResourceWithRawResponse,
    AsyncInfoResourceWithRawResponse,
    InfoResourceWithStreamingResponse,
    AsyncInfoResourceWithStreamingResponse,
)
from .list import (
    ListResource,
    AsyncListResource,
    ListResourceWithRawResponse,
    AsyncListResourceWithRawResponse,
    ListResourceWithStreamingResponse,
    AsyncListResourceWithStreamingResponse,
)
from .adjacent import (
    AdjacentResource,
    AsyncAdjacentResource,
    AdjacentResourceWithRawResponse,
    AsyncAdjacentResourceWithRawResponse,
    AdjacentResourceWithStreamingResponse,
    AsyncAdjacentResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["RegionResource", "AsyncRegionResource"]


class RegionResource(SyncAPIResource):
    @cached_property
    def adjacent(self) -> AdjacentResource:
        return AdjacentResource(self._client)

    @cached_property
    def info(self) -> InfoResource:
        return InfoResource(self._client)

    @cached_property
    def list(self) -> ListResource:
        return ListResource(self._client)

    @cached_property
    def with_raw_response(self) -> RegionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return RegionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RegionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return RegionResourceWithStreamingResponse(self)


class AsyncRegionResource(AsyncAPIResource):
    @cached_property
    def adjacent(self) -> AsyncAdjacentResource:
        return AsyncAdjacentResource(self._client)

    @cached_property
    def info(self) -> AsyncInfoResource:
        return AsyncInfoResource(self._client)

    @cached_property
    def list(self) -> AsyncListResource:
        return AsyncListResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncRegionResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncRegionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRegionResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncRegionResourceWithStreamingResponse(self)


class RegionResourceWithRawResponse:
    def __init__(self, region: RegionResource) -> None:
        self._region = region

    @cached_property
    def adjacent(self) -> AdjacentResourceWithRawResponse:
        return AdjacentResourceWithRawResponse(self._region.adjacent)

    @cached_property
    def info(self) -> InfoResourceWithRawResponse:
        return InfoResourceWithRawResponse(self._region.info)

    @cached_property
    def list(self) -> ListResourceWithRawResponse:
        return ListResourceWithRawResponse(self._region.list)


class AsyncRegionResourceWithRawResponse:
    def __init__(self, region: AsyncRegionResource) -> None:
        self._region = region

    @cached_property
    def adjacent(self) -> AsyncAdjacentResourceWithRawResponse:
        return AsyncAdjacentResourceWithRawResponse(self._region.adjacent)

    @cached_property
    def info(self) -> AsyncInfoResourceWithRawResponse:
        return AsyncInfoResourceWithRawResponse(self._region.info)

    @cached_property
    def list(self) -> AsyncListResourceWithRawResponse:
        return AsyncListResourceWithRawResponse(self._region.list)


class RegionResourceWithStreamingResponse:
    def __init__(self, region: RegionResource) -> None:
        self._region = region

    @cached_property
    def adjacent(self) -> AdjacentResourceWithStreamingResponse:
        return AdjacentResourceWithStreamingResponse(self._region.adjacent)

    @cached_property
    def info(self) -> InfoResourceWithStreamingResponse:
        return InfoResourceWithStreamingResponse(self._region.info)

    @cached_property
    def list(self) -> ListResourceWithStreamingResponse:
        return ListResourceWithStreamingResponse(self._region.list)


class AsyncRegionResourceWithStreamingResponse:
    def __init__(self, region: AsyncRegionResource) -> None:
        self._region = region

    @cached_property
    def adjacent(self) -> AsyncAdjacentResourceWithStreamingResponse:
        return AsyncAdjacentResourceWithStreamingResponse(self._region.adjacent)

    @cached_property
    def info(self) -> AsyncInfoResourceWithStreamingResponse:
        return AsyncInfoResourceWithStreamingResponse(self._region.info)

    @cached_property
    def list(self) -> AsyncListResourceWithStreamingResponse:
        return AsyncListResourceWithStreamingResponse(self._region.list)
