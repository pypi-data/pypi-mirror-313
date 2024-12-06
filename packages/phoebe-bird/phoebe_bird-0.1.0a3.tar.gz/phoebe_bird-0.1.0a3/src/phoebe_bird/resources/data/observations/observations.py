# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .geo import (
    GeoResource,
    AsyncGeoResource,
    GeoResourceWithRawResponse,
    AsyncGeoResourceWithRawResponse,
    GeoResourceWithStreamingResponse,
    AsyncGeoResourceWithStreamingResponse,
)
from .recent import (
    RecentResource,
    AsyncRecentResource,
    RecentResourceWithRawResponse,
    AsyncRecentResourceWithRawResponse,
    RecentResourceWithStreamingResponse,
    AsyncRecentResourceWithStreamingResponse,
)
from .geo.geo import GeoResource, AsyncGeoResource
from .nearest import (
    NearestResource,
    AsyncNearestResource,
    NearestResourceWithRawResponse,
    AsyncNearestResourceWithRawResponse,
    NearestResourceWithStreamingResponse,
    AsyncNearestResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from .recent.recent import RecentResource, AsyncRecentResource
from .nearest.nearest import NearestResource, AsyncNearestResource

__all__ = ["ObservationsResource", "AsyncObservationsResource"]


class ObservationsResource(SyncAPIResource):
    @cached_property
    def recent(self) -> RecentResource:
        return RecentResource(self._client)

    @cached_property
    def geo(self) -> GeoResource:
        return GeoResource(self._client)

    @cached_property
    def nearest(self) -> NearestResource:
        return NearestResource(self._client)

    @cached_property
    def with_raw_response(self) -> ObservationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return ObservationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ObservationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return ObservationsResourceWithStreamingResponse(self)


class AsyncObservationsResource(AsyncAPIResource):
    @cached_property
    def recent(self) -> AsyncRecentResource:
        return AsyncRecentResource(self._client)

    @cached_property
    def geo(self) -> AsyncGeoResource:
        return AsyncGeoResource(self._client)

    @cached_property
    def nearest(self) -> AsyncNearestResource:
        return AsyncNearestResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncObservationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncObservationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncObservationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncObservationsResourceWithStreamingResponse(self)


class ObservationsResourceWithRawResponse:
    def __init__(self, observations: ObservationsResource) -> None:
        self._observations = observations

    @cached_property
    def recent(self) -> RecentResourceWithRawResponse:
        return RecentResourceWithRawResponse(self._observations.recent)

    @cached_property
    def geo(self) -> GeoResourceWithRawResponse:
        return GeoResourceWithRawResponse(self._observations.geo)

    @cached_property
    def nearest(self) -> NearestResourceWithRawResponse:
        return NearestResourceWithRawResponse(self._observations.nearest)


class AsyncObservationsResourceWithRawResponse:
    def __init__(self, observations: AsyncObservationsResource) -> None:
        self._observations = observations

    @cached_property
    def recent(self) -> AsyncRecentResourceWithRawResponse:
        return AsyncRecentResourceWithRawResponse(self._observations.recent)

    @cached_property
    def geo(self) -> AsyncGeoResourceWithRawResponse:
        return AsyncGeoResourceWithRawResponse(self._observations.geo)

    @cached_property
    def nearest(self) -> AsyncNearestResourceWithRawResponse:
        return AsyncNearestResourceWithRawResponse(self._observations.nearest)


class ObservationsResourceWithStreamingResponse:
    def __init__(self, observations: ObservationsResource) -> None:
        self._observations = observations

    @cached_property
    def recent(self) -> RecentResourceWithStreamingResponse:
        return RecentResourceWithStreamingResponse(self._observations.recent)

    @cached_property
    def geo(self) -> GeoResourceWithStreamingResponse:
        return GeoResourceWithStreamingResponse(self._observations.geo)

    @cached_property
    def nearest(self) -> NearestResourceWithStreamingResponse:
        return NearestResourceWithStreamingResponse(self._observations.nearest)


class AsyncObservationsResourceWithStreamingResponse:
    def __init__(self, observations: AsyncObservationsResource) -> None:
        self._observations = observations

    @cached_property
    def recent(self) -> AsyncRecentResourceWithStreamingResponse:
        return AsyncRecentResourceWithStreamingResponse(self._observations.recent)

    @cached_property
    def geo(self) -> AsyncGeoResourceWithStreamingResponse:
        return AsyncGeoResourceWithStreamingResponse(self._observations.geo)

    @cached_property
    def nearest(self) -> AsyncNearestResourceWithStreamingResponse:
        return AsyncNearestResourceWithStreamingResponse(self._observations.nearest)
