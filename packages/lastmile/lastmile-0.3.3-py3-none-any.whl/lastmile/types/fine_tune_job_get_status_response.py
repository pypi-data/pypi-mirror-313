# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "FineTuneJobGetStatusResponse",
    "FineTuneJobResult",
    "FineTuneJobResultProgress",
    "FineTuneJobResultTrainedModelFile",
]


class FineTuneJobResultProgress(BaseModel):
    accuracy: float

    epoch: int

    job_id: str = FieldInfo(alias="jobId")

    loss: float

    progress: float

    timestamp: datetime


class FineTuneJobResultTrainedModelFile(BaseModel):
    id: str

    content_md5_hash: str = FieldInfo(alias="contentMd5Hash")

    created_at: datetime = FieldInfo(alias="createdAt")

    file_size_bytes: int = FieldInfo(alias="fileSizeBytes")

    model_id: str = FieldInfo(alias="modelId")

    updated_at: datetime = FieldInfo(alias="updatedAt")


class FineTuneJobResult(BaseModel):
    progress: List[FineTuneJobResultProgress]

    result_url: Optional[str] = FieldInfo(alias="resultUrl", default=None)
    """Url to view the full results and progress (e.g. external W&B url)"""

    trained_model_file: Optional[FineTuneJobResultTrainedModelFile] = FieldInfo(alias="trainedModelFile", default=None)
    """The trained model, if it was created successfully."""


class FineTuneJobGetStatusResponse(BaseModel):
    fine_tune_job_result: FineTuneJobResult = FieldInfo(alias="fineTuneJobResult")
    """Result of a Fine-Tuning Job."""

    status: str
