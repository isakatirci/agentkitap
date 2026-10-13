"""Chain of thought: once ara adim, sonra cevap.

Model aksiyon uretmez, token uretir. Ara adim istemek, o tokenlarin
sirasini degistirir. Hesap veya secim sorularinda ise yarar.
Agent dongusunun yerine gecmez.
"""

from langchain_core.messages import HumanMessage

from labs.kit.models import make_chat_model


def chain_of_thought_prompt(question: str) -> str:
    """Adimlari yaz, en sonda Final: ile cevabi koy."""

    # "Step by step" ara adim ister. Tool cagrisi uretmez.

    # "step by step" ara token ister. Final: satiri cevabin yerini isaretler.
    return (
        "Think step by step. End with a line that starts with Final:.\n\n"
        f"Question: {question}"
    )


def run_chain_of_thought(question: str, model) -> str:
    # Bu cagri tool calistirmaz. Yalnizca daha uzun bir metin ister.
    message = model.invoke([HumanMessage(content=chain_of_thought_prompt(question))])
    # Donen metin hem adimlari hem Final: satirini icerir.
    return str(message.content)


def main(model=None) -> str:
    # Sayilar promptun icindedir. Model dosyayi acmaz, token uretir.
    chosen = model or make_chat_model()
    answer = run_chain_of_thought(
        "The course list has 2 python-tagged jobs and 1 of them is an intern. "
        "How many python-tagged jobs are not internships?",
        chosen,
    )
    print(answer)
    # Final: satirini kod ayirmaz. Tum metin oldugu gibi doner.
    return answer


if __name__ == "__main__":
    main()
