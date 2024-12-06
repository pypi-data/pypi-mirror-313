from functools import reduce
from openai import NOT_GIVEN
import pytest
from dotenv import load_dotenv
import time
from anthropic import Anthropic

from openai import OpenAI
from .client import OpenPipe
from .test_config import TEST_LAST_LOGGED, OPENPIPE_BASE_URL, OPENPIPE_API_KEY

load_dotenv()

client = OpenAI()
op_client = OpenPipe(api_key=OPENPIPE_API_KEY, base_url=OPENPIPE_BASE_URL)
anthropic_client = Anthropic()


def last_logged_call():
    return op_client.base_client.local_testing_only_get_latest_logged_call()


def test_sync_reports_valid_response_payload():
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": "count to 3"}],
        "store": True,
        "metadata": {"prompt_id": "test_sync_reports_valid_response_payload"},
    }

    completion = client.chat.completions.create(**payload)

    op_client.report(
        requested_at=int(time.time() * 1000),
        received_at=int(time.time() * 1000),
        req_payload=payload,
        resp_payload=completion,
        status_code=200,
    )

    if not TEST_LAST_LOGGED:
        return

    time.sleep(0.1)
    last_logged = last_logged_call()
    assert last_logged.req_payload["messages"][0]["content"] == "count to 3"
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == completion.choices[0].message.content
    )
    assert (
        last_logged.metadata["prompt_id"] == "test_sync_reports_valid_response_payload"
    )


def test_sync_reports_null_response_payload():
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": "count to 3"}],
        "store": True,
        "metadata": {"prompt_id": "test_sync_reports_null_response_payload"},
    }

    op_client.report(
        requested_at=int(time.time() * 1000),
        received_at=int(time.time() * 1000),
        req_payload=payload,
        resp_payload=None,
        status_code=200,
    )

    if not TEST_LAST_LOGGED:
        return

    time.sleep(0.1)
    last_logged = last_logged_call()
    assert last_logged.req_payload["messages"][0]["content"] == "count to 3"
    assert last_logged.resp_payload == None
    assert (
        last_logged.metadata["prompt_id"] == "test_sync_reports_null_response_payload"
    )


def test_sync_reports_invalid_request_payload():
    payload = {
        "x": "invalid",
        "metadata": {"prompt_id": "test_sync_reports_invalid_request_payload"},
    }

    op_client.report(
        requested_at=int(time.time() * 1000),
        received_at=int(time.time() * 1000),
        req_payload=payload,
        resp_payload=None,
        status_code=400,
    )

    if not TEST_LAST_LOGGED:
        return

    time.sleep(0.1)
    last_logged = last_logged_call()
    assert last_logged.req_payload == payload
    assert last_logged.resp_payload == None
    assert (
        last_logged.metadata["prompt_id"] == "test_sync_reports_invalid_request_payload"
    )


def test_sync_reports_unusual_deprecated_tags():
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": "count to 3"}],
        "metadata": {"prompt_id": "test_sync_reports_unusual_deprecated_tags"},
    }

    openpipe_deprecated_tags = {
        "numberTag": 1,
        "booleanTag": True,
        "nullTag": None,
    }

    op_client.report(
        requested_at=int(time.time() * 1000),
        received_at=int(time.time() * 1000),
        req_payload=payload,
        resp_payload=None,
        tags=openpipe_deprecated_tags,
        status_code=200,
    )

    if not TEST_LAST_LOGGED:
        return

    time.sleep(0.1)
    last_logged = last_logged_call()
    assert last_logged.req_payload["messages"][0]["content"] == "count to 3"
    assert last_logged.resp_payload == None
    assert (
        last_logged.metadata["prompt_id"] == "test_sync_reports_unusual_deprecated_tags"
    )
    assert last_logged.metadata["numberTag"] == "1"
    assert last_logged.metadata["booleanTag"] == "true"
    assert last_logged.metadata.get("nullTag") == None


def test_sync_report_anthropic():
    payload = {
        "model": "claude-3-opus-20240229",
        "messages": [{"role": "user", "content": "Hello, Claude"}],
        "max_tokens": 100,
    }

    completion = anthropic_client.messages.create(**payload)

    op_client.report_anthropic(
        requested_at=int(time.time() * 1000 - 1050),
        received_at=int(time.time() * 1000),
        req_payload=payload,
        resp_payload=completion,
        status_code=200,
        metadata={"prompt_id": "test_sync_report_anthropic"},
    )

    if not TEST_LAST_LOGGED:
        return

    time.sleep(0.1)
    last_logged = last_logged_call()
    assert last_logged.req_payload["messages"][0]["content"] == "Hello, Claude"
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == completion.content[0].text
    )


def test_sync_report_not_given():
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": "count to 5"}],
        "response_format": NOT_GIVEN,
        "store": True,
        "metadata": {"prompt_id": "test_sync_report_not_given"},
    }

    completion = client.chat.completions.create(**payload)

    op_client.report(
        requested_at=int(time.time() * 1000),
        received_at=int(time.time() * 1000),
        req_payload=payload,
        resp_payload=completion,
        status_code=200,
    )

    if not TEST_LAST_LOGGED:
        return

    time.sleep(0.1)
    last_logged = last_logged_call()
    assert last_logged.req_payload["messages"][0]["content"] == "count to 5"
    assert "response_format" not in last_logged.req_payload
