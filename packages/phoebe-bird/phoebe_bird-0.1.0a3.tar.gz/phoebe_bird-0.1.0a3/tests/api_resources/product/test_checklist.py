# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from phoebe_bird import Phoebe, AsyncPhoebe
from tests.utils import assert_matches_type
from phoebe_bird.types.product import ChecklistViewResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChecklist:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_view(self, client: Phoebe) -> None:
        checklist = client.product.checklist.view(
            "subId",
        )
        assert_matches_type(ChecklistViewResponse, checklist, path=["response"])

    @parametrize
    def test_raw_response_view(self, client: Phoebe) -> None:
        response = client.product.checklist.with_raw_response.view(
            "subId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        checklist = response.parse()
        assert_matches_type(ChecklistViewResponse, checklist, path=["response"])

    @parametrize
    def test_streaming_response_view(self, client: Phoebe) -> None:
        with client.product.checklist.with_streaming_response.view(
            "subId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            checklist = response.parse()
            assert_matches_type(ChecklistViewResponse, checklist, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_view(self, client: Phoebe) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `sub_id` but received ''"):
            client.product.checklist.with_raw_response.view(
                "",
            )


class TestAsyncChecklist:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_view(self, async_client: AsyncPhoebe) -> None:
        checklist = await async_client.product.checklist.view(
            "subId",
        )
        assert_matches_type(ChecklistViewResponse, checklist, path=["response"])

    @parametrize
    async def test_raw_response_view(self, async_client: AsyncPhoebe) -> None:
        response = await async_client.product.checklist.with_raw_response.view(
            "subId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        checklist = await response.parse()
        assert_matches_type(ChecklistViewResponse, checklist, path=["response"])

    @parametrize
    async def test_streaming_response_view(self, async_client: AsyncPhoebe) -> None:
        async with async_client.product.checklist.with_streaming_response.view(
            "subId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            checklist = await response.parse()
            assert_matches_type(ChecklistViewResponse, checklist, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_view(self, async_client: AsyncPhoebe) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `sub_id` but received ''"):
            await async_client.product.checklist.with_raw_response.view(
                "",
            )
