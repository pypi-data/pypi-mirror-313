import pytest
from dotenv import load_dotenv
import os
from openai import OpenAI as BaseOpenAI
import httpx
from . import OpenAI

load_dotenv()

client = OpenAI()
client_with_timeout = OpenAI(timeout=0.1)

ft_model = "openpipe:tool-calls-test"
oai_model = "gpt-3.5-turbo-0125"

payload = {
    "model": ft_model,
    "messages": [{"role": "system", "content": "count to 3"}],
}


def test_works_without_fallback():
    completion = client.chat.completions.create(**payload)
    assert completion.model == ft_model


def test_error_on_timeout():
    with pytest.raises(Exception):
        client_with_timeout.chat.completions.create(
            **payload,
        )


def test_does_not_fallback_if_not_timeout():
    completion = client.chat.completions.create(
        **payload, openpipe={"fallback": {"model": oai_model}}
    )
    assert completion.model == ft_model


def test_uses_default_timeout_in_fallback():
    with pytest.raises(Exception):
        client_with_timeout.chat.completions.create(
            **payload,
            openpipe={
                "fallback": {
                    "model": oai_model,
                }
            },
        )


def test_fallback_timeout_overrides_default():
    completion = client_with_timeout.chat.completions.create(
        **payload,
        openpipe={
            "fallback": {
                "model": oai_model,
                "timeout": httpx.Timeout(60.0, read=5.0, write=10.0, connect=2.0),
            }
        },
    )

    assert completion.model == oai_model


def test_fallback_if_timeout_is_zero():
    with pytest.raises(Exception):
        client_with_timeout.chat.completions.create(
            **payload,
            openpipe={"fallback": {"model": oai_model, "timeout": 0}},
        )


def test_fallback_to_specific_client():
    client_with_fallback_client = OpenAI(
        timeout=0.1,
        api_key="wrong",
        openpipe={"fallback_client": BaseOpenAI(api_key=os.environ["OPENAI_API_KEY"])},
    )

    completion = client_with_fallback_client.chat.completions.create(
        **payload,
        openpipe={
            "fallback": {
                "model": oai_model,
                "timeout": httpx.Timeout(60.0, read=5.0, write=10.0, connect=2.0),
            }
        },
    )
    assert completion.model == oai_model


def test_fallback_client_uses_settings():
    client_with_fallback_client = OpenAI(
        timeout=0.1, openpipe={"fallback_client": BaseOpenAI(api_key="wrong")}
    )

    with pytest.raises(Exception):
        client_with_fallback_client.chat.completions.create(
            **payload, openpipe={"fallback": {"model": oai_model, "timeout": 1000}}
        )


# RUN THIS WHEN SERVER IS DOWN
# def test_fallback_with_server_down():
#     completion = client.chat.completions.create(
#         **payload,
#         openpipe={
#             "fallback": {
#                 "model": oai_model
#             }
#         }
#     )
#     assert completion.model == oai_model
