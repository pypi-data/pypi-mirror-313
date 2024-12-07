# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["JobGetResponse"]


class JobGetResponse(BaseModel):
    data: List[object]
    """List of jobs matching the search criteria"""

    pagination: object
    """Pagination information"""

    error: Optional[str] = None
    """Error message if any"""
