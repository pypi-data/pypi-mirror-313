# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from bespokelabs import BespokeLabs, AsyncBespokeLabs
from tests.utils import assert_matches_type
from bespokelabs.types.minicheck import FactcheckCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFactcheck:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: BespokeLabs) -> None:
        factcheck = client.minicheck.factcheck.create(
            claim="claim",
            context="context",
        )
        assert_matches_type(FactcheckCreateResponse, factcheck, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: BespokeLabs) -> None:
        response = client.minicheck.factcheck.with_raw_response.create(
            claim="claim",
            context="context",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        factcheck = response.parse()
        assert_matches_type(FactcheckCreateResponse, factcheck, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: BespokeLabs) -> None:
        with client.minicheck.factcheck.with_streaming_response.create(
            claim="claim",
            context="context",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            factcheck = response.parse()
            assert_matches_type(FactcheckCreateResponse, factcheck, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncFactcheck:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncBespokeLabs) -> None:
        factcheck = await async_client.minicheck.factcheck.create(
            claim="claim",
            context="context",
        )
        assert_matches_type(FactcheckCreateResponse, factcheck, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncBespokeLabs) -> None:
        response = await async_client.minicheck.factcheck.with_raw_response.create(
            claim="claim",
            context="context",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        factcheck = await response.parse()
        assert_matches_type(FactcheckCreateResponse, factcheck, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncBespokeLabs) -> None:
        async with async_client.minicheck.factcheck.with_streaming_response.create(
            claim="claim",
            context="context",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            factcheck = await response.parse()
            assert_matches_type(FactcheckCreateResponse, factcheck, path=["response"])

        assert cast(Any, response.is_closed) is True
