# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .region import (
    RegionResource,
    AsyncRegionResource,
    RegionResourceWithRawResponse,
    AsyncRegionResourceWithRawResponse,
    RegionResourceWithStreamingResponse,
    AsyncRegionResourceWithStreamingResponse,
)
from .hotspot import (
    HotspotResource,
    AsyncHotspotResource,
    HotspotResourceWithRawResponse,
    AsyncHotspotResourceWithRawResponse,
    HotspotResourceWithStreamingResponse,
    AsyncHotspotResourceWithStreamingResponse,
)
from .taxonomy import (
    TaxonomyResource,
    AsyncTaxonomyResource,
    TaxonomyResourceWithRawResponse,
    AsyncTaxonomyResourceWithRawResponse,
    TaxonomyResourceWithStreamingResponse,
    AsyncTaxonomyResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .region.region import RegionResource, AsyncRegionResource
from .hotspot.hotspot import HotspotResource, AsyncHotspotResource
from .taxonomy.taxonomy import TaxonomyResource, AsyncTaxonomyResource

__all__ = ["RefResource", "AsyncRefResource"]


class RefResource(SyncAPIResource):
    @cached_property
    def region(self) -> RegionResource:
        return RegionResource(self._client)

    @cached_property
    def hotspot(self) -> HotspotResource:
        return HotspotResource(self._client)

    @cached_property
    def taxonomy(self) -> TaxonomyResource:
        return TaxonomyResource(self._client)

    @cached_property
    def with_raw_response(self) -> RefResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return RefResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RefResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return RefResourceWithStreamingResponse(self)


class AsyncRefResource(AsyncAPIResource):
    @cached_property
    def region(self) -> AsyncRegionResource:
        return AsyncRegionResource(self._client)

    @cached_property
    def hotspot(self) -> AsyncHotspotResource:
        return AsyncHotspotResource(self._client)

    @cached_property
    def taxonomy(self) -> AsyncTaxonomyResource:
        return AsyncTaxonomyResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncRefResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncRefResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRefResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncRefResourceWithStreamingResponse(self)


class RefResourceWithRawResponse:
    def __init__(self, ref: RefResource) -> None:
        self._ref = ref

    @cached_property
    def region(self) -> RegionResourceWithRawResponse:
        return RegionResourceWithRawResponse(self._ref.region)

    @cached_property
    def hotspot(self) -> HotspotResourceWithRawResponse:
        return HotspotResourceWithRawResponse(self._ref.hotspot)

    @cached_property
    def taxonomy(self) -> TaxonomyResourceWithRawResponse:
        return TaxonomyResourceWithRawResponse(self._ref.taxonomy)


class AsyncRefResourceWithRawResponse:
    def __init__(self, ref: AsyncRefResource) -> None:
        self._ref = ref

    @cached_property
    def region(self) -> AsyncRegionResourceWithRawResponse:
        return AsyncRegionResourceWithRawResponse(self._ref.region)

    @cached_property
    def hotspot(self) -> AsyncHotspotResourceWithRawResponse:
        return AsyncHotspotResourceWithRawResponse(self._ref.hotspot)

    @cached_property
    def taxonomy(self) -> AsyncTaxonomyResourceWithRawResponse:
        return AsyncTaxonomyResourceWithRawResponse(self._ref.taxonomy)


class RefResourceWithStreamingResponse:
    def __init__(self, ref: RefResource) -> None:
        self._ref = ref

    @cached_property
    def region(self) -> RegionResourceWithStreamingResponse:
        return RegionResourceWithStreamingResponse(self._ref.region)

    @cached_property
    def hotspot(self) -> HotspotResourceWithStreamingResponse:
        return HotspotResourceWithStreamingResponse(self._ref.hotspot)

    @cached_property
    def taxonomy(self) -> TaxonomyResourceWithStreamingResponse:
        return TaxonomyResourceWithStreamingResponse(self._ref.taxonomy)


class AsyncRefResourceWithStreamingResponse:
    def __init__(self, ref: AsyncRefResource) -> None:
        self._ref = ref

    @cached_property
    def region(self) -> AsyncRegionResourceWithStreamingResponse:
        return AsyncRegionResourceWithStreamingResponse(self._ref.region)

    @cached_property
    def hotspot(self) -> AsyncHotspotResourceWithStreamingResponse:
        return AsyncHotspotResourceWithStreamingResponse(self._ref.hotspot)

    @cached_property
    def taxonomy(self) -> AsyncTaxonomyResourceWithStreamingResponse:
        return AsyncTaxonomyResourceWithStreamingResponse(self._ref.taxonomy)
