# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "FineTuneJobListBaseModelsResponse",
    "Model",
    "ModelMetricBaseModel",
    "ModelModelCard",
    "ModelModelCardTrainingProgress",
]


class ModelMetricBaseModel(BaseModel):
    id: str

    base_model_architecture: str = FieldInfo(alias="baseModelArchitecture")

    model_id: str = FieldInfo(alias="modelId")

    base_evaluation_metric: Optional[str] = FieldInfo(alias="baseEvaluationMetric", default=None)


class ModelModelCardTrainingProgress(BaseModel):
    accuracy: float

    epoch: int

    job_id: str = FieldInfo(alias="jobId")

    loss: float

    progress: float

    timestamp: datetime


class ModelModelCard(BaseModel):
    base_model_architecture: str = FieldInfo(alias="baseModelArchitecture")

    columns: List[str]

    created_at: datetime = FieldInfo(alias="createdAt")

    deployment_status: str = FieldInfo(alias="deploymentStatus")

    description: str

    model_id: str = FieldInfo(alias="modelId")

    model_size: int = FieldInfo(alias="modelSize")

    name: str

    purpose: str

    tags: List[str]

    training_progress: ModelModelCardTrainingProgress = FieldInfo(alias="trainingProgress")
    """Progress metrics from model training."""

    updated_at: datetime = FieldInfo(alias="updatedAt")

    values: Dict[str, str]

    base_evaluation_metric: Optional[str] = FieldInfo(alias="baseEvaluationMetric", default=None)


class Model(BaseModel):
    id: str

    created_at: datetime = FieldInfo(alias="createdAt")

    metric_base_model: ModelMetricBaseModel = FieldInfo(alias="metricBaseModel")
    """Information about a base model corresponding to a metric"""

    updated_at: datetime = FieldInfo(alias="updatedAt")

    deleted_at: Optional[datetime] = FieldInfo(alias="deletedAt", default=None)

    model_card: Optional[ModelModelCard] = FieldInfo(alias="modelCard", default=None)

    user_id: Optional[str] = FieldInfo(alias="userId", default=None)


class FineTuneJobListBaseModelsResponse(BaseModel):
    models: List[Model]
