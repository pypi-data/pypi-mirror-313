# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .lists import (
    ListsResource,
    AsyncListsResource,
    ListsResourceWithRawResponse,
    AsyncListsResourceWithRawResponse,
    ListsResourceWithStreamingResponse,
    AsyncListsResourceWithStreamingResponse,
)
from .stats import (
    StatsResource,
    AsyncStatsResource,
    StatsResourceWithRawResponse,
    AsyncStatsResourceWithRawResponse,
    StatsResourceWithStreamingResponse,
    AsyncStatsResourceWithStreamingResponse,
)
from .top100 import (
    Top100Resource,
    AsyncTop100Resource,
    Top100ResourceWithRawResponse,
    AsyncTop100ResourceWithRawResponse,
    Top100ResourceWithStreamingResponse,
    AsyncTop100ResourceWithStreamingResponse,
)
from ..._compat import cached_property
from .checklist import (
    ChecklistResource,
    AsyncChecklistResource,
    ChecklistResourceWithRawResponse,
    AsyncChecklistResourceWithRawResponse,
    ChecklistResourceWithStreamingResponse,
    AsyncChecklistResourceWithStreamingResponse,
)
from ..._resource import SyncAPIResource, AsyncAPIResource
from .lists.lists import ListsResource, AsyncListsResource
from .species_list import (
    SpeciesListResource,
    AsyncSpeciesListResource,
    SpeciesListResourceWithRawResponse,
    AsyncSpeciesListResourceWithRawResponse,
    SpeciesListResourceWithStreamingResponse,
    AsyncSpeciesListResourceWithStreamingResponse,
)

__all__ = ["ProductResource", "AsyncProductResource"]


class ProductResource(SyncAPIResource):
    @cached_property
    def lists(self) -> ListsResource:
        return ListsResource(self._client)

    @cached_property
    def top100(self) -> Top100Resource:
        return Top100Resource(self._client)

    @cached_property
    def stats(self) -> StatsResource:
        return StatsResource(self._client)

    @cached_property
    def species_list(self) -> SpeciesListResource:
        return SpeciesListResource(self._client)

    @cached_property
    def checklist(self) -> ChecklistResource:
        return ChecklistResource(self._client)

    @cached_property
    def with_raw_response(self) -> ProductResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return ProductResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProductResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return ProductResourceWithStreamingResponse(self)


class AsyncProductResource(AsyncAPIResource):
    @cached_property
    def lists(self) -> AsyncListsResource:
        return AsyncListsResource(self._client)

    @cached_property
    def top100(self) -> AsyncTop100Resource:
        return AsyncTop100Resource(self._client)

    @cached_property
    def stats(self) -> AsyncStatsResource:
        return AsyncStatsResource(self._client)

    @cached_property
    def species_list(self) -> AsyncSpeciesListResource:
        return AsyncSpeciesListResource(self._client)

    @cached_property
    def checklist(self) -> AsyncChecklistResource:
        return AsyncChecklistResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncProductResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncProductResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProductResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncProductResourceWithStreamingResponse(self)


class ProductResourceWithRawResponse:
    def __init__(self, product: ProductResource) -> None:
        self._product = product

    @cached_property
    def lists(self) -> ListsResourceWithRawResponse:
        return ListsResourceWithRawResponse(self._product.lists)

    @cached_property
    def top100(self) -> Top100ResourceWithRawResponse:
        return Top100ResourceWithRawResponse(self._product.top100)

    @cached_property
    def stats(self) -> StatsResourceWithRawResponse:
        return StatsResourceWithRawResponse(self._product.stats)

    @cached_property
    def species_list(self) -> SpeciesListResourceWithRawResponse:
        return SpeciesListResourceWithRawResponse(self._product.species_list)

    @cached_property
    def checklist(self) -> ChecklistResourceWithRawResponse:
        return ChecklistResourceWithRawResponse(self._product.checklist)


class AsyncProductResourceWithRawResponse:
    def __init__(self, product: AsyncProductResource) -> None:
        self._product = product

    @cached_property
    def lists(self) -> AsyncListsResourceWithRawResponse:
        return AsyncListsResourceWithRawResponse(self._product.lists)

    @cached_property
    def top100(self) -> AsyncTop100ResourceWithRawResponse:
        return AsyncTop100ResourceWithRawResponse(self._product.top100)

    @cached_property
    def stats(self) -> AsyncStatsResourceWithRawResponse:
        return AsyncStatsResourceWithRawResponse(self._product.stats)

    @cached_property
    def species_list(self) -> AsyncSpeciesListResourceWithRawResponse:
        return AsyncSpeciesListResourceWithRawResponse(self._product.species_list)

    @cached_property
    def checklist(self) -> AsyncChecklistResourceWithRawResponse:
        return AsyncChecklistResourceWithRawResponse(self._product.checklist)


class ProductResourceWithStreamingResponse:
    def __init__(self, product: ProductResource) -> None:
        self._product = product

    @cached_property
    def lists(self) -> ListsResourceWithStreamingResponse:
        return ListsResourceWithStreamingResponse(self._product.lists)

    @cached_property
    def top100(self) -> Top100ResourceWithStreamingResponse:
        return Top100ResourceWithStreamingResponse(self._product.top100)

    @cached_property
    def stats(self) -> StatsResourceWithStreamingResponse:
        return StatsResourceWithStreamingResponse(self._product.stats)

    @cached_property
    def species_list(self) -> SpeciesListResourceWithStreamingResponse:
        return SpeciesListResourceWithStreamingResponse(self._product.species_list)

    @cached_property
    def checklist(self) -> ChecklistResourceWithStreamingResponse:
        return ChecklistResourceWithStreamingResponse(self._product.checklist)


class AsyncProductResourceWithStreamingResponse:
    def __init__(self, product: AsyncProductResource) -> None:
        self._product = product

    @cached_property
    def lists(self) -> AsyncListsResourceWithStreamingResponse:
        return AsyncListsResourceWithStreamingResponse(self._product.lists)

    @cached_property
    def top100(self) -> AsyncTop100ResourceWithStreamingResponse:
        return AsyncTop100ResourceWithStreamingResponse(self._product.top100)

    @cached_property
    def stats(self) -> AsyncStatsResourceWithStreamingResponse:
        return AsyncStatsResourceWithStreamingResponse(self._product.stats)

    @cached_property
    def species_list(self) -> AsyncSpeciesListResourceWithStreamingResponse:
        return AsyncSpeciesListResourceWithStreamingResponse(self._product.species_list)

    @cached_property
    def checklist(self) -> AsyncChecklistResourceWithStreamingResponse:
        return AsyncChecklistResourceWithStreamingResponse(self._product.checklist)
