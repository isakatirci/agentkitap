"""Chapter 1: foundations labs."""

from langchain_core.messages import AIMessage


def test_load_settings_skips_comments_and_reads_model():
    from labs.ch01.load_env import load_settings

    settings = load_settings(".env.example")

    assert settings["MODEL"] == "gemma3:4b"
    assert "LANGSMITH_TRACING" in settings
    assert not any(key.startswith("#") for key in settings)


def test_summarize_returns_model_text_and_sends_the_source():
    from labs.ch01.summarize_chain import summarize
    from labs.kit.models import FakeChatModel

    model = FakeChatModel(script=[AIMessage(content="Python is for beginners.")])
    result = summarize("Python is a language used by beginners.", model)

    assert result == "Python is for beginners."
    sent = " ".join(
        message.content
        for message in model.calls[0]
        if isinstance(message.content, str)
    )
    assert "Python is a language used by beginners." in sent


def test_describe_response_reads_type_content_and_tool_calls():
    from labs.ch01.read_response import describe_response

    info = describe_response(AIMessage(content="hello", tool_calls=[]))

    assert info["type"] == "ai"
    assert info["content"] == "hello"
    assert info["tool_calls"] == []


def test_swap_model_uses_the_injected_model():
    from labs.ch01.swap_model import main
    from labs.kit.models import FakeChatModel

    model = FakeChatModel(script=[AIMessage(content="Local summary.")])

    assert main(model=model) == "Local summary."


def test_traced_summary_records_one_llm_event():
    from labs.ch01.trace_chain import traced_summarize
    from labs.kit.models import FakeChatModel
    from labs.kit.tracer import LocalTracer

    model = FakeChatModel(script=[AIMessage(content="Traced.")])
    tracer = LocalTracer()

    assert traced_summarize("A short note.", model, tracer) == "Traced."
    assert [event["kind"] for event in tracer.events] == ["llm"]
    assert "A short note." in tracer.events[0]["prompt"]
    assert tracer.events[0]["response"] == "Traced."


def test_bullet_answer_asks_for_three_bullets():
    from labs.ch01.bullet_summary_answer import summarize_as_bullets
    from labs.kit.models import FakeChatModel

    model = FakeChatModel(script=[AIMessage(content="- a\n- b\n- c")])
    result = summarize_as_bullets("Python, tests, and agents.", model)

    assert result == "- a\n- b\n- c"
    sent = " ".join(
        message.content
        for message in model.calls[0]
        if isinstance(message.content, str)
    )
    assert "three bullet" in sent.lower()


def test_print_css_keeps_code_blocks_and_answers_together():
    from pathlib import Path

    css = Path("course/css/course.css").read_text(encoding="utf-8")

    assert "@page" in css
    assert "size: A4" in css
    assert "break-inside: avoid" in css
    assert ".answer" in css
