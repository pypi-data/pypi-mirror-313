# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .chunk_pages import ChunkPages

__all__ = ["SearchChunksResponse"]

SearchChunksResponse: TypeAlias = List[ChunkPages]
