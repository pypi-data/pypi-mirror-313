# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["VehiclesForAgencyListParams"]


class VehiclesForAgencyListParams(TypedDict, total=False):
    time: str
    """Specific time for querying the status (timestamp format)"""
