"""Chapter 4 tests."""


class ScriptedClient:
    """ollama.chat yerine scriptli sozluk dondurur."""

    def __init__(self, script: list[dict]) -> None:
        self.script = list(script)
        self.calls: list[dict] = []

    def chat(self, messages: list[dict], tools: list[dict]) -> dict:
        self.calls.append({"messages": messages, "tools": tools})
        if not self.script:
            raise RuntimeError("script is empty")
        return self.script.pop(0)


def test_schema_names_the_keyword_argument():
    from labs.ch04.raw_loop import search_jobs_schema

    schema = search_jobs_schema()

    assert schema["function"]["name"] == "search_jobs"
    assert "keyword" in schema["function"]["parameters"]["properties"]
    assert schema["function"]["parameters"]["required"] == ["keyword"]


def test_raw_loop_extracts_the_tool_and_returns_the_final_text():
    from labs.ch04.raw_loop import run_raw_agent
    from labs.kit.tracer import LocalTracer

    client = ScriptedClient(
        [
            {
                "content": "",
                "tool_calls": [
                    {
                        "function": {
                            "name": "search_jobs",
                            "arguments": {"keyword": "python"},
                        }
                    }
                ],
            },
            {
                "content": "Acme and Bright hire junior Python developers.",
                "tool_calls": [],
            },
        ]
    )
    tracer = LocalTracer()
    answer = run_raw_agent("Find python jobs", client, tracer)

    assert "Acme" in answer
    assert [event["kind"] for event in tracer.events] == ["llm", "tool", "llm"]
    assert tracer.events[1]["arguments"]["keyword"] == "python"
    # Ikinci cagri, tool sonucunu mesaj listesinde gormelidir.
    second_messages = client.calls[1]["messages"]
    assert any(item.get("role") == "tool" and "Acme" in item["content"] for item in second_messages)


def test_extract_tool_call_parses_a_json_string_argument():
    from labs.ch04.raw_loop import extract_tool_call

    name, arguments = extract_tool_call(
        {
            "content": "",
            "tool_calls": [
                {"function": {"name": "search_jobs", "arguments": '{"keyword": "sql"}'}}
            ],
        }
    )

    assert name == "search_jobs"
    assert arguments == {"keyword": "sql"}
