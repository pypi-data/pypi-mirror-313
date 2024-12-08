# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from senso_developers import SensoDevelopers, AsyncSensoDevelopers
from senso_developers.types import Org, OrgList
from senso_developers.types.shared import Message

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOrgs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: SensoDevelopers) -> None:
        org = client.orgs.create(
            name="name",
        )
        assert_matches_type(Org, org, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: SensoDevelopers) -> None:
        response = client.orgs.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        org = response.parse()
        assert_matches_type(Org, org, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: SensoDevelopers) -> None:
        with client.orgs.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            org = response.parse()
            assert_matches_type(Org, org, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: SensoDevelopers) -> None:
        org = client.orgs.retrieve(
            "org_id",
        )
        assert_matches_type(Org, org, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: SensoDevelopers) -> None:
        response = client.orgs.with_raw_response.retrieve(
            "org_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        org = response.parse()
        assert_matches_type(Org, org, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: SensoDevelopers) -> None:
        with client.orgs.with_streaming_response.retrieve(
            "org_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            org = response.parse()
            assert_matches_type(Org, org, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: SensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.orgs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_update(self, client: SensoDevelopers) -> None:
        org = client.orgs.update(
            org_id="org_id",
            name="name",
        )
        assert_matches_type(Org, org, path=["response"])

    @parametrize
    def test_raw_response_update(self, client: SensoDevelopers) -> None:
        response = client.orgs.with_raw_response.update(
            org_id="org_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        org = response.parse()
        assert_matches_type(Org, org, path=["response"])

    @parametrize
    def test_streaming_response_update(self, client: SensoDevelopers) -> None:
        with client.orgs.with_streaming_response.update(
            org_id="org_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            org = response.parse()
            assert_matches_type(Org, org, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update(self, client: SensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.orgs.with_raw_response.update(
                org_id="",
                name="name",
            )

    @parametrize
    def test_method_list(self, client: SensoDevelopers) -> None:
        org = client.orgs.list()
        assert_matches_type(OrgList, org, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: SensoDevelopers) -> None:
        response = client.orgs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        org = response.parse()
        assert_matches_type(OrgList, org, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: SensoDevelopers) -> None:
        with client.orgs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            org = response.parse()
            assert_matches_type(OrgList, org, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: SensoDevelopers) -> None:
        org = client.orgs.delete(
            "org_id",
        )
        assert_matches_type(Message, org, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: SensoDevelopers) -> None:
        response = client.orgs.with_raw_response.delete(
            "org_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        org = response.parse()
        assert_matches_type(Message, org, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: SensoDevelopers) -> None:
        with client.orgs.with_streaming_response.delete(
            "org_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            org = response.parse()
            assert_matches_type(Message, org, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: SensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            client.orgs.with_raw_response.delete(
                "",
            )


class TestAsyncOrgs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncSensoDevelopers) -> None:
        org = await async_client.orgs.create(
            name="name",
        )
        assert_matches_type(Org, org, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.orgs.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        org = await response.parse()
        assert_matches_type(Org, org, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.orgs.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            org = await response.parse()
            assert_matches_type(Org, org, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSensoDevelopers) -> None:
        org = await async_client.orgs.retrieve(
            "org_id",
        )
        assert_matches_type(Org, org, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.orgs.with_raw_response.retrieve(
            "org_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        org = await response.parse()
        assert_matches_type(Org, org, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.orgs.with_streaming_response.retrieve(
            "org_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            org = await response.parse()
            assert_matches_type(Org, org, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.orgs.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_update(self, async_client: AsyncSensoDevelopers) -> None:
        org = await async_client.orgs.update(
            org_id="org_id",
            name="name",
        )
        assert_matches_type(Org, org, path=["response"])

    @parametrize
    async def test_raw_response_update(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.orgs.with_raw_response.update(
            org_id="org_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        org = await response.parse()
        assert_matches_type(Org, org, path=["response"])

    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.orgs.with_streaming_response.update(
            org_id="org_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            org = await response.parse()
            assert_matches_type(Org, org, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update(self, async_client: AsyncSensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.orgs.with_raw_response.update(
                org_id="",
                name="name",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSensoDevelopers) -> None:
        org = await async_client.orgs.list()
        assert_matches_type(OrgList, org, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.orgs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        org = await response.parse()
        assert_matches_type(OrgList, org, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.orgs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            org = await response.parse()
            assert_matches_type(OrgList, org, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncSensoDevelopers) -> None:
        org = await async_client.orgs.delete(
            "org_id",
        )
        assert_matches_type(Message, org, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncSensoDevelopers) -> None:
        response = await async_client.orgs.with_raw_response.delete(
            "org_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        org = await response.parse()
        assert_matches_type(Message, org, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncSensoDevelopers) -> None:
        async with async_client.orgs.with_streaming_response.delete(
            "org_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            org = await response.parse()
            assert_matches_type(Message, org, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncSensoDevelopers) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `org_id` but received ''"):
            await async_client.orgs.with_raw_response.delete(
                "",
            )
