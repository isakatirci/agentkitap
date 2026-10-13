"""Chat model fabrikasi.

Junior notu: Gercek model (Ollama) ve test modeli ayni `invoke` sozlesmesini
kullanir. Ders kodu hangisinin geldini bilmek zorunda kalmaz.
"""

from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import Field


class FakeChatModel(BaseChatModel):
    """Sirayla onceden yazilmis AIMessage donduren chat model.

    Agent dongusunu kelimesi kelimesine test etmek icin kullanilir.
    Ilk invoke script[0], ikinci invoke script[1] dondurur.
    """

    # Siradaki cevaplar. invoke her cagrildiginda bastakini tuketir.
    script: list[AIMessage]
    # Testler modelin hangi mesajlari gordugunu buradan okur.
    calls: list[list[BaseMessage]] = Field(default_factory=list)

    @property
    def _llm_type(self) -> str:
        return "fake-script"

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: Any = None,
        **kwargs: Any,
    ) -> ChatResult:
        # Her cagriyi sakla ki test "model su mesaji gordu" diyebilsin.
        self.calls.append(list(messages))
        if not self.script:
            raise RuntimeError("FakeChatModel script is empty")
        message = self.script.pop(0)
        # Chapter 5 stop sequence: metin stop kelimesinde kesilir.
        if stop and isinstance(message.content, str):
            text = message.content
            cut = len(text)
            for token in stop:
                index = text.find(token)
                if index != -1:
                    cut = min(cut, index)
            message = message.model_copy(update={"content": text[:cut]})
        return ChatResult(generations=[ChatGeneration(message=message)])

    def bind_tools(self, tools: Any, **kwargs: Any) -> "FakeChatModel":
        # Gercek model tool semasini modele baglar. Scriptli model araclari
        # yok sayar; cevaplar testin yazdigi sirayi izler.
        del tools, kwargs
        return self


# Gemma 3 4B duz metin lablarinda kalir. Bu Ollama surumu gemma3:4b
# icin tools parametresini reddeder. Tool calling lablarinda Qwen 2.5 3B
# kullanilir. Ikisi de yereldir, ikisi de anahtar istemez.
CHAT_MODEL_NAME = "gemma3:4b"
TOOL_MODEL_NAME = "qwen2.5:3b"


def make_chat_model(model_name: str = CHAT_MODEL_NAME) -> Any:
    """Yerel Ollama chat modeli. Varsayilan Gemma 3 4B, temperature 0.

    temperature 0 ayni soruya daha kararli cevap vermesi icindir.
    Ucretli bir bulut anahtari gerekmez. Tool isteyen lablar
    make_tool_model kullanir.
    """

    from langchain_ollama import ChatOllama

    # num_predict, cevabi keser. Kesilmezse kucuk bir model sayfa sayfa yazar
    # ve lab donmus gibi durur.
    return ChatOllama(model=model_name, temperature=0, num_predict=256)


def make_tool_model(model_name: str = TOOL_MODEL_NAME) -> Any:
    """Tool calling destekleyen yerel model. Varsayilan Qwen 2.5 3B."""

    return make_chat_model(model_name)
