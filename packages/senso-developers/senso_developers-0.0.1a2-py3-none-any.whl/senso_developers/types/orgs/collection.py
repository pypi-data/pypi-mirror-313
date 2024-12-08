# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["Collection"]


class Collection(BaseModel):
    collection_id: Optional[str] = None

    created_at: Optional[datetime] = None

    name: Optional[str] = None

    org_id: Optional[str] = None

    updated_at: Optional[datetime] = None

    visibility: Optional[int] = None
