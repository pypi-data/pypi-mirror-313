# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from phoebe_bird import Phoebe, AsyncPhoebe
from tests.utils import assert_matches_type
from phoebe_bird.types.ref.taxonomy import SpeciesGroupListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSpeciesGroups:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Phoebe) -> None:
        species_group = client.ref.taxonomy.species_groups.list(
            species_grouping="merlin",
        )
        assert_matches_type(SpeciesGroupListResponse, species_group, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Phoebe) -> None:
        species_group = client.ref.taxonomy.species_groups.list(
            species_grouping="merlin",
            group_name_locale="groupNameLocale",
        )
        assert_matches_type(SpeciesGroupListResponse, species_group, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Phoebe) -> None:
        response = client.ref.taxonomy.species_groups.with_raw_response.list(
            species_grouping="merlin",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        species_group = response.parse()
        assert_matches_type(SpeciesGroupListResponse, species_group, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Phoebe) -> None:
        with client.ref.taxonomy.species_groups.with_streaming_response.list(
            species_grouping="merlin",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            species_group = response.parse()
            assert_matches_type(SpeciesGroupListResponse, species_group, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSpeciesGroups:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncPhoebe) -> None:
        species_group = await async_client.ref.taxonomy.species_groups.list(
            species_grouping="merlin",
        )
        assert_matches_type(SpeciesGroupListResponse, species_group, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncPhoebe) -> None:
        species_group = await async_client.ref.taxonomy.species_groups.list(
            species_grouping="merlin",
            group_name_locale="groupNameLocale",
        )
        assert_matches_type(SpeciesGroupListResponse, species_group, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncPhoebe) -> None:
        response = await async_client.ref.taxonomy.species_groups.with_raw_response.list(
            species_grouping="merlin",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        species_group = await response.parse()
        assert_matches_type(SpeciesGroupListResponse, species_group, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncPhoebe) -> None:
        async with async_client.ref.taxonomy.species_groups.with_streaming_response.list(
            species_grouping="merlin",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            species_group = await response.parse()
            assert_matches_type(SpeciesGroupListResponse, species_group, path=["response"])

        assert cast(Any, response.is_closed) is True
