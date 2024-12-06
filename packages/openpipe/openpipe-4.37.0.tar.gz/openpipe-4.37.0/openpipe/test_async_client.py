from functools import reduce
import pytest
import os
from dotenv import load_dotenv
import asyncio
import random
from openai import AsyncOpenAI as BaseAsyncOpenAI
from pydantic import BaseModel

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


async def test_async_content():
    completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "count to 3"}],
        metadata={"prompt_id": "test_async_content"},
    )

    if not TEST_LAST_LOGGED:
        return

    await asyncio.sleep(0.1)
    last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert last_logged.req_payload["messages"][0]["content"] == "count to 3"
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == completion.choices[0].message.content
    )


async def test_async_content_llama():
    completion = await client.chat.completions.create(
        model="openpipe:llama-3-1-8b-content",
        messages=[{"role": "system", "content": "count to 3"}],
        metadata={"prompt_id": "test_async_content_llama"},
    )

    if not TEST_LAST_LOGGED:
        return

    await asyncio.sleep(0.1)
    last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert last_logged.req_payload["messages"][0]["content"] == "count to 3"
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == completion.choices[0].message.content
    )


async def test_async_function_call():
    completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "tell me the weather in SF"}],
        function_call=function_call,
        functions=[function],
        metadata={"prompt_id": "test_async_function_call"},
    )

    if not TEST_LAST_LOGGED:
        return

    await asyncio.sleep(0.1)
    last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert (
        last_logged.req_payload["messages"][0]["content"] == "tell me the weather in SF"
    )
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == completion.choices[0].message.content
    )
    assert (
        last_logged.resp_payload["choices"][0]["message"]["function_call"]["name"]
        == "get_current_weather"
    )


async def test_async_function_call_llama():
    completion = await client.chat.completions.create(
        model="openpipe:tool-calls-test",
        messages=[
            {"role": "system", "content": "tell me the weather in SF and Orlando"}
        ],
        function_call=function_call,
        functions=[function],
        metadata={"prompt_id": "test_async_function_call_llama"},
    )

    if not TEST_LAST_LOGGED:
        return

    await asyncio.sleep(0.1)
    last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert (
        last_logged.req_payload["messages"][0]["content"]
        == "tell me the weather in SF and Orlando"
    )
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == completion.choices[0].message.content
    )
    assert (
        last_logged.resp_payload["choices"][0]["message"]["function_call"]["name"]
        == "get_current_weather"
    )


async def test_async_tool_calls():
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
        metadata={"prompt_id": "test_async_tool_calls"},
    )

    if not TEST_LAST_LOGGED:
        return

    await asyncio.sleep(0.1)
    last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert (
        last_logged.req_payload["messages"][0]["content"]
        == "tell me the weather in SF and Orlando"
    )
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == completion.choices[0].message.content
    )
    assert (
        last_logged.resp_payload["choices"][0]["message"]["tool_calls"][0]["function"][
            "name"
        ]
        == "get_current_weather"
    )


async def test_async_tool_calls_llama():
    completion = await client.chat.completions.create(
        model="openpipe:tool-calls-test",
        messages=[
            {"role": "system", "content": "tell me the weather in SF and Orlando"}
        ],
        tools=[
            {
                "type": "function",
                "function": function,
            },
        ],
        metadata={"prompt_id": "test_async_tool_calls_llama"},
    )

    if not TEST_LAST_LOGGED:
        return

    await asyncio.sleep(0.1)
    last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert (
        last_logged.req_payload["messages"][0]["content"]
        == "tell me the weather in SF and Orlando"
    )
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == completion.choices[0].message.content
    )
    assert (
        last_logged.resp_payload["choices"][0]["message"]["tool_calls"][0]["function"][
            "name"
        ]
        == "get_current_weather"
    )


async def test_async_with_tags_and_metadata():
    completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "count to 10"}],
        metadata={"prompt_id": "test_async_with_tags"},
        openpipe={"tags": {"any_key": "any_value"}},
    )

    if not TEST_LAST_LOGGED:
        return

    await asyncio.sleep(0.1)
    last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == completion.choices[0].message.content
    )
    assert last_logged.metadata["prompt_id"] == "test_async_with_tags"
    assert last_logged.metadata["any_key"] == "any_value"
    assert last_logged.metadata["$sdk"] == "python"


async def test_async_caching():
    models = ["gpt-3.5-turbo", "openpipe:test-content-35"]

    for model in models:
        messages = [{"role": "system", "content": f"{random_letters} count to 10"}]
        completion = await client.chat.completions.create(
            model=model,
            messages=messages,
            metadata={"prompt_id": "test_async_caching"},
        )
        await asyncio.sleep(0.1)
        completion = await client.chat.completions.create(
            model=model,
            messages=messages,
            metadata={"prompt_id": "test_async_caching"},
        )

        if not TEST_LAST_LOGGED:
            return

        await asyncio.sleep(0.1)
        last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
        assert last_logged.cache_hit == False

        completion = await client.chat.completions.create(
            model=model,
            messages=messages,
            metadata={"prompt_id": "test_async_caching"},
            openpipe={"cache": True},
        )
        await asyncio.sleep(0.1)
        completion = await client.chat.completions.create(
            model=model,
            messages=messages,
            metadata={"prompt_id": "test_async_caching"},
            openpipe={"cache": True},
        )

        await asyncio.sleep(0.1)
        last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
        assert last_logged.cache_hit == True


async def test_async_default_base_url():
    default_client = AsyncOpenAI(api_key=os.environ["OPENPIPE_API_KEY"])

    completion = await default_client.chat.completions.create(
        model="openpipe:test-content-35",
        messages=[{"role": "system", "content": "count to 10"}],
        metadata={"prompt_id": "test_async_default_base_url"},
    )

    assert completion.choices[0].message.content != None


async def test_async_bad_openai_call():
    try:
        await client.chat.completions.create(
            model="gpt-3.5-turbo-blaster",
            messages=[{"role": "system", "content": "count to 10"}],
            stream=True,
            metadata={"prompt_id": "test_async_bad_openai_call"},
        )
        assert False
    except Exception as e:
        print(e)
        pass

    if not TEST_LAST_LOGGED:
        return

    await asyncio.sleep(0.1)
    last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert (
        last_logged.error_message
        == "The model `gpt-3.5-turbo-blaster` does not exist or you do not have access to it."
    )
    assert last_logged.status_code == 404


async def test_async_bad_openpipe_call():
    try:
        await client.chat.completions.create(
            model="openpipe:gpt-3.5-turbo-blaster",
            messages=[{"role": "system", "content": "count to 10"}],
            stream=True,
            metadata={"prompt_id": "test_async_bad_openpipe_call"},
        )
        assert False
    except Exception as e:
        print(e)
        pass

    if not TEST_LAST_LOGGED:
        return

    await asyncio.sleep(0.1)
    last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert (
        last_logged.error_message
        == "The model `openpipe:gpt-3.5-turbo-blaster` does not exist"
    )
    assert last_logged.status_code == 404


class PydanticType(BaseModel):
    name: str
    date: str


async def test_async_beta_parse_success():
    completion = await client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "system", "content": "count to 3"}],
        response_format=PydanticType,
        metadata={"prompt_id": "test_async_content"},
    )

    parsed = completion.choices[0].message.parsed
    assert parsed.name is not None
    assert parsed.date is not None

    if not TEST_LAST_LOGGED:
        return

    await asyncio.sleep(0.1)
    last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()

    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == completion.choices[0].message.content
    )


async def test_async_beta_parse_failure():
    try:
        await client.beta.chat.completions.parse(
            model="openpipe:llama-3-1-8b-content",
            messages=[{"role": "system", "content": "count to 3"}],
            response_format=PydanticType,
            metadata={"prompt_id": "test_async_content"},
        )
        assert False
    except Exception as e:
        print(e)
        pass


@pytest.mark.skip(reason="This test hangs indefinitely when run as part of a set")
async def test_async_bad_openai_call_base_sdk():
    try:
        await base_client.chat.completions.create(
            model="gpt-3.5-turbo-blaster",
            messages=[{"role": "system", "content": "count to 10"}],
            stream=True,
            store=True,
            metadata={"prompt_id": "test_async_bad_openai_call_base_sdk"},
        )
        assert False
    except Exception as e:
        print(e)
        pass

    if not TEST_LAST_LOGGED:
        return

    await asyncio.sleep(0.1)
    last_logged = await client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert (
        last_logged.error_message
        == "404 The model `gpt-3.5-turbo-blaster` does not exist"
    )
    assert last_logged.status_code == 404
