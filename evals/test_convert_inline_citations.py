"""Tests for convert_inline_citations.py."""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from convert_inline_citations import (
    extract_citations,
    dedup_key,
    assign_numbers,
    convert_citations,
    _add_per_slide_sources,
)


class TestExtractCitations:
    def test_author_year_pmid(self):
        text = '(Smith et al., 2020; PMID: 12345678)'
        cites = extract_citations(text)
        assert len(cites) == 1
        assert cites[0]['pmid'] == '12345678'
        assert cites[0]['author'] == 'Smith et al.'
        assert cites[0]['year'] == '2020'

    def test_author_year_doi(self):
        text = '(Jones, 2021; DOI: 10.1016/j.jss.2021.01.001)'
        cites = extract_citations(text)
        assert len(cites) == 1
        assert cites[0]['doi'] == '10.1016/j.jss.2021.01.001'
        assert cites[0]['pmid'] is None

    def test_author_year_only(self):
        text = '(Brown et al., 2019)'
        cites = extract_citations(text)
        assert len(cites) == 1
        assert cites[0]['pmid'] is None
        assert cites[0]['doi'] is None

    def test_multiple_citations(self):
        text = 'Rate was 30% (Smith et al., 2020; PMID: 12345678) and 50% (Jones, 2021; PMID: 87654321)'
        cites = extract_citations(text)
        assert len(cites) == 2

    def test_no_citations(self):
        assert extract_citations('No citations here.') == []

    def test_no_overlapping_spans(self):
        # Same citation matched by multiple patterns should only appear once
        text = '(Smith et al., 2020; PMID: 12345678)'
        cites = extract_citations(text)
        assert len(cites) == 1

    def test_sorted_by_position(self):
        text = '(Jones, 2021; PMID: 11111111) then (Smith, 2020; PMID: 22222222)'
        cites = extract_citations(text)
        assert cites[0]['pmid'] == '11111111'
        assert cites[1]['pmid'] == '22222222'


class TestDedupKey:
    def test_pmid_key(self):
        cite = {'pmid': '12345678', 'doi': None, 'author': 'Smith', 'year': '2020'}
        assert dedup_key(cite) == 'pmid:12345678'

    def test_author_year_key_when_no_pmid(self):
        cite = {'pmid': None, 'doi': '10.1016/x', 'author': 'Smith', 'year': '2020'}
        assert dedup_key(cite) == 'smith:2020'

    def test_case_insensitive(self):
        cite = {'pmid': None, 'doi': None, 'author': 'JONES', 'year': '2019'}
        assert dedup_key(cite) == 'jones:2019'


class TestAssignNumbers:
    def test_sequential_unique(self):
        cites = [
            {'pmid': '111', 'doi': None, 'author': 'A', 'year': '2020'},
            {'pmid': '222', 'doi': None, 'author': 'B', 'year': '2021'},
        ]
        mapping = assign_numbers(cites)
        assert mapping['pmid:111'] == 1
        assert mapping['pmid:222'] == 2

    def test_deduplication(self):
        cites = [
            {'pmid': '111', 'doi': None, 'author': 'A', 'year': '2020'},
            {'pmid': '111', 'doi': None, 'author': 'A', 'year': '2020'},  # duplicate
        ]
        mapping = assign_numbers(cites)
        assert len(mapping) == 1
        assert mapping['pmid:111'] == 1


class TestConvertCitations:
    def test_converts_to_numbered(self):
        text = 'Found (Smith et al., 2020; PMID: 12345678) effective.'
        result, unique, replacements = convert_citations(text)
        assert '[1]' in result
        assert '(Smith' not in result
        assert unique == 1
        assert replacements == 1

    def test_no_citations_unchanged(self):
        text = 'No citations here.'
        result, unique, replacements = convert_citations(text)
        assert result == text
        assert unique == 0
        assert replacements == 0

    def test_deduplicates_same_pmid(self):
        text = '(Smith, 2020; PMID: 12345678) again (Smith, 2020; PMID: 12345678)'
        result, unique, replacements = convert_citations(text)
        assert unique == 1
        assert replacements == 2
        # [1] appears in body (x2), Sources block, and References — at least 2 occurrences
        assert result.count('[1]') >= 2

    def test_adds_references_section(self):
        text = 'Text (Smith, 2020; PMID: 12345678).'
        result, _, _ = convert_citations(text)
        assert '## References' in result
        assert 'PMID: 12345678' in result

    def test_multiple_unique_citations_numbered_in_order(self):
        text = 'A (Alpha, 2020; PMID: 11111111) then B (Beta, 2021; PMID: 22222222).'
        result, unique, _ = convert_citations(text)
        assert unique == 2
        pos1 = result.find('[1]')
        pos2 = result.find('[2]')
        assert pos1 < pos2


class TestAddPerSlideSource:
    def test_adds_sources_to_card_with_citations(self):
        content = 'Card with [1] and [2] citations.'
        result = _add_per_slide_sources(content)
        assert '**Sources:**' in result
        assert '[1]' in result
        assert '[2]' in result

    def test_no_sources_added_when_no_citations(self):
        content = 'Card with no citation numbers.'
        result = _add_per_slide_sources(content)
        assert '**Sources:**' not in result

    def test_no_duplicate_sources_block(self):
        content = 'Card [1].\n\n**Sources:** [1]\n'
        result = _add_per_slide_sources(content)
        assert result.count('**Sources:**') == 1

    def test_multiple_cards(self):
        content = 'Card A [1].\n---\nCard B [2].'
        result = _add_per_slide_sources(content)
        cards = result.split('\n---\n')
        assert '**Sources:** [1]' in cards[0]
        assert '**Sources:** [2]' in cards[1]
