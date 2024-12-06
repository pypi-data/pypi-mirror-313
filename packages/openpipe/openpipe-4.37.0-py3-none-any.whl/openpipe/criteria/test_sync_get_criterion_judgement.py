import os
from dotenv import load_dotenv

from openpipe.client import OpenPipe

load_dotenv()

exposed_op_client = OpenPipe(
    base_url=os.environ["OPENPIPE_BASE_URL"],
    api_key=os.environ["OPENPIPE_API_KEY"],
)


def test_sync_get_criterion_judgement():
    messages = [{"role": "user", "content": "count to 3"}]
    output = {"role": "assistant", "content": "1, 2, 3"}

    result = exposed_op_client.get_criterion_judgement(
        criterion_id="highlight-format",
        input={"messages": messages},
        output=output,
    )

    assert isinstance(result.score, float)
    assert isinstance(result.explanation, str)


def test_sync_get_criterion_judgement_reward_model():
    messages = [{"role": "user", "content": "count to 3"}]
    output = {"role": "assistant", "content": "1, 2, 3"}

    result = exposed_op_client.get_criterion_judgement(
        criterion_id="reward-v1",
        input={"messages": messages},
        output=output,
    )

    assert isinstance(result.score, float)
    assert result.explanation is None
