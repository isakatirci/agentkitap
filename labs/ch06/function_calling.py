"""Function calling neden ReAct metninin yerini aldi.

ReAct prompt'u modelden Action: satiri yazmasini ister. Satir bozulursa
regex kirilir. Function calling ayni istegi JSON schema ile gonderir.
Model tool_calls alanini doldurur. Ayrıştırma kutuphaneye kalir.
"""

from labs.ch04.raw_loop import search_jobs_schema


def react_shape() -> str:
    """Eski duz metin sekli. Insan okur, regex ayirir."""

    # Insan bu satirlari okur. Regex Action ve Action Input'u ayirir.
    return 'Thought: look\nAction: search_jobs\nAction Input: {"keyword": "python"}'


def function_schema() -> dict:
    """Ayni tool'un makine okur hali. Chapter 4 semasinin aynisidir."""

    # Ayni tool'un makineye giden hali. Ad, parameters icinde keyword olur.
    return search_jobs_schema()


def why_function_calling_replaced_react() -> str:
    """Kisa karsilastirma. Ders metni kodun icinde de dursun."""

    # Kirilgan satir ile JSON schema arasindaki odun. Tip kontrolu durur.
    return (
        "ReAct text can break when the model adds an extra sentence. "
        "Function calling sends a JSON schema and reads tool_calls. "
        "The tradeoff: you need a model that supports tool calling, "
        "and you still must check argument types."
    )


def main() -> str:
    # Once eski sekli, sonra semadaki tool adini bas.
    print(react_shape())
    print(function_schema()["function"]["name"])
    text = why_function_calling_replaced_react()
    # Karsilastirma cumlesi hem ekrana hem teste gider.
    print(text)
    return text


if __name__ == "__main__":
    main()
