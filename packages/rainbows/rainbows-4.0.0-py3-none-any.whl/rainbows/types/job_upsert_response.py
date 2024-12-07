# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["JobUpsertResponse"]


class JobUpsertResponse(BaseModel):
    inserted: int
    """Number of jobs inserted"""

    updated: int
    """Number of jobs updated"""
