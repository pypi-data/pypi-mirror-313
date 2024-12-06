from functools import reduce
import pytest
import time
from dotenv import load_dotenv
import os
from openai import OpenAI as BaseOpenAI

from . import OpenAI
from .merge_openai_chunks import merge_openai_chunks
from .test_config import TEST_LAST_LOGGED

load_dotenv()

base_client = BaseOpenAI(
    base_url=os.environ["OPENPIPE_BASE_URL"], api_key=os.environ["OPENPIPE_API_KEY"]
)
client = OpenAI()

function_call = {"name": "get_current_weather"}
function = {
    "name": "get_current_weather",
    "description": "Get the current weather in a given location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g. San Francisco, CA",
            },
            "unit": {
                "type": "string",
                "enum": ["celsius", "fahrenheit"],
            },
        },
        "required": ["location"],
    },
}


def test_sync_streaming_content():
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "count to 4"}],
        stream=True,
        metadata={"prompt_id": "test_sync_streaming_content"},
    )
    merged = None
    last_chunk = None
    for chunk in completion:
        merged = merge_openai_chunks(merged, chunk)
        last_chunk = chunk

    print(last_chunk)
    assert last_chunk != "[DONE]", "Last chunk should not be '[DONE]'"
    if not TEST_LAST_LOGGED:
        return

    time.sleep(0.1)

    last_logged = (
        client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    )
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == merged.choices[0].message.content
    )


def test_sync_streaming_content_ft_35():
    completion = client.chat.completions.create(
        model="openpipe:test-content-35",
        messages=[{"role": "system", "content": "count to 4"}],
        stream=True,
        store=True,
        metadata={"prompt_id": "test_sync_streaming_content_ft_35"},
    )

    merged = None
    last_chunk = None
    for chunk in completion:
        merged = merge_openai_chunks(merged, chunk)
        last_chunk = chunk

    print(last_chunk)
    assert last_chunk != "[DONE]", "Last chunk should not be '[DONE]'"

    if not TEST_LAST_LOGGED:
        return

    time.sleep(0.1)

    last_logged = (
        client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    )
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == merged.choices[0].message.content
    )


def test_sync_streaming_content_ft_35_base_sdk():
    completion = base_client.chat.completions.create(
        model="openpipe:test-content-35",
        messages=[{"role": "system", "content": "count to 5"}],
        stream=True,
        store=True,
        metadata={"prompt_id": "test_sync_streaming_content_ft_35_base_sdk"},
    )

    merged = None
    last_chunk = None
    for chunk in completion:
        merged = merge_openai_chunks(merged, chunk)
        last_chunk = chunk

    print(last_chunk)
    assert last_chunk != "[DONE]", "Last chunk should not be '[DONE]'"

    if not TEST_LAST_LOGGED:
        return

    last_logged = (
        client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    )
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == merged.choices[0].message.content
    )


def test_sync_streaming_function_call():
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "tell me the weather in SF"}],
        function_call=function_call,
        functions=[function],
        stream=True,
        metadata={"prompt_id": "test_sync_streaming_function_call"},
    )

    merged = None
    last_chunk = None
    for chunk in completion:
        merged = merge_openai_chunks(merged, chunk)
        last_chunk = chunk

    print(last_chunk)
    assert last_chunk != "[DONE]", "Last chunk should not be '[DONE]'"

    if not TEST_LAST_LOGGED:
        return

    last_logged = (
        client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    )

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


def test_sync_streaming_tool_calls_kwal():
    response = client.chat.completions.create(
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
        metadata={"prompt_id": "test_sync_streaming_tool_calls_kwal"},
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
    for chunk in response:
        completion.append(chunk)

    print(completion)


def test_sync_streaming_tool_calls():
    completion = client.chat.completions.create(
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
        metadata={"prompt_id": "test_sync_streaming_tool_calls"},
    )

    merged = None
    last_chunk = None
    for chunk in completion:
        merged = merge_openai_chunks(merged, chunk)
        last_chunk = chunk

    print(last_chunk)
    assert last_chunk != "[DONE]", "Last chunk should not be '[DONE]'"

    if not TEST_LAST_LOGGED:
        return

    last_logged = (
        client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    )
    assert (
        last_logged.resp_payload["choices"][0]["message"]["tool_calls"][0]["function"][
            "arguments"
        ]
        == merged.choices[0].message.tool_calls[0].function.arguments
    )
