# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from .._models import BaseModel

__all__ = ["Org"]


class Org(BaseModel):
    created_at: datetime

    name: str

    org_id: str

    updated_at: datetime
