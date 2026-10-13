"""Shared lab kit: scripted chat model and local trace log."""

from langchain_core.messages import AIMessage, HumanMessage


def test_fake_model_returns_scripted_messages_in_order():
    from labs.kit.models import FakeChatModel

    model = FakeChatModel(
        script=[
            AIMessage(content="one"),
            AIMessage(content="two"),
        ]
    )

    assert model.invoke([HumanMessage(content="hi")]).content == "one"
    assert model.invoke([HumanMessage(content="again")]).content == "two"


def test_fake_model_records_every_invoke():
    from labs.kit.models import FakeChatModel

    model = FakeChatModel(script=[AIMessage(content="ok")])
    model.invoke([HumanMessage(content="ping")])

    assert len(model.calls) == 1
    assert model.calls[0][0].content == "ping"


def test_bind_tools_keeps_the_same_script():
    from labs.kit.models import FakeChatModel

    model = FakeChatModel(script=[AIMessage(content="still scripted")])
    bound = model.bind_tools(
        [{"name": "search", "description": "find", "parameters": {"type": "object"}}]
    )

    assert bound.invoke([HumanMessage(content="go")]).content == "still scripted"


def test_make_chat_model_targets_local_gemma():
    from labs.kit.models import make_chat_model

    model = make_chat_model()

    assert model.model == "gemma3:4b"
    assert model.temperature == 0


def test_make_tool_model_targets_qwen_because_gemma3_4b_rejects_tools():
    from labs.kit.models import make_tool_model

    model = make_tool_model()

    assert model.model == "qwen2.5:3b"
    assert model.temperature == 0


def test_tracer_records_llm_then_tool_in_order():
    from labs.kit.tracer import LocalTracer

    tracer = LocalTracer()
    tracer.record_llm(prompt="find python jobs", response="call search")
    tracer.record_tool(
        name="search_jobs",
        arguments={"keyword": "python"},
        result="Acme: junior python",
    )
    tracer.record_llm(prompt="observation", response="Acme is hiring")

    assert [event["kind"] for event in tracer.events] == ["llm", "tool", "llm"]
    assert tracer.events[1]["name"] == "search_jobs"
    assert tracer.events[1]["arguments"]["keyword"] == "python"
