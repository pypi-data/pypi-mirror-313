# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from phoebe_bird import Phoebe, AsyncPhoebe
from tests.utils import assert_matches_type
from phoebe_bird.types.product.lists import HistoricalRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestHistorical:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Phoebe) -> None:
        historical = client.product.lists.historical.retrieve(
            d=1,
            region_code="regionCode",
            y=0,
            m=1,
        )
        assert_matches_type(HistoricalRetrieveResponse, historical, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Phoebe) -> None:
        historical = client.product.lists.historical.retrieve(
            d=1,
            region_code="regionCode",
            y=0,
            m=1,
            max_results=1,
            sort_key="obs_dt",
        )
        assert_matches_type(HistoricalRetrieveResponse, historical, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Phoebe) -> None:
        response = client.product.lists.historical.with_raw_response.retrieve(
            d=1,
            region_code="regionCode",
            y=0,
            m=1,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        historical = response.parse()
        assert_matches_type(HistoricalRetrieveResponse, historical, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Phoebe) -> None:
        with client.product.lists.historical.with_streaming_response.retrieve(
            d=1,
            region_code="regionCode",
            y=0,
            m=1,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            historical = response.parse()
            assert_matches_type(HistoricalRetrieveResponse, historical, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Phoebe) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `region_code` but received ''"):
            client.product.lists.historical.with_raw_response.retrieve(
                d=1,
                region_code="",
                y=0,
                m=1,
            )


class TestAsyncHistorical:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncPhoebe) -> None:
        historical = await async_client.product.lists.historical.retrieve(
            d=1,
            region_code="regionCode",
            y=0,
            m=1,
        )
        assert_matches_type(HistoricalRetrieveResponse, historical, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncPhoebe) -> None:
        historical = await async_client.product.lists.historical.retrieve(
            d=1,
            region_code="regionCode",
            y=0,
            m=1,
            max_results=1,
            sort_key="obs_dt",
        )
        assert_matches_type(HistoricalRetrieveResponse, historical, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncPhoebe) -> None:
        response = await async_client.product.lists.historical.with_raw_response.retrieve(
            d=1,
            region_code="regionCode",
            y=0,
            m=1,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        historical = await response.parse()
        assert_matches_type(HistoricalRetrieveResponse, historical, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncPhoebe) -> None:
        async with async_client.product.lists.historical.with_streaming_response.retrieve(
            d=1,
            region_code="regionCode",
            y=0,
            m=1,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            historical = await response.parse()
            assert_matches_type(HistoricalRetrieveResponse, historical, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncPhoebe) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `region_code` but received ''"):
            await async_client.product.lists.historical.with_raw_response.retrieve(
                d=1,
                region_code="",
                y=0,
                m=1,
            )
