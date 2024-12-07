# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["JobRetrieveTermBasedResponse"]


class JobRetrieveTermBasedResponse(BaseModel):
    llm_responses: List[object]
    """llm outputs used in creating the query"""

    nl_query: str
    """Original natural language query"""

    result: object
    """query result"""

    error: Optional[str] = None
    """Error message if any"""
