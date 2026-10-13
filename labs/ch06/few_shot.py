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

    return (
        "Answer with one line in the shape Company: name.\n\n"
        "Question: Who hires SQL analysts in the course list?\n"
        "Answer: Company: Northwind\n\n"
        f"Question: {question}\n"
        "Answer:"
    )


def run_few_shot(question: str, model) -> str:
    message = model.invoke([HumanMessage(content=few_shot_prompt(question))])
    return str(message.content)


def main(model=None) -> str:
    chosen = model or make_chat_model()
    answer = run_few_shot("Who hires junior Python developers?", chosen)
    print(answer)
    return answer


if __name__ == "__main__":
    main()
