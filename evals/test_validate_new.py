"""Tests for new validation checks 11-17 in validate_gamma_ready.py."""

from validate_gamma_ready import (
    check_word_density,
    check_bullet_count,
    check_table_dimensions,
    check_bottom_line_presence,
    check_sources_on_evidence,
    check_assertion_titles,
    check_unfilled_placeholders,
)

# Title card prefix — ensures test content cards are at index 1+
# so classify_card doesn't auto-label them as "Title" (index 0).
_TITLE = "## Presentation Title\n\nPresenter Name\n\n---\n\n"


# --- Check 11: Word density ---

def test_word_density_clean():
    content = _TITLE + "## Content Slide\n\n- Short point\n- Another point\n\n> **Bottom Line:** Key message."
    ok, _ = check_word_density(content)
    assert ok is True  # Soft check always returns True


def test_word_density_dense():
    content = _TITLE + "## Content Slide\n\n" + " ".join(["word"] * 200) + "\n\n> **Bottom Line:** Message."
    ok, msg = check_word_density(content)
    assert ok is True  # Soft check
    assert "body words" in msg or "WARN" in msg or "word" in msg.lower()


# --- Check 12: Bullet count ---

def test_bullet_count_ok():
    content = _TITLE + "## Content Slide\n\n- One\n- Two\n- Three\n\n> **Bottom Line:** Key message."
    ok, _ = check_bullet_count(content)
    assert ok is True


def test_bullet_count_too_many():
    bullets = "\n".join([f"- Bullet {i}" for i in range(12)])
    content = _TITLE + f"## Content Slide\n\n{bullets}\n\n> **Bottom Line:** Key message."
    ok, msg = check_bullet_count(content)
    assert ok is True  # Soft check
    assert "bullet" in msg.lower()


# --- Check 13: Table dimensions ---

def test_table_dimensions_ok():
    content = _TITLE + "## Content Slide\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n> **Bottom Line:** Key message."
    ok, _ = check_table_dimensions(content)
    assert ok is True


def test_table_dimensions_oversized():
    rows = "\n".join([f"| {'cell |' * 7}" for _ in range(12)])
    content = _TITLE + f"## Content Slide\n\n| {'H |' * 7}\n|{'---|' * 7}\n{rows}\n\n> **Bottom Line:** Key."
    ok, msg = check_table_dimensions(content)
    assert ok is True  # Soft check
    assert "table" in msg.lower() or "row" in msg.lower() or "col" in msg.lower()


# --- Check 14: Bottom Line presence (HARD gate) ---

def test_bottom_line_present():
    content = _TITLE + "## Slide A\n\n- Point\n\n> **Bottom Line:** Key message.\n\n---\n\n## Slide B\n\n- Data\n\n> **Bottom Line:** Another."
    ok, _ = check_bottom_line_presence(content)
    assert ok is True


def test_bottom_line_missing():
    content = _TITLE + "## Content Slide\n\nContent without bottom line."
    ok, msg = check_bottom_line_presence(content)
    assert ok is False
    assert "missing" in msg.lower() or "Bottom Line" in msg


# --- Check 15: Sources on evidence ---

def test_sources_present_with_citations():
    content = _TITLE + "## Evidence Slide\n\nEvidence<sup>[1]</sup>\n\n**Sources:**\n- [1] Author.\n\n> **Bottom Line:** Key."
    ok, _ = check_sources_on_evidence(content)
    assert ok is True


def test_sources_missing_with_citations():
    content = _TITLE + "## Evidence Slide\n\nEvidence<sup>[1]</sup> and more<sup>[2]</sup>\n\n> **Bottom Line:** Key."
    ok, msg = check_sources_on_evidence(content)
    assert ok is True  # Soft check
    assert "citation" in msg.lower() or "source" in msg.lower()


# --- Check 16: Assertion titles ---

def test_assertion_title_present():
    content = _TITLE + "## Permissive Hypotension Reduces Mortality\n\n- Point\n\n> **Bottom Line:** Key."
    ok, _ = check_assertion_titles(content)
    assert ok is True


def test_topic_label_title():
    content = _TITLE + "## Pathophysiology of Hemorrhagic Shock\n\n- Point\n\n> **Bottom Line:** Key."
    ok, msg = check_assertion_titles(content)
    assert ok is True  # Soft check
    assert "topic" in msg.lower() or "verb" in msg.lower() or "assertion" in msg.lower()


# --- Check 17: Unfilled placeholders (HARD gate) ---

def test_no_placeholders():
    content = "## Real Title\n\nReal content with details."
    ok, _ = check_unfilled_placeholders(content)
    assert ok is True


def test_has_placeholders():
    content = "## [TOPIC]: Evidence Review\n\n[PLACEHOLDER content]\n\n[TODO: finish this]"
    ok, msg = check_unfilled_placeholders(content)
    assert ok is False
    assert "unfilled" in msg.lower() or "placeholder" in msg.lower()
