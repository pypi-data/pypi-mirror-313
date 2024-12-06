# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.product.checklist_view_response import ChecklistViewResponse

__all__ = ["ChecklistResource", "AsyncChecklistResource"]


class ChecklistResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ChecklistResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return ChecklistResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChecklistResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return ChecklistResourceWithStreamingResponse(self)

    def view(
        self,
        sub_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChecklistViewResponse:
        """
        Get the details and observations of a checklist.

        #### Notes Do NOT use this to download large amounts of data. You will be banned if you do. In the fields for each observation, the following fields are duplicates or obsolete and will be removed at a future date: _howManyAtleast_, _howManyAtmost_, _hideFlags_, _projId_, _subId_, _subnational1Code_ and _present_.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not sub_id:
            raise ValueError(f"Expected a non-empty value for `sub_id` but received {sub_id!r}")
        return self._get(
            f"/product/checklist/view/{sub_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChecklistViewResponse,
        )


class AsyncChecklistResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncChecklistResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return the
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#accessing-raw-response-data-eg-headers
        """
        return AsyncChecklistResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChecklistResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/phoebe-bird/phoebe-python#with_streaming_response
        """
        return AsyncChecklistResourceWithStreamingResponse(self)

    async def view(
        self,
        sub_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChecklistViewResponse:
        """
        Get the details and observations of a checklist.

        #### Notes Do NOT use this to download large amounts of data. You will be banned if you do. In the fields for each observation, the following fields are duplicates or obsolete and will be removed at a future date: _howManyAtleast_, _howManyAtmost_, _hideFlags_, _projId_, _subId_, _subnational1Code_ and _present_.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not sub_id:
            raise ValueError(f"Expected a non-empty value for `sub_id` but received {sub_id!r}")
        return await self._get(
            f"/product/checklist/view/{sub_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChecklistViewResponse,
        )


class ChecklistResourceWithRawResponse:
    def __init__(self, checklist: ChecklistResource) -> None:
        self._checklist = checklist

        self.view = to_raw_response_wrapper(
            checklist.view,
        )


class AsyncChecklistResourceWithRawResponse:
    def __init__(self, checklist: AsyncChecklistResource) -> None:
        self._checklist = checklist

        self.view = async_to_raw_response_wrapper(
            checklist.view,
        )


class ChecklistResourceWithStreamingResponse:
    def __init__(self, checklist: ChecklistResource) -> None:
        self._checklist = checklist

        self.view = to_streamed_response_wrapper(
            checklist.view,
        )


class AsyncChecklistResourceWithStreamingResponse:
    def __init__(self, checklist: AsyncChecklistResource) -> None:
        self._checklist = checklist

        self.view = async_to_streamed_response_wrapper(
            checklist.view,
        )
