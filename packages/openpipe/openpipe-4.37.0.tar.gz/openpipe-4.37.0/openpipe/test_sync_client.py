from functools import reduce
import pytest
import time
from dotenv import load_dotenv
import os
from openai import OpenAI as BaseOpenAI

from . import OpenAI
from .merge_openai_chunks import merge_openai_chunks
from .test_config import TEST_LAST_LOGGED
from pydantic import BaseModel

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


def test_sync_content():
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "count to 3"}],
        metadata={"prompt_id": "test_sync_content"},
    )

    if not TEST_LAST_LOGGED:
        return

    last_logged = client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert last_logged.req_payload["messages"][0]["content"] == "count to 3"
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == completion.choices[0].message.content
    )


def test_sync_content_llama():
    completion = client.chat.completions.create(
        model="openpipe:llama-3-1-8b-content",
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": "count to 3"}],
        metadata={"prompt_id": "test_sync_content_llama"},
    )

    if not TEST_LAST_LOGGED:
        return

    time.sleep(0.1)

    last_logged = client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert last_logged.req_payload["messages"][0]["content"] == "count to 3"
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == completion.choices[0].message.content
    )


def test_sync_function_call():
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "tell me the weather in SF"}],
        function_call=function_call,
        functions=[function],
        metadata={"prompt_id": "test_sync_function_call"},
    )

    if not TEST_LAST_LOGGED:
        return

    last_logged = client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
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


def test_sync_function_call_llama():
    completion = client.chat.completions.create(
        model="openpipe:tool-calls-test",
        messages=[
            {"role": "system", "content": "tell me the weather in SF and Orlando"}
        ],
        function_call=function_call,
        functions=[function],
        metadata={"prompt_id": "test_sync_function_call_llama"},
    )

    if not TEST_LAST_LOGGED:
        return

    # wait 100ms to ensure the call is logged
    time.sleep(0.1)

    last_logged = client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
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


def test_sync_tool_calls():
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
        metadata={"prompt_id": "test_sync_tool_calls"},
    )

    if not TEST_LAST_LOGGED:
        return

    last_logged = client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
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


def test_sync_tool_calls_llama():
    completion = client.chat.completions.create(
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
        metadata={"prompt_id": "test_sync_tool_calls_llama"},
    )

    if not TEST_LAST_LOGGED:
        return

    last_logged = client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
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


def test_sync_with_tags_and_metadata():
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "count to 10"}],
        metadata={"prompt_id": "test_sync_with_tags"},
        openpipe={"tags": {"any_key": "any_value"}},
    )

    if not TEST_LAST_LOGGED:
        return

    last_logged = client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == completion.choices[0].message.content
    )
    assert last_logged.metadata["prompt_id"] == "test_sync_with_tags"
    assert last_logged.metadata["any_key"] == "any_value"
    assert last_logged.metadata["$sdk"] == "python"


def test_bad_openai_call():
    try:
        client.chat.completions.create(
            model="gpt-3.5-turbo-blaster",
            messages=[{"role": "system", "content": "count to 10"}],
            stream=True,
        )
        assert False
    except Exception:
        pass

    if not TEST_LAST_LOGGED:
        return

    last_logged = client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert (
        last_logged.error_message
        == "The model `gpt-3.5-turbo-blaster` does not exist or you do not have access to it."
    )
    assert last_logged.status_code == 404


def test_bad_openpipe_call():
    try:
        client.chat.completions.create(
            model="openpipe:gpt-3.5-turbo-blaster",
            messages=[{"role": "system", "content": "count to 10"}],
            stream=True,
        )
        assert False
    except Exception:
        pass

    if not TEST_LAST_LOGGED:
        return

    last_logged = client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert (
        last_logged.error_message
        == "The model `openpipe:gpt-3.5-turbo-blaster` does not exist"
    )
    assert last_logged.status_code == 404


def test_bad_openai_initialization():
    bad_client = OpenAI(api_key="bad_key")
    try:
        bad_client.chat.completions.create(
            model="gpt-3.5-turbo-blaster",
            messages=[{"role": "system", "content": "count to 10"}],
            stream=True,
        )
        assert False
    except Exception:
        pass


def test_bad_openpipe_initialization():
    bad_client = OpenAI(openpipe={"api_key": "bad_key"})

    system_content = f"Write this number: {time.time()}"

    bad_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system_content}],
        metadata={"prompt_id": "test_bad_openpipe_initialization"},
    )

    if not TEST_LAST_LOGGED:
        return

    last_logged = client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert last_logged.req_payload["messages"][0]["content"] != system_content


class PydanticType(BaseModel):
    name: str
    date: str


def test_async_beta_parse_success():
    completion = client.beta.chat.completions.parse(
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

    last_logged = client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()

    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == completion.choices[0].message.content
    )


def test_async_beta_parse_failure():
    try:
        client.beta.chat.completions.parse(
            model="openpipe:llama-3-1-8b-content",
            messages=[{"role": "system", "content": "count to 3"}],
            response_format=PydanticType,
            metadata={"prompt_id": "test_async_content"},
        )
        assert False
    except Exception as e:
        print(e)
        pass
