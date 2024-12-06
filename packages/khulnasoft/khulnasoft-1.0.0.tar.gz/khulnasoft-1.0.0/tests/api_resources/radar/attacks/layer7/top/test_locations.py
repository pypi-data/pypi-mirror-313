# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from khulnasoft import Khulnasoft, AsyncKhulnasoft
from tests.utils import assert_matches_type
from khulnasoft._utils import parse_datetime
from khulnasoft.types.radar.attacks.layer7.top import (
    LocationOriginResponse,
    LocationTargetResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestLocations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_origin(self, client: Khulnasoft) -> None:
        location = client.radar.attacks.layer7.top.locations.origin()
        assert_matches_type(LocationOriginResponse, location, path=["response"])

    @parametrize
    def test_method_origin_with_all_params(self, client: Khulnasoft) -> None:
        location = client.radar.attacks.layer7.top.locations.origin(
            asn=["string", "string", "string"],
            continent=["string", "string", "string"],
            date_end=[
                parse_datetime("2019-12-27T18:11:19.117Z"),
                parse_datetime("2019-12-27T18:11:19.117Z"),
                parse_datetime("2019-12-27T18:11:19.117Z"),
            ],
            date_range=["7d", "7d", "7d"],
            date_start=[
                parse_datetime("2019-12-27T18:11:19.117Z"),
                parse_datetime("2019-12-27T18:11:19.117Z"),
                parse_datetime("2019-12-27T18:11:19.117Z"),
            ],
            format="JSON",
            http_method=["GET", "POST", "DELETE"],
            http_version=["HTTPv1", "HTTPv2", "HTTPv3"],
            ip_version=["IPv4", "IPv6"],
            limit=5,
            mitigation_product=["DDOS", "WAF", "BOT_MANAGEMENT"],
            name=["string", "string", "string"],
        )
        assert_matches_type(LocationOriginResponse, location, path=["response"])

    @parametrize
    def test_raw_response_origin(self, client: Khulnasoft) -> None:
        response = client.radar.attacks.layer7.top.locations.with_raw_response.origin()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        location = response.parse()
        assert_matches_type(LocationOriginResponse, location, path=["response"])

    @parametrize
    def test_streaming_response_origin(self, client: Khulnasoft) -> None:
        with client.radar.attacks.layer7.top.locations.with_streaming_response.origin() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            location = response.parse()
            assert_matches_type(LocationOriginResponse, location, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_target(self, client: Khulnasoft) -> None:
        location = client.radar.attacks.layer7.top.locations.target()
        assert_matches_type(LocationTargetResponse, location, path=["response"])

    @parametrize
    def test_method_target_with_all_params(self, client: Khulnasoft) -> None:
        location = client.radar.attacks.layer7.top.locations.target(
            continent=["string", "string", "string"],
            date_end=[
                parse_datetime("2019-12-27T18:11:19.117Z"),
                parse_datetime("2019-12-27T18:11:19.117Z"),
                parse_datetime("2019-12-27T18:11:19.117Z"),
            ],
            date_range=["7d", "7d", "7d"],
            date_start=[
                parse_datetime("2019-12-27T18:11:19.117Z"),
                parse_datetime("2019-12-27T18:11:19.117Z"),
                parse_datetime("2019-12-27T18:11:19.117Z"),
            ],
            format="JSON",
            http_method=["GET", "POST", "DELETE"],
            http_version=["HTTPv1", "HTTPv2", "HTTPv3"],
            ip_version=["IPv4", "IPv6"],
            limit=5,
            mitigation_product=["DDOS", "WAF", "BOT_MANAGEMENT"],
            name=["string", "string", "string"],
        )
        assert_matches_type(LocationTargetResponse, location, path=["response"])

    @parametrize
    def test_raw_response_target(self, client: Khulnasoft) -> None:
        response = client.radar.attacks.layer7.top.locations.with_raw_response.target()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        location = response.parse()
        assert_matches_type(LocationTargetResponse, location, path=["response"])

    @parametrize
    def test_streaming_response_target(self, client: Khulnasoft) -> None:
        with client.radar.attacks.layer7.top.locations.with_streaming_response.target() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            location = response.parse()
            assert_matches_type(LocationTargetResponse, location, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncLocations:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_origin(self, async_client: AsyncKhulnasoft) -> None:
        location = await async_client.radar.attacks.layer7.top.locations.origin()
        assert_matches_type(LocationOriginResponse, location, path=["response"])

    @parametrize
    async def test_method_origin_with_all_params(self, async_client: AsyncKhulnasoft) -> None:
        location = await async_client.radar.attacks.layer7.top.locations.origin(
            asn=["string", "string", "string"],
            continent=["string", "string", "string"],
            date_end=[
                parse_datetime("2019-12-27T18:11:19.117Z"),
                parse_datetime("2019-12-27T18:11:19.117Z"),
                parse_datetime("2019-12-27T18:11:19.117Z"),
            ],
            date_range=["7d", "7d", "7d"],
            date_start=[
                parse_datetime("2019-12-27T18:11:19.117Z"),
                parse_datetime("2019-12-27T18:11:19.117Z"),
                parse_datetime("2019-12-27T18:11:19.117Z"),
            ],
            format="JSON",
            http_method=["GET", "POST", "DELETE"],
            http_version=["HTTPv1", "HTTPv2", "HTTPv3"],
            ip_version=["IPv4", "IPv6"],
            limit=5,
            mitigation_product=["DDOS", "WAF", "BOT_MANAGEMENT"],
            name=["string", "string", "string"],
        )
        assert_matches_type(LocationOriginResponse, location, path=["response"])

    @parametrize
    async def test_raw_response_origin(self, async_client: AsyncKhulnasoft) -> None:
        response = await async_client.radar.attacks.layer7.top.locations.with_raw_response.origin()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        location = await response.parse()
        assert_matches_type(LocationOriginResponse, location, path=["response"])

    @parametrize
    async def test_streaming_response_origin(self, async_client: AsyncKhulnasoft) -> None:
        async with async_client.radar.attacks.layer7.top.locations.with_streaming_response.origin() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            location = await response.parse()
            assert_matches_type(LocationOriginResponse, location, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_target(self, async_client: AsyncKhulnasoft) -> None:
        location = await async_client.radar.attacks.layer7.top.locations.target()
        assert_matches_type(LocationTargetResponse, location, path=["response"])

    @parametrize
    async def test_method_target_with_all_params(self, async_client: AsyncKhulnasoft) -> None:
        location = await async_client.radar.attacks.layer7.top.locations.target(
            continent=["string", "string", "string"],
            date_end=[
                parse_datetime("2019-12-27T18:11:19.117Z"),
                parse_datetime("2019-12-27T18:11:19.117Z"),
                parse_datetime("2019-12-27T18:11:19.117Z"),
            ],
            date_range=["7d", "7d", "7d"],
            date_start=[
                parse_datetime("2019-12-27T18:11:19.117Z"),
                parse_datetime("2019-12-27T18:11:19.117Z"),
                parse_datetime("2019-12-27T18:11:19.117Z"),
            ],
            format="JSON",
            http_method=["GET", "POST", "DELETE"],
            http_version=["HTTPv1", "HTTPv2", "HTTPv3"],
            ip_version=["IPv4", "IPv6"],
            limit=5,
            mitigation_product=["DDOS", "WAF", "BOT_MANAGEMENT"],
            name=["string", "string", "string"],
        )
        assert_matches_type(LocationTargetResponse, location, path=["response"])

    @parametrize
    async def test_raw_response_target(self, async_client: AsyncKhulnasoft) -> None:
        response = await async_client.radar.attacks.layer7.top.locations.with_raw_response.target()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        location = await response.parse()
        assert_matches_type(LocationTargetResponse, location, path=["response"])

    @parametrize
    async def test_streaming_response_target(self, async_client: AsyncKhulnasoft) -> None:
        async with async_client.radar.attacks.layer7.top.locations.with_streaming_response.target() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            location = await response.parse()
            assert_matches_type(LocationTargetResponse, location, path=["response"])

        assert cast(Any, response.is_closed) is True
