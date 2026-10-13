"""Function calling olmadan ReAct.

Model tool_calls alani uretmez. Thought / Action / Action Input
satirlarini duz metin olarak yazar. Biz regex ile ayiririz.
Stop sequence, modelin Observation satirini kendisinin uydurmasini keser.
Gercek observation'i ancak tool calistiktan sonra scratchpad'e yazariz.
"""

import json
import re

from langchain_core.messages import HumanMessage

from labs.ch02.job_data import format_jobs
from labs.kit.models import make_chat_model
from labs.kit.tracer import LocalTracer

TOOL_TEXT = "search_jobs: keyword must be a string, for example python."

REACT_INSTRUCTIONS = """You are a job agent. Tools:
{tools}

Use exactly this shape. Stop before Observation. The program will write Observation.

Thought: why you chose the next step
Action: search_jobs
Action Input: {{"keyword": "python"}}

When you know the answer, write:
Thought: I know the answer
Final Answer: the jobs you found
"""


def extract_final_answer(text: str) -> str | None:
    """Final Answer satirindan sonrasini alir. Yoksa None."""

    # DOTALL, cevabin alt satirlara tasmasina izin verir.
    match = re.search(r"Final Answer:\s*(.*)", text, re.DOTALL)
    if match is None:
        return None
    # Basindaki ve sonundaki bosluklar cevabin parcasi sayilmaz.
    return match.group(1).strip()


def extract_action(text: str) -> tuple[str, dict] | None:
    """Action adi ve Action Input JSON nesnesini cikarir.

    JSON kiriksa None doner. Dongu bunu 'ayristiramadim' diye gorur.
    """

    action = re.search(r"Action:\s*([A-Za-z_][A-Za-z0-9_]*)", text)
    raw = re.search(r"Action Input:\s*(\{.*?\})", text, re.DOTALL)
    if action is None or raw is None:
        return None
    try:
        arguments = json.loads(raw.group(1))
    except json.JSONDecodeError:
        return None
    if not isinstance(arguments, dict):
        return None
    return action.group(1), arguments


def execute_tool(name: str, arguments: dict) -> str:
    """Tool'u calistirir. Tip uyusmazligi exception degil, observation metnidir.

    Model sayi gonderirse Python fonksiyonu patlamasin. Hata cumlesi
    scratchpad'e yazilsin ki model bir sonraki turda string gondersin.
    """

    if name != "search_jobs":
        return f"Unknown tool: {name}"
    keyword = arguments.get("keyword")
    if not isinstance(keyword, str):
        return "Type error: keyword must be a string."
    return format_jobs(keyword)


def run_prompt_react(
    user_text: str,
    model,
    tracer: LocalTracer | None = None,
    max_steps: int = 4,
) -> str:
    """Metin tabanli ReAct dongusu.

    stop=['Observation:'] modelin sahte gozlem yazmasini keser.
    Scratchpad onceki thought/action ve gercek observation'i tasir.
    """

    scratchpad = ""
    instructions = REACT_INSTRUCTIONS.format(tools=TOOL_TEXT)
    for _ in range(max_steps):
        prompt = f"{instructions}\nQuestion: {user_text}\n{scratchpad}"
        # Stop, Observation kelimesinde uretimi keser. Uydurma gozlem prompt'a girmez.
        message = model.invoke([HumanMessage(content=prompt)], stop=["Observation:"])
        text = str(message.content)
        if tracer is not None:
            tracer.record_llm(prompt=user_text, response=text)
        final = extract_final_answer(text)
        if final:
            return final
        parsed = extract_action(text)
        if parsed is None:
            return "Could not parse an action or a final answer."
        name, arguments = parsed
        observation = execute_tool(name, arguments)
        if tracer is not None:
            tracer.record_tool(name=name, arguments=arguments, result=observation)
        # Gercek observation burada eklenir. Modelin yazdigi degil.
        scratchpad += f"{text}\nObservation: {observation}\n"
    raise RuntimeError("prompt ReAct hit max_steps")


def main(model=None) -> str:
    chosen = model or make_chat_model()
    answer = run_prompt_react("Find python jobs", chosen, LocalTracer())
    print(answer)
    # Bu lab tool API'si kullanmaz. Gemma yeter.
    return answer


if __name__ == "__main__":
    main()
