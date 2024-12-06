from __future__ import annotations

import os
import asyncio
from typing import Union, Mapping
from typing_extensions import override

import httpx
from openai import resources, _exceptions
from openai._qs import Querystring
from openai._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from openai._utils import is_given, is_mapping
from openai._version import __version__
from openai._streaming import Stream
from openai._streaming import AsyncStream
from openai._exceptions import APIStatusError
from openai._base_client import DEFAULT_MAX_RETRIES, SyncAPIClient, AsyncAPIClient

from nexusflowai.resources import (
    Completions,
    AsyncCompletions,
    CompletionsWithRawResponse,
    AsyncCompletionsWithRawResponse,
    Chat,
    AsyncChat,
    ChatWithRawResponse,
    AsyncChatWithRawResponse,
    Models,
    AsyncModels,
    ModelsWithRawResponse,
    AsyncModelsWithRawResponse,
)

from nexusflowai._exceptions import NexusflowAIError


__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "resources",
    "NexusflowAI",
    "AsyncNexusflowAI",
    "Client",
    "AsyncClient",
]


class NexusflowAI(SyncAPIClient):
    completions: Completions
    chat: Chat
    models: Models
    with_raw_response: NexusflowAIWithRawResponse

    # client options
    api_key: str
    organization: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        organization: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client. See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous openai client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `NEXUSFLOWAI_API_KEY`
        - `organization` from `NEXUSFLOWAI_ORG_ID` - Defaults to `None`
        """
        if api_key is None:
            api_key = os.environ.get("NEXUSFLOWAI_API_KEY")
        if api_key is None:
            raise NexusflowAIError(
                "The api_key client option must be set either by passing api_key to the client or by setting the NEXUSFLOWAI_API_KEY environment variable"
            )
        self.api_key = api_key

        if organization is None:
            organization = os.environ.get("NEXUSFLOWAI_ORG_ID")
        self.organization = organization

        if base_url is None:
            base_url = os.environ.get("NEXUSFLOWAI_BASE_URL")
        if base_url is None:
            base_url = "https://api.nexusflow.ai/v1"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self._default_stream_cls = Stream

        self.completions = Completions(self)
        self.chat = Chat(self)
        self.models = Models(self)
        self.with_raw_response = NexusflowAIWithRawResponse(self)

    @property
    @override
    def qs(self) -> Querystring:  # pragma: no cover
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:  # pragma: no cover
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:  # pragma: no cover
        return {
            **super().default_headers,
            "NexusflowAI-Organization": (
                self.organization if self.organization is not None else Omit()
            ),
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        organization: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
    ) -> NexusflowAI:  # pragma: no cover
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.

        It should be noted that this does not share the underlying httpx client class which may lead
        to performance issues.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError(
                "The `default_headers` and `set_default_headers` arguments are mutually exclusive"
            )

        if default_query is not None and set_default_query is not None:
            raise ValueError(
                "The `default_query` and `set_default_query` arguments are mutually exclusive"
            )

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            organization=organization or self.organization,
            base_url=base_url or str(self.base_url),
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    def __del__(self) -> None:  # pragma: no cover
        if not hasattr(self, "_has_custom_http_client") or not hasattr(self, "close"):
            # this can happen if the '__init__' method raised an error
            return

        if self._has_custom_http_client:
            return

        self.close()

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:  # pragma: no cover
        data = body.get("error", body) if is_mapping(body) else body
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=data)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(
                err_msg, response=response, body=data
            )

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(
                err_msg, response=response, body=data
            )

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=data)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=data)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(
                err_msg, response=response, body=data
            )

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=data)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(
                err_msg, response=response, body=data
            )
        return APIStatusError(err_msg, response=response, body=data)


class AsyncNexusflowAI(AsyncAPIClient):
    completions: AsyncCompletions
    chat: AsyncChat
    models: AsyncModels
    with_raw_response: AsyncNexusflowAIWithRawResponse
    # client options
    api_key: str
    organization: str | None

    def __init__(
        self,
        *,
        api_key: str | None = None,
        organization: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client. See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async openai client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `NEXUSFLOWAI_API_KEY`
        - `organization` from `NEXUSFLOWAI_ORG_ID` - Defaults to `None`
        """
        if api_key is None:
            api_key = os.environ.get("NEXUSFLOWAI_API_KEY")
        if api_key is None:
            raise NexusflowAIError(
                "The api_key client option must be set either by passing api_key to the client or by setting the NEXUSFLOWAI_API_KEY environment variable"
            )
        self.api_key = api_key

        if organization is None:
            organization = os.environ.get("NEXUSFLOWAI_ORG_ID")
        self.organization = organization

        if base_url is None:
            base_url = os.environ.get("NEXUSFLOWAI_BASE_URL")
        if base_url is None:
            base_url = "https://api.nexusflow.ai/v1"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self._default_stream_cls = AsyncStream

        self.completions = AsyncCompletions(self)
        self.chat = AsyncChat(self)
        self.models = AsyncModels(self)
        self.with_raw_response = AsyncNexusflowAIWithRawResponse(self)

    @property
    @override
    def qs(self) -> Querystring:  # pragma: no cover
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:  # pragma: no cover
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:  # pragma: no cover
        return {
            **super().default_headers,
            "NexusflowAI-Organization": (
                self.organization if self.organization is not None else Omit()
            ),
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        organization: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
    ) -> AsyncNexusflowAI:  # pragma: no cover
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.

        It should be noted that this does not share the underlying httpx client class which may lead
        to performance issues.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError(
                "The `default_headers` and `set_default_headers` arguments are mutually exclusive"
            )

        if default_query is not None and set_default_query is not None:
            raise ValueError(
                "The `default_query` and `set_default_query` arguments are mutually exclusive"
            )

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            organization=organization or self.organization,
            base_url=base_url or str(self.base_url),
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    def __del__(self) -> None:  # pragma: no cover
        if not hasattr(self, "_has_custom_http_client") or not hasattr(self, "close"):
            # this can happen if the '__init__' method raised an error
            return

        if self._has_custom_http_client:
            return

        try:
            asyncio.get_running_loop().create_task(self.close())
        except Exception:  # pylint: disable=broad-exception-caught
            pass

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:  # pragma: no cover
        data = body.get("error", body) if is_mapping(body) else body
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=data)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(
                err_msg, response=response, body=data
            )

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(
                err_msg, response=response, body=data
            )

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=data)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=data)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(
                err_msg, response=response, body=data
            )

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=data)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(
                err_msg, response=response, body=data
            )
        return APIStatusError(err_msg, response=response, body=data)


class NexusflowAIWithRawResponse:
    def __init__(self, client: NexusflowAI) -> None:
        self.completions = CompletionsWithRawResponse(client.completions)
        self.chat = ChatWithRawResponse(client.chat)
        self.models = ModelsWithRawResponse(client.models)


class AsyncNexusflowAIWithRawResponse:
    def __init__(self, client: AsyncNexusflowAI) -> None:
        self.completions = AsyncCompletionsWithRawResponse(client.completions)
        self.chat = AsyncChatWithRawResponse(client.chat)
        self.models = AsyncModelsWithRawResponse(client.models)


Client = NexusflowAI

AsyncClient = AsyncNexusflowAI
