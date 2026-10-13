"""Few-shot: promptun icine cozulmus ornek koymak.

Model ornegin sekliyle cevap vermeye egilimlidir.
Ornek, talimatin yerini tutmaz. Talimat hala durur.
"""

from langchain_core.messages import HumanMessage

from labs.kit.models import make_chat_model


def few_shot_prompt(question: str) -> str:
    """Bir cozulmus ornek, sonra gercek soru.

    Ornek 'Company: Acme' bicimini gosterir. Model ayni kalibi surdurur.
    """

    # Ilk soru cozulmus ornektir. Ikincisi modelin surdurecegi gercek sorudur.
    return (
        "Answer with one line in the shape Company: name.\n\n"
        "Question: Who hires SQL analysts in the course list?\n"
        "Answer: Company: Northwind\n\n"
        f"Question: {question}\n"
        "Answer:"
    )


def run_few_shot(question: str, model) -> str:
    # Model ornegin "Company: ad" satirini gorur ve ayni kaliba yaklasir.
    message = model.invoke([HumanMessage(content=few_shot_prompt(question))])
    return str(message.content)


def main(model=None) -> str:
    # Few-shot da Gemma ile calisir. Tool semasi gonderilmez.
    chosen = model or make_chat_model()
    # Ornek Northwind icindir. Bu soru Python ilanini sorar.
    answer = run_few_shot("Who hires junior Python developers?", chosen)
    print(answer)
    # Kalip "Company:" ile baslamaya egilimlidir. Garanti degildir.
    return answer


if __name__ == "__main__":
    main()
