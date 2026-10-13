"""The full course must print as one colorful HTML page."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_print_page_includes_every_chapter_and_colors_comments():
    from tools.build_print import build_print_html

    page = build_print_html()

    assert "LangChain Foundations" in page
    assert "Building Your First Agent" in page
    assert "Agents Under the Hood" in page
    assert "Without a Framework" in page
    assert "ReAct From Scratch" in page
    assert "Prompt and Context" in page
    assert "Deep Agents" in page
    assert "Job Assistant" in page
    assert 'class="k"' in page
    assert 'class="c"' in page
    assert 'class="s"' in page
    assert "print-color-adjust: exact" in (ROOT / "course" / "css" / "course.css").read_text(
        encoding="utf-8"
    )
    assert '<span class="c"># MODEL, ChatOllama' in page


def test_every_lab_has_several_inline_comments():
    labs = [
        path
        for path in (ROOT / "labs").rglob("*.py")
        if path.name != "__init__.py"
    ]
    thin = []
    for path in labs:
        comments = [
            line
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip().startswith("#")
        ]
        if len(comments) < 5:
            thin.append(f"{path.as_posix()} has {len(comments)}")
    assert thin == []
