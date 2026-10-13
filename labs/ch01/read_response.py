"""Model cevabini nesne olarak okumak.

Junior'lar siklikla print(response) yapip tum nesneyi cumle sanir.
Asil metin content alanindadir. tool_calls bos ise model arac istememis demektir.
"""

from langchain_core.messages import AIMessage


def describe_response(message: AIMessage) -> dict:
    """AIMessage icinden junior'in bakacagi uc alani cikarir.

    type: mesajin rolu. Model cevabinda bu deger "ai" olur.
    content: kullaniciya gosterilecek metin.
    tool_calls: model bir tool istiyorsa burasi dolu olur. Chapter 2'de kullanilir.
    """

    return {
        "type": message.type,
        "content": message.content,
        "tool_calls": list(message.tool_calls),
    }


def main() -> dict:
    """Elle kurulmus bir AIMessage ile alanlari yazdirir.

    Bu dosya modele gitmez. Amac, response nesnesinin şeklini gormektir.
    """

    sample = AIMessage(content="Python is beginner friendly.", tool_calls=[])
    info = describe_response(sample)
    print(info)
    return info


if __name__ == "__main__":
    main()
