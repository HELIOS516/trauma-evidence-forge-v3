"""Tests for audit_slide_design.py — design quality checks."""

from pathlib import Path
from audit_slide_design import (
    audit_presentation,
    check_d1_word_density,
    check_d2_chunking,
    check_d3_table_dimensions,
    check_d4_bottom_line,
    check_d5_citations,
    check_d6_assertion_title,
    check_d7_mcq_spacing,
    check_d8_placeholders,
    PASS, WARN, FAIL, ADVISORY,
)
from card_utils import split_cards

FILES_DIR = Path(__file__).resolve().parent / "files"


# --- D1: Word density ---

def test_d1_content_under_limit():
    card = "## Title\n\n- Short bullet one\n- Short bullet two"
    sev, _ = check_d1_word_density(card, "Content")
    assert sev == PASS


def test_d1_content_over_limit():
    card = "## Title\n\n" + " ".join(["word"] * 150)
    sev, _ = check_d1_word_density(card, "Content")
    assert sev == WARN


def test_d1_case_higher_threshold():
    card = "## Case\n\n" + " ".join(["word"] * 55)
    sev, _ = check_d1_word_density(card, "Case")
    assert sev == PASS  # 55 < 60 max for Case


def test_d1_exempt_types():
    card = "## References\n\n" + " ".join(["word"] * 500)
    sev, _ = check_d1_word_density(card, "References")
    assert sev == PASS


# --- D2: Chunking ---

def test_d2_few_bullets():
    card = "## Title\n\n- One\n- Two\n- Three"
    sev, _ = check_d2_chunking(card, "Content")
    assert sev == PASS


def test_d2_too_many_bullets():
    card = "## Title\n\n" + "\n".join([f"- Bullet {i}" for i in range(10)])
    sev, _ = check_d2_chunking(card, "Content")
    assert sev == WARN


def test_d2_case_allows_more():
    card = "## Case\n\n" + "\n".join([f"- Finding {i}" for i in range(7)])
    sev, _ = check_d2_chunking(card, "Case")
    assert sev == PASS  # 7 < 8 max for Case


# --- D3: Table dimensions ---

def test_d3_small_table():
    card = "## Title\n\n| A | B |\n|---|---|\n| 1 | 2 |\n| 3 | 4 |"
    sev, _ = check_d3_table_dimensions(card, "Content")
    assert sev == PASS


def test_d3_oversized_table():
    rows = "\n".join([f"| {'val |' * 7}" for _ in range(10)])
    card = f"## Title\n\n| {'H |' * 7}\n|{'---|' * 7}\n{rows}"
    sev, _ = check_d3_table_dimensions(card, "Content")
    assert sev == WARN


def test_d3_guideline_allows_more_rows():
    rows = "\n".join([f"| Society {i} | Rec {i} |" for i in range(9)])
    card = f"## Title\n\n| Society | Recommendation |\n|---|---|\n{rows}"
    sev, _ = check_d3_table_dimensions(card, "Guideline")
    assert sev == PASS  # 9 < 10 max for Guideline


# --- D4: Bottom Line ---

def test_d4_present():
    card = '## Title\n\nContent\n\n> **Bottom Line:** Key message.'
    sev, _ = check_d4_bottom_line(card, "Content")
    assert sev == PASS


def test_d4_missing_on_content():
    card = "## Title\n\nContent without bottom line."
    sev, _ = check_d4_bottom_line(card, "Content")
    assert sev == FAIL


def test_d4_not_required_on_title():
    card = "## Title Slide\n\nPresenter info"
    sev, _ = check_d4_bottom_line(card, "Title")
    assert sev == PASS


# --- D5: Citations ---

def test_d5_citations_with_sources():
    card = "## Title\n\nEvidence<sup>[1]</sup>\n\n**Sources:**\n- [1] Author."
    sev, _ = check_d5_citations(card, "Content")
    assert sev == PASS


def test_d5_citations_without_sources():
    card = "## Title\n\nEvidence<sup>[1]</sup> and more<sup>[2]</sup>"
    sev, _ = check_d5_citations(card, "Content")
    assert sev == WARN


# --- D6: Assertion titles ---

def test_d6_assertion_title():
    card = "## Permissive Hypotension Reduces Mortality\n\nContent"
    sev, _ = check_d6_assertion_title(card, "Content")
    assert sev == PASS


def test_d6_topic_label():
    card = "## Pathophysiology of Hemorrhagic Shock\n\nContent"
    sev, _ = check_d6_assertion_title(card, "Content")
    assert sev == ADVISORY


def test_d6_exempt_types():
    card = "## Learning Objectives\n\n1. First"
    sev, _ = check_d6_assertion_title(card, "Learning Objectives")
    assert sev == PASS


# --- D7: MCQ spacing ---

def test_d7_good_spacing():
    types = ["Title", "Disclosures", "Content", "Content", "MCQ", "Content", "Content", "MCQ"]
    gaps = check_d7_mcq_spacing([""] * len(types), types)
    assert len(gaps) == 0


def test_d7_long_gap():
    types = ["Title"] + ["Content"] * 15 + ["MCQ"]
    gaps = check_d7_mcq_spacing([""] * len(types), types)
    assert len(gaps) > 0


# --- D8: Placeholders ---

def test_d8_no_placeholders():
    card = "## Real Title\n\nReal content."
    sev, _ = check_d8_placeholders(card)
    assert sev == PASS


def test_d8_has_placeholder():
    card = "## [TOPIC]: Evidence Review\n\n[PLACEHOLDER content]"
    sev, _ = check_d8_placeholders(card)
    assert sev == FAIL


def test_d8_has_todo():
    card = "## Title\n\n[TODO: Add data here]"
    sev, _ = check_d8_placeholders(card)
    assert sev == FAIL


# --- Integration: Dense fixture ---

def test_dense_fixture_has_violations():
    content = (FILES_DIR / "sample_dense.md").read_text()
    audit = audit_presentation(content)
    # Dense fixture should have multiple warnings
    warn_count = sum(1 for c in audit["cards"] if c["severity"] in (WARN, FAIL))
    assert warn_count >= 2, f"Expected >=2 violations in dense fixture, got {warn_count}"


def test_clean_fixture_mostly_passes():
    content = (FILES_DIR / "sample_clean.md").read_text()
    audit = audit_presentation(content)
    # Clean fixture should mostly pass
    pass_count = sum(1 for c in audit["cards"] if c["severity"] == PASS)
    assert pass_count >= 3, f"Expected >=3 passes in clean fixture, got {pass_count}"
