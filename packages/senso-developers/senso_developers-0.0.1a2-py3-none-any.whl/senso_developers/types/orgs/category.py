# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["Category"]


class Category(BaseModel):
    category_id: Optional[str] = None

    created_at: Optional[datetime] = None

    description: Optional[str] = None

    name: Optional[str] = None

    org_id: Optional[str] = None

    updated_at: Optional[datetime] = None
