# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["ResourceCreated"]


class ResourceCreated(BaseModel):
    id: str

    created_at: datetime

    jobs: Optional[List[str]] = None
