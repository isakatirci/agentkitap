"""Tum kursu tek yazdirilabilir HTML sayfasinda birlestirir.

Kod bloklari labs dosyasindan yeniden okunur ve renklendirilir.
Boylece basilan kod, calisan dosyanin guncel halidir.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.highlight import highlight_python
COURSE = ROOT / "course"
PAGES = [
    "index.html",
    "ch01.html",
    "ch02.html",
    "ch03.html",
    "ch04.html",
    "ch05.html",
    "ch06.html",
    "ch07.html",
    "capstone.html",
    "glossary.html",
]
MAIN = re.compile(r"<main>(.*)</main>", re.DOTALL)
LAB = re.compile(r'<pre><code data-lab="([^"]+)">.*?</code></pre>', re.DOTALL)


def _highlight_labs(html_text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        relative = match.group(1)
        source = (ROOT / relative).read_text(encoding="utf-8")
        # Renk span'leri yazi rengidir; yorumlar .c, aciklamalar .d olur.
        colored = highlight_python(source)
        return f'<pre class="py"><code>{colored}</code></pre>'

    return LAB.sub(replace, html_text)


def build_print_html() -> str:
    """Kapak, yedi bolum, capstone ve glossary tek main icinde."""

    sections: list[str] = []
    for name in PAGES:
        page = (COURSE / name).read_text(encoding="utf-8")
        main = MAIN.search(page)
        if main is None:
            raise RuntimeError(f"{name} has no main element")
        sections.append(_highlight_labs(main.group(1).strip()))
    body = "\n".join(sections)
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="utf-8">
  <title>LangChain Agent Kursu — yazdir</title>
  <link rel="stylesheet" href="css/course.css">
</head>
<body>
<nav class="no-print">
  <a href="index.html">Kurs</a>
  <a href="print.html">Tek sayfa</a>
</nav>
<main>
{body}
</main>
</body>
</html>
"""


def main() -> None:
    target = COURSE / "print.html"
    target.write_text(build_print_html(), encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
