# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

import httpx

from ..types import (
    evaluation_evaluate_params,
    evaluation_get_metric_params,
    evaluation_evaluate_dataset_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.evaluation_evaluate_response import EvaluationEvaluateResponse
from ..types.evaluation_get_metric_response import EvaluationGetMetricResponse
from ..types.evaluation_list_metrics_response import EvaluationListMetricsResponse
from ..types.evaluation_evaluate_dataset_response import EvaluationEvaluateDatasetResponse

__all__ = ["EvaluationResource", "AsyncEvaluationResource"]


class EvaluationResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EvaluationResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/lastmile-ai/lastmile-python#accessing-raw-response-data-eg-headers
        """
        return EvaluationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EvaluationResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/lastmile-ai/lastmile-python#with_streaming_response
        """
        return EvaluationResourceWithStreamingResponse(self)

    def evaluate(
        self,
        *,
        ground_truth: List[str],
        input: List[str],
        metric: evaluation_evaluate_params.Metric,
        output: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationEvaluateResponse:
        """Evaluate a metric on rows of data, returning scores for each row.

        Specify
        metric.id or metric.name to identify the metric.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/2/auto_eval/evaluation/evaluate",
            body=maybe_transform(
                {
                    "ground_truth": ground_truth,
                    "input": input,
                    "metric": metric,
                    "output": output,
                },
                evaluation_evaluate_params.EvaluationEvaluateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationEvaluateResponse,
        )

    def evaluate_dataset(
        self,
        *,
        dataset_id: str,
        metric: evaluation_evaluate_dataset_params.Metric,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationEvaluateDatasetResponse:
        """Evaluate a metric on a dataset, returning scores for each example.

        Specify
        metric.id or metric.name to identify the metric.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/2/auto_eval/evaluation/evaluate_dataset",
            body=maybe_transform(
                {
                    "dataset_id": dataset_id,
                    "metric": metric,
                },
                evaluation_evaluate_dataset_params.EvaluationEvaluateDatasetParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationEvaluateDatasetResponse,
        )

    def get_metric(
        self,
        *,
        metric: evaluation_get_metric_params.Metric,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationGetMetricResponse:
        """
        Get a specific evaluation metric by id or name.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/2/auto_eval/evaluation/get_metric",
            body=maybe_transform({"metric": metric}, evaluation_get_metric_params.EvaluationGetMetricParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationGetMetricResponse,
        )

    def list_metrics(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationListMetricsResponse:
        """List all available evaluation metrics."""
        return self._post(
            "/api/2/auto_eval/evaluation/list_metrics",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationListMetricsResponse,
        )


class AsyncEvaluationResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEvaluationResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/lastmile-ai/lastmile-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEvaluationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEvaluationResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/lastmile-ai/lastmile-python#with_streaming_response
        """
        return AsyncEvaluationResourceWithStreamingResponse(self)

    async def evaluate(
        self,
        *,
        ground_truth: List[str],
        input: List[str],
        metric: evaluation_evaluate_params.Metric,
        output: List[str],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationEvaluateResponse:
        """Evaluate a metric on rows of data, returning scores for each row.

        Specify
        metric.id or metric.name to identify the metric.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/2/auto_eval/evaluation/evaluate",
            body=await async_maybe_transform(
                {
                    "ground_truth": ground_truth,
                    "input": input,
                    "metric": metric,
                    "output": output,
                },
                evaluation_evaluate_params.EvaluationEvaluateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationEvaluateResponse,
        )

    async def evaluate_dataset(
        self,
        *,
        dataset_id: str,
        metric: evaluation_evaluate_dataset_params.Metric,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationEvaluateDatasetResponse:
        """Evaluate a metric on a dataset, returning scores for each example.

        Specify
        metric.id or metric.name to identify the metric.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/2/auto_eval/evaluation/evaluate_dataset",
            body=await async_maybe_transform(
                {
                    "dataset_id": dataset_id,
                    "metric": metric,
                },
                evaluation_evaluate_dataset_params.EvaluationEvaluateDatasetParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationEvaluateDatasetResponse,
        )

    async def get_metric(
        self,
        *,
        metric: evaluation_get_metric_params.Metric,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationGetMetricResponse:
        """
        Get a specific evaluation metric by id or name.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/2/auto_eval/evaluation/get_metric",
            body=await async_maybe_transform(
                {"metric": metric}, evaluation_get_metric_params.EvaluationGetMetricParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationGetMetricResponse,
        )

    async def list_metrics(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationListMetricsResponse:
        """List all available evaluation metrics."""
        return await self._post(
            "/api/2/auto_eval/evaluation/list_metrics",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationListMetricsResponse,
        )


class EvaluationResourceWithRawResponse:
    def __init__(self, evaluation: EvaluationResource) -> None:
        self._evaluation = evaluation

        self.evaluate = to_raw_response_wrapper(
            evaluation.evaluate,
        )
        self.evaluate_dataset = to_raw_response_wrapper(
            evaluation.evaluate_dataset,
        )
        self.get_metric = to_raw_response_wrapper(
            evaluation.get_metric,
        )
        self.list_metrics = to_raw_response_wrapper(
            evaluation.list_metrics,
        )


class AsyncEvaluationResourceWithRawResponse:
    def __init__(self, evaluation: AsyncEvaluationResource) -> None:
        self._evaluation = evaluation

        self.evaluate = async_to_raw_response_wrapper(
            evaluation.evaluate,
        )
        self.evaluate_dataset = async_to_raw_response_wrapper(
            evaluation.evaluate_dataset,
        )
        self.get_metric = async_to_raw_response_wrapper(
            evaluation.get_metric,
        )
        self.list_metrics = async_to_raw_response_wrapper(
            evaluation.list_metrics,
        )


class EvaluationResourceWithStreamingResponse:
    def __init__(self, evaluation: EvaluationResource) -> None:
        self._evaluation = evaluation

        self.evaluate = to_streamed_response_wrapper(
            evaluation.evaluate,
        )
        self.evaluate_dataset = to_streamed_response_wrapper(
            evaluation.evaluate_dataset,
        )
        self.get_metric = to_streamed_response_wrapper(
            evaluation.get_metric,
        )
        self.list_metrics = to_streamed_response_wrapper(
            evaluation.list_metrics,
        )


class AsyncEvaluationResourceWithStreamingResponse:
    def __init__(self, evaluation: AsyncEvaluationResource) -> None:
        self._evaluation = evaluation

        self.evaluate = async_to_streamed_response_wrapper(
            evaluation.evaluate,
        )
        self.evaluate_dataset = async_to_streamed_response_wrapper(
            evaluation.evaluate_dataset,
        )
        self.get_metric = async_to_streamed_response_wrapper(
            evaluation.get_metric,
        )
        self.list_metrics = async_to_streamed_response_wrapper(
            evaluation.list_metrics,
        )
