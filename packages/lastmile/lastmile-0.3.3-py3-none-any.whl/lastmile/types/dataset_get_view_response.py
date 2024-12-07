# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["DatasetGetViewResponse", "DatasetView", "DatasetViewColumn", "DatasetViewData"]


class DatasetViewColumn(BaseModel):
    id: str
    """The ID of the dataset file."""

    created_at: datetime = FieldInfo(alias="createdAt")

    index: int
    """Index of the column within the dataset file."""

    literal_name: str = FieldInfo(alias="literalName")
    """The literal name for the column."""

    updated_at: datetime = FieldInfo(alias="updatedAt")

    dtype: Optional[str] = None


class DatasetViewData(BaseModel):
    id: str

    row_values: List[Dict[str, object]] = FieldInfo(alias="rowValues")


class DatasetView(BaseModel):
    columns: List[DatasetViewColumn]

    data: List[DatasetViewData]

    num_cols: int = FieldInfo(alias="numCols")

    num_rows: int = FieldInfo(alias="numRows")


class DatasetGetViewResponse(BaseModel):
    dataset_file_id: str = FieldInfo(alias="datasetFileId")

    dataset_id: str = FieldInfo(alias="datasetId")

    dataset_view: DatasetView = FieldInfo(alias="datasetView")
