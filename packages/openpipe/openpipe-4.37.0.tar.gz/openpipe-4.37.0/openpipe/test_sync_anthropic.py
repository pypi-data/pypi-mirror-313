from functools import reduce
import pytest
import time
from dotenv import load_dotenv
import os
from openai import OpenAI as BaseOpenAI

from .test_sync_client import function
from . import OpenAI
from .test_config import TEST_LAST_LOGGED

load_dotenv()

base_client = BaseOpenAI(
    base_url=os.environ["OPENPIPE_BASE_URL"], api_key=os.environ["OPENPIPE_API_KEY"]
)
client = OpenAI()


def test_sync_anthropic_content():
    completion = client.chat.completions.create(
        model="anthropic:claude-3-5-sonnet-20241022",
        messages=[{"role": "system", "content": "count to 3"}],
        openpipe={"tags": {"prompt_id": "test_sync_anthropic_content"}},
    )

    if not TEST_LAST_LOGGED:
        return

    last_logged = (
        client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    )
    assert last_logged.req_payload["messages"][0]["content"] == "count to 3"
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == completion.choices[0].message.content
    )


def test_sync_tool_calls():
    completion = client.chat.completions.create(
        model="anthropic:claude-3-5-sonnet-20241022",
        messages=[
            {"role": "system", "content": "tell me the weather in SF and Orlando"}
        ],
        tools=[
            {
                "type": "function",
                "function": function,
            },
        ],
        openpipe={"tags": {"prompt_id": "test_sync_anthropic_tool_calls"}},
    )

    if not TEST_LAST_LOGGED:
        return

    last_logged = (
        client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    )
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
