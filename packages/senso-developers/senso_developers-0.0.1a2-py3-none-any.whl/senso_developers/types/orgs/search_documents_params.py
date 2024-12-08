# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SearchDocumentsParams"]


class SearchDocumentsParams(TypedDict, total=False):
    query: Required[str]

    top_k: int
