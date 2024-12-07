# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from lastmile import Lastmile, AsyncLastmile
from tests.utils import assert_matches_type
from lastmile.types import (
    DatasetGetResponse,
    DatasetListResponse,
    DatasetCreateResponse,
    DatasetGetViewResponse,
    DatasetUploadFileResponse,
    DatasetGetDownloadURLResponse,
    DatasetFinalizeFileUploadResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDatasets:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Lastmile) -> None:
        dataset = client.datasets.create()
        assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Lastmile) -> None:
        dataset = client.datasets.create(
            description="description",
            is_active_labels=True,
            is_few_shot_examples=True,
            name="name",
        )
        assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Lastmile) -> None:
        response = client.datasets.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Lastmile) -> None:
        with client.datasets.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list(self, client: Lastmile) -> None:
        dataset = client.datasets.list()
        assert_matches_type(DatasetListResponse, dataset, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Lastmile) -> None:
        dataset = client.datasets.list(
            filters={"query": "query"},
        )
        assert_matches_type(DatasetListResponse, dataset, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Lastmile) -> None:
        response = client.datasets.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetListResponse, dataset, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Lastmile) -> None:
        with client.datasets.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetListResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_finalize_file_upload(self, client: Lastmile) -> None:
        dataset = client.datasets.finalize_file_upload(
            dataset_id="datasetId",
            s3_presigned_post={
                "fields": {"foo": "string"},
                "url": "url",
            },
        )
        assert_matches_type(DatasetFinalizeFileUploadResponse, dataset, path=["response"])

    @parametrize
    def test_raw_response_finalize_file_upload(self, client: Lastmile) -> None:
        response = client.datasets.with_raw_response.finalize_file_upload(
            dataset_id="datasetId",
            s3_presigned_post={
                "fields": {"foo": "string"},
                "url": "url",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetFinalizeFileUploadResponse, dataset, path=["response"])

    @parametrize
    def test_streaming_response_finalize_file_upload(self, client: Lastmile) -> None:
        with client.datasets.with_streaming_response.finalize_file_upload(
            dataset_id="datasetId",
            s3_presigned_post={
                "fields": {"foo": "string"},
                "url": "url",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetFinalizeFileUploadResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_get(self, client: Lastmile) -> None:
        dataset = client.datasets.get(
            id="id",
        )
        assert_matches_type(DatasetGetResponse, dataset, path=["response"])

    @parametrize
    def test_raw_response_get(self, client: Lastmile) -> None:
        response = client.datasets.with_raw_response.get(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetGetResponse, dataset, path=["response"])

    @parametrize
    def test_streaming_response_get(self, client: Lastmile) -> None:
        with client.datasets.with_streaming_response.get(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetGetResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_get_download_url(self, client: Lastmile) -> None:
        dataset = client.datasets.get_download_url(
            dataset_id="datasetId",
        )
        assert_matches_type(DatasetGetDownloadURLResponse, dataset, path=["response"])

    @parametrize
    def test_raw_response_get_download_url(self, client: Lastmile) -> None:
        response = client.datasets.with_raw_response.get_download_url(
            dataset_id="datasetId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetGetDownloadURLResponse, dataset, path=["response"])

    @parametrize
    def test_streaming_response_get_download_url(self, client: Lastmile) -> None:
        with client.datasets.with_streaming_response.get_download_url(
            dataset_id="datasetId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetGetDownloadURLResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_get_view(self, client: Lastmile) -> None:
        dataset = client.datasets.get_view(
            dataset_file_id="datasetFileId",
            dataset_id="datasetId",
        )
        assert_matches_type(DatasetGetViewResponse, dataset, path=["response"])

    @parametrize
    def test_method_get_view_with_all_params(self, client: Lastmile) -> None:
        dataset = client.datasets.get_view(
            dataset_file_id="datasetFileId",
            dataset_id="datasetId",
            after=0,
            limit=0,
        )
        assert_matches_type(DatasetGetViewResponse, dataset, path=["response"])

    @parametrize
    def test_raw_response_get_view(self, client: Lastmile) -> None:
        response = client.datasets.with_raw_response.get_view(
            dataset_file_id="datasetFileId",
            dataset_id="datasetId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetGetViewResponse, dataset, path=["response"])

    @parametrize
    def test_streaming_response_get_view(self, client: Lastmile) -> None:
        with client.datasets.with_streaming_response.get_view(
            dataset_file_id="datasetFileId",
            dataset_id="datasetId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetGetViewResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_upload_file(self, client: Lastmile) -> None:
        dataset = client.datasets.upload_file(
            dataset_id="datasetId",
        )
        assert_matches_type(DatasetUploadFileResponse, dataset, path=["response"])

    @parametrize
    def test_raw_response_upload_file(self, client: Lastmile) -> None:
        response = client.datasets.with_raw_response.upload_file(
            dataset_id="datasetId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = response.parse()
        assert_matches_type(DatasetUploadFileResponse, dataset, path=["response"])

    @parametrize
    def test_streaming_response_upload_file(self, client: Lastmile) -> None:
        with client.datasets.with_streaming_response.upload_file(
            dataset_id="datasetId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = response.parse()
            assert_matches_type(DatasetUploadFileResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDatasets:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.create()
        assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.create(
            description="description",
            is_active_labels=True,
            is_few_shot_examples=True,
            name="name",
        )
        assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncLastmile) -> None:
        response = await async_client.datasets.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncLastmile) -> None:
        async with async_client.datasets.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetCreateResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.list()
        assert_matches_type(DatasetListResponse, dataset, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.list(
            filters={"query": "query"},
        )
        assert_matches_type(DatasetListResponse, dataset, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncLastmile) -> None:
        response = await async_client.datasets.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetListResponse, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncLastmile) -> None:
        async with async_client.datasets.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetListResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_finalize_file_upload(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.finalize_file_upload(
            dataset_id="datasetId",
            s3_presigned_post={
                "fields": {"foo": "string"},
                "url": "url",
            },
        )
        assert_matches_type(DatasetFinalizeFileUploadResponse, dataset, path=["response"])

    @parametrize
    async def test_raw_response_finalize_file_upload(self, async_client: AsyncLastmile) -> None:
        response = await async_client.datasets.with_raw_response.finalize_file_upload(
            dataset_id="datasetId",
            s3_presigned_post={
                "fields": {"foo": "string"},
                "url": "url",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetFinalizeFileUploadResponse, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_finalize_file_upload(self, async_client: AsyncLastmile) -> None:
        async with async_client.datasets.with_streaming_response.finalize_file_upload(
            dataset_id="datasetId",
            s3_presigned_post={
                "fields": {"foo": "string"},
                "url": "url",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetFinalizeFileUploadResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_get(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.get(
            id="id",
        )
        assert_matches_type(DatasetGetResponse, dataset, path=["response"])

    @parametrize
    async def test_raw_response_get(self, async_client: AsyncLastmile) -> None:
        response = await async_client.datasets.with_raw_response.get(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetGetResponse, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncLastmile) -> None:
        async with async_client.datasets.with_streaming_response.get(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetGetResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_get_download_url(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.get_download_url(
            dataset_id="datasetId",
        )
        assert_matches_type(DatasetGetDownloadURLResponse, dataset, path=["response"])

    @parametrize
    async def test_raw_response_get_download_url(self, async_client: AsyncLastmile) -> None:
        response = await async_client.datasets.with_raw_response.get_download_url(
            dataset_id="datasetId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetGetDownloadURLResponse, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_get_download_url(self, async_client: AsyncLastmile) -> None:
        async with async_client.datasets.with_streaming_response.get_download_url(
            dataset_id="datasetId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetGetDownloadURLResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_get_view(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.get_view(
            dataset_file_id="datasetFileId",
            dataset_id="datasetId",
        )
        assert_matches_type(DatasetGetViewResponse, dataset, path=["response"])

    @parametrize
    async def test_method_get_view_with_all_params(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.get_view(
            dataset_file_id="datasetFileId",
            dataset_id="datasetId",
            after=0,
            limit=0,
        )
        assert_matches_type(DatasetGetViewResponse, dataset, path=["response"])

    @parametrize
    async def test_raw_response_get_view(self, async_client: AsyncLastmile) -> None:
        response = await async_client.datasets.with_raw_response.get_view(
            dataset_file_id="datasetFileId",
            dataset_id="datasetId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetGetViewResponse, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_get_view(self, async_client: AsyncLastmile) -> None:
        async with async_client.datasets.with_streaming_response.get_view(
            dataset_file_id="datasetFileId",
            dataset_id="datasetId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetGetViewResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_upload_file(self, async_client: AsyncLastmile) -> None:
        dataset = await async_client.datasets.upload_file(
            dataset_id="datasetId",
        )
        assert_matches_type(DatasetUploadFileResponse, dataset, path=["response"])

    @parametrize
    async def test_raw_response_upload_file(self, async_client: AsyncLastmile) -> None:
        response = await async_client.datasets.with_raw_response.upload_file(
            dataset_id="datasetId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        dataset = await response.parse()
        assert_matches_type(DatasetUploadFileResponse, dataset, path=["response"])

    @parametrize
    async def test_streaming_response_upload_file(self, async_client: AsyncLastmile) -> None:
        async with async_client.datasets.with_streaming_response.upload_file(
            dataset_id="datasetId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            dataset = await response.parse()
            assert_matches_type(DatasetUploadFileResponse, dataset, path=["response"])

        assert cast(Any, response.is_closed) is True
