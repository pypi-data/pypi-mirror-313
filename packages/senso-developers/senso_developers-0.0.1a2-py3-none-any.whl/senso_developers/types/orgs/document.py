# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["Document"]


class Document(BaseModel):
    content: Optional[str] = None

    created_at: Optional[datetime] = None

    created_by: Optional[str] = None

    document_id: Optional[str] = None

    org_id: Optional[str] = None

    title: Optional[str] = None

    updated_at: Optional[datetime] = None

    updated_by: Optional[str] = None
