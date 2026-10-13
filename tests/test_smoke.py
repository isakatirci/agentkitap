"""Live Ollama checks. They must run, not skip, in the final verification."""

import json
import urllib.request

import pytest

pytestmark = pytest.mark.smoke


def _models_ready() -> bool:
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=3) as response:
            payload = json.load(response)
    except Exception:
        return False
    names = [item.get("name", "") for item in payload.get("models", [])]
    has_gemma = any(name.startswith("gemma3:4b") for name in names)
    has_qwen = any(name.startswith("qwen2.5:3b") for name in names)
    return has_gemma and has_qwen


@pytest.fixture(scope="module", autouse=True)
def require_local_models():
    if not _models_ready():
        pytest.fail("gemma3:4b and qwen2.5:3b must both be installed in Ollama")


def test_summarize_live_returns_text():
    from labs.ch01.summarize_chain import summarize
    from labs.kit.models import make_chat_model

    text = (
        "Python is a programming language used by beginners. "
        "It reads like English and is common in automation."
    )
    result = summarize(text, make_chat_model())
    assert isinstance(result, str)
    assert len(result.strip()) > 15


def test_job_agent_live_calls_search_jobs():
    from labs.ch02.job_agent import run_job_agent
    from labs.kit.models import make_tool_model
    from labs.kit.tracer import LocalTracer

    tracer = LocalTracer()
    answer = run_job_agent("Find python jobs", make_tool_model(), tracer)
    tool_names = [event["name"] for event in tracer.events if event["kind"] == "tool"]
    assert "search_jobs" in tool_names
    assert len(answer.strip()) > 5


def test_manual_loop_live_calls_search_jobs():
    from labs.ch03.react_loop import run_react_loop, search_jobs
    from labs.kit.models import make_tool_model
    from labs.kit.tracer import LocalTracer

    tracer = LocalTracer()
    answer = run_react_loop("Find python jobs", make_tool_model(), [search_jobs], tracer)
    tool_names = [event["name"] for event in tracer.events if event["kind"] == "tool"]
    assert "search_jobs" in tool_names
    assert len(answer.strip()) > 5


def test_raw_ollama_loop_live_calls_search_jobs():
    from labs.ch04.raw_loop import OllamaClient, run_raw_agent
    from labs.kit.tracer import LocalTracer

    tracer = LocalTracer()
    answer = run_raw_agent("Find python jobs", OllamaClient(), tracer)
    tool_names = [event["name"] for event in tracer.events if event["kind"] == "tool"]
    assert "search_jobs" in tool_names
    assert len(answer.strip()) > 5


def test_deep_agent_live_returns_text():
    from labs.ch07.deep_agent import ask_deep_agent
    from labs.kit.models import make_tool_model

    answer = ask_deep_agent("Say hello in one short sentence.", make_tool_model())
    assert len(answer.strip()) > 2


def test_capstone_live_writes_files_and_a_report(tmp_path):
    from labs.capstone.assistant import run_assistant
    from labs.ch07.sandbox import Sandbox
    from labs.kit.models import make_tool_model

    sandbox = Sandbox(tmp_path)
    report = run_assistant(
        "Find a junior python job and save a report.",
        make_tool_model(),
        sandbox,
    )
    assert report.company.strip()
    assert report.title.strip()
    assert report.reason.strip()
    assert sandbox.read("plan.txt").strip()
    assert sandbox.read("report.txt").strip()
