"""Zero-shot: ornek yok, sadece talimat.

Model token uretir. Bu dosya ona bir talimat ve bir soru verir.
Dogru cevap garanti degildir; promptun sekli buradaki derstir.
"""

from langchain_core.messages import HumanMessage

from labs.kit.models import make_chat_model


def zero_shot_prompt(question: str) -> str:
    """Ornek icermeyen prompt. Soru oldugu gibi yapisir."""

    return f"Answer the question in one short sentence.\n\nQuestion: {question}"


def run_zero_shot(question: str, model) -> str:
    message = model.invoke([HumanMessage(content=zero_shot_prompt(question))])
    return str(message.content)


def main(model=None) -> str:
    chosen = model or make_chat_model()
    answer = run_zero_shot("Which company in the course list hires junior Python developers?", chosen)
    print(answer)
    return answer


if __name__ == "__main__":
    main()
