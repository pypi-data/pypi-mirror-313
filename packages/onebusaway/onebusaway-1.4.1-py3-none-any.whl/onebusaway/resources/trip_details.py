# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import trip_detail_retrieve_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.trip_detail_retrieve_response import TripDetailRetrieveResponse

__all__ = ["TripDetailsResource", "AsyncTripDetailsResource"]


class TripDetailsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TripDetailsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/OneBusAway/python-sdk#accessing-raw-response-data-eg-headers
        """
        return TripDetailsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TripDetailsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/OneBusAway/python-sdk#with_streaming_response
        """
        return TripDetailsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        trip_id: str,
        *,
        include_schedule: bool | NotGiven = NOT_GIVEN,
        include_status: bool | NotGiven = NOT_GIVEN,
        include_trip: bool | NotGiven = NOT_GIVEN,
        service_date: int | NotGiven = NOT_GIVEN,
        time: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TripDetailRetrieveResponse:
        """
        Retrieve Trip Details

        Args:
          include_schedule: Whether to include the full schedule element in the tripDetails section
              (defaults to true).

          include_status: Whether to include the full status element in the tripDetails section (defaults
              to true).

          include_trip: Whether to include the full trip element in the references section (defaults to
              true).

          service_date: Service date for the trip as Unix time in milliseconds (optional).

          time: Time parameter to query the system at a specific time (optional).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not trip_id:
            raise ValueError(f"Expected a non-empty value for `trip_id` but received {trip_id!r}")
        return self._get(
            f"/api/where/trip-details/{trip_id}.json",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "include_schedule": include_schedule,
                        "include_status": include_status,
                        "include_trip": include_trip,
                        "service_date": service_date,
                        "time": time,
                    },
                    trip_detail_retrieve_params.TripDetailRetrieveParams,
                ),
            ),
            cast_to=TripDetailRetrieveResponse,
        )


class AsyncTripDetailsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTripDetailsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/OneBusAway/python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncTripDetailsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTripDetailsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/OneBusAway/python-sdk#with_streaming_response
        """
        return AsyncTripDetailsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        trip_id: str,
        *,
        include_schedule: bool | NotGiven = NOT_GIVEN,
        include_status: bool | NotGiven = NOT_GIVEN,
        include_trip: bool | NotGiven = NOT_GIVEN,
        service_date: int | NotGiven = NOT_GIVEN,
        time: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TripDetailRetrieveResponse:
        """
        Retrieve Trip Details

        Args:
          include_schedule: Whether to include the full schedule element in the tripDetails section
              (defaults to true).

          include_status: Whether to include the full status element in the tripDetails section (defaults
              to true).

          include_trip: Whether to include the full trip element in the references section (defaults to
              true).

          service_date: Service date for the trip as Unix time in milliseconds (optional).

          time: Time parameter to query the system at a specific time (optional).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not trip_id:
            raise ValueError(f"Expected a non-empty value for `trip_id` but received {trip_id!r}")
        return await self._get(
            f"/api/where/trip-details/{trip_id}.json",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "include_schedule": include_schedule,
                        "include_status": include_status,
                        "include_trip": include_trip,
                        "service_date": service_date,
                        "time": time,
                    },
                    trip_detail_retrieve_params.TripDetailRetrieveParams,
                ),
            ),
            cast_to=TripDetailRetrieveResponse,
        )


class TripDetailsResourceWithRawResponse:
    def __init__(self, trip_details: TripDetailsResource) -> None:
        self._trip_details = trip_details

        self.retrieve = to_raw_response_wrapper(
            trip_details.retrieve,
        )


class AsyncTripDetailsResourceWithRawResponse:
    def __init__(self, trip_details: AsyncTripDetailsResource) -> None:
        self._trip_details = trip_details

        self.retrieve = async_to_raw_response_wrapper(
            trip_details.retrieve,
        )


class TripDetailsResourceWithStreamingResponse:
    def __init__(self, trip_details: TripDetailsResource) -> None:
        self._trip_details = trip_details

        self.retrieve = to_streamed_response_wrapper(
            trip_details.retrieve,
        )


class AsyncTripDetailsResourceWithStreamingResponse:
    def __init__(self, trip_details: AsyncTripDetailsResource) -> None:
        self._trip_details = trip_details

        self.retrieve = async_to_streamed_response_wrapper(
            trip_details.retrieve,
        )
