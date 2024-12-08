# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from senso_developers import SensoDevelopers, AsyncSensoDevelopers
from senso_developers.types.orgs import Collection, CollectionList
from senso_developers.types.shared import Message

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCollections:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SensoDevelopers) -> None:
        collection = client.orgs.collections.create(
            org_id="org_id",
            name="name",
        )
        assert_matches_type(Collection, collection, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SensoDevelopers) -> None:
        collection = client.orgs.collections.create(
            org_id="org_id",
            name="name",
            visibility=0,
        )
        assert_matches_type(Collection, collection, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SensoDevelopers) -> None:
        response = client.orgs.collections.with_raw_response.create(
            org_id="org_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        collection = response.parse()
        assert_matches_type(Collection, collection, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SensoDevelopers) -> None:
        with client.orgs.collections.with_streaming_response.create(
            org_id="org_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            collection = response.parse()
            assert_matches_type(Collection, collection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.orgs.collections.with_raw_response.create(
                org_id="",
                name="name",
            )

    @parametrize
    def test_method_retrieve(self, client: SensoDevelopers) -> None:
        collection = client.orgs.collections.retrieve(
            collection_id="collection_id",
            org_id="org_id",
        )
        assert_matches_type(Collection, collection, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SensoDevelopers) -> None:
        response = client.orgs.collections.with_raw_response.retrieve(
            collection_id="collection_id",
            org_id="org_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        collection = response.parse()
        assert_matches_type(Collection, collection, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SensoDevelopers) -> None:
        with client.orgs.collections.with_streaming_response.retrieve(
            collection_id="collection_id",
            org_id="org_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            collection = response.parse()
            assert_matches_type(Collection, collection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.orgs.collections.with_raw_response.retrieve(
                collection_id="collection_id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `collection_id` but received ''"):
            client.orgs.collections.with_raw_response.retrieve(
                collection_id="",
                org_id="org_id",
            )

    @parametrize
    def test_method_update(self, client: SensoDevelopers) -> None:
        collection = client.orgs.collections.update(
            collection_id="collection_id",
            org_id="org_id",
            name="name",
        )
        assert_matches_type(Collection, collection, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SensoDevelopers) -> None:
        collection = client.orgs.collections.update(
            collection_id="collection_id",
            org_id="org_id",
            name="name",
            visibility=0,
        )
        assert_matches_type(Collection, collection, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SensoDevelopers) -> None:
        response = client.orgs.collections.with_raw_response.update(
            collection_id="collection_id",
            org_id="org_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        collection = response.parse()
        assert_matches_type(Collection, collection, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SensoDevelopers) -> None:
        with client.orgs.collections.with_streaming_response.update(
            collection_id="collection_id",
            org_id="org_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            collection = response.parse()
            assert_matches_type(Collection, collection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.orgs.collections.with_raw_response.update(
                collection_id="collection_id",
                org_id="",
                name="name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `collection_id` but received ''"):
            client.orgs.collections.with_raw_response.update(
                collection_id="",
                org_id="org_id",
                name="name",
            )

    @parametrize
    def test_method_list(self, client: SensoDevelopers) -> None:
        collection = client.orgs.collections.list(
            "org_id",
        )
        assert_matches_type(CollectionList, collection, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SensoDevelopers) -> None:
        response = client.orgs.collections.with_raw_response.list(
            "org_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        collection = response.parse()
        assert_matches_type(CollectionList, collection, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SensoDevelopers) -> None:
        with client.orgs.collections.with_streaming_response.list(
            "org_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            collection = response.parse()
            assert_matches_type(CollectionList, collection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.orgs.collections.with_raw_response.list(
                "",
            )

    @parametrize
    def test_method_delete(self, client: SensoDevelopers) -> None:
        collection = client.orgs.collections.delete(
            collection_id="collection_id",
            org_id="org_id",
        )
        assert_matches_type(Message, collection, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SensoDevelopers) -> None:
        response = client.orgs.collections.with_raw_response.delete(
            collection_id="collection_id",
            org_id="org_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        collection = response.parse()
        assert_matches_type(Message, collection, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SensoDevelopers) -> None:
        with client.orgs.collections.with_streaming_response.delete(
            collection_id="collection_id",
            org_id="org_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            collection = response.parse()
            assert_matches_type(Message, collection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.orgs.collections.with_raw_response.delete(
                collection_id="collection_id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `collection_id` but received ''"):
            client.orgs.collections.with_raw_response.delete(
                collection_id="",
                org_id="org_id",
            )


class TestAsyncCollections:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSensoDevelopers) -> None:
        collection = await async_client.orgs.collections.create(
            org_id="org_id",
            name="name",
        )
        assert_matches_type(Collection, collection, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSensoDevelopers) -> None:
        collection = await async_client.orgs.collections.create(
            org_id="org_id",
            name="name",
            visibility=0,
        )
        assert_matches_type(Collection, collection, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.orgs.collections.with_raw_response.create(
            org_id="org_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        collection = await response.parse()
        assert_matches_type(Collection, collection, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.orgs.collections.with_streaming_response.create(
            org_id="org_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            collection = await response.parse()
            assert_matches_type(Collection, collection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.orgs.collections.with_raw_response.create(
                org_id="",
                name="name",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSensoDevelopers) -> None:
        collection = await async_client.orgs.collections.retrieve(
            collection_id="collection_id",
            org_id="org_id",
        )
        assert_matches_type(Collection, collection, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.orgs.collections.with_raw_response.retrieve(
            collection_id="collection_id",
            org_id="org_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        collection = await response.parse()
        assert_matches_type(Collection, collection, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.orgs.collections.with_streaming_response.retrieve(
            collection_id="collection_id",
            org_id="org_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            collection = await response.parse()
            assert_matches_type(Collection, collection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.orgs.collections.with_raw_response.retrieve(
                collection_id="collection_id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `collection_id` but received ''"):
            await async_client.orgs.collections.with_raw_response.retrieve(
                collection_id="",
                org_id="org_id",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSensoDevelopers) -> None:
        collection = await async_client.orgs.collections.update(
            collection_id="collection_id",
            org_id="org_id",
            name="name",
        )
        assert_matches_type(Collection, collection, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSensoDevelopers) -> None:
        collection = await async_client.orgs.collections.update(
            collection_id="collection_id",
            org_id="org_id",
            name="name",
            visibility=0,
        )
        assert_matches_type(Collection, collection, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.orgs.collections.with_raw_response.update(
            collection_id="collection_id",
            org_id="org_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        collection = await response.parse()
        assert_matches_type(Collection, collection, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.orgs.collections.with_streaming_response.update(
            collection_id="collection_id",
            org_id="org_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            collection = await response.parse()
            assert_matches_type(Collection, collection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.orgs.collections.with_raw_response.update(
                collection_id="collection_id",
                org_id="",
                name="name",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `collection_id` but received ''"):
            await async_client.orgs.collections.with_raw_response.update(
                collection_id="",
                org_id="org_id",
                name="name",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSensoDevelopers) -> None:
        collection = await async_client.orgs.collections.list(
            "org_id",
        )
        assert_matches_type(CollectionList, collection, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.orgs.collections.with_raw_response.list(
            "org_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        collection = await response.parse()
        assert_matches_type(CollectionList, collection, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.orgs.collections.with_streaming_response.list(
            "org_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            collection = await response.parse()
            assert_matches_type(CollectionList, collection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.orgs.collections.with_raw_response.list(
                "",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncSensoDevelopers) -> None:
        collection = await async_client.orgs.collections.delete(
            collection_id="collection_id",
            org_id="org_id",
        )
        assert_matches_type(Message, collection, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.orgs.collections.with_raw_response.delete(
            collection_id="collection_id",
            org_id="org_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        collection = await response.parse()
        assert_matches_type(Message, collection, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.orgs.collections.with_streaming_response.delete(
            collection_id="collection_id",
            org_id="org_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            collection = await response.parse()
            assert_matches_type(Message, collection, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.orgs.collections.with_raw_response.delete(
                collection_id="collection_id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `collection_id` but received ''"):
            await async_client.orgs.collections.with_raw_response.delete(
                collection_id="",
                org_id="org_id",
            )
