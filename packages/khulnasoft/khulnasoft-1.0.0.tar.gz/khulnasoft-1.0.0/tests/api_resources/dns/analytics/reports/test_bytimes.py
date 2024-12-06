# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Optional, cast

import pytest

from khulnasoft import Khulnasoft, AsyncKhulnasoft
from tests.utils import assert_matches_type
from khulnasoft._utils import parse_datetime
from khulnasoft.types.dns.analytics.reports import ByTime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBytimes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_get(self, client: Khulnasoft) -> None:
        bytime = client.dns.analytics.reports.bytimes.get(
            zone_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(Optional[ByTime], bytime, path=["response"])

    @parametrize
    def test_method_get_with_all_params(self, client: Khulnasoft) -> None:
        bytime = client.dns.analytics.reports.bytimes.get(
            zone_id="023e105f4ecef8ad9ca31a8372d0c353",
            dimensions="queryType",
            filters="responseCode==NOERROR,queryType==A",
            limit=100,
            metrics="queryCount,uncachedCount",
            since=parse_datetime("2023-11-11T12:00:00Z"),
            sort="+responseCode,-queryName",
            time_delta="hour",
            until=parse_datetime("2023-11-11T13:00:00Z"),
        )
        assert_matches_type(Optional[ByTime], bytime, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Khulnasoft) -> None:
        response = client.dns.analytics.reports.bytimes.with_raw_response.get(
            zone_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bytime = response.parse()
        assert_matches_type(Optional[ByTime], bytime, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Khulnasoft) -> None:
        with client.dns.analytics.reports.bytimes.with_streaming_response.get(
            zone_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bytime = response.parse()
            assert_matches_type(Optional[ByTime], bytime, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get(self, client: Khulnasoft) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `zone_id` but received ''"):
            client.dns.analytics.reports.bytimes.with_raw_response.get(
                zone_id="",
            )


class TestAsyncBytimes:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_get(self, async_client: AsyncKhulnasoft) -> None:
        bytime = await async_client.dns.analytics.reports.bytimes.get(
            zone_id="023e105f4ecef8ad9ca31a8372d0c353",
        )
        assert_matches_type(Optional[ByTime], bytime, path=["response"])

    @parametrize
    async def test_method_get_with_all_params(self, async_client: AsyncKhulnasoft) -> None:
        bytime = await async_client.dns.analytics.reports.bytimes.get(
            zone_id="023e105f4ecef8ad9ca31a8372d0c353",
            dimensions="queryType",
            filters="responseCode==NOERROR,queryType==A",
            limit=100,
            metrics="queryCount,uncachedCount",
            since=parse_datetime("2023-11-11T12:00:00Z"),
            sort="+responseCode,-queryName",
            time_delta="hour",
            until=parse_datetime("2023-11-11T13:00:00Z"),
        )
        assert_matches_type(Optional[ByTime], bytime, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncKhulnasoft) -> None:
        response = await async_client.dns.analytics.reports.bytimes.with_raw_response.get(
            zone_id="023e105f4ecef8ad9ca31a8372d0c353",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bytime = await response.parse()
        assert_matches_type(Optional[ByTime], bytime, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncKhulnasoft) -> None:
        async with async_client.dns.analytics.reports.bytimes.with_streaming_response.get(
            zone_id="023e105f4ecef8ad9ca31a8372d0c353",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bytime = await response.parse()
            assert_matches_type(Optional[ByTime], bytime, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get(self, async_client: AsyncKhulnasoft) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `zone_id` but received ''"):
            await async_client.dns.analytics.reports.bytimes.with_raw_response.get(
                zone_id="",
            )
