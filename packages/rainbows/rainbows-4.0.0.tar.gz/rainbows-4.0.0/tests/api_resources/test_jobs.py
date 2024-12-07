# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from rainbows import Rainbows, AsyncRainbows
from tests.utils import assert_matches_type
from rainbows.types import (
    JobGetResponse,
    JobUpsertResponse,
    JobRetrieveTermBasedResponse,
)
from rainbows._utils import parse_date

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestJobs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_get(self, client: Rainbows) -> None:
        job = client.jobs.get()
        assert_matches_type(JobGetResponse, job, path=["response"])

    @parametrize
    def test_method_get_with_all_params(self, client: Rainbows) -> None:
        job = client.jobs.get(
            board_url_contains="board_url_contains",
            board_urls=["string"],
            countries=[{"code": "code"}],
            description_terms={
                "all_of": ["string"],
                "any_of": ["string"],
                "none_of": ["string"],
            },
            last_scraped_date_range={
                "end": parse_date("2019-12-27"),
                "start": parse_date("2019-12-27"),
            },
            null_columns=["string"],
            page_number=0,
            page_size=0,
            title_terms={
                "all_of": ["string"],
                "any_of": ["string"],
                "none_of": ["string"],
            },
            urls=["string"],
        )
        assert_matches_type(JobGetResponse, job, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Rainbows) -> None:
        response = client.jobs.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(JobGetResponse, job, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Rainbows) -> None:
        with client.jobs.with_streaming_response.get() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(JobGetResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve_term_based(self, client: Rainbows) -> None:
        job = client.jobs.retrieve_term_based(
            query="Find software engineering jobs in the US posted in the last month",
        )
        assert_matches_type(JobRetrieveTermBasedResponse, job, path=["response"])

    @parametrize
    def test_raw_response_retrieve_term_based(self, client: Rainbows) -> None:
        response = client.jobs.with_raw_response.retrieve_term_based(
            query="Find software engineering jobs in the US posted in the last month",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(JobRetrieveTermBasedResponse, job, path=["response"])

    @parametrize
    def test_streaming_response_retrieve_term_based(self, client: Rainbows) -> None:
        with client.jobs.with_streaming_response.retrieve_term_based(
            query="Find software engineering jobs in the US posted in the last month",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(JobRetrieveTermBasedResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_upsert(self, client: Rainbows) -> None:
        job = client.jobs.upsert(
            jobs=[{"url": "url"}],
        )
        assert_matches_type(JobUpsertResponse, job, path=["response"])

    @parametrize
    def test_method_upsert_with_all_params(self, client: Rainbows) -> None:
        job = client.jobs.upsert(
            jobs=[
                {
                    "url": "url",
                    "board_url": "board_url",
                    "countries": ["string"],
                    "description": "description",
                    "last_scraped_date": "last_scraped_date",
                    "location": "location",
                    "title": "title",
                }
            ],
            batch_size=0,
        )
        assert_matches_type(JobUpsertResponse, job, path=["response"])

    @parametrize
    def test_raw_response_upsert(self, client: Rainbows) -> None:
        response = client.jobs.with_raw_response.upsert(
            jobs=[{"url": "url"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(JobUpsertResponse, job, path=["response"])

    @parametrize
    def test_streaming_response_upsert(self, client: Rainbows) -> None:
        with client.jobs.with_streaming_response.upsert(
            jobs=[{"url": "url"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(JobUpsertResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncJobs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_get(self, async_client: AsyncRainbows) -> None:
        job = await async_client.jobs.get()
        assert_matches_type(JobGetResponse, job, path=["response"])

    @parametrize
    async def test_method_get_with_all_params(self, async_client: AsyncRainbows) -> None:
        job = await async_client.jobs.get(
            board_url_contains="board_url_contains",
            board_urls=["string"],
            countries=[{"code": "code"}],
            description_terms={
                "all_of": ["string"],
                "any_of": ["string"],
                "none_of": ["string"],
            },
            last_scraped_date_range={
                "end": parse_date("2019-12-27"),
                "start": parse_date("2019-12-27"),
            },
            null_columns=["string"],
            page_number=0,
            page_size=0,
            title_terms={
                "all_of": ["string"],
                "any_of": ["string"],
                "none_of": ["string"],
            },
            urls=["string"],
        )
        assert_matches_type(JobGetResponse, job, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncRainbows) -> None:
        response = await async_client.jobs.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(JobGetResponse, job, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncRainbows) -> None:
        async with async_client.jobs.with_streaming_response.get() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(JobGetResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve_term_based(self, async_client: AsyncRainbows) -> None:
        job = await async_client.jobs.retrieve_term_based(
            query="Find software engineering jobs in the US posted in the last month",
        )
        assert_matches_type(JobRetrieveTermBasedResponse, job, path=["response"])

    @parametrize
    async def test_raw_response_retrieve_term_based(self, async_client: AsyncRainbows) -> None:
        response = await async_client.jobs.with_raw_response.retrieve_term_based(
            query="Find software engineering jobs in the US posted in the last month",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(JobRetrieveTermBasedResponse, job, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve_term_based(self, async_client: AsyncRainbows) -> None:
        async with async_client.jobs.with_streaming_response.retrieve_term_based(
            query="Find software engineering jobs in the US posted in the last month",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(JobRetrieveTermBasedResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_upsert(self, async_client: AsyncRainbows) -> None:
        job = await async_client.jobs.upsert(
            jobs=[{"url": "url"}],
        )
        assert_matches_type(JobUpsertResponse, job, path=["response"])

    @parametrize
    async def test_method_upsert_with_all_params(self, async_client: AsyncRainbows) -> None:
        job = await async_client.jobs.upsert(
            jobs=[
                {
                    "url": "url",
                    "board_url": "board_url",
                    "countries": ["string"],
                    "description": "description",
                    "last_scraped_date": "last_scraped_date",
                    "location": "location",
                    "title": "title",
                }
            ],
            batch_size=0,
        )
        assert_matches_type(JobUpsertResponse, job, path=["response"])

    @parametrize
    async def test_raw_response_upsert(self, async_client: AsyncRainbows) -> None:
        response = await async_client.jobs.with_raw_response.upsert(
            jobs=[{"url": "url"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(JobUpsertResponse, job, path=["response"])

    @parametrize
    async def test_streaming_response_upsert(self, async_client: AsyncRainbows) -> None:
        async with async_client.jobs.with_streaming_response.upsert(
            jobs=[{"url": "url"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(JobUpsertResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True
