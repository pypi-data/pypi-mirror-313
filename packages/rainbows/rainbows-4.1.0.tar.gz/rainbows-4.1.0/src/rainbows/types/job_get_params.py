# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from datetime import date
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["JobGetParams", "Country", "DescriptionTerms", "LastScrapedDateRange", "TitleTerms"]


class JobGetParams(TypedDict, total=False):
    board_url_contains: Optional[str]
    """Selects for all board urls which contain it"""

    board_urls: Optional[List[str]]
    """Board urls to search"""

    countries: Optional[Iterable[Country]]
    """List of countries to filter jobs"""

    description_terms: Optional[DescriptionTerms]
    """Filter configuration for term-based searches"""

    last_scraped_date_range: Optional[LastScrapedDateRange]
    """Represents a period of time between two dates"""

    null_columns: Optional[List[str]]
    """List of columns that should be null"""

    page_number: int
    """Page number for pagination"""

    page_size: int
    """Number of results per page"""

    title_terms: Optional[TitleTerms]
    """Filter configuration for term-based searches"""

    urls: Optional[List[str]]
    """Specific job urls to fetch. If not None, all other parameters are ignored."""


class Country(TypedDict, total=False):
    code: Required[str]
    """Two-letter country code (e.g., 'US', 'FR', 'CA') or special region code"""


class DescriptionTerms(TypedDict, total=False):
    all_of: Optional[List[str]]
    """Match only if all these words appear"""

    any_of: Optional[List[str]]
    """Match if any of these words appear"""

    none_of: Optional[List[str]]
    """Match only if none of these words appear"""


class LastScrapedDateRange(TypedDict, total=False):
    end: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """End date in ISO format (YYYY-MM-DD)"""

    start: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]
    """Start date in ISO format (YYYY-MM-DD)"""


class TitleTerms(TypedDict, total=False):
    all_of: Optional[List[str]]
    """Match only if all these words appear"""

    any_of: Optional[List[str]]
    """Match if any of these words appear"""

    none_of: Optional[List[str]]
    """Match only if none of these words appear"""
