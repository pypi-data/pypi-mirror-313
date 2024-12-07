# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "LabelDatasetJobCreateParams",
    "PseudoLabelJobConfig",
    "PseudoLabelJobConfigChatCompletionConfig",
    "PseudoLabelJobConfigChatCompletionConfigMessage",
    "PseudoLabelJobConfigPromptTemplate",
]


class LabelDatasetJobCreateParams(TypedDict, total=False):
    pseudo_label_job_config: Required[Annotated[PseudoLabelJobConfig, PropertyInfo(alias="pseudoLabelJobConfig")]]
    """Partial configuration containing updates via its non-null fields."""


class PseudoLabelJobConfigChatCompletionConfigMessage(TypedDict, total=False):
    content: Required[str]
    """The content of the message."""

    role: Required[str]
    """Role can be 'system', 'user', or 'assistant'."""


class PseudoLabelJobConfigChatCompletionConfig(TypedDict, total=False):
    max_tokens: Required[Annotated[int, PropertyInfo(alias="maxTokens")]]
    """The maximum number of tokens to generate."""

    messages: Required[Iterable[PseudoLabelJobConfigChatCompletionConfigMessage]]

    model: Required[str]
    """The ID of the model to use for the completion."""

    temperature: Required[float]
    """The temperature to use for the completion."""

    top_p: Required[Annotated[float, PropertyInfo(alias="topP")]]
    """The top_p value to use for the completion."""

    vendor: Required[str]


class PseudoLabelJobConfigPromptTemplate(TypedDict, total=False):
    id: Required[str]

    template: Required[str]
    """The template string that defines the prompt"""


class PseudoLabelJobConfig(TypedDict, total=False):
    base_evaluation_metric: Required[Annotated[str, PropertyInfo(alias="baseEvaluationMetric")]]
    """Reserved field. Do not use at the moment."""

    chat_completion_config: Required[
        Annotated[PseudoLabelJobConfigChatCompletionConfig, PropertyInfo(alias="chatCompletionConfig")]
    ]
    """
    For Chat LLM based labeling, the configuration to use with the requests
    (messages omitted)
    """

    dataset_id: Required[Annotated[str, PropertyInfo(alias="datasetId")]]
    """ID of the main dataset to be pseudo-labeled"""

    prompt_template: Required[Annotated[PseudoLabelJobConfigPromptTemplate, PropertyInfo(alias="promptTemplate")]]

    selected_columns: Required[Annotated[List[str], PropertyInfo(alias="selectedColumns")]]

    skip_active_labeling: Required[Annotated[bool, PropertyInfo(alias="skipActiveLabeling")]]
    """
    If true, skip active labeling, which involves an intermediate Dataset created
    for human labeling.
    """

    active_labeled_dataset_id: Annotated[str, PropertyInfo(alias="activeLabeledDatasetId")]
    """ID of the actively labeled dataset.

    Optional. If null, this job is for active learning.
    """

    description: str
    """Optional description for the job."""

    few_shot_dataset_id: Annotated[str, PropertyInfo(alias="fewShotDatasetId")]
    """ID of the dataset containing few-shot examples. Optional."""

    name: str
    """Optional name for the job."""
