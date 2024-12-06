# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .ebird import (
    EbirdResource,
    AsyncEbirdResource,
    EbirdResourceWithRawResponse,
    AsyncEbirdResourceWithRawResponse,
    EbirdResourceWithStreamingResponse,
    AsyncEbirdResourceWithStreamingResponse,
)
from .forms import (
    FormsResource,
    AsyncFormsResource,
    FormsResourceWithRawResponse,
    AsyncFormsResourceWithRawResponse,
    FormsResourceWithStreamingResponse,
    AsyncFormsResourceWithStreamingResponse,
)
from .locales import (
    LocalesResource,
    AsyncLocalesResource,
    LocalesResourceWithRawResponse,
    AsyncLocalesResourceWithRawResponse,
    LocalesResourceWithStreamingResponse,
    AsyncLocalesResourceWithStreamingResponse,
)
from .versions import (
    VersionsResource,
    AsyncVersionsResource,
    VersionsResourceWithRawResponse,
    AsyncVersionsResourceWithRawResponse,
    VersionsResourceWithStreamingResponse,
    AsyncVersionsResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from .species_groups import (
    SpeciesGroupsResource,
    AsyncSpeciesGroupsResource,
    SpeciesGroupsResourceWithRawResponse,
    AsyncSpeciesGroupsResourceWithRawResponse,
    SpeciesGroupsResourceWithStreamingResponse,
    AsyncSpeciesGroupsResourceWithStreamingResponse,
)

__all__ = ["TaxonomyResource", "AsyncTaxonomyResource"]


class TaxonomyResource(SyncAPIResource):
    @cached_property
    def ebird(self) -> EbirdResource:
        return EbirdResource(self._client)

    @cached_property
    def forms(self) -> FormsResource:
        return FormsResource(self._client)

    @cached_property
    def locales(self) -> LocalesResource:
        return LocalesResource(self._client)

    @cached_property
    def versions(self) -> VersionsResource:
        return VersionsResource(self._client)

    @cached_property
    def species_groups(self) -> SpeciesGroupsResource:
        return SpeciesGroupsResource(self._client)

    @cached_property
    def with_raw_response(self) -> TaxonomyResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return TaxonomyResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TaxonomyResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return TaxonomyResourceWithStreamingResponse(self)


class AsyncTaxonomyResource(AsyncAPIResource):
    @cached_property
    def ebird(self) -> AsyncEbirdResource:
        return AsyncEbirdResource(self._client)

    @cached_property
    def forms(self) -> AsyncFormsResource:
        return AsyncFormsResource(self._client)

    @cached_property
    def locales(self) -> AsyncLocalesResource:
        return AsyncLocalesResource(self._client)

    @cached_property
    def versions(self) -> AsyncVersionsResource:
        return AsyncVersionsResource(self._client)

    @cached_property
    def species_groups(self) -> AsyncSpeciesGroupsResource:
        return AsyncSpeciesGroupsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTaxonomyResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTaxonomyResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTaxonomyResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncTaxonomyResourceWithStreamingResponse(self)


class TaxonomyResourceWithRawResponse:
    def __init__(self, taxonomy: TaxonomyResource) -> None:
        self._taxonomy = taxonomy

    @cached_property
    def ebird(self) -> EbirdResourceWithRawResponse:
        return EbirdResourceWithRawResponse(self._taxonomy.ebird)

    @cached_property
    def forms(self) -> FormsResourceWithRawResponse:
        return FormsResourceWithRawResponse(self._taxonomy.forms)

    @cached_property
    def locales(self) -> LocalesResourceWithRawResponse:
        return LocalesResourceWithRawResponse(self._taxonomy.locales)

    @cached_property
    def versions(self) -> VersionsResourceWithRawResponse:
        return VersionsResourceWithRawResponse(self._taxonomy.versions)

    @cached_property
    def species_groups(self) -> SpeciesGroupsResourceWithRawResponse:
        return SpeciesGroupsResourceWithRawResponse(self._taxonomy.species_groups)


class AsyncTaxonomyResourceWithRawResponse:
    def __init__(self, taxonomy: AsyncTaxonomyResource) -> None:
        self._taxonomy = taxonomy

    @cached_property
    def ebird(self) -> AsyncEbirdResourceWithRawResponse:
        return AsyncEbirdResourceWithRawResponse(self._taxonomy.ebird)

    @cached_property
    def forms(self) -> AsyncFormsResourceWithRawResponse:
        return AsyncFormsResourceWithRawResponse(self._taxonomy.forms)

    @cached_property
    def locales(self) -> AsyncLocalesResourceWithRawResponse:
        return AsyncLocalesResourceWithRawResponse(self._taxonomy.locales)

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithRawResponse:
        return AsyncVersionsResourceWithRawResponse(self._taxonomy.versions)

    @cached_property
    def species_groups(self) -> AsyncSpeciesGroupsResourceWithRawResponse:
        return AsyncSpeciesGroupsResourceWithRawResponse(self._taxonomy.species_groups)


class TaxonomyResourceWithStreamingResponse:
    def __init__(self, taxonomy: TaxonomyResource) -> None:
        self._taxonomy = taxonomy

    @cached_property
    def ebird(self) -> EbirdResourceWithStreamingResponse:
        return EbirdResourceWithStreamingResponse(self._taxonomy.ebird)

    @cached_property
    def forms(self) -> FormsResourceWithStreamingResponse:
        return FormsResourceWithStreamingResponse(self._taxonomy.forms)

    @cached_property
    def locales(self) -> LocalesResourceWithStreamingResponse:
        return LocalesResourceWithStreamingResponse(self._taxonomy.locales)

    @cached_property
    def versions(self) -> VersionsResourceWithStreamingResponse:
        return VersionsResourceWithStreamingResponse(self._taxonomy.versions)

    @cached_property
    def species_groups(self) -> SpeciesGroupsResourceWithStreamingResponse:
        return SpeciesGroupsResourceWithStreamingResponse(self._taxonomy.species_groups)


class AsyncTaxonomyResourceWithStreamingResponse:
    def __init__(self, taxonomy: AsyncTaxonomyResource) -> None:
        self._taxonomy = taxonomy

    @cached_property
    def ebird(self) -> AsyncEbirdResourceWithStreamingResponse:
        return AsyncEbirdResourceWithStreamingResponse(self._taxonomy.ebird)

    @cached_property
    def forms(self) -> AsyncFormsResourceWithStreamingResponse:
        return AsyncFormsResourceWithStreamingResponse(self._taxonomy.forms)

    @cached_property
    def locales(self) -> AsyncLocalesResourceWithStreamingResponse:
        return AsyncLocalesResourceWithStreamingResponse(self._taxonomy.locales)

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithStreamingResponse:
        return AsyncVersionsResourceWithStreamingResponse(self._taxonomy.versions)

    @cached_property
    def species_groups(self) -> AsyncSpeciesGroupsResourceWithStreamingResponse:
        return AsyncSpeciesGroupsResourceWithStreamingResponse(self._taxonomy.species_groups)
