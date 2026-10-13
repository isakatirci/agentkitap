"""Yerel trace gunlugu.

LangSmith buluttaki trace ekraninin kucuk karsiligidir. Hesap acmadan
'once LLM, sonra tool, sonra yine LLM' sirasini gorebilirsiniz.
"""


class LocalTracer:
    """Olaylari eklenme sirasiyla tutar."""

    def __init__(self) -> None:
        # Her olay bir sozluk: kind, ve türe gore diger alanlar.
        self.events: list[dict] = []

    def record_llm(self, prompt: str, response: str) -> None:
        """Bir model cagrisini kaydet."""

        self.events.append(
            {
                "kind": "llm",
                "prompt": prompt,
                "response": response,
            }
        )

    def record_tool(self, name: str, arguments: dict, result: str) -> None:
        """Bir tool cagrisini kaydet."""

        self.events.append(
            {
                "kind": "tool",
                "name": name,
                "arguments": arguments,
                "result": result,
            }
        )
