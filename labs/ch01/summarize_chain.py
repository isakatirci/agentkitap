"""Prompt template ve chain ile metin ozeti.

Bir chain, bir adimin ciktisini sonraki adima verir.
Burada ilk adim prompt template, ikinci adim chat modeldir.
LCEL'de bu baglanti | operatoru ile yazilir.
"""

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate

from labs.kit.models import make_chat_model


def build_summarize_chain(model):
    """Tek cumlelik ozet isteyen chain.

    {text} bir bosluktur. invoke sirasinda gercek metin oraya yapisir.
    Model ham metni degil, bu kalibin doldurulmus halini gorur.
    """

    # from_template, tek bir human mesaji ureten prompt template kurar.
    prompt = ChatPromptTemplate.from_template(
        "Summarize the text in one sentence.\n\nText:\n{text}"
    )
    # | operatoru: once prompt calisir, ciktisi modele gider.
    return prompt | model


def summarize(text: str, model) -> str:
    """Metni chain'den gecirip modelin content alanini dondurur.

    invoke sozlugu, template icindeki {text} boslugunu doldurur.
    Chat model bir AIMessage dondurur. Junior'in okumasi gereken
    alan content'tir; nesnenin kendisi duz yazi degildir.
    """

    chain = build_summarize_chain(model)
    message = chain.invoke({"text": text})
    # Bazi chain'ler duz str dondurebilir. Bu kurs chat model kullandigi
    # icin beklenti AIMessage'tir. Yine de str gelirse onu oldugu gibi alin.
    if isinstance(message, str):
        return message
    if not isinstance(message, AIMessage):
        return str(message.content)
    return str(message.content)


def main(model=None) -> str:
    """Kucuk bir paragrafi ozetler. model verilmezse yerel Gemma kullanilir."""

    source = (
        "Python is a programming language used by beginners. "
        "It reads like English and is common in automation."
    )
    chosen = model or make_chat_model()
    summary = summarize(source, chosen)
    print(summary)
    return summary


if __name__ == "__main__":
    main()
