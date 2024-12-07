# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable, Optional
from typing_extensions import Required, TypedDict

__all__ = ["JobUpsertParams", "Job"]


class JobUpsertParams(TypedDict, total=False):
    jobs: Required[Iterable[Job]]
    """List of jobs to upsert"""

    batch_size: Optional[int]
    """Optional batch size for processing"""


class Job(TypedDict, total=False):
    url: Required[str]

    board_url: Optional[str]

    countries: Optional[List[str]]

    description: Optional[str]

    last_scraped_date: Optional[str]

    location: Optional[str]

    title: Optional[str]
