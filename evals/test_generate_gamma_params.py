"""Tests for generate_gamma_params.py — group_consecutive, extract_topic, card classification.

gamma-presentation-core is an optional external dependency. Tests that require it
are skipped when it is absent.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import generate_gamma_params as ggp
from generate_gamma_params import (
    group_consecutive,
    extract_topic,
    build_api_instructions,
    strip_lo_tags,
    normalize_instruction_title,
    build_image_prompt,
    enforce_photoreal_instruction,
)
from card_utils import classify_card, split_cards


# ---------------------------------------------------------------------------
# group_consecutive
# ---------------------------------------------------------------------------

class TestGroupConsecutive:
    def test_empty(self):
        assert group_consecutive([]) == ""

    def test_single(self):
        assert group_consecutive([3]) == "3"

    def test_consecutive_range(self):
        assert group_consecutive([1, 2, 3]) == "1-3"

    def test_non_consecutive(self):
        assert group_consecutive([1, 3, 5]) == "1,3,5"

    def test_mixed(self):
        assert group_consecutive([1, 2, 3, 5, 7, 8]) == "1-3,5,7-8"

    def test_two_consecutive(self):
        assert group_consecutive([4, 5]) == "4-5"

    def test_single_gap(self):
        assert group_consecutive([1, 2, 4]) == "1-2,4"


# ---------------------------------------------------------------------------
# extract_topic
# ---------------------------------------------------------------------------

class TestExtractTopic:
    def test_basic_heading(self):
        cards = ['## DVT Prophylaxis in Trauma\nContent here']
        assert extract_topic(cards) == 'DVT Prophylaxis in Trauma'

    def test_skips_disclosures(self):
        cards = [
            '## Disclosures\nNo conflicts',
            '## DVT Prophylaxis\nContent',
        ]
        assert extract_topic(cards) == 'DVT Prophylaxis'

    def test_skips_learning_objectives(self):
        cards = [
            '## Learning Objectives\nAfter this...',
            '## The VTE Problem\nContent',
        ]
        assert extract_topic(cards) == 'The VTE Problem'

    def test_empty_cards_returns_default(self):
        assert extract_topic([]) == 'Medical Presentation'

    def test_all_skipped_returns_default(self):
        cards = ['## Disclosures\nNone', '## Learning Objectives\nList']
        assert extract_topic(cards) == 'Medical Presentation'

    def test_no_h2_heading_returns_default(self):
        cards = ['Just text without heading']
        assert extract_topic(cards) == 'Medical Presentation'


# ---------------------------------------------------------------------------
# build_api_instructions
# ---------------------------------------------------------------------------

class TestBuildApiInstructions:
    def test_truncates_to_2000(self):
        # Many slides of the same type should still truncate
        card_types = [(i, 'Content') for i in range(1, 200)]
        result = build_api_instructions(card_types)
        assert len(result) <= 2000

    def test_includes_slide_type_label(self):
        card_types = [(1, 'Title'), (2, 'Content')]
        result = build_api_instructions(card_types)
        assert 'Title' in result
        assert 'Content' in result

    def test_groups_consecutive_slides(self):
        card_types = [(1, 'Content'), (2, 'Content'), (3, 'Content')]
        result = build_api_instructions(card_types)
        assert 'Slides 1-3' in result

    def test_single_slide_label(self):
        card_types = [(1, 'Title')]
        result = build_api_instructions(card_types)
        assert 'Slide 1' in result

    def test_global_rule_appended(self):
        card_types = [(1, 'Content')]
        result = build_api_instructions(card_types)
        assert 'GLOBAL' in result


# ---------------------------------------------------------------------------
# strip_lo_tags / normalize_instruction_title
# ---------------------------------------------------------------------------

class TestStripLoTags:
    def test_removes_lo_tag(self):
        assert strip_lo_tags('Title Text [LO: 1, 2]') == 'Title Text'

    def test_no_tag_unchanged(self):
        assert strip_lo_tags('Plain Title') == 'Plain Title'


class TestNormalizeInstructionTitle:
    def test_truncates_to_140(self):
        long_title = 'A' * 200
        result = normalize_instruction_title(long_title)
        assert len(result) <= 140

    def test_strips_pipe_suffix(self):
        result = normalize_instruction_title('Title | Extra stuff')
        assert result == 'Title'

    def test_strips_bold_suffix(self):
        result = normalize_instruction_title('Title **bold')
        assert result == 'Title'


# ---------------------------------------------------------------------------
# build_image_prompt
# ---------------------------------------------------------------------------

class TestBuildImagePrompt:
    def test_no_image_for_disclosures(self):
        assert build_image_prompt('Disclosures', 'Disclosures') == 'NO_IMAGE'

    def test_no_image_for_references(self):
        assert build_image_prompt('References', 'References') == 'NO_IMAGE'

    def test_no_image_for_learning_objectives(self):
        assert build_image_prompt('Learning Objectives', 'Learning Objectives') == 'NO_IMAGE'

    def test_data_table_background_only(self):
        result = build_image_prompt('Outcome Data', 'Data/Table')
        assert result.startswith('NO_IMAGE')

    def test_content_card_has_prompt(self):
        result = build_image_prompt('DVT Prophylaxis', 'Content')
        assert 'NO_IMAGE' not in result
        assert 'photoreal' in result.lower() or 'clinical' in result.lower()

    def test_case_card_uses_trauma_imagery(self):
        result = build_image_prompt('Case Presentation', 'Case')
        assert 'trauma' in result.lower() or 'clinical' in result.lower()

    def test_qa_card_conference_scene(self):
        result = build_image_prompt('Questions?', 'Q&A')
        assert 'conference' in result.lower() or 'podium' in result.lower()


# ---------------------------------------------------------------------------
# enforce_photoreal_instruction
# ---------------------------------------------------------------------------

class TestEnforcePhotorealInstruction:
    def test_non_photoreal_tokens_replaced_for_content(self):
        instruction = 'Use a diagram to explain the flowchart.'
        result = enforce_photoreal_instruction('Content', instruction)
        # Original instruction is replaced; the replacement contains 'photoreal'
        # (replacement may mention 'diagrams' in a "no diagrams" exclusion clause)
        assert result != instruction
        assert 'photoreal' in result.lower()

    def test_exempt_types_unchanged(self):
        instruction = 'Use a flowchart illustration.'
        result = enforce_photoreal_instruction('Disclosures', instruction)
        assert result == instruction

    def test_clean_instruction_unchanged(self):
        instruction = 'Use photoreal clinical imagery.'
        result = enforce_photoreal_instruction('Content', instruction)
        assert result == instruction

    def test_case_card_photoreal_replacement(self):
        instruction = 'Show an anatomical illustration.'
        result = enforce_photoreal_instruction('Case', instruction)
        # Original instruction is replaced with a photoreal version
        assert result != instruction
        assert 'photoreal' in result.lower()


# ---------------------------------------------------------------------------
# Card classification via card_utils (used by generate_gamma_params)
# ---------------------------------------------------------------------------

class TestCardClassification:
    def test_first_card_is_title(self):
        card = '## DVT Prophylaxis\nPresenter Name'
        assert classify_card(card, 0, 10) == 'Title'

    def test_disclosures_card(self):
        card = '## Financial Disclosures\nNone to report.'
        assert classify_card(card, 1, 10) == 'Disclosures'

    def test_learning_objectives_card(self):
        card = '## Learning Objectives\n1. Identify risks'
        assert classify_card(card, 1, 10) == 'Learning Objectives'

    def test_references_card(self):
        card = '## References\n1. Author. Title. PMID: 12345678'
        assert classify_card(card, 9, 10) == 'References'

    def test_content_card_default(self):
        card = '## DVT Pathophysiology\nContent about thrombosis.'
        # Not title, not disclosure, not objectives — should be Content or another type
        result = classify_card(card, 2, 10)
        assert result in {'Content', 'Data/Table', 'Trial', 'Guideline', 'Case', 'MCQ',
                          'Take-Home', 'Future Directions', 'Learning Objectives'}
