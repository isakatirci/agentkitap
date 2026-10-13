"""Yerel trace gunlugu.

LangSmith buluttaki trace ekraninin kucuk karsiligidir. Hesap acmadan
'once LLM, sonra tool, sonra yine LLM' sirasini gorebilirsiniz.
"""


# Olay listesi sirali kalir. Testler ilk olayin llm olmasini bekler.
class LocalTracer:
    """Olaylari eklenme sirasiyla tutar."""

    def __init__(self) -> None:
        # Her olay bir sozluk: kind, ve türe gore diger alanlar.
        self.events: list[dict] = []

    def record_llm(self, prompt: str, response: str) -> None:
        """Bir model cagrisini kaydet."""

        # kind alani sirayi okumayi kolaylastirir: llm, tool, llm.
        self.events.append(
            {
                "kind": "llm",
                "prompt": prompt,
                # response, modelin content metnidir. Mesaj nesnesi saklanmaz.
                "response": response,
            }
        )

    def record_tool(self, name: str, arguments: dict, result: str) -> None:
        """Bir tool cagrisini kaydet."""

        # Argumanlar tool sonucunun icinde degil, bu olayin icindedir.
        self.events.append(
            {
                "kind": "tool",
                "name": name,
                "arguments": arguments,
                "result": result,
            }
        )
