"""Ders HTML dosyalarindaki EMBED isaretlerini lab kaynagina cevirir.

Isaret bir kez gercek koda donusur. Sayfa bundan sonra tek basina acilir.
"""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = re.compile(r"<!-- EMBED:(.+?) -->")


def fill(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        relative = match.group(1).strip()
        source = (ROOT / relative).read_text(encoding="utf-8")
        # < ve & HTML'de bozulmasin diye kacilir. Test ayni kacisi arar.
        return "<pre><code>" + html.escape(source) + "</code></pre>"

    return MARKER.sub(replace, text)


def refresh_tagged(text: str) -> str:
    """data-lab isaretli bloklari guncel dosyayla degistirir."""

    pattern = re.compile(
        r'<pre><code data-lab="([^"]+)">.*?</code></pre>',
        re.DOTALL,
    )

    def replace(match: re.Match[str]) -> str:
        relative = match.group(1)
        source = (ROOT / relative).read_text(encoding="utf-8")
        return f'<pre><code data-lab="{relative}">' + html.escape(source) + "</code></pre>"

    return pattern.sub(replace, text)


def main() -> None:
    for page in (ROOT / "course").glob("*.html"):
        original = page.read_text(encoding="utf-8")
        filled = refresh_tagged(fill(original))
        if filled != original:
            page.write_text(filled, encoding="utf-8")
            print(page.name)


if __name__ == "__main__":
    main()
