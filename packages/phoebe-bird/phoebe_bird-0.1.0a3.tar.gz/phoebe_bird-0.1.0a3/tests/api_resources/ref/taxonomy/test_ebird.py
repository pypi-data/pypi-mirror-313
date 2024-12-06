# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from phoebe_bird import Phoebe, AsyncPhoebe
from tests.utils import assert_matches_type
from phoebe_bird.types.ref.taxonomy import EbirdRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEbird:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Phoebe) -> None:
        ebird = client.ref.taxonomy.ebird.retrieve()
        assert_matches_type(EbirdRetrieveResponse, ebird, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Phoebe) -> None:
        ebird = client.ref.taxonomy.ebird.retrieve(
            cat="cat",
            fmt="csv",
            locale="locale",
            species="species",
            version="version",
        )
        assert_matches_type(EbirdRetrieveResponse, ebird, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Phoebe) -> None:
        response = client.ref.taxonomy.ebird.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        ebird = response.parse()
        assert_matches_type(EbirdRetrieveResponse, ebird, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Phoebe) -> None:
        with client.ref.taxonomy.ebird.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            ebird = response.parse()
            assert_matches_type(EbirdRetrieveResponse, ebird, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEbird:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncPhoebe) -> None:
        ebird = await async_client.ref.taxonomy.ebird.retrieve()
        assert_matches_type(EbirdRetrieveResponse, ebird, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncPhoebe) -> None:
        ebird = await async_client.ref.taxonomy.ebird.retrieve(
            cat="cat",
            fmt="csv",
            locale="locale",
            species="species",
            version="version",
        )
        assert_matches_type(EbirdRetrieveResponse, ebird, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncPhoebe) -> None:
        response = await async_client.ref.taxonomy.ebird.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        ebird = await response.parse()
        assert_matches_type(EbirdRetrieveResponse, ebird, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncPhoebe) -> None:
        async with async_client.ref.taxonomy.ebird.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            ebird = await response.parse()
            assert_matches_type(EbirdRetrieveResponse, ebird, path=["response"])

        assert cast(Any, response.is_closed) is True
