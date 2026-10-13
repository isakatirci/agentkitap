"""Chapter 2 tests."""

from langchain_core.messages import AIMessage


def _tool_call(name: str, args: dict, call_id: str) -> AIMessage:
    return AIMessage(
        content="",
        tool_calls=[{"name": name, "args": args, "id": call_id, "type": "tool_call"}],
    )


def test_job_agent_calls_search_then_answers():
    from labs.ch02.job_agent import run_job_agent
    from labs.kit.models import FakeChatModel
    from labs.kit.tracer import LocalTracer

    model = FakeChatModel(
        script=[
            _tool_call("search_jobs", {"keyword": "python"}, "call_1"),
            AIMessage(content="Acme and Bright hire junior Python developers."),
        ]
    )
    tracer = LocalTracer()
    answer = run_job_agent("Find python jobs", model, tracer)

    assert "Acme" in answer
    assert [event["kind"] for event in tracer.events] == ["llm", "tool", "llm"]
    assert tracer.events[1]["name"] == "search_jobs"
    assert tracer.events[1]["arguments"]["keyword"] == "python"
    assert "Acme: Junior Python Developer" in tracer.events[1]["result"]


def test_search_corpus_finds_python_and_skips_network_without_a_key(monkeypatch):
    from labs.ch02.search_corpus import run_search_agent, search

    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    found = search("python")
    assert "Acme" in found
    assert "Northwind" not in found

    from labs.kit.models import FakeChatModel

    model = FakeChatModel(
        script=[
            _tool_call("search_documents", {"query": "python"}, "call_1"),
            AIMessage(content="Acme hires junior Python developers."),
        ]
    )
    assert "Acme" in run_search_agent("python jobs", model)


def test_both_structured_output_strategies_return_a_job_match():
    from labs.ch02.structured_output import (
        recommend_with_provider_strategy,
        recommend_with_tool_strategy,
    )
    from labs.kit.models import FakeChatModel

    payload = {
        "title": "Junior Python Developer",
        "company": "Acme",
        "reason": "python tag",
    }
    tool_model = FakeChatModel(
        script=[_tool_call("JobMatch", payload, "call_1")]
    )
    provider_model = FakeChatModel(
        script=[
            AIMessage(
                content=(
                    '{"title":"Junior Python Developer","company":"Acme",'
                    '"reason":"python tag"}'
                )
            )
        ]
    )

    via_tool = recommend_with_tool_strategy("python", tool_model)
    via_provider = recommend_with_provider_strategy("python", provider_model)

    assert via_tool.company == "Acme"
    assert via_provider.title == "Junior Python Developer"
    assert via_tool.reason == via_provider.reason


def test_first_job_answer_returns_only_acme():
    from labs.ch02.first_job_answer import first_python_job

    assert first_python_job() == "Acme: Junior Python Developer"
