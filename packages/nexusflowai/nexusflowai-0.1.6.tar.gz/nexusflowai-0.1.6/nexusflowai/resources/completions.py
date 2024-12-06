from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal

import httpx

from openai._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from openai._utils import required_args, maybe_transform
from openai._resource import SyncAPIResource, AsyncAPIResource
from openai._response import to_raw_response_wrapper, async_to_raw_response_wrapper
from openai._streaming import Stream, AsyncStream
from openai._base_client import make_request_options
from openai.types.completion_create_params import CompletionCreateParams
from openai.types.chat import (
    ChatCompletionToolParam,
    ChatCompletionMessageParam,
    ChatCompletionToolChoiceOptionParam,
    completion_create_params,
)

from nexusflowai.validators import (
    CompletionsInputValidator,
    ChatCompletionsInputValidator,
    ChatCompletionToolsFlow,
)
from nexusflowai.types import (
    NexusflowAICompletion,
    NexusflowAIChatCompletion,
    NexusflowAIChatCompletionCreateParams,
)
from nexusflowai.utils import ALLOWED_MODELS, transform_client_header
from nexusflowai.resources.utils import (
    maybe_print_hints,
    maybe_parse_into_pydantic,
    batch_call,
)


if TYPE_CHECKING:
    from nexusflowai.client import NexusflowAI, AsyncNexusflowAI

__all__ = ["Completions", "AsyncCompletions"]


class Completions(SyncAPIResource):
    with_raw_response: CompletionsWithRawResponse

    def __init__(self, client: NexusflowAI) -> None:
        super().__init__(client)
        self.with_raw_response = CompletionsWithRawResponse(self)

    @required_args(["model", "prompt"], ["model", "prompt", "stream"])
    def create(
        self,
        *,
        model: Union[
            str,
            ALLOWED_MODELS,
        ],
        prompt: Union[str, List[str], List[int], List[List[int]], None],
        best_of: Optional[int] | NotGiven = NOT_GIVEN,
        echo: Optional[bool] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str], None] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        suffix: Optional[str] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NexusflowAICompletion | Stream[NexusflowAICompletion]:
        """
        Creates a completion for the provided prompt and parameters.

        Args:
          model: ID of the model to use. You can use the
              [List models](https://platform.openai.com/docs/api-reference/models/list) API to
              see all of your available models, or see our
              [Model overview](https://platform.openai.com/docs/models/overview) for
              descriptions of them.

          prompt: The prompt(s) to generate completions for, encoded as a string, array of
              strings, array of tokens, or array of token arrays.

              Note that <|endoftext|> is the document separator that the model sees during
              training, so if a prompt is not specified the model will generate as if from the
              beginning of a new document.

          stream: Whether to stream back partial progress. If set, tokens will be sent as
              data-only
              [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format)
              as they become available, with the stream terminated by a `data: [DONE]`
              message.
              [Example Python code](https://cookbook.openai.com/examples/how_to_stream_completions).

          best_of: Generates `best_of` completions server-side and returns the "best" (the one with
              the highest log probability per token). Results cannot be streamed.

              When used with `n`, `best_of` controls the number of candidate completions and
              `n` specifies how many to return – `best_of` must be greater than `n`.

              **Note:** Because this parameter generates many completions, it can quickly
              consume your token quota. Use carefully and ensure that you have reasonable
              settings for `max_tokens` and `stop`.

          echo: Echo back the prompt in addition to the completion

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

              [See more information about frequency and presence penalties.](https://platform.openai.com/docs/guides/gpt/parameter-details)

          logit_bias: Modify the likelihood of specified tokens appearing in the completion.

              Accepts a JSON object that maps tokens (specified by their token ID in the GPT
              tokenizer) to an associated bias value from -100 to 100. You can use this
              [tokenizer tool](/tokenizer?view=bpe) (which works for both GPT-2 and GPT-3) to
              convert text to token IDs. Mathematically, the bias is added to the logits
              generated by the model prior to sampling. The exact effect will vary per model,
              but values between -1 and 1 should decrease or increase likelihood of selection;
              values like -100 or 100 should result in a ban or exclusive selection of the
              relevant token.

              As an example, you can pass `{"50256": -100}` to prevent the <|endoftext|> token
              from being generated.

          logprobs: Include the log probabilities on the `logprobs` most likely tokens, as well the
              chosen tokens. For example, if `logprobs` is 5, the API will return a list of
              the 5 most likely tokens. The API will always return the `logprob` of the
              sampled token, so there may be up to `logprobs+1` elements in the response.

              The maximum value for `logprobs` is 5.

          max_tokens: The maximum number of [tokens](/tokenizer) to generate in the completion.

              The token count of your prompt plus `max_tokens` cannot exceed the model's
              context length.
              [Example Python code](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken)
              for counting tokens.

          n: How many completions to generate for each prompt.

              **Note:** Because this parameter generates many completions, it can quickly
              consume your token quota. Use carefully and ensure that you have reasonable
              settings for `max_tokens` and `stop`.

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

              [See more information about frequency and presence penalties.](https://platform.openai.com/docs/guides/gpt/parameter-details)

          seed: If specified, our system will make a best effort to sample deterministically,
              such that repeated requests with the same `seed` and parameters should return
              the same result.

              Determinism is not guaranteed, and you should refer to the `system_fingerprint`
              response parameter to monitor changes in the backend.

          stop: Up to 4 sequences where the API will stop generating further tokens. The
              returned text will not contain the stop sequence.

          suffix: The suffix that comes after a completion of inserted text.

          temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will
              make the output more random, while lower values like 0.2 will make it more
              focused and deterministic.

              We generally recommend altering this or `top_p` but not both.

          top_p: An alternative to sampling with temperature, called nucleus sampling, where the
              model considers the results of the tokens with top_p probability mass. So 0.1
              means only the tokens comprising the top 10% probability mass are considered.

              We generally recommend altering this or `temperature` but not both.

          user: A unique identifier representing your end-user, which can help OpenAI to monitor
              and detect abuse.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        request_body = maybe_transform(
            {
                "model": model,
                "prompt": prompt,
                "best_of": best_of,
                "echo": echo,
                "frequency_penalty": frequency_penalty,
                "logit_bias": logit_bias,
                "logprobs": logprobs,
                "max_tokens": max_tokens,
                "n": n,
                "presence_penalty": presence_penalty,
                "seed": seed,
                "stop": stop,
                "stream": stream,
                "suffix": suffix,
                "temperature": temperature,
                "top_p": top_p,
                "user": user,
            },
            completion_create_params.CompletionCreateParams,
        )
        request_body = CompletionsInputValidator(request_body=request_body).validate()

        extra_headers = transform_client_header(extra_headers=extra_headers)

        return self._post(
            "/completions",
            body=request_body,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=NexusflowAICompletion,
            stream=stream or False,
            stream_cls=Stream[NexusflowAICompletion],
        )

    @required_args(["messages", "model"], ["messages", "model", "stream"])
    def create_with_tools(
        self,
        *,
        messages: List[ChatCompletionMessageParam],
        model: Union[
            str,
            ALLOWED_MODELS,
        ],
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        function_call: completion_create_params.FunctionCall | NotGiven = NOT_GIVEN,
        functions: List[completion_create_params.Function] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
        tools: List[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NexusflowAIChatCompletion:
        """
        Convert a ChatCompletion with tools or response_format into a Completion with a raw prompt.
        """
        request_body = maybe_transform(
            {
                "messages": messages,
                "model": model,
                "frequency_penalty": frequency_penalty,
                "function_call": function_call,
                "functions": functions,
                "logit_bias": logit_bias,
                "max_tokens": max_tokens,
                "n": n,
                "parallel_tool_calls": parallel_tool_calls,
                "presence_penalty": presence_penalty,
                "response_format": response_format,
                "seed": seed,
                "stop": stop,
                "stream": stream,
                "temperature": temperature,
                "tool_choice": tool_choice,
                "tools": tools,
                "top_p": top_p,
                "user": user,
            },
            completion_create_params.CompletionCreateParams,
        )

        request_body = ChatCompletionsInputValidator(
            request_body=request_body
        ).validate()

        pythonic_request_body = {
            k: v for k, v in request_body.items() if not isinstance(v, NotGiven)
        }

        flow = ChatCompletionToolsFlow()
        request_body_to_send = flow.preprocess(pythonic_request_body)
        request_body_to_send = {
            k: NOT_GIVEN if v is None else v for k, v in request_body_to_send.items()
        }

        extra_headers = transform_client_header(extra_headers=extra_headers)

        res = self._post(
            "/completions",
            body=request_body_to_send,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=NexusflowAICompletion,
            stream=stream or False,
            stream_cls=Stream[NexusflowAICompletion],
        )

        res = flow.postprocess(pythonic_request_body, res)

        maybe_print_hints(res)

        for choice in res.choices:
            parsed = choice.message.parsed
            choice.message.parsed = maybe_parse_into_pydantic(response_format, parsed)

        return res


class AsyncCompletions(AsyncAPIResource):
    with_raw_response: AsyncCompletionsWithRawResponse

    def __init__(self, client: AsyncNexusflowAI) -> None:
        super().__init__(client)
        self.with_raw_response = AsyncCompletionsWithRawResponse(self)

    @required_args(["model", "prompt"], ["model", "prompt", "stream"])
    async def create(
        self,
        *,
        model: Union[
            str,
            ALLOWED_MODELS,
        ],
        prompt: Union[str, List[str], List[int], List[List[int]], None],
        best_of: Optional[int] | NotGiven = NOT_GIVEN,
        echo: Optional[bool] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str], None] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        suffix: Optional[str] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NexusflowAICompletion | AsyncStream[NexusflowAICompletion]:
        """
        Creates a completion for the provided prompt and parameters.

        Args:
          model: ID of the model to use. You can use the
              [List models](https://platform.openai.com/docs/api-reference/models/list) API to
              see all of your available models, or see our
              [Model overview](https://platform.openai.com/docs/models/overview) for
              descriptions of them.

          prompt: The prompt(s) to generate completions for, encoded as a string, array of
              strings, array of tokens, or array of token arrays.

              Note that <|endoftext|> is the document separator that the model sees during
              training, so if a prompt is not specified the model will generate as if from the
              beginning of a new document.

          stream: Whether to stream back partial progress. If set, tokens will be sent as
              data-only
              [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format)
              as they become available, with the stream terminated by a `data: [DONE]`
              message.
              [Example Python code](https://cookbook.openai.com/examples/how_to_stream_completions).

          best_of: Generates `best_of` completions server-side and returns the "best" (the one with
              the highest log probability per token). Results cannot be streamed.

              When used with `n`, `best_of` controls the number of candidate completions and
              `n` specifies how many to return – `best_of` must be greater than `n`.

              **Note:** Because this parameter generates many completions, it can quickly
              consume your token quota. Use carefully and ensure that you have reasonable
              settings for `max_tokens` and `stop`.

          echo: Echo back the prompt in addition to the completion

          frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their
              existing frequency in the text so far, decreasing the model's likelihood to
              repeat the same line verbatim.

              [See more information about frequency and presence penalties.](https://platform.openai.com/docs/guides/gpt/parameter-details)

          logit_bias: Modify the likelihood of specified tokens appearing in the completion.

              Accepts a JSON object that maps tokens (specified by their token ID in the GPT
              tokenizer) to an associated bias value from -100 to 100. You can use this
              [tokenizer tool](/tokenizer?view=bpe) (which works for both GPT-2 and GPT-3) to
              convert text to token IDs. Mathematically, the bias is added to the logits
              generated by the model prior to sampling. The exact effect will vary per model,
              but values between -1 and 1 should decrease or increase likelihood of selection;
              values like -100 or 100 should result in a ban or exclusive selection of the
              relevant token.

              As an example, you can pass `{"50256": -100}` to prevent the <|endoftext|> token
              from being generated.

          logprobs: Include the log probabilities on the `logprobs` most likely tokens, as well the
              chosen tokens. For example, if `logprobs` is 5, the API will return a list of
              the 5 most likely tokens. The API will always return the `logprob` of the
              sampled token, so there may be up to `logprobs+1` elements in the response.

              The maximum value for `logprobs` is 5.

          max_tokens: The maximum number of [tokens](/tokenizer) to generate in the completion.

              The token count of your prompt plus `max_tokens` cannot exceed the model's
              context length.
              [Example Python code](https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken)
              for counting tokens.

          n: How many completions to generate for each prompt.

              **Note:** Because this parameter generates many completions, it can quickly
              consume your token quota. Use carefully and ensure that you have reasonable
              settings for `max_tokens` and `stop`.

          presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on
              whether they appear in the text so far, increasing the model's likelihood to
              talk about new topics.

              [See more information about frequency and presence penalties.](https://platform.openai.com/docs/guides/gpt/parameter-details)

          seed: If specified, our system will make a best effort to sample deterministically,
              such that repeated requests with the same `seed` and parameters should return
              the same result.

              Determinism is not guaranteed, and you should refer to the `system_fingerprint`
              response parameter to monitor changes in the backend.

          stop: Up to 4 sequences where the API will stop generating further tokens. The
              returned text will not contain the stop sequence.

          suffix: The suffix that comes after a completion of inserted text.

          temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will
              make the output more random, while lower values like 0.2 will make it more
              focused and deterministic.

              We generally recommend altering this or `top_p` but not both.

          top_p: An alternative to sampling with temperature, called nucleus sampling, where the
              model considers the results of the tokens with top_p probability mass. So 0.1
              means only the tokens comprising the top 10% probability mass are considered.

              We generally recommend altering this or `temperature` but not both.

          user: A unique identifier representing your end-user, which can help OpenAI to monitor
              and detect abuse.
              [Learn more](https://platform.openai.com/docs/guides/safety-best-practices/end-user-ids).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """

        request_body = maybe_transform(
            {
                "model": model,
                "prompt": prompt,
                "best_of": best_of,
                "echo": echo,
                "frequency_penalty": frequency_penalty,
                "logit_bias": logit_bias,
                "logprobs": logprobs,
                "max_tokens": max_tokens,
                "n": n,
                "presence_penalty": presence_penalty,
                "seed": seed,
                "stop": stop,
                "stream": stream,
                "suffix": suffix,
                "temperature": temperature,
                "top_p": top_p,
                "user": user,
            },
            completion_create_params.CompletionCreateParams,
        )

        request_body = CompletionsInputValidator(request_body=request_body).validate()

        extra_headers = transform_client_header(extra_headers=extra_headers)

        return await self._post(
            "/completions",
            body=request_body,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=NexusflowAICompletion,
            stream=stream or False,
            stream_cls=AsyncStream[NexusflowAICompletion],
        )

    @required_args(["messages", "model"], ["messages", "model", "stream"])
    async def create_with_tools(
        self,
        *,
        messages: List[ChatCompletionMessageParam],
        model: Union[
            str,
            ALLOWED_MODELS,
        ],
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        function_call: completion_create_params.FunctionCall | NotGiven = NOT_GIVEN,
        functions: List[completion_create_params.Function] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | Literal[True] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
        tools: List[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> NexusflowAIChatCompletion:  # pragma: no cover
        """
        Convert a ChatCompletion with tools or response_format into a Completion with a raw prompt.

        This function is a copy of the Sync `Completions.create_with_tools`
        """
        request_body = maybe_transform(
            {
                "messages": messages,
                "model": model,
                "frequency_penalty": frequency_penalty,
                "function_call": function_call,
                "functions": functions,
                "logit_bias": logit_bias,
                "max_tokens": max_tokens,
                "n": n,
                "parallel_tool_calls": parallel_tool_calls,
                "presence_penalty": presence_penalty,
                "response_format": response_format,
                "seed": seed,
                "stop": stop,
                "stream": stream,
                "temperature": temperature,
                "tool_choice": tool_choice,
                "tools": tools,
                "top_p": top_p,
                "user": user,
            },
            completion_create_params.CompletionCreateParams,
        )

        request_body = ChatCompletionsInputValidator(
            request_body=request_body
        ).validate()

        pythonic_request_body = {
            k: v for k, v in request_body.items() if not isinstance(v, NotGiven)
        }

        flow = ChatCompletionToolsFlow()
        request_body_to_send = flow.preprocess(pythonic_request_body)
        request_body_to_send = {
            k: NOT_GIVEN if v is None else v for k, v in request_body_to_send.items()
        }

        extra_headers = transform_client_header(extra_headers=extra_headers)

        res = await self._post(
            "/completions",
            body=request_body,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
            ),
            cast_to=NexusflowAICompletion,
            stream=stream or False,
            stream_cls=AsyncStream[NexusflowAICompletion],
        )

        res = flow.postprocess(pythonic_request_body, res)

        maybe_print_hints(res)

        for choice in res.choices:
            parsed = choice.message.parsed
            choice.message.parsed = maybe_parse_into_pydantic(response_format, parsed)

        return res

    def batch_create(
        self,
        batch: List[CompletionCreateParams],
        num_calls_in_parallel: Optional[int] = None,
    ) -> List[Union[NexusflowAICompletion, Exception]]:
        """
        Will run the batched prompts in an async manner.
        """
        return batch_call(self.create, batch, num_calls_in_parallel)

    def batch_create_with_tools(
        self,
        batch: List[NexusflowAIChatCompletionCreateParams],
        num_calls_in_parallel: Optional[int] = None,
    ) -> List[Union[NexusflowAIChatCompletion, Exception]]:
        """
        Will run the batched prompts in an async manner.
        """
        return batch_call(self.create_with_tools, batch, num_calls_in_parallel)

    def batch_run_prompts(
        self,
        batch_prompts_str: List[str],
        params: CompletionCreateParams,
        num_calls_in_parallel: Optional[int] = None,
    ) -> List[NexusflowAICompletion]:
        """
        This function takes in a list of raw string prompts, appends other parameters (like modelname, temperature, etc) to it and creates a list of CompletionCreateParams objects. These objects are then passed to the batch_create function to be run asynchronously.

        Args:
        batch_prompts_str: A list of raw prompt strings
        params: A CompletionCreateParams object which is essentially a TypedDict. The key - value pairs should correspond to the input parameters - parameter types of the AsynCompletions.create function.

        Returns:
        A list of NexusflowAICompletion objects.
        """

        if params.get("stream", False):
            raise ValueError("Batch create does not support streaming requests!")

        batched_prompts: List[CompletionCreateParams] = [
            {**params, "prompt": prompt_str} for prompt_str in batch_prompts_str
        ]

        return self.batch_create(batched_prompts, num_calls_in_parallel)


class CompletionsWithRawResponse:
    def __init__(self, completions: Completions) -> None:
        self.create = to_raw_response_wrapper(
            completions.create,
        )


class AsyncCompletionsWithRawResponse:
    def __init__(self, completions: AsyncCompletions) -> None:
        self.create = async_to_raw_response_wrapper(
            completions.create,
        )
