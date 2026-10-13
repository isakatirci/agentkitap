"""Python kaynak metnini yazdirmada renkli duran HTML span'lerine cevirir.

Renkler arka plan degil, yazi rengidir. Tarayici arka plan grafiklerini
kapatsa bile keyword, string ve comment ayirt edilir.
"""

import html

# Python anahtar kelimeleri. Bunlar komutun iskeletidir, isim degildir.
KEYWORDS = {
    "False",
    "None",
    "True",
    "and",
    "as",
    "assert",
    "async",
    "await",
    "break",
    "class",
    "continue",
    "def",
    "del",
    "elif",
    "else",
    "except",
    "finally",
    "for",
    "from",
    "global",
    "if",
    "import",
    "in",
    "is",
    "lambda",
    "nonlocal",
    "not",
    "or",
    "pass",
    "raise",
    "return",
    "try",
    "while",
    "with",
    "yield",
}


def _span(kind: str, text: str) -> str:
    return f'<span class="{kind}">{html.escape(text)}</span>'


def highlight_python(source: str) -> str:
    """Kaynak metni oldugu gibi tarar. String icindeki # comment sayilmaz."""

    parts: list[str] = []
    index = 0
    length = len(source)
    while index < length:
        chunk = _take_comment(source, index)
        if chunk is None:
            chunk = _take_string(source, index)
        if chunk is None:
            chunk = _take_number(source, index)
        if chunk is None:
            chunk = _take_word(source, index)
        if chunk is None:
            parts.append(html.escape(source[index]))
            index += 1
            continue
        parts.append(chunk[0])
        index = chunk[1]
    return "".join(parts)


def _take_comment(source: str, index: int) -> tuple[str, int] | None:
    if source[index] != "#":
        return None
    end = source.find("\n", index)
    if end == -1:
        end = len(source)
    # Satir sonu span disinda kalir ki HTML kaynagi bozulmasin.
    return _span("c", source[index:end]), end


def _take_string(source: str, index: int) -> tuple[str, int] | None:
    start = index
    while index < len(source) and source[index] in "rRfFbBuU":
        index += 1
    if index >= len(source) or source[index] not in "\"'":
        return None
    if index > start and not source[start:index].lower() in {
        "r",
        "f",
        "b",
        "u",
        "rf",
        "fr",
        "rb",
        "br",
    }:
        return None
    quote = source[index]
    if source.startswith(quote * 3, index):
        marker = quote * 3
    else:
        marker = quote
    cursor = index + len(marker)
    while cursor < len(source):
        if source.startswith(marker, cursor):
            cursor += len(marker)
            kind = "d" if marker == quote * 3 else "s"
            return _span(kind, source[start:cursor]), cursor
        if source[cursor] == "\\" and marker == quote:
            cursor += 2
            continue
        cursor += 1
    kind = "d" if len(marker) == 3 else "s"
    return _span(kind, source[start:]), len(source)


def _take_number(source: str, index: int) -> tuple[str, int] | None:
    if not source[index].isdigit():
        return None
    cursor = index + 1
    while cursor < len(source) and (source[cursor].isdigit() or source[cursor] == "."):
        cursor += 1
    return _span("n", source[index:cursor]), cursor


def _take_word(source: str, index: int) -> tuple[str, int] | None:
    if not (source[index].isalpha() or source[index] == "_"):
        return None
    cursor = index + 1
    while cursor < len(source) and (source[cursor].isalnum() or source[cursor] == "_"):
        cursor += 1
    word = source[index:cursor]
    if word in KEYWORDS:
        return _span("k", word), cursor
    return html.escape(word), cursor
