# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .shared.references import References
from .shared.response_wrapper import ResponseWrapper

__all__ = ["StopIDsForAgencyListResponse", "StopIDsForAgencyListResponseData"]


class StopIDsForAgencyListResponseData(BaseModel):
    limit_exceeded: bool = FieldInfo(alias="limitExceeded")

    list: List[str]

    references: References


class StopIDsForAgencyListResponse(ResponseWrapper):
    data: StopIDsForAgencyListResponseData
