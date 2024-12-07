# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["DatasetGetViewParams"]


class DatasetGetViewParams(TypedDict, total=False):
    dataset_file_id: Required[Annotated[str, PropertyInfo(alias="datasetFileId")]]
    """
    The ID of the (pinned) dataset file from which to retrieve content. Requests
    iterating over pages of results are recommended to use this pinned identifier
    after the first page in order to prevent any effects from a dataset changing
    between the queries.
    """

    dataset_id: Required[Annotated[str, PropertyInfo(alias="datasetId")]]
    """The ID of the dataset from which to retrieve content.

    When specified, gets data from the current file in the dataset.
    """

    after: int
    """Pagination: The index, by row-order, after which to query results."""

    limit: int
    """Pagination: The maximum number of results to return on this page."""
