from openai import (
    OpenAI as OriginalOpenAI,
    OpenAIError,
    APIError as OpenAIAPIError,
    Timeout,
    APITimeoutError,
)
from openai.resources import Chat
from openai.resources.chat.completions import Completions
from openai._types import NotGiven, NOT_GIVEN
from openai.types.chat import ChatCompletionChunk
from openai._streaming import Stream
from openai._base_client import DEFAULT_MAX_RETRIES

import os
import time
import json
from typing import Union, Mapping, Optional, Dict
import httpx

from .merge_openai_chunks import merge_openai_chunks
from .shared import (
    OpenPipeChatCompletion,
    report,
    get_extra_headers,
    get_chat_completion_json,
    configure_openpipe_clients,
)

from .client import OpenPipe
from .api_client.core.api_error import ApiError as OpenPipeApiError
from .openai_sync_beta_wrapper import SyncBetaWrapper

MISSING_OPENAI_API_KEY = "MISSING_OPENAI_API_KEY"


class CompletionsWrapper(Completions):
    openpipe_reporting_client: OpenPipe
    openpipe_completions_client: OriginalOpenAI
    fallback_client: OriginalOpenAI

    def __init__(
        self,
        client: OriginalOpenAI,
        openpipe_reporting_client: OpenPipe,
        openpipe_completions_client: OriginalOpenAI,
        fallback_client: OriginalOpenAI,
    ) -> None:
        super().__init__(client)
        self.openpipe_reporting_client = openpipe_reporting_client
        self.openpipe_completions_client = openpipe_completions_client
        self.fallback_client = fallback_client

    def create(
        self, *args, **kwargs
    ) -> Union[OpenPipeChatCompletion, Stream[ChatCompletionChunk]]:
        openpipe_options = kwargs.pop("openpipe", {}) or {}
        requested_at = int(time.time() * 1000)
        model = kwargs.get("model", "")
        default_timeout = self.openpipe_completions_client.timeout

        if (
            model.startswith("openpipe:")
            or model.startswith("openai:")
            or model.startswith("anthropic:")
            or openpipe_options.get("cache") is True
        ):
            extra_headers = get_extra_headers(kwargs, openpipe_options)
            try:
                return self.openpipe_completions_client.chat.completions.create(
                    **kwargs, extra_headers=extra_headers
                )
            except Exception as e:
                if (
                    "fallback" in openpipe_options
                    and "model" in openpipe_options["fallback"]
                ):
                    kwargs["model"] = openpipe_options["fallback"]["model"]
                    kwargs["timeout"] = openpipe_options["fallback"].get(
                        "timeout", default_timeout
                    )
                    try:
                        chat_completion = self.fallback_client.chat.completions.create(
                            **kwargs
                        )
                        return self._handle_response(
                            chat_completion, kwargs, openpipe_options, requested_at
                        )
                    except Exception as e:
                        return self._handle_error(
                            e, kwargs, openpipe_options, requested_at
                        )
                else:
                    raise e

        try:
            if self._client.api_key == MISSING_OPENAI_API_KEY:
                raise OpenAIError(
                    "The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable"
                )

            # OpenAI does not accept metadata if store is false
            openai_compatible_kwargs = kwargs.copy()
            if (
                "metadata" in openai_compatible_kwargs
                and not openai_compatible_kwargs.get("store")
            ):
                del openai_compatible_kwargs["metadata"]

            chat_completion = super().create(*args, **openai_compatible_kwargs)
            return self._handle_response(
                chat_completion, kwargs, openpipe_options, requested_at
            )
        except Exception as e:
            return self._handle_error(e, kwargs, openpipe_options, requested_at)

    def _handle_response(self, chat_completion, kwargs, openpipe_options, requested_at):
        if isinstance(chat_completion, Stream):

            def _gen():
                assembled_completion = None
                for chunk in chat_completion:
                    assembled_completion = merge_openai_chunks(
                        assembled_completion, chunk
                    )
                    yield chunk

                received_at = int(time.time() * 1000)
                report(
                    configured_client=self.openpipe_reporting_client,
                    openpipe_options=openpipe_options,
                    requested_at=requested_at,
                    received_at=received_at,
                    req_payload=kwargs,
                    resp_payload=get_chat_completion_json(assembled_completion),
                    status_code=200,
                )

            return _gen()
        else:
            received_at = int(time.time() * 1000)
            report(
                configured_client=self.openpipe_reporting_client,
                openpipe_options=openpipe_options,
                requested_at=requested_at,
                received_at=received_at,
                req_payload=kwargs,
                resp_payload=get_chat_completion_json(chat_completion),
                status_code=200,
            )
            return chat_completion

    def _handle_error(self, e, kwargs, openpipe_options, requested_at):
        received_at = int(time.time() * 1000)
        if isinstance(e, OpenPipeApiError) or isinstance(e, OpenAIAPIError):
            error_content = None
            error_message = ""
            try:
                error_content = e.body
                if isinstance(e.body, str):
                    error_message = error_content
                else:
                    error_message = error_content["message"]
            except:
                pass

            report(
                configured_client=self.openpipe_reporting_client,
                openpipe_options=openpipe_options,
                requested_at=requested_at,
                received_at=received_at,
                req_payload=kwargs,
                resp_payload=error_content,
                error_message=error_message,
                status_code=e.status_code,
            )
        raise e


class ChatWrapper(Chat):
    def __init__(
        self,
        client: OriginalOpenAI,
        openpipe_reporting_client: OpenPipe,
        openpipe_completions_client: OriginalOpenAI,
        fallback_client: OriginalOpenAI,
    ) -> None:
        super().__init__(client)
        self.completions = CompletionsWrapper(
            client,
            openpipe_reporting_client,
            openpipe_completions_client,
            fallback_client,
        )


def get_api_key(api_key):
    return api_key or os.getenv("OPENAI_API_KEY") or MISSING_OPENAI_API_KEY


class OpenAIWrapper(OriginalOpenAI):
    chat: ChatWrapper
    beta: SyncBetaWrapper
    openpipe_reporting_client: OpenPipe
    openpipe_completions_client: OriginalOpenAI

    # Support auto-complete
    def __init__(
        self,
        *,
        openpipe: Optional[Dict[str, Union[str, OriginalOpenAI]]] = None,
        api_key: Union[str, None] = None,
        organization: Union[str, None] = None,
        base_url: Union[str, httpx.URL, None] = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Union[Mapping[str, str], None] = None,
        default_query: Union[Mapping[str, object], None] = None,
        http_client: Union[httpx.Client, None] = None,
        _strict_response_validation: bool = False,
    ) -> None:
        super().__init__(
            api_key=get_api_key(api_key),
            organization=organization,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=http_client,
            _strict_response_validation=_strict_response_validation,
        )

        self.openpipe_reporting_client = OpenPipe()
        self.openpipe_completions_client = OriginalOpenAI(
            api_key=get_api_key(api_key),
            organization=organization,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            default_query=default_query,
            http_client=http_client,
            _strict_response_validation=_strict_response_validation,
        )
        configure_openpipe_clients(
            self.openpipe_reporting_client, self.openpipe_completions_client, openpipe
        )

        self.fallback_client = (
            openpipe.get("fallback_client")
            if openpipe
            else OriginalOpenAI(
                api_key=get_api_key(api_key),
                organization=organization,
                base_url=base_url,
                timeout=timeout,
                max_retries=max_retries,
                default_headers=default_headers,
                default_query=default_query,
                http_client=http_client,
                _strict_response_validation=_strict_response_validation,
            )
        )

        self.chat = ChatWrapper(
            self,
            self.openpipe_reporting_client,
            self.openpipe_completions_client,
            self.fallback_client,
        )

        self.beta = SyncBetaWrapper(
            self,
            self.openpipe_reporting_client,
            self.openpipe_completions_client,
            self.fallback_client,
        )
