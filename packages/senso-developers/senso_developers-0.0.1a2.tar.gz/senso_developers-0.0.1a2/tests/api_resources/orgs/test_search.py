# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from senso_developers import SensoDevelopers, AsyncSensoDevelopers
from senso_developers.types.orgs import (
    SearchChunksResponse,
    SearchDocumentsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSearch:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_chunks(self, client: SensoDevelopers) -> None:
        search = client.orgs.search.chunks(
            org_id="org_id",
            query="query",
        )
        assert_matches_type(SearchChunksResponse, search, path=["response"])

    @parametrize
    def test_method_chunks_with_all_params(self, client: SensoDevelopers) -> None:
        search = client.orgs.search.chunks(
            org_id="org_id",
            query="query",
            top_k=0,
        )
        assert_matches_type(SearchChunksResponse, search, path=["response"])

    @parametrize
    def test_raw_response_chunks(self, client: SensoDevelopers) -> None:
        response = client.orgs.search.with_raw_response.chunks(
            org_id="org_id",
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(SearchChunksResponse, search, path=["response"])

    @parametrize
    def test_streaming_response_chunks(self, client: SensoDevelopers) -> None:
        with client.orgs.search.with_streaming_response.chunks(
            org_id="org_id",
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(SearchChunksResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_chunks(self, client: SensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.orgs.search.with_raw_response.chunks(
                org_id="",
                query="query",
            )

    @parametrize
    def test_method_documents(self, client: SensoDevelopers) -> None:
        search = client.orgs.search.documents(
            org_id="org_id",
            query="query",
        )
        assert_matches_type(SearchDocumentsResponse, search, path=["response"])

    @parametrize
    def test_method_documents_with_all_params(self, client: SensoDevelopers) -> None:
        search = client.orgs.search.documents(
            org_id="org_id",
            query="query",
            top_k=0,
        )
        assert_matches_type(SearchDocumentsResponse, search, path=["response"])

    @parametrize
    def test_raw_response_documents(self, client: SensoDevelopers) -> None:
        response = client.orgs.search.with_raw_response.documents(
            org_id="org_id",
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(SearchDocumentsResponse, search, path=["response"])

    @parametrize
    def test_streaming_response_documents(self, client: SensoDevelopers) -> None:
        with client.orgs.search.with_streaming_response.documents(
            org_id="org_id",
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(SearchDocumentsResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_documents(self, client: SensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.orgs.search.with_raw_response.documents(
                org_id="",
                query="query",
            )


class TestAsyncSearch:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_chunks(self, async_client: AsyncSensoDevelopers) -> None:
        search = await async_client.orgs.search.chunks(
            org_id="org_id",
            query="query",
        )
        assert_matches_type(SearchChunksResponse, search, path=["response"])

    @parametrize
    async def test_method_chunks_with_all_params(self, async_client: AsyncSensoDevelopers) -> None:
        search = await async_client.orgs.search.chunks(
            org_id="org_id",
            query="query",
            top_k=0,
        )
        assert_matches_type(SearchChunksResponse, search, path=["response"])

    @parametrize
    async def test_raw_response_chunks(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.orgs.search.with_raw_response.chunks(
            org_id="org_id",
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(SearchChunksResponse, search, path=["response"])

    @parametrize
    async def test_streaming_response_chunks(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.orgs.search.with_streaming_response.chunks(
            org_id="org_id",
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(SearchChunksResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_chunks(self, async_client: AsyncSensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.orgs.search.with_raw_response.chunks(
                org_id="",
                query="query",
            )

    @parametrize
    async def test_method_documents(self, async_client: AsyncSensoDevelopers) -> None:
        search = await async_client.orgs.search.documents(
            org_id="org_id",
            query="query",
        )
        assert_matches_type(SearchDocumentsResponse, search, path=["response"])

    @parametrize
    async def test_method_documents_with_all_params(self, async_client: AsyncSensoDevelopers) -> None:
        search = await async_client.orgs.search.documents(
            org_id="org_id",
            query="query",
            top_k=0,
        )
        assert_matches_type(SearchDocumentsResponse, search, path=["response"])

    @parametrize
    async def test_raw_response_documents(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.orgs.search.with_raw_response.documents(
            org_id="org_id",
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(SearchDocumentsResponse, search, path=["response"])

    @parametrize
    async def test_streaming_response_documents(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.orgs.search.with_streaming_response.documents(
            org_id="org_id",
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(SearchDocumentsResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_documents(self, async_client: AsyncSensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.orgs.search.with_raw_response.documents(
                org_id="",
                query="query",
            )
