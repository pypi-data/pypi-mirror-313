import os
from dotenv import load_dotenv
import pytest

from openpipe.client import AsyncOpenPipe

load_dotenv()

exposed_op_client = AsyncOpenPipe(
    base_url=os.environ["OPENPIPE_BASE_URL"],
    api_key=os.environ["OPENPIPE_API_KEY"],
)


@pytest.fixture(autouse=True)
def setup():
    print("\nresetting async client\n")
    global exposed_op_client
    exposed_op_client = AsyncOpenPipe(
        base_url=os.environ["OPENPIPE_BASE_URL"],
        api_key=os.environ["OPENPIPE_API_KEY"],
    )


async def test_async_get_criterion_judgement():
    messages = [{"role": "user", "content": "count to 3"}]
    output = {"role": "assistant", "content": "1, 2, 3"}

    result = await exposed_op_client.get_criterion_judgement(
        criterion_id="highlight-format",
        input={"messages": messages},
        output=output,
    )

    assert isinstance(result.score, float)
    assert isinstance(result.explanation, str)


async def test_async_get_criterion_judgement_reward_model():
    messages = [{"role": "user", "content": "count to 3"}]
    output = {"role": "assistant", "content": "1, 2, 3"}

    result = await exposed_op_client.get_criterion_judgement(
        criterion_id="reward-v1",
        input={"messages": messages},
        output=output,
    )

    assert isinstance(result.score, float)
    assert result.explanation is None
