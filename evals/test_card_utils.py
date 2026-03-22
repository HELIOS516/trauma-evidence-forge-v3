"""Tests for card_utils.py — shared card parsing utilities."""

from card_utils import (
    split_cards,
    classify_card,
    get_title,
    count_body_words,
    count_table_words,
    count_bullets,
    extract_tables,
    has_bottom_line,
    has_sources,
    has_citations,
    title_has_verb,
)
from pathlib import Path

FILES_DIR = Path(__file__).resolve().parent / "files"


# --- split_cards ---

def test_split_cards_basic():
    content = "Card 1\n---\nCard 2\n---\nCard 3"
    cards = split_cards(content)
    assert len(cards) == 3


def test_split_cards_single():
    content = "Only one card, no separators"
    cards = split_cards(content)
    assert len(cards) == 1


# --- classify_card ---

def test_classify_title():
    card = "## Topic: An Evidence-Based Approach\n\nEvan DeCan, MD\nUVA"
    assert classify_card(card, 0, 10) == "Title"


def test_classify_disclosures():
    card = "## Disclosures\n\nFinancial Disclosures:\n- None"
    assert classify_card(card, 1, 10) == "Disclosures"


def test_classify_learning_objectives():
    card = "## Learning Objectives\n[LO: ALL]\n\n1. Identify key features"
    assert classify_card(card, 2, 10) == "Learning Objectives"


def test_classify_mcq():
    card = "## Knowledge Check: Question 1\n\nA. Option A\nB. Option B\nC. Option C\nD. Option D"
    assert classify_card(card, 5, 10) == "MCQ"


def test_classify_case():
    card = "## Opening Case\n\nA 45-year-old male presents to the ED after a fall."
    assert classify_card(card, 3, 10) == "Case"


def test_classify_data_table():
    card = "## Outcomes\n\n| Trial | N | Result |\n|---|---|---|\n| PROPPR | 680 | Reduced mortality |"
    assert classify_card(card, 5, 10) == "Data/Table"


def test_classify_guideline():
    card = "## Guideline Comparison\n\n| Society | Recommendation |\n|---|---|\n| EAST | Early TXA |"
    assert classify_card(card, 8, 10) == "Guideline"


def test_classify_references():
    card = "## References\n\n- [1] Author A. Title. Journal. 2020."
    assert classify_card(card, 9, 10) == "References"


def test_classify_content_default():
    card = "## Pathophysiology of Shock\n\nKey mechanisms include..."
    assert classify_card(card, 4, 10) == "Content"


# --- get_title ---

def test_get_title_h2():
    card = "## Hemorrhage Control\n\nBody text"
    assert get_title(card) == "Hemorrhage Control"


def test_get_title_no_heading():
    card = "Just body text, no heading"
    assert get_title(card) == "(untitled)"


# --- count_body_words ---

def test_count_body_words_excludes_tables():
    card = "## Title\n\nSome body text here.\n\n| A | B |\n|---|---|\n| 1 | 2 |"
    words = count_body_words(card)
    assert words == 4  # "Some body text here."


def test_count_body_words_excludes_headings():
    card = "## Title Heading\n\nBody text only."
    words = count_body_words(card)
    assert words == 3  # "Body text only."


def test_count_body_words_excludes_sources():
    card = "## Title\n\nBody text.\n\n**Sources:**\n- [1] Author. Journal. 2020."
    words = count_body_words(card)
    assert words == 2  # "Body text."


def test_count_body_words_excludes_blockquotes():
    card = "## Title\n\nBody text.\n\n> **Bottom Line:** This is the takeaway."
    words = count_body_words(card)
    assert words == 2  # "Body text."


# --- count_table_words ---

def test_count_table_words():
    card = "## Title\n\n| Drug | Dose | Route |\n|---|---|---|\n| TXA | 1g | IV |"
    words = count_table_words(card)
    assert words >= 3  # At least header row + data row words


# --- count_bullets ---

def test_count_bullets_basic():
    card = "## Title\n\n- Bullet one\n- Bullet two\n- Bullet three"
    assert count_bullets(card) == 3


def test_count_bullets_excludes_sources():
    card = "## Title\n\n- Point one\n- Point two\n\n- [1] Author. Journal.\n- [2] Author2. Journal2."
    assert count_bullets(card) == 2


def test_count_bullets_numbered():
    card = "## Title\n\n1. First\n2. Second\n3. Third"
    assert count_bullets(card) == 3


# --- extract_tables ---

def test_extract_tables():
    card = "## Title\n\n| A | B | C |\n|---|---|---|\n| 1 | 2 | 3 |\n| 4 | 5 | 6 |"
    tables = extract_tables(card)
    assert len(tables) == 1
    assert tables[0]['rows'] == 3  # header + 2 data rows (header row is a regular | row)
    assert tables[0]['cols'] == 3


def test_extract_no_tables():
    card = "## Title\n\nJust text, no tables."
    tables = extract_tables(card)
    assert len(tables) == 0


# --- has_bottom_line ---

def test_has_bottom_line_true():
    card = '## Title\n\nContent\n\n> **Bottom Line:** Key message here.'
    assert has_bottom_line(card) is True


def test_has_bottom_line_false():
    card = "## Title\n\nContent without bottom line."
    assert has_bottom_line(card) is False


# --- has_sources ---

def test_has_sources_block():
    card = "## Title\n\nContent\n\n**Sources:**\n- [1] Author."
    assert has_sources(card) is True


def test_has_sources_citations_only():
    card = "## Title\n\nContent\n\n- [1] Author. Journal. 2020."
    assert has_sources(card) is True


def test_has_sources_none():
    card = "## Title\n\nContent without sources."
    assert has_sources(card) is False


# --- title_has_verb ---

def test_title_assertion():
    assert title_has_verb("Permissive Hypotension Reduces Mortality in Penetrating Trauma") is True


def test_title_topic_label():
    assert title_has_verb("Pathophysiology of Hemorrhagic Shock") is False


def test_title_with_is():
    assert title_has_verb("1:1:1 Ratio Is Superior to 1:1:2 for Early Mortality") is True


# --- Fixture-based tests ---

def test_dense_fixture_word_counts():
    """Dense fixture cards should have high word counts."""
    content = (FILES_DIR / "sample_dense.md").read_text()
    cards = split_cards(content)
    # First card (Pathophysiology) should be very wordy
    body_words = count_body_words(cards[0])
    assert body_words > 150, f"Expected dense card to have >150 body words, got {body_words}"


def test_clean_fixture_word_counts():
    """Clean fixture cards should have reasonable word counts."""
    content = (FILES_DIR / "sample_clean.md").read_text()
    cards = split_cards(content)
    # First card should be concise
    body_words = count_body_words(cards[0])
    assert body_words < 130, f"Expected clean card to have <130 body words, got {body_words}"
