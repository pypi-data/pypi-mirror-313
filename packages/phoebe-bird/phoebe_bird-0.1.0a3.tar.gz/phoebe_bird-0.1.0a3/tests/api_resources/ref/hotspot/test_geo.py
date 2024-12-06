# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from phoebe_bird import Phoebe, AsyncPhoebe
from tests.utils import assert_matches_type
from phoebe_bird.types.ref.hotspot import GeoRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestGeo:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Phoebe) -> None:
        geo = client.ref.hotspot.geo.retrieve(
            lat=-90,
            lng=-180,
        )
        assert_matches_type(GeoRetrieveResponse, geo, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Phoebe) -> None:
        geo = client.ref.hotspot.geo.retrieve(
            lat=-90,
            lng=-180,
            back=1,
            dist=0,
            fmt="csv",
        )
        assert_matches_type(GeoRetrieveResponse, geo, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Phoebe) -> None:
        response = client.ref.hotspot.geo.with_raw_response.retrieve(
            lat=-90,
            lng=-180,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        geo = response.parse()
        assert_matches_type(GeoRetrieveResponse, geo, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Phoebe) -> None:
        with client.ref.hotspot.geo.with_streaming_response.retrieve(
            lat=-90,
            lng=-180,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            geo = response.parse()
            assert_matches_type(GeoRetrieveResponse, geo, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncGeo:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncPhoebe) -> None:
        geo = await async_client.ref.hotspot.geo.retrieve(
            lat=-90,
            lng=-180,
        )
        assert_matches_type(GeoRetrieveResponse, geo, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncPhoebe) -> None:
        geo = await async_client.ref.hotspot.geo.retrieve(
            lat=-90,
            lng=-180,
            back=1,
            dist=0,
            fmt="csv",
        )
        assert_matches_type(GeoRetrieveResponse, geo, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncPhoebe) -> None:
        response = await async_client.ref.hotspot.geo.with_raw_response.retrieve(
            lat=-90,
            lng=-180,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        geo = await response.parse()
        assert_matches_type(GeoRetrieveResponse, geo, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncPhoebe) -> None:
        async with async_client.ref.hotspot.geo.with_streaming_response.retrieve(
            lat=-90,
            lng=-180,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            geo = await response.parse()
            assert_matches_type(GeoRetrieveResponse, geo, path=["response"])

        assert cast(Any, response.is_closed) is True
