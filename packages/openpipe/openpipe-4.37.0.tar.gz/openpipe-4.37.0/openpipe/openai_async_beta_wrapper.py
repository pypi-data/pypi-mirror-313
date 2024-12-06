from openai import (
    AsyncOpenAI as OriginalAsyncOpenAI,
)
import httpx
import json
from .client import AsyncOpenPipe
from typing import Dict, List, Union, Iterable, Optional
from typing_extensions import Literal

from openai._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from openai.types.chat import completion_create_params
from openai.lib._parsing import (
    ResponseFormatT,
    validate_input_tools,
    parse_chat_completion,
    type_to_response_format_param,
)
from openai.types.chat_model import ChatModel
from openai.types.chat.parsed_chat_completion import ParsedChatCompletion
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_stream_options_param import ChatCompletionStreamOptionsParam
from openai.types.chat.chat_completion_tool_choice_option_param import ChatCompletionToolChoiceOptionParam
from openai.resources.beta import AsyncBeta
from openai.resources.beta.chat import AsyncChat as AsyncBetaChat
from openai.resources.beta.chat.completions import AsyncCompletions as AsyncBetaCompletions


class AsyncBetaCompletionsWrapper(AsyncBetaCompletions):
    def __init__(
        self,
        client: OriginalAsyncOpenAI,
        openpipe_reporting_client: AsyncOpenPipe,
        openpipe_completions_client: OriginalAsyncOpenAI,
        fallback_client: OriginalAsyncOpenAI,
    ) -> None:
        super().__init__(client)
        self.openpipe_reporting_client = openpipe_reporting_client
        self.openpipe_completions_client = openpipe_completions_client
        self.fallback_client = fallback_client


    async def parse(
        self,
        *,
        messages: Iterable[ChatCompletionMessageParam],
        model: Union[str, ChatModel],
        response_format: type[ResponseFormatT] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        function_call: completion_create_params.FunctionCall | NotGiven = NOT_GIVEN,
        functions: Iterable[completion_create_params.Function] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        max_completion_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        metadata: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        service_tier: Optional[Literal["auto", "default"]] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        store: Optional[bool] | NotGiven = NOT_GIVEN,
        stream_options: Optional[ChatCompletionStreamOptionsParam] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
        tools: Iterable[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        openpipe: Optional[Dict[str, Union[str, OriginalAsyncOpenAI]]] = None,
    ) -> ParsedChatCompletion[ResponseFormatT]:
        validate_input_tools(tools)

        error_message = f"OpenPipe cannot guarantee json schema for {model}. Use the 'chat.completions.create()' API instead."

        if isinstance(model, str) and model.startswith("anthropic:"):
            raise ValueError(error_message)

        extra_headers = {
            "X-Stainless-Helper-Method": "beta.chat.completions.parse",
            **(extra_headers or {}),
        }

        raw_completion = await self._client.chat.completions.create(
            messages=messages,
            model=model,
            response_format=type_to_response_format_param(response_format),
            frequency_penalty=frequency_penalty,
            function_call=function_call,
            functions=functions,
            logit_bias=logit_bias,
            logprobs=logprobs,
            max_completion_tokens=max_completion_tokens,
            max_tokens=max_tokens,
            metadata=metadata,
            n=n,
            parallel_tool_calls=parallel_tool_calls,
            presence_penalty=presence_penalty,
            seed=seed,
            service_tier=service_tier,
            stop=stop,
            store=store,
            stream_options=stream_options,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_logprobs=top_logprobs,
            top_p=top_p,
            user=user,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            openpipe=openpipe,
        )
        
        # Check if the content of each choice is valid JSON
        for choice in raw_completion.choices:
            if isinstance(choice.message.content, str):
                try:
                    json.loads(choice.message.content)
                except json.JSONDecodeError:
                    raise ValueError(error_message)

        try:
            parsed_completion = parse_chat_completion(
                response_format=response_format,
                chat_completion=raw_completion,
                input_tools=tools,
            )
        except Exception:
            raise ValueError(error_message)

        # Add OpenPipe metadata if available
        if hasattr(raw_completion, 'openpipe'):
            parsed_completion.openpipe = raw_completion.openpipe

        return parsed_completion

class AsyncBetaChatWrapper(AsyncBetaChat):
    def __init__(
        self,
        client: OriginalAsyncOpenAI,
        openpipe_reporting_client: AsyncOpenPipe,
        openpipe_completions_client: OriginalAsyncOpenAI,
        fallback_client: OriginalAsyncOpenAI,
    ) -> None:
        super().__init__(client)
        self.completions = AsyncBetaCompletionsWrapper(
            client,
            openpipe_reporting_client,
            openpipe_completions_client,
            fallback_client,
        )

class AsyncBetaWrapper(AsyncBeta):
    def __init__(
        self,
        client: OriginalAsyncOpenAI,
        openpipe_reporting_client: AsyncOpenPipe,
        openpipe_completions_client: OriginalAsyncOpenAI,
        fallback_client: OriginalAsyncOpenAI,
    ) -> None:
        super().__init__(client)
        self.chat = AsyncBetaChatWrapper(
            client,
            openpipe_reporting_client,
            openpipe_completions_client,
            fallback_client,
        )
