# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .recent import (
    RecentResource,
    AsyncRecentResource,
    RecentResourceWithRawResponse,
    AsyncRecentResourceWithRawResponse,
    RecentResourceWithStreamingResponse,
    AsyncRecentResourceWithStreamingResponse,
)
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from .recent.recent import RecentResource, AsyncRecentResource

__all__ = ["GeoResource", "AsyncGeoResource"]


class GeoResource(SyncAPIResource):
    @cached_property
    def recent(self) -> RecentResource:
        return RecentResource(self._client)

    @cached_property
    def with_raw_response(self) -> GeoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return GeoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> GeoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return GeoResourceWithStreamingResponse(self)


class AsyncGeoResource(AsyncAPIResource):
    @cached_property
    def recent(self) -> AsyncRecentResource:
        return AsyncRecentResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncGeoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncGeoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncGeoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncGeoResourceWithStreamingResponse(self)


class GeoResourceWithRawResponse:
    def __init__(self, geo: GeoResource) -> None:
        self._geo = geo

    @cached_property
    def recent(self) -> RecentResourceWithRawResponse:
        return RecentResourceWithRawResponse(self._geo.recent)


class AsyncGeoResourceWithRawResponse:
    def __init__(self, geo: AsyncGeoResource) -> None:
        self._geo = geo

    @cached_property
    def recent(self) -> AsyncRecentResourceWithRawResponse:
        return AsyncRecentResourceWithRawResponse(self._geo.recent)


class GeoResourceWithStreamingResponse:
    def __init__(self, geo: GeoResource) -> None:
        self._geo = geo

    @cached_property
    def recent(self) -> RecentResourceWithStreamingResponse:
        return RecentResourceWithStreamingResponse(self._geo.recent)


class AsyncGeoResourceWithStreamingResponse:
    def __init__(self, geo: AsyncGeoResource) -> None:
        self._geo = geo

    @cached_property
    def recent(self) -> AsyncRecentResourceWithStreamingResponse:
        return AsyncRecentResourceWithStreamingResponse(self._geo.recent)
