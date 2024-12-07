# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["EvaluationEvaluateDatasetResponse", "Metric"]


class Metric(BaseModel):
    id: Optional[str] = None

    deployment_status: Optional[str] = FieldInfo(alias="deploymentStatus", default=None)

    description: Optional[str] = None

    name: Optional[str] = None


class EvaluationEvaluateDatasetResponse(BaseModel):
    metric: Metric

    scores: List[float]
