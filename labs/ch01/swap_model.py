"""Ayni chain, farkli chat model.

Uygulama kodu modelin nereden geldigini bilmemeli.
make_chat_model() varsayilan olarak yerel Gemma dondurur.
Testler ayni main() fonksiyonuna FakeChatModel verir.
Bulut modeline gecmek, bu fabrikada tek satiri degistirmektir.
"""

from langchain_core.prompts import ChatPromptTemplate

from labs.kit.models import make_chat_model


def summarize_with(model, text: str) -> str:
    """Chapter 1 ozet chain'inin modelden bagimsiz hali.

    Prompt ayni kalir. Degisen sadece invoke edilen chat modeldir.
    """

    prompt = ChatPromptTemplate.from_template(
        "Summarize the text in one sentence.\n\nText:\n{text}"
    )
    chain = prompt | model
    message = chain.invoke({"text": text})
    return str(message.content)


def main(model=None) -> str:
    """model None ise Ollama Gemma, degilse verilen model kullanilir."""

    source = "Local open-weight models can run on your own machine."
    chosen = model or make_chat_model()
    summary = summarize_with(chosen, source)
    print(summary)
    return summary


if __name__ == "__main__":
    main()
