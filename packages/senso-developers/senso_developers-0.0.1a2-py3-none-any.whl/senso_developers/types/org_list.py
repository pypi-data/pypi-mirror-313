# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from datetime import datetime
from typing_extensions import TypeAlias

from .._models import BaseModel

__all__ = ["OrgList", "OrgListItem"]


class OrgListItem(BaseModel):
    created_at: datetime

    name: str

    org_id: str

    updated_at: datetime


OrgList: TypeAlias = List[OrgListItem]
