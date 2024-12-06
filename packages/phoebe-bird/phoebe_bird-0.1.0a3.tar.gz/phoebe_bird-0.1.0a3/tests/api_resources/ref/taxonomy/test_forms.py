# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from phoebe_bird import Phoebe, AsyncPhoebe
from tests.utils import assert_matches_type
from phoebe_bird.types.ref.taxonomy import FormListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestForms:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: Phoebe) -> None:
        form = client.ref.taxonomy.forms.list(
            "speciesCode",
        )
        assert_matches_type(FormListResponse, form, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Phoebe) -> None:
        response = client.ref.taxonomy.forms.with_raw_response.list(
            "speciesCode",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        form = response.parse()
        assert_matches_type(FormListResponse, form, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Phoebe) -> None:
        with client.ref.taxonomy.forms.with_streaming_response.list(
            "speciesCode",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            form = response.parse()
            assert_matches_type(FormListResponse, form, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: Phoebe) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `species_code` but received ''"):
            client.ref.taxonomy.forms.with_raw_response.list(
                "",
            )


class TestAsyncForms:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncPhoebe) -> None:
        form = await async_client.ref.taxonomy.forms.list(
            "speciesCode",
        )
        assert_matches_type(FormListResponse, form, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncPhoebe) -> None:
        response = await async_client.ref.taxonomy.forms.with_raw_response.list(
            "speciesCode",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        form = await response.parse()
        assert_matches_type(FormListResponse, form, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncPhoebe) -> None:
        async with async_client.ref.taxonomy.forms.with_streaming_response.list(
            "speciesCode",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            form = await response.parse()
            assert_matches_type(FormListResponse, form, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncPhoebe) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `species_code` but received ''"):
            await async_client.ref.taxonomy.forms.with_raw_response.list(
                "",
            )
