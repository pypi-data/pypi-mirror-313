# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from phoebe_bird import Phoebe, AsyncPhoebe
from tests.utils import assert_matches_type
from phoebe_bird.types.ref.region import ListListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestList:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Phoebe) -> None:
        list_ = client.ref.region.list.list(
            parent_region_code="parentRegionCode",
            region_type="regionType",
        )
        assert_matches_type(ListListResponse, list_, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Phoebe) -> None:
        list_ = client.ref.region.list.list(
            parent_region_code="parentRegionCode",
            region_type="regionType",
            fmt="csv",
        )
        assert_matches_type(ListListResponse, list_, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Phoebe) -> None:
        response = client.ref.region.list.with_raw_response.list(
            parent_region_code="parentRegionCode",
            region_type="regionType",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        list_ = response.parse()
        assert_matches_type(ListListResponse, list_, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Phoebe) -> None:
        with client.ref.region.list.with_streaming_response.list(
            parent_region_code="parentRegionCode",
            region_type="regionType",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            list_ = response.parse()
            assert_matches_type(ListListResponse, list_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Phoebe) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `region_type` but received ''"):
            client.ref.region.list.with_raw_response.list(
                parent_region_code="parentRegionCode",
                region_type="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `parent_region_code` but received ''"):
            client.ref.region.list.with_raw_response.list(
                parent_region_code="",
                region_type="regionType",
            )


class TestAsyncList:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncPhoebe) -> None:
        list_ = await async_client.ref.region.list.list(
            parent_region_code="parentRegionCode",
            region_type="regionType",
        )
        assert_matches_type(ListListResponse, list_, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncPhoebe) -> None:
        list_ = await async_client.ref.region.list.list(
            parent_region_code="parentRegionCode",
            region_type="regionType",
            fmt="csv",
        )
        assert_matches_type(ListListResponse, list_, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncPhoebe) -> None:
        response = await async_client.ref.region.list.with_raw_response.list(
            parent_region_code="parentRegionCode",
            region_type="regionType",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        list_ = await response.parse()
        assert_matches_type(ListListResponse, list_, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncPhoebe) -> None:
        async with async_client.ref.region.list.with_streaming_response.list(
            parent_region_code="parentRegionCode",
            region_type="regionType",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            list_ = await response.parse()
            assert_matches_type(ListListResponse, list_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncPhoebe) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `region_type` but received ''"):
            await async_client.ref.region.list.with_raw_response.list(
                parent_region_code="parentRegionCode",
                region_type="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `parent_region_code` but received ''"):
            await async_client.ref.region.list.with_raw_response.list(
                parent_region_code="",
                region_type="regionType",
            )
