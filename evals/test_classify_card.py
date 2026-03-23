"""test_classify_card.py — Edge-case tests for classify_card() declarative typing."""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from card_utils import classify_card


# ---------------------------------------------------------------------------
# Helper: wrap content in a minimal card string
# ---------------------------------------------------------------------------

def card(body: str) -> str:
    return body


# ---------------------------------------------------------------------------
# Declarative type tag — all 12 valid types
# ---------------------------------------------------------------------------

def test_declarative_case():
    """<!-- type: Case --> returns 'Case' regardless of content."""
    c = "<!-- type: Case -->\n## Some Heading\nThis slide has no patient info."
    assert classify_card(c, 3, 20) == "Case"


def test_declarative_mcq():
    """<!-- type: MCQ --> returns 'MCQ' even without A/B/C/D options."""
    c = "<!-- type: MCQ -->\n## Knowledge Check\nWhat is the best management?"
    assert classify_card(c, 5, 20) == "MCQ"


def test_declarative_title():
    """<!-- type: Title --> on a non-first card still returns 'Title'."""
    c = "<!-- type: Title -->\n## Trauma Surgery 2025"
    assert classify_card(c, 4, 20) == "Title"


def test_declarative_disclosures():
    c = "<!-- type: Disclosures -->\n## Disclosures\nNothing to disclose."
    assert classify_card(c, 1, 20) == "Disclosures"


def test_declarative_learning_objectives():
    c = "<!-- type: Learning Objectives -->\n## Objectives\n- Understand trauma management"
    assert classify_card(c, 2, 20) == "Learning Objectives"


def test_declarative_content():
    """<!-- type: Content --> with table markers returns 'Content', not 'Data/Table'."""
    c = "<!-- type: Content -->\n## Overview\n| A | B |\n|---|---|\n| 1 | 2 |"
    assert classify_card(c, 3, 20) == "Content"


def test_declarative_data_table():
    c = "<!-- type: Data/Table -->\n## Outcomes\n| Col1 | Col2 |\n|---|---|\n| val | val |"
    assert classify_card(c, 4, 20) == "Data/Table"


def test_declarative_trial():
    c = "<!-- type: Trial -->\n## CRASH-3 Trial\nSome summary text."
    assert classify_card(c, 5, 20) == "Trial"


def test_declarative_guideline():
    c = "<!-- type: Guideline -->\n## EAST Guidelines\nRecommendation text."
    assert classify_card(c, 6, 20) == "Guideline"


def test_declarative_take_home():
    c = "<!-- type: Take-Home -->\n## Summary\n- Key point one\n- Key point two"
    assert classify_card(c, 10, 20) == "Take-Home"


def test_declarative_references():
    c = "<!-- type: References -->\n## References\n- [1] Smith et al. 2020"
    assert classify_card(c, 18, 20) == "References"


def test_declarative_qanda():
    c = "<!-- type: Q&A -->\n## Questions?\nThank you."
    assert classify_card(c, 19, 20) == "Q&A"


# ---------------------------------------------------------------------------
# Declarative tag overrides heuristics
# ---------------------------------------------------------------------------

def test_content_tag_overrides_question_heading():
    """<!-- type: Content --> beats 'question' in heading heuristic."""
    c = "<!-- type: Content -->\n## Question: When to operate?\nSome explanation text here."
    assert classify_card(c, 5, 20) == "Content"


def test_content_tag_overrides_patient_case_heuristic():
    """Card with patient age in body but type:Content returns 'Content'."""
    c = (
        "<!-- type: Content -->\n"
        "## Management Principles\n"
        "A 45-year-old presents with blunt trauma. This is used as an illustration."
    )
    assert classify_card(c, 4, 20) == "Content"


def test_content_tag_overrides_table_classification():
    """Type tag wins over table-based Data/Table heuristic."""
    c = (
        "<!-- type: Content -->\n"
        "## Comparison\n"
        "| Metric | Value |\n|---|---|\n| Mortality | 12% |"
    )
    assert classify_card(c, 6, 20) == "Content"


# ---------------------------------------------------------------------------
# Invalid / unknown type tag falls through to heuristics
# ---------------------------------------------------------------------------

def test_invalid_type_tag_falls_through_to_heuristic():
    """Unknown type 'Foo' falls through; card has disclosure keyword -> Disclosures."""
    c = "<!-- type: Foo -->\n## Financial Disclosures\nNothing to disclose."
    assert classify_card(c, 1, 20) == "Disclosures"


def test_unknown_type_tag_falls_through_to_case():
    """Unknown type tag; patient age + 'presents' -> Case via heuristic."""
    c = (
        "<!-- type: UnknownType -->\n"
        "## Trauma Bay\n"
        "A 30-year-old presents after MVC."
    )
    assert classify_card(c, 3, 20) == "Case"


# ---------------------------------------------------------------------------
# Backward compatibility — no type tag uses existing heuristics
# ---------------------------------------------------------------------------

def test_no_tag_first_card_is_title():
    """First card (index 0) with no tag still returns 'Title'."""
    c = "## Trauma Surgery Grand Rounds\nEvan DeCan, MD"
    assert classify_card(c, 0, 20) == "Title"


def test_no_tag_mcq_detected_by_heuristic():
    """MCQ-like content (A. B. C. D.) without tag still detected as MCQ."""
    c = (
        "## Knowledge Check\n"
        "**Question:** What is the first step?\n\n"
        "**A.** Airway\n**B.** Breathing\n**C.** Circulation\n**D.** Disability"
    )
    assert classify_card(c, 8, 20) == "MCQ"


def test_no_tag_disclosure_detected():
    c = "## Disclosures\nI have no financial conflicts of interest."
    assert classify_card(c, 1, 20) == "Disclosures"


def test_no_tag_references_detected():
    c = "## References\n- [1] Smith et al. NEJM 2020"
    assert classify_card(c, 17, 20) == "References"


# ---------------------------------------------------------------------------
# Tag must be in first 3 lines (not buried mid-card)
# ---------------------------------------------------------------------------

def test_tag_buried_after_line_3_ignored():
    """Type tag on line 4+ is not honoured; heuristics determine type."""
    c = (
        "## Patient Presentation\n"
        "A 55-year-old presents with penetrating trauma.\n"
        "Management follows ATLS.\n"
        "<!-- type: Content -->\n"
        "Additional text here."
    )
    # Heuristic: age + 'presents' -> Case
    assert classify_card(c, 3, 20) == "Case"
