import os
from dotenv import load_dotenv
from openai import OpenAI as BaseOpenAI
import time

from openpipe import OpenAI
from openpipe.test_config import TEST_LAST_LOGGED

load_dotenv()

base_client = BaseOpenAI(
    base_url=os.environ["OPENPIPE_BASE_URL"], api_key=os.environ["OPENPIPE_API_KEY"]
)
client = OpenAI()


def is_number(value) -> bool:
    if isinstance(value, float):
        return True
    return isinstance(value, int)


def test_sync_criteria_base_client():
    completion = base_client.chat.completions.create(
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

    time.sleep(0.1)
    last_logged = client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert last_logged.req_payload["messages"][0]["content"] == "count to 3"
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == completion.choices[0].message.content
    )


def test_sync_criteria_openpipe_client():
    completion = client.chat.completions.create(
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

    time.sleep(0.1)
    last_logged = client.openpipe_reporting_client.base_client.local_testing_only_get_latest_logged_call()
    assert last_logged.req_payload["messages"][0]["content"] == "count to 3"
    assert (
        last_logged.resp_payload["choices"][0]["message"]["content"]
        == completion.choices[0].message.content
    )


def test_sync_invalid_criterion_and_version():
    try:
        client.chat.completions.create(
            model="openai:gpt-3.5-turbo",
            messages=[{"role": "system", "content": "count to 3"}],
            n=2,
            metadata={"prompt_id": "test_async_criteria_openpipe_client"},
            openpipe={"criteria": ["invalid-criterion-name"]},
        )
    except Exception as e:
        assert "Criterion invalid-criterion-name not found" in str(e)

    try:
        client.chat.completions.create(
            model="openai:gpt-3.5-turbo",
            messages=[{"role": "system", "content": "count to 3"}],
            n=2,
            metadata={"prompt_id": "test_async_criteria_openpipe_client"},
            openpipe={"criteria": ["highlight-format@fake-version"]},
        )
    except Exception as e:
        assert (
            "Criterion version fake-version not found for criterion highlight-format"
            in str(e)
        )
