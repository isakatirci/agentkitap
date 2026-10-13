"""Uygulama cevabi: ozeti uc madde olarak iste.

Soru: summarize_chain.py icindeki talimati degistir.
Modelden tek cumle degil, tam olarak uc madde iste.
Asagidaki prompt bu degisikligin tam halidir.
"""

from langchain_core.prompts import ChatPromptTemplate

from labs.kit.models import make_chat_model


def summarize_as_bullets(text: str, model) -> str:
    """Ayni chain deseni, farkli talimat.

    'three bullet' ifadesi talimatin parcasi olarak modele gider.
    Model yine serbest metin dondurur; madde isareti istemek sema degildir.
    Sema Chapter 2 structured output konusudur.
    """

    # "three bullet" talimati modele giden metnin parcasi olur.
    prompt = ChatPromptTemplate.from_template(
        "Summarize the text as three bullet points.\n\nText:\n{text}"
    )
    # Chain yine prompt, sonra modeldir. Tek cumlelik labdan farki bu satirdir.
    message = (prompt | model).invoke({"text": text})
    # Donen sey hala serbest metindir, Pydantic nesnesi degildir.
    return str(message.content)


def main(model=None) -> str:
    source = "Python, tests, and agents help a junior ship small programs."
    # model verilmezse Gemma kullanilir. Test scriptli model gecirir.
    chosen = model or make_chat_model()
    answer = summarize_as_bullets(source, chosen)
    print(answer)
    # Madde isaretleri modelden gelir. Kod onlarin yerini zorlamaz.
    return answer


if __name__ == "__main__":
    main()
