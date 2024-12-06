from functools import reduce
import pytest
import os
from dotenv import load_dotenv
import asyncio
import random
from openai import AsyncOpenAI as BaseAsyncOpenAI

from . import AsyncOpenAI
from .merge_openai_chunks import merge_openai_chunks
from .test_sync_client import function_call, function
from .test_config import TEST_LAST_LOGGED

load_dotenv()

base_client = BaseAsyncOpenAI(
    base_url=os.environ["OPENPIPE_BASE_URL"], api_key=os.environ["OPENPIPE_API_KEY"]
)
client = AsyncOpenAI()


@pytest.fixture(autouse=True)
def setup():
    print("\nresetting async client\n")
    global client
    client = AsyncOpenAI()


random_letters = "".join(
    [random.choice("abcdefghijklmnopqrstuvwxyz") for i in range(10)]
)


async def test_async_streaming_content():
    completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "count to 4"}],
        stream=True,
        openpipe={"tags": {"prompt_id": "test_async_streaming_content"}},
    )

    merged = None
    last_chunk = None
    async for chunk in completion:
        merged = merge_openai_chunks(merged, chunk)
        last_chunk = chunk

    print(last_chunk)
    # Assert that the last chunk is not "[DONE]"
    assert last_chunk != "[DONE]", "Last chunk should not be '[DONE]'"

    if not TEST_LAST_LOGGED:
        return

    await asyncio.sleep(0.1)
    last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == merged.choices[0].message.content
    )


async def test_async_streaming_content_ft_35():
    completion = await client.chat.completions.create(
        model="openpipe:test-content-35",
        messages=[{"role": "system", "content": "count to 4"}],
        stream=True,
        openpipe={"tags": {"prompt_id": "test_async_streaming_content_ft_35"}},
    )

    merged = None
    last_chunk = None
    async for chunk in completion:
        merged = merge_openai_chunks(merged, chunk)
        last_chunk = chunk

    print(last_chunk)
    # Assert that the last chunk is not "[DONE]"
    assert last_chunk != "[DONE]", "Last chunk should not be '[DONE]'"

    if not TEST_LAST_LOGGED:
        return

    await asyncio.sleep(0.1)
    last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == merged.choices[0].message.content
    )


async def test_async_streaming_content_openai_ft_model():
    completion = await client.chat.completions.create(
        model="openpipe:itchy-birds-dress",
        messages=[{"role": "system", "content": "count to 4"}],
        stream=True,
        openpipe={"tags": {"prompt_id": "test_async_streaming_content_ft_35"}},
    )

    merged = None
    last_chunk = None
    async for chunk in completion:
        merged = merge_openai_chunks(merged, chunk)
        last_chunk = chunk

    print(last_chunk)
    # Assert that the last chunk is not "[DONE]"
    assert last_chunk != "[DONE]", "Last chunk should not be '[DONE]'"

    if not TEST_LAST_LOGGED:
        return

    await asyncio.sleep(0.1)
    last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == merged.choices[0].message.content
    )


async def test_async_streaming_content_openpipe_ft_model():
    completion = await client.chat.completions.create(
        model="openpipe:llama-3-1-8b-content",
        messages=[{"role": "system", "content": "count to 3"}],
        stream=True,
        max_tokens=20,
        openpipe={"tags": {"prompt_id": "test_async_streaming_content_ft_35"}},
    )

    merged = None
    last_chunk = None
    async for chunk in completion:
        merged = merge_openai_chunks(merged, chunk)
        last_chunk = chunk

    print(last_chunk)
    # Assert that the last chunk is not "[DONE]"
    assert last_chunk != "[DONE]", "Last chunk should not be '[DONE]'"

    if not TEST_LAST_LOGGED:
        return

    await asyncio.sleep(0.1)
    last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == merged.choices[0].message.content
    )


async def test_async_streaming_content_ft_35_base_sdk():
    completion = await base_client.chat.completions.create(
        model="openpipe:test-content-35",
        messages=[{"role": "system", "content": "count to 5"}],
        stream=True,
        store=True,
        extra_headers={
            "op-tags": '{"prompt_id": "test_async_streaming_content_ft_35_base_sdk"}',
        },
    )

    merged = None
    last_chunk = None
    async for chunk in completion:
        merged = merge_openai_chunks(merged, chunk)
        last_chunk = chunk

    # Assert that the last chunk is not "[DONE]"
    print(last_chunk)
    assert last_chunk != "[DONE]", "Last chunk should not be '[DONE]'"

    if not TEST_LAST_LOGGED:
        return

    await asyncio.sleep(0.1)
    last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == merged.choices[0].message.content
    )


async def test_async_streaming_function_call():
    completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "tell me the weather in SF"}],
        function_call=function_call,
        functions=[function],
        stream=True,
        openpipe={"tags": {"prompt_id": "test_async_streaming_function_call"}},
    )

    merged = None
    last_chunk = None
    async for chunk in completion:
        merged = merge_openai_chunks(merged, chunk)
        last_chunk = chunk

    # Assert that the last chunk is not "[DONE]"
    print(last_chunk)
    assert last_chunk != "[DONE]", "Last chunk should not be '[DONE]'"

    if not TEST_LAST_LOGGED:
        return

    await asyncio.sleep(0.1)
    last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()

    assert (
        last_logged.req_payload["messages"][0]["content"] == "tell me the weather in SF"
    )
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == merged.choices[0].message.content
    )
    assert (
        last_logged.resp_payload["choices"][0]["message"]["function_call"]["name"]
        == merged.choices[0].message.function_call.name
    )


async def test_async_streaming_tool_calls_kwal():
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        stream=True,
        messages=[
            {
                "role": "system",
                "content": "Help me test the tool call",
            },
            {
                "role": "user",
                "content": "Call the respond function, use 'Hello, World!' as the reply.",
            },
        ],
        openpipe={"tags": {"prompt_id": "test_async_streaming_tool_calls_kwal"}},
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "respond",
                    "description": "Select the next stage of the conversation and reply to the user.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "reply": {
                                "type": "string",
                                "description": "The reply for the user.",
                            },
                        },
                        "required": ["reply"],
                    },
                },
            }
        ],
    )

    completion = []
    async for chunk in response:
        completion.append(chunk)

    print(completion)


async def test_async_streaming_tool_calls():
    completion = await client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "tell me the weather in SF and Orlando"}
        ],
        tools=[
            {
                "type": "function",
                "function": function,
            },
        ],
        stream=True,
        openpipe={"tags": {"prompt_id": "test_async_streaming_tool_calls"}},
    )

    merged = None
    last_chunk = None
    async for chunk in completion:
        merged = merge_openai_chunks(merged, chunk)
        last_chunk = chunk

    # Assert that the last chunk is not "[DONE]"
    print(last_chunk)
    assert last_chunk != "[DONE]", "Last chunk should not be '[DONE]'"

    if not TEST_LAST_LOGGED:
        return

    await asyncio.sleep(0.1)
    last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert (
        last_logged.resp_payload["choices"][0]["message"]["tool_calls"][0]["function"][
            "arguments"
        ]
        == merged.choices[0].message.tool_calls[0].function.arguments
    )
