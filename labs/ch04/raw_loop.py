"""Decorator olmadan tool: elle JSON schema ve ham Ollama dongusu.

LangChain @tool semayi docstring ve tip ipucundan uretir.
Bu dosya ayni semayi sozluk olarak yazar ve ollama SDK sozlesmesine
benzeyen bir client.chat cagrisina verir.
"""

import json

from labs.ch02.job_data import format_jobs
from labs.kit.tracer import LocalTracer


def search_jobs(keyword: str) -> str:
    """Yerel ilan listesinde tag arar. Decorator yoktur."""

    return format_jobs(keyword)


# Isim -> fonksiyon. Sema ile uygulama ayni isimde bulusur.
TOOLS = {"search_jobs": search_jobs}


def search_jobs_schema() -> dict:
    """Ollama'nin bekledigi function schema.

    parameters bir JSON schema'dir. required, modelin keyword'u
    bos birakmasini zorlastirir. Zorunlu kilmak yine de garanti degildir;
    dongu eksik argumani yine de kontrol etmelidir.
    """

    return {
        "type": "function",
        "function": {
            "name": "search_jobs",
            "description": "Find local jobs whose tags contain the keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Tag to match, for example python.",
                    }
                },
                "required": ["keyword"],
            },
        },
    }


def extract_tool_call(message: dict) -> tuple[str, dict] | None:
    """Ham mesajdan tool adi ve arguman sozlugunu cikarir.

    Argumanlar bazen sozluk, bazen JSON string gelir. Ikisini de kabul et.
    Tool yoksa None doner; dongu o zaman nihai metni alir.
    """

    calls = message.get("tool_calls") or []
    if not calls:
        return None
    function = calls[0]["function"]
    arguments = function["arguments"]
    if isinstance(arguments, str):
        arguments = json.loads(arguments)
    return function["name"], arguments


class OllamaClient:
    """Gercek ollama.chat cagrisini sozluge cevirir."""

    def __init__(self, model_name: str = "qwen2.5:3b") -> None:
        # gemma3:4b bu Ollama surumunde tools listesini 400 ile reddeder.
        self.model_name = model_name

    def chat(self, messages: list[dict], tools: list[dict]) -> dict:
        from ollama import chat

        response = chat(model=self.model_name, messages=messages, tools=tools)
        message = response["message"] if isinstance(response, dict) else response.message
        content = message["content"] if isinstance(message, dict) else (message.content or "")
        raw_calls = (
            message["tool_calls"] if isinstance(message, dict) else message.tool_calls
        )
        tool_calls = []
        for call in raw_calls or []:
            function = call["function"] if isinstance(call, dict) else call.function
            name = function["name"] if isinstance(function, dict) else function.name
            arguments = (
                function["arguments"] if isinstance(function, dict) else function.arguments
            )
            tool_calls.append({"function": {"name": name, "arguments": arguments}})
        return {"content": content or "", "tool_calls": tool_calls}


def run_raw_agent(
    user_text: str,
    client,
    tracer: LocalTracer | None = None,
    max_steps: int = 4,
) -> str:
    """JSON schema'li ham agent dongusu.

    client.chat(messages, tools) bir sozluk dondurur:
    content ve tool_calls. Bu, Ollama SDK cevabinin sade halidir.
    """

    messages: list[dict] = [{"role": "user", "content": user_text}]
    tools = [search_jobs_schema()]
    for _ in range(max_steps):
        message = client.chat(messages, tools)
        if tracer is not None:
            tracer.record_llm(
                prompt=user_text,
                response=str(message["content"] or message["tool_calls"]),
            )
        messages.append(
            {
                "role": "assistant",
                "content": message["content"],
                "tool_calls": message["tool_calls"],
            }
        )
        extracted = extract_tool_call(message)
        if extracted is None:
            return str(message["content"])
        name, arguments = extracted
        if name not in TOOLS:
            result = f"Unknown tool: {name}"
        else:
            result = TOOLS[name](**arguments)
        if tracer is not None:
            tracer.record_tool(name=name, arguments=arguments, result=result)
        messages.append({"role": "tool", "content": result, "name": name})
    raise RuntimeError("raw agent hit max_steps")


def main(client=None) -> str:
    chosen = client or OllamaClient()
    answer = run_raw_agent("Find python jobs", chosen, LocalTracer())
    print(answer)
    return answer


if __name__ == "__main__":
    main()
