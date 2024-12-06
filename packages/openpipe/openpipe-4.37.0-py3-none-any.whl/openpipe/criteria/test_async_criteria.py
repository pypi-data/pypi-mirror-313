from openpipe.shared import OpenPipeChatCompletion
import pytest
import os
from dotenv import load_dotenv
import asyncio
from openai import AsyncOpenAI as BaseAsyncOpenAI

from openpipe import AsyncOpenAI
from openpipe.test_config import TEST_LAST_LOGGED

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


def is_number(value) -> bool:
    if isinstance(value, float):
        return True
    return isinstance(value, int)


async def test_async_criteria_base_client():
    completion = await base_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "count to 3"}],
        n=2,
        metadata={"prompt_id": "test_async_criteria_base_client"},
        extra_headers={"op-criteria": '["highlight-format", "juicebox-relevance@v2"]'},
    )

    # test that score is a number
    assert is_number(
        completion.choices[0].criteria_results["highlight-format"]["score"]
    )
    assert is_number(
        completion.choices[0].criteria_results["juicebox-relevance"]["score"]
    )
    assert is_number(
        completion.choices[1].criteria_results["highlight-format"]["score"]
    )
    assert is_number(
        completion.choices[1].criteria_results["juicebox-relevance"]["score"]
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


async def test_async_criteria_openpipe_client():
    completion: OpenPipeChatCompletion = await client.chat.completions.create(
        model="openai:gpt-3.5-turbo",
        messages=[{"role": "system", "content": "count to 3"}],
        n=2,
        metadata={"prompt_id": "test_async_criteria_openpipe_client"},
        openpipe={"criteria": ["highlight-format", "juicebox-relevance@v2"]},
    )

    # test that score is a number
    assert is_number(
        completion.choices[0].criteria_results["highlight-format"]["score"]
    )
    assert is_number(
        completion.choices[0].criteria_results["juicebox-relevance"]["score"]
    )
    assert is_number(
        completion.choices[1].criteria_results["highlight-format"]["score"]
    )
    assert is_number(
        completion.choices[1].criteria_results["juicebox-relevance"]["score"]
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


async def test_async_invalid_criterion_and_version():
    try:
        await client.chat.completions.create(
            model="openai:gpt-3.5-turbo",
            messages=[{"role": "system", "content": "count to 3"}],
            n=2,
            metadata={"prompt_id": "test_async_criteria_openpipe_client"},
            openpipe={"criteria": ["highlight-format", "juicebox-relevance@v2"]},
        )
    except Exception as e:
        assert "Criterion invalid-criterion-name not found" in str(e)

    try:
        await client.chat.completions.create(
            model="openai:gpt-3.5-turbo",
            messages=[{"role": "system", "content": "count to 3"}],
            n=2,
            metadata={"prompt_id": "test_async_criteria_openpipe_client"},
            extra_headers={"op-criteria": '["highlight-format@fake-version"]'},
        )
    except Exception as e:
        assert (
            "Criterion version fake-version not found for criterion highlight-format"
            in str(e)
        )
