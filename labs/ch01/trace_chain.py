"""Chain calismasini yerel trace'e yazmak.

LangSmith ayni fikrin bulut ekranidir: hangi prompt gitti, model ne dedi.
Bu lab hesap acmadan ayni olayi LocalTracer icine yazar.
"""

from langchain_core.prompts import ChatPromptTemplate

from labs.kit.models import make_chat_model
from labs.kit.tracer import LocalTracer


def traced_summarize(text: str, model, tracer: LocalTracer) -> str:
    """Ozet uretir ve tek bir llm olayi kaydeder.

    prompt alanina kullanicinin verdigi metin yazilir ki izde
    'modele ne sorduk' gorulsun. response, modelin content degeridir.
    """

    # Ozet chain'i Chapter 1 ile aynidir. Eklenen sey tracer kaydidir.
    prompt = ChatPromptTemplate.from_template(
        "Summarize the text in one sentence.\n\nText:\n{text}"
    )
    # Pipe, promptu modele baglar. Ara degisken tutulmaz.
    message = (prompt | model).invoke({"text": text})
    answer = str(message.content)
    # Trace, chain bittikten sonra da okunabilsin diye ayri nesnededir.
    tracer.record_llm(prompt=text, response=answer)
    return answer


def main(model=None) -> str:
    """Bir ozeti calistirir ve trace satirini yazdirir."""

    # Yeni bir gunluk. Onceki labin olaylari buraya karismaz.
    tracer = LocalTracer()
    chosen = model or make_chat_model()
    answer = traced_summarize("Tracing shows each model call.", chosen, tracer)
    print(answer)
    # Tek olay beklenir: kind degeri llm.
    print(tracer.events)
    return answer


if __name__ == "__main__":
    main()
