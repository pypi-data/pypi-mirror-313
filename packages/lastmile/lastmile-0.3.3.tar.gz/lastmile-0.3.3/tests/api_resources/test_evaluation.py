# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from lastmile import Lastmile, AsyncLastmile
from tests.utils import assert_matches_type
from lastmile.types import (
    EvaluationEvaluateResponse,
    EvaluationGetMetricResponse,
    EvaluationListMetricsResponse,
    EvaluationEvaluateDatasetResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvaluation:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_evaluate(self, client: Lastmile) -> None:
        evaluation = client.evaluation.evaluate(
            ground_truth=["string"],
            input=["string"],
            metric={},
            output=["string"],
        )
        assert_matches_type(EvaluationEvaluateResponse, evaluation, path=["response"])

    @parametrize
    def test_method_evaluate_with_all_params(self, client: Lastmile) -> None:
        evaluation = client.evaluation.evaluate(
            ground_truth=["string"],
            input=["string"],
            metric={
                "id": "id",
                "deployment_status": "deploymentStatus",
                "description": "description",
                "name": "name",
            },
            output=["string"],
        )
        assert_matches_type(EvaluationEvaluateResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_evaluate(self, client: Lastmile) -> None:
        response = client.evaluation.with_raw_response.evaluate(
            ground_truth=["string"],
            input=["string"],
            metric={},
            output=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationEvaluateResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_evaluate(self, client: Lastmile) -> None:
        with client.evaluation.with_streaming_response.evaluate(
            ground_truth=["string"],
            input=["string"],
            metric={},
            output=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationEvaluateResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_evaluate_dataset(self, client: Lastmile) -> None:
        evaluation = client.evaluation.evaluate_dataset(
            dataset_id="datasetId",
            metric={},
        )
        assert_matches_type(EvaluationEvaluateDatasetResponse, evaluation, path=["response"])

    @parametrize
    def test_method_evaluate_dataset_with_all_params(self, client: Lastmile) -> None:
        evaluation = client.evaluation.evaluate_dataset(
            dataset_id="datasetId",
            metric={
                "id": "id",
                "deployment_status": "deploymentStatus",
                "description": "description",
                "name": "name",
            },
        )
        assert_matches_type(EvaluationEvaluateDatasetResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_evaluate_dataset(self, client: Lastmile) -> None:
        response = client.evaluation.with_raw_response.evaluate_dataset(
            dataset_id="datasetId",
            metric={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationEvaluateDatasetResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_evaluate_dataset(self, client: Lastmile) -> None:
        with client.evaluation.with_streaming_response.evaluate_dataset(
            dataset_id="datasetId",
            metric={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationEvaluateDatasetResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_get_metric(self, client: Lastmile) -> None:
        evaluation = client.evaluation.get_metric(
            metric={},
        )
        assert_matches_type(EvaluationGetMetricResponse, evaluation, path=["response"])

    @parametrize
    def test_method_get_metric_with_all_params(self, client: Lastmile) -> None:
        evaluation = client.evaluation.get_metric(
            metric={
                "id": "id",
                "deployment_status": "deploymentStatus",
                "description": "description",
                "name": "name",
            },
        )
        assert_matches_type(EvaluationGetMetricResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_get_metric(self, client: Lastmile) -> None:
        response = client.evaluation.with_raw_response.get_metric(
            metric={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationGetMetricResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_get_metric(self, client: Lastmile) -> None:
        with client.evaluation.with_streaming_response.get_metric(
            metric={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationGetMetricResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_list_metrics(self, client: Lastmile) -> None:
        evaluation = client.evaluation.list_metrics()
        assert_matches_type(EvaluationListMetricsResponse, evaluation, path=["response"])

    @parametrize
    def test_raw_response_list_metrics(self, client: Lastmile) -> None:
        response = client.evaluation.with_raw_response.list_metrics()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = response.parse()
        assert_matches_type(EvaluationListMetricsResponse, evaluation, path=["response"])

    @parametrize
    def test_streaming_response_list_metrics(self, client: Lastmile) -> None:
        with client.evaluation.with_streaming_response.list_metrics() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = response.parse()
            assert_matches_type(EvaluationListMetricsResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncEvaluation:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_evaluate(self, async_client: AsyncLastmile) -> None:
        evaluation = await async_client.evaluation.evaluate(
            ground_truth=["string"],
            input=["string"],
            metric={},
            output=["string"],
        )
        assert_matches_type(EvaluationEvaluateResponse, evaluation, path=["response"])

    @parametrize
    async def test_method_evaluate_with_all_params(self, async_client: AsyncLastmile) -> None:
        evaluation = await async_client.evaluation.evaluate(
            ground_truth=["string"],
            input=["string"],
            metric={
                "id": "id",
                "deployment_status": "deploymentStatus",
                "description": "description",
                "name": "name",
            },
            output=["string"],
        )
        assert_matches_type(EvaluationEvaluateResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_evaluate(self, async_client: AsyncLastmile) -> None:
        response = await async_client.evaluation.with_raw_response.evaluate(
            ground_truth=["string"],
            input=["string"],
            metric={},
            output=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationEvaluateResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_evaluate(self, async_client: AsyncLastmile) -> None:
        async with async_client.evaluation.with_streaming_response.evaluate(
            ground_truth=["string"],
            input=["string"],
            metric={},
            output=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationEvaluateResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_evaluate_dataset(self, async_client: AsyncLastmile) -> None:
        evaluation = await async_client.evaluation.evaluate_dataset(
            dataset_id="datasetId",
            metric={},
        )
        assert_matches_type(EvaluationEvaluateDatasetResponse, evaluation, path=["response"])

    @parametrize
    async def test_method_evaluate_dataset_with_all_params(self, async_client: AsyncLastmile) -> None:
        evaluation = await async_client.evaluation.evaluate_dataset(
            dataset_id="datasetId",
            metric={
                "id": "id",
                "deployment_status": "deploymentStatus",
                "description": "description",
                "name": "name",
            },
        )
        assert_matches_type(EvaluationEvaluateDatasetResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_evaluate_dataset(self, async_client: AsyncLastmile) -> None:
        response = await async_client.evaluation.with_raw_response.evaluate_dataset(
            dataset_id="datasetId",
            metric={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationEvaluateDatasetResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_evaluate_dataset(self, async_client: AsyncLastmile) -> None:
        async with async_client.evaluation.with_streaming_response.evaluate_dataset(
            dataset_id="datasetId",
            metric={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationEvaluateDatasetResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_get_metric(self, async_client: AsyncLastmile) -> None:
        evaluation = await async_client.evaluation.get_metric(
            metric={},
        )
        assert_matches_type(EvaluationGetMetricResponse, evaluation, path=["response"])

    @parametrize
    async def test_method_get_metric_with_all_params(self, async_client: AsyncLastmile) -> None:
        evaluation = await async_client.evaluation.get_metric(
            metric={
                "id": "id",
                "deployment_status": "deploymentStatus",
                "description": "description",
                "name": "name",
            },
        )
        assert_matches_type(EvaluationGetMetricResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_get_metric(self, async_client: AsyncLastmile) -> None:
        response = await async_client.evaluation.with_raw_response.get_metric(
            metric={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationGetMetricResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_get_metric(self, async_client: AsyncLastmile) -> None:
        async with async_client.evaluation.with_streaming_response.get_metric(
            metric={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationGetMetricResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_list_metrics(self, async_client: AsyncLastmile) -> None:
        evaluation = await async_client.evaluation.list_metrics()
        assert_matches_type(EvaluationListMetricsResponse, evaluation, path=["response"])

    @parametrize
    async def test_raw_response_list_metrics(self, async_client: AsyncLastmile) -> None:
        response = await async_client.evaluation.with_raw_response.list_metrics()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        evaluation = await response.parse()
        assert_matches_type(EvaluationListMetricsResponse, evaluation, path=["response"])

    @parametrize
    async def test_streaming_response_list_metrics(self, async_client: AsyncLastmile) -> None:
        async with async_client.evaluation.with_streaming_response.list_metrics() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            evaluation = await response.parse()
            assert_matches_type(EvaluationListMetricsResponse, evaluation, path=["response"])

        assert cast(Any, response.is_closed) is True
