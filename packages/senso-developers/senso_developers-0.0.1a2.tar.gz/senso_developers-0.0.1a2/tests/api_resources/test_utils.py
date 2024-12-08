# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from senso_developers import SensoDevelopers, AsyncSensoDevelopers
from senso_developers.types.shared import Message

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUtils:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_health_check(self, client: SensoDevelopers) -> None:
        util = client.utils.health_check()
        assert_matches_type(Message, util, path=["response"])

    @parametrize
    def test_raw_response_health_check(self, client: SensoDevelopers) -> None:
        response = client.utils.with_raw_response.health_check()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        util = response.parse()
        assert_matches_type(Message, util, path=["response"])

    @parametrize
    def test_streaming_response_health_check(self, client: SensoDevelopers) -> None:
        with client.utils.with_streaming_response.health_check() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            util = response.parse()
            assert_matches_type(Message, util, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_index(self, client: SensoDevelopers) -> None:
        util = client.utils.index()
        assert_matches_type(Message, util, path=["response"])

    @parametrize
    def test_raw_response_index(self, client: SensoDevelopers) -> None:
        response = client.utils.with_raw_response.index()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        util = response.parse()
        assert_matches_type(Message, util, path=["response"])

    @parametrize
    def test_streaming_response_index(self, client: SensoDevelopers) -> None:
        with client.utils.with_streaming_response.index() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            util = response.parse()
            assert_matches_type(Message, util, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncUtils:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_health_check(self, async_client: AsyncSensoDevelopers) -> None:
        util = await async_client.utils.health_check()
        assert_matches_type(Message, util, path=["response"])

    @parametrize
    async def test_raw_response_health_check(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.utils.with_raw_response.health_check()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        util = await response.parse()
        assert_matches_type(Message, util, path=["response"])

    @parametrize
    async def test_streaming_response_health_check(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.utils.with_streaming_response.health_check() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            util = await response.parse()
            assert_matches_type(Message, util, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_index(self, async_client: AsyncSensoDevelopers) -> None:
        util = await async_client.utils.index()
        assert_matches_type(Message, util, path=["response"])

    @parametrize
    async def test_raw_response_index(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.utils.with_raw_response.index()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        util = await response.parse()
        assert_matches_type(Message, util, path=["response"])

    @parametrize
    async def test_streaming_response_index(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.utils.with_streaming_response.index() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            util = await response.parse()
            assert_matches_type(Message, util, path=["response"])

        assert cast(Any, response.is_closed) is True
