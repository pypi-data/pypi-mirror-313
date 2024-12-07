# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["JobRetrieveTermBasedParams"]


class JobRetrieveTermBasedParams(TypedDict, total=False):
    query: Required[str]
    """Natural language query to search for jobs"""
