# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["DatasetListParams", "Filters"]


class DatasetListParams(TypedDict, total=False):
    filters: Filters


class Filters(TypedDict, total=False):
    query: str
    """search query substring match for name and description"""
