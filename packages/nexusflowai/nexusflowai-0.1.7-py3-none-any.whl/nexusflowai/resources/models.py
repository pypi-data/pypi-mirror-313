from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from openai.types import Model, ModelDeleted
from openai._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from openai._resource import SyncAPIResource, AsyncAPIResource
from openai._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from openai.pagination import SyncPage, AsyncPage
from openai._base_client import AsyncPaginator, make_request_options

from nexusflowai.utils import transform_client_header

if TYPE_CHECKING:
    from nexusflowai import NexusflowAI, AsyncNexusflowAI


__all__ = ["Models", "AsyncModels"]


class Models(SyncAPIResource):
    with_raw_response: ModelsWithRawResponse

    def __init__(self, client: NexusflowAI) -> None:
        super().__init__(client)
        self.with_raw_response = ModelsWithRawResponse(self)

    def retrieve(
        self,
        model: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Model:
        """
        Retrieves a model instance, providing basic information about the model such as
        the owner and permissioning.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """

        extra_headers = transform_client_header(extra_headers=extra_headers)

        return self._get(
            f"/models/{model}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=Model,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncPage[Model]:
        """
        Lists the currently available models, and provides basic information about each
        one such as the owner and availability.
        """

        extra_headers = transform_client_header(extra_headers=extra_headers)

        return self._get_api_list(
            "/models",
            page=SyncPage[Model],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            model=Model,
        )

    def delete(
        self,
        model: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModelDeleted:
        """Delete a fine-tuned model.

        You must have the Owner role in your organization to
        delete a model.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """

        extra_headers = transform_client_header(extra_headers=extra_headers)

        return self._delete(
            f"/models/{model}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=ModelDeleted,
        )


class AsyncModels(AsyncAPIResource):
    with_raw_response: AsyncModelsWithRawResponse

    def __init__(self, client: AsyncNexusflowAI) -> None:
        super().__init__(client)
        self.with_raw_response = AsyncModelsWithRawResponse(self)

    async def retrieve(
        self,
        model: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> Model:
        """
        Retrieves a model instance, providing basic information about the model such as
        the owner and permissioning.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """

        extra_headers = transform_client_header(extra_headers=extra_headers)

        return await self._get(
            f"/models/{model}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=Model,
        )

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[Model, AsyncPage[Model]]:
        """
        Lists the currently available models, and provides basic information about each
        one such as the owner and availability.
        """

        extra_headers = transform_client_header(extra_headers=extra_headers)

        return self._get_api_list(
            "/models",
            page=AsyncPage[Model],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            model=Model,
        )

    async def delete(
        self,
        model: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModelDeleted:
        """Delete a fine-tuned model.

        You must have the Owner role in your organization to
        delete a model.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """

        extra_headers = transform_client_header(extra_headers=extra_headers)

        return await self._delete(
            f"/models/{model}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=ModelDeleted,
        )


class ModelsWithRawResponse:
    def __init__(self, models: Models) -> None:
        self.retrieve = to_raw_response_wrapper(
            models.retrieve,
        )
        self.list = to_raw_response_wrapper(
            models.list,
        )
        self.delete = to_raw_response_wrapper(
            models.delete,
        )


class AsyncModelsWithRawResponse:
    def __init__(self, models: AsyncModels) -> None:
        self.retrieve = async_to_raw_response_wrapper(
            models.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            models.list,
        )
        self.delete = async_to_raw_response_wrapper(
            models.delete,
        )
