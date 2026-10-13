"""Printed pages must contain the same source as the lab files."""

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def assert_embeds(page_name: str, lab_paths: list[str]) -> None:
    page = (ROOT / "course" / page_name).read_text(encoding="utf-8")
    for relative in lab_paths:
        source = (ROOT / relative).read_text(encoding="utf-8")
        assert html.escape(source) in page, relative


def test_ch01_page_embeds_every_lab_and_has_answers():
    assert_embeds(
        "ch01.html",
        [
            "labs/ch01/load_env.py",
            "labs/ch01/summarize_chain.py",
            "labs/ch01/read_response.py",
            "labs/ch01/swap_model.py",
            "labs/ch01/trace_chain.py",
            "labs/ch01/bullet_summary_answer.py",
        ],
    )
    page = (ROOT / "course" / "ch01.html").read_text(encoding="utf-8")
    assert page.count('class="qa"') >= 7
    assert page.count('class="answer"') >= 7
    assert "Cevap 7" in page


def test_later_chapters_embed_labs_and_answer_every_question():
    pages = {
        "ch02.html": [
            "labs/ch02/job_data.py",
            "labs/ch02/job_agent.py",
            "labs/ch02/search_corpus.py",
            "labs/ch02/structured_output.py",
            "labs/ch02/first_job_answer.py",
        ],
        "ch03.html": ["labs/ch03/react_loop.py"],
        "ch04.html": ["labs/ch04/raw_loop.py"],
        "ch05.html": ["labs/ch05/prompt_react.py"],
        "ch06.html": [
            "labs/ch06/zero_shot.py",
            "labs/ch06/few_shot.py",
            "labs/ch06/chain_of_thought.py",
            "labs/ch06/function_calling.py",
            "labs/ch06/prompt_tips.py",
            "labs/ch06/context_window.py",
        ],
        "ch07.html": [
            "labs/ch07/sandbox.py",
            "labs/ch07/mini_harness.py",
            "labs/ch07/deep_agent.py",
            "labs/ch07/review.py",
        ],
        "capstone.html": ["labs/capstone/assistant.py"],
    }
    for page_name, labs in pages.items():
        assert_embeds(page_name, labs)
        text = (ROOT / "course" / page_name).read_text(encoding="utf-8")
        assert text.count('class="qa"') >= 1
        assert text.count('class="answer"') >= text.count('class="qa"')
        assert "Cevap" in text
