# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from senso_developers import SensoDevelopers, AsyncSensoDevelopers
from senso_developers.types.orgs import Category, CategoryListResponse
from senso_developers.types.shared import Message

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCategories:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SensoDevelopers) -> None:
        category = client.orgs.categories.create(
            org_id="org_id",
            name="name",
        )
        assert_matches_type(Category, category, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: SensoDevelopers) -> None:
        category = client.orgs.categories.create(
            org_id="org_id",
            name="name",
            description="description",
        )
        assert_matches_type(Category, category, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SensoDevelopers) -> None:
        response = client.orgs.categories.with_raw_response.create(
            org_id="org_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        category = response.parse()
        assert_matches_type(Category, category, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SensoDevelopers) -> None:
        with client.orgs.categories.with_streaming_response.create(
            org_id="org_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            category = response.parse()
            assert_matches_type(Category, category, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_create(self, client: SensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.orgs.categories.with_raw_response.create(
                org_id="",
                name="name",
            )

    @parametrize
    def test_method_retrieve(self, client: SensoDevelopers) -> None:
        category = client.orgs.categories.retrieve(
            category_id="category_id",
            org_id="org_id",
        )
        assert_matches_type(Category, category, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SensoDevelopers) -> None:
        response = client.orgs.categories.with_raw_response.retrieve(
            category_id="category_id",
            org_id="org_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        category = response.parse()
        assert_matches_type(Category, category, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SensoDevelopers) -> None:
        with client.orgs.categories.with_streaming_response.retrieve(
            category_id="category_id",
            org_id="org_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            category = response.parse()
            assert_matches_type(Category, category, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.orgs.categories.with_raw_response.retrieve(
                category_id="category_id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `category_id` but received ''"):
            client.orgs.categories.with_raw_response.retrieve(
                category_id="",
                org_id="org_id",
            )

    @parametrize
    def test_method_update(self, client: SensoDevelopers) -> None:
        category = client.orgs.categories.update(
            category_id="category_id",
            org_id="org_id",
        )
        assert_matches_type(Category, category, path=["response"])

    @parametrize
    def test_method_update_with_all_params(self, client: SensoDevelopers) -> None:
        category = client.orgs.categories.update(
            category_id="category_id",
            org_id="org_id",
            description="description",
            name="name",
        )
        assert_matches_type(Category, category, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SensoDevelopers) -> None:
        response = client.orgs.categories.with_raw_response.update(
            category_id="category_id",
            org_id="org_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        category = response.parse()
        assert_matches_type(Category, category, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SensoDevelopers) -> None:
        with client.orgs.categories.with_streaming_response.update(
            category_id="category_id",
            org_id="org_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            category = response.parse()
            assert_matches_type(Category, category, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.orgs.categories.with_raw_response.update(
                category_id="category_id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `category_id` but received ''"):
            client.orgs.categories.with_raw_response.update(
                category_id="",
                org_id="org_id",
            )

    @parametrize
    def test_method_list(self, client: SensoDevelopers) -> None:
        category = client.orgs.categories.list(
            "org_id",
        )
        assert_matches_type(CategoryListResponse, category, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SensoDevelopers) -> None:
        response = client.orgs.categories.with_raw_response.list(
            "org_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        category = response.parse()
        assert_matches_type(CategoryListResponse, category, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SensoDevelopers) -> None:
        with client.orgs.categories.with_streaming_response.list(
            "org_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            category = response.parse()
            assert_matches_type(CategoryListResponse, category, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list(self, client: SensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.orgs.categories.with_raw_response.list(
                "",
            )

    @parametrize
    def test_method_delete(self, client: SensoDevelopers) -> None:
        category = client.orgs.categories.delete(
            category_id="category_id",
            org_id="org_id",
        )
        assert_matches_type(Message, category, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SensoDevelopers) -> None:
        response = client.orgs.categories.with_raw_response.delete(
            category_id="category_id",
            org_id="org_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        category = response.parse()
        assert_matches_type(Message, category, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SensoDevelopers) -> None:
        with client.orgs.categories.with_streaming_response.delete(
            category_id="category_id",
            org_id="org_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            category = response.parse()
            assert_matches_type(Message, category, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.orgs.categories.with_raw_response.delete(
                category_id="category_id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `category_id` but received ''"):
            client.orgs.categories.with_raw_response.delete(
                category_id="",
                org_id="org_id",
            )


class TestAsyncCategories:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSensoDevelopers) -> None:
        category = await async_client.orgs.categories.create(
            org_id="org_id",
            name="name",
        )
        assert_matches_type(Category, category, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSensoDevelopers) -> None:
        category = await async_client.orgs.categories.create(
            org_id="org_id",
            name="name",
            description="description",
        )
        assert_matches_type(Category, category, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.orgs.categories.with_raw_response.create(
            org_id="org_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        category = await response.parse()
        assert_matches_type(Category, category, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.orgs.categories.with_streaming_response.create(
            org_id="org_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            category = await response.parse()
            assert_matches_type(Category, category, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_create(self, async_client: AsyncSensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.orgs.categories.with_raw_response.create(
                org_id="",
                name="name",
            )

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSensoDevelopers) -> None:
        category = await async_client.orgs.categories.retrieve(
            category_id="category_id",
            org_id="org_id",
        )
        assert_matches_type(Category, category, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.orgs.categories.with_raw_response.retrieve(
            category_id="category_id",
            org_id="org_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        category = await response.parse()
        assert_matches_type(Category, category, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.orgs.categories.with_streaming_response.retrieve(
            category_id="category_id",
            org_id="org_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            category = await response.parse()
            assert_matches_type(Category, category, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.orgs.categories.with_raw_response.retrieve(
                category_id="category_id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `category_id` but received ''"):
            await async_client.orgs.categories.with_raw_response.retrieve(
                category_id="",
                org_id="org_id",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSensoDevelopers) -> None:
        category = await async_client.orgs.categories.update(
            category_id="category_id",
            org_id="org_id",
        )
        assert_matches_type(Category, category, path=["response"])

    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncSensoDevelopers) -> None:
        category = await async_client.orgs.categories.update(
            category_id="category_id",
            org_id="org_id",
            description="description",
            name="name",
        )
        assert_matches_type(Category, category, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.orgs.categories.with_raw_response.update(
            category_id="category_id",
            org_id="org_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        category = await response.parse()
        assert_matches_type(Category, category, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.orgs.categories.with_streaming_response.update(
            category_id="category_id",
            org_id="org_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            category = await response.parse()
            assert_matches_type(Category, category, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.orgs.categories.with_raw_response.update(
                category_id="category_id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `category_id` but received ''"):
            await async_client.orgs.categories.with_raw_response.update(
                category_id="",
                org_id="org_id",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSensoDevelopers) -> None:
        category = await async_client.orgs.categories.list(
            "org_id",
        )
        assert_matches_type(CategoryListResponse, category, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.orgs.categories.with_raw_response.list(
            "org_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        category = await response.parse()
        assert_matches_type(CategoryListResponse, category, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.orgs.categories.with_streaming_response.list(
            "org_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            category = await response.parse()
            assert_matches_type(CategoryListResponse, category, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list(self, async_client: AsyncSensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.orgs.categories.with_raw_response.list(
                "",
            )

    @parametrize
    async def test_method_delete(self, async_client: AsyncSensoDevelopers) -> None:
        category = await async_client.orgs.categories.delete(
            category_id="category_id",
            org_id="org_id",
        )
        assert_matches_type(Message, category, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.orgs.categories.with_raw_response.delete(
            category_id="category_id",
            org_id="org_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        category = await response.parse()
        assert_matches_type(Message, category, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.orgs.categories.with_streaming_response.delete(
            category_id="category_id",
            org_id="org_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            category = await response.parse()
            assert_matches_type(Message, category, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.orgs.categories.with_raw_response.delete(
                category_id="category_id",
                org_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `category_id` but received ''"):
            await async_client.orgs.categories.with_raw_response.delete(
                category_id="",
                org_id="org_id",
            )
