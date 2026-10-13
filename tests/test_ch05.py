"""Chapter 5 tests."""

from langchain_core.messages import AIMessage


def test_regex_extracts_final_answer_and_action():
    from labs.ch05.prompt_react import extract_action, extract_final_answer

    assert extract_final_answer("Thought: done\nFinal Answer: Acme hires juniors.") == (
        "Acme hires juniors."
    )
    assert extract_action(
        'Thought: look\nAction: search_jobs\nAction Input: {"keyword": "python"}'
    ) == ("search_jobs", {"keyword": "python"})
    assert extract_action("no action here") is None


def test_stop_sequence_drops_invented_observation_and_uses_the_tool():
    from labs.ch05.prompt_react import run_prompt_react
    from labs.kit.models import FakeChatModel

    model = FakeChatModel(
        script=[
            AIMessage(
                content=(
                    "Thought: look\n"
                    "Action: search_jobs\n"
                    'Action Input: {"keyword": "python"}\n'
                    "Observation: invented"
                )
            ),
            AIMessage(content="Thought: done\nFinal Answer: Acme hires juniors."),
        ]
    )
    answer = run_prompt_react("Find python jobs", model, None)

    assert answer == "Acme hires juniors."
    second = model.calls[1][0].content
    assert "invented" not in second
    assert "Acme: Junior Python Developer" in second


def test_type_mismatch_is_an_observation_and_the_loop_retries():
    from labs.ch05.prompt_react import run_prompt_react
    from labs.kit.models import FakeChatModel
    from labs.kit.tracer import LocalTracer

    model = FakeChatModel(
        script=[
            AIMessage(
                content=(
                    "Thought: search\n"
                    "Action: search_jobs\n"
                    'Action Input: {"keyword": 3}'
                )
            ),
            AIMessage(
                content=(
                    "Thought: keyword must be text\n"
                    "Action: search_jobs\n"
                    'Action Input: {"keyword": "python"}'
                )
            ),
            AIMessage(content="Thought: done\nFinal Answer: Acme hires juniors."),
        ]
    )
    tracer = LocalTracer()
    answer = run_prompt_react("Find python jobs", model, tracer)

    assert answer == "Acme hires juniors."
    assert tracer.events[1]["result"].startswith("Type error")
    assert tracer.events[3]["arguments"]["keyword"] == "python"
