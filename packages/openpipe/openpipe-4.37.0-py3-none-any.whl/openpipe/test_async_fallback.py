from functools import reduce
import pytest
import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI as BaseAsyncOpenAI

from . import AsyncOpenAI
from .merge_openai_chunks import merge_openai_chunks
from .test_config import TEST_LAST_LOGGED

load_dotenv()

base_client = BaseAsyncOpenAI()
client = AsyncOpenAI()
client_with_timeout = AsyncOpenAI(timeout=0.1)
client_with_fallback_client = AsyncOpenAI(
    openpipe={"fallback_client": BaseAsyncOpenAI()}
)


@pytest.fixture(autouse=True)
def setup():
    print("\nresetting async client\n")
    global client
    global client_with_timeout
    global client_with_fallback_client
    client = AsyncOpenAI()
    client_with_timeout = AsyncOpenAI(timeout=0.1)
    client_with_fallback_client = AsyncOpenAI(
        timeout=0.1, openpipe={"fallback_client": BaseAsyncOpenAI()}
    )


ft_model = "openpipe:tool-calls-test"
oai_model = "gpt-3.5-turbo-0125"

payload = {
    "model": ft_model,
    "messages": [{"role": "system", "content": "count to 3"}],
}


async def test_async_works_without_fallback():
    completion = await client.chat.completions.create(**payload)

    assert completion.model == ft_model


async def test_async_error_on_timeout():
    with pytest.raises(Exception):
        await client_with_timeout.chat.completions.create(**payload)


async def test_async_uses_default_timeout_in_fallback():
    with pytest.raises(Exception):
        await client_with_timeout.chat.completions.create(
            **payload,
            openpipe={
                "fallback": {
                    "model": oai_model,
                }
            },
        )


async def test_async_fallback_timeout_overrides_default():
    completion = await client_with_timeout.chat.completions.create(
        **payload,
        openpipe={"fallback": {"model": oai_model, "timeout": 1000}},
    )

    assert completion.model == oai_model


async def test_async_fallback_works_with_streaming():
    completion = await client_with_timeout.chat.completions.create(
        model=ft_model,
        messages=[{"role": "system", "content": "count to 3"}],
        stream=True,
        openpipe={"fallback": {"model": oai_model, "timeout": 1000}},
    )

    merged = None
    async for chunk in completion:
        merged = merge_openai_chunks(merged, chunk)

    assert merged.model == oai_model


async def test_async_does_not_fallback_if_not_timeout():
    completion = await client.chat.completions.create(
        **payload, openpipe={"fallback": {"model": oai_model}}
    )
    assert completion.model == ft_model


async def test_async_fallback_if_timeout_is_zero():
    with pytest.raises(Exception):
        await client_with_timeout.chat.completions.create(
            **payload,
            openpipe={"fallback": {"model": oai_model, "timeout": 0}},
        )


async def test_fallback_to_specific_client():
    completion = await client_with_fallback_client.chat.completions.create(
        **payload, openpipe={"fallback": {"model": oai_model, "timeout": 10000}}
    )
    assert completion.model == oai_model


async def test_async_fallback_custom_client_works_with_streaming():
    completion = await client_with_fallback_client.chat.completions.create(
        model=ft_model,
        messages=[{"role": "system", "content": "count to 3"}],
        stream=True,
        openpipe={"fallback": {"model": oai_model, "timeout": 10000}},
    )

    # wait 100ms to ensure the call is logged
    await asyncio.sleep(0.1)

    merged = None
    async for chunk in completion:
        merged = merge_openai_chunks(merged, chunk)

    assert merged.model == oai_model
