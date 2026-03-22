"""Tests for format_references.py — extract_references, check_format, check_duplicates."""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from format_references import extract_references, check_format, check_duplicates


class TestExtractReferences:
    def test_bracket_format(self):
        text = '## References\n[1] Smith J. Title. J Surg. 2020. PMID: 12345678\n'
        refs = extract_references(text)
        assert len(refs) == 1
        assert refs[0]['number'] == 1
        assert refs[0]['has_pmid'] is True

    def test_numbered_dot_format(self):
        text = '# References\n1. Smith J. Title. J Surg. 2020. PMID: 12345678\n'
        refs = extract_references(text)
        assert len(refs) == 1
        assert refs[0]['number'] == 1

    def test_multiple_refs_sorted(self):
        text = (
            '## References\n'
            '2. Author B. Title B. J Surg. 2021. DOI: 10.1016/x\n'
            '1. Author A. Title A. J Med. 2020. PMID: 12345678\n'
        )
        refs = extract_references(text)
        assert refs[0]['number'] == 1
        assert refs[1]['number'] == 2

    def test_no_references_section(self):
        assert extract_references('No refs here.') == []

    def test_has_doi_flag(self):
        text = '## References\n1. Author. Title. J Surg. 2020. doi.org/10.1016/x\n'
        refs = extract_references(text)
        assert refs[0]['has_doi'] is True

    def test_ignores_blank_lines(self):
        text = '## References\n\n1. Author. Title. J Surg. 2020. PMID: 12345678\n\n'
        refs = extract_references(text)
        assert len(refs) == 1

    def test_stops_at_next_heading(self):
        text = '## References\n1. Author. Title. J Surg. 2020. PMID: 12345678\n## Appendix\nExtra\n'
        refs = extract_references(text)
        assert len(refs) == 1


class TestCheckFormat:
    def test_passes_correct_refs(self):
        refs = [
            {'number': 1, 'text': 'Smith J. Title. J Surg. 2020.', 'has_pmid': True, 'has_doi': False},
            {'number': 2, 'text': 'Jones A. Study. Ann Med. 2021.', 'has_pmid': False, 'has_doi': True},
        ]
        issues = check_format(refs)
        assert issues == []

    def test_detects_missing_identifier(self):
        refs = [
            {'number': 1, 'text': 'Smith J. Title. J Surg. 2020.', 'has_pmid': False, 'has_doi': False},
        ]
        issues = check_format(refs)
        issue_msgs = [i['issue'] for i in issues]
        assert any('Missing PMID' in m for m in issue_msgs)

    def test_detects_sequence_gap(self):
        refs = [
            {'number': 1, 'text': 'Author A. Title. J Surg. 2020.', 'has_pmid': True, 'has_doi': False},
            {'number': 3, 'text': 'Author C. Title. J Med. 2022.', 'has_pmid': True, 'has_doi': False},
        ]
        issues = check_format(refs)
        issue_nums = [i['ref'] for i in issues]
        assert 3 in issue_nums


class TestCheckDuplicates:
    def test_no_duplicates(self):
        refs = [
            {'number': 1, 'text': 'Author A. Title. PMID: 11111111'},
            {'number': 2, 'text': 'Author B. Title. PMID: 22222222'},
        ]
        assert check_duplicates(refs) == []

    def test_detects_duplicate_pmid(self):
        refs = [
            {'number': 1, 'text': 'Author A. Title. PMID: 12345678'},
            {'number': 2, 'text': 'Author B. Title. PMID: 12345678'},
        ]
        dupes = check_duplicates(refs)
        assert len(dupes) == 1
        assert dupes[0]['pmid'] == '12345678'
        assert 1 in dupes[0]['refs']
        assert 2 in dupes[0]['refs']

    def test_no_pmid_refs_ignored(self):
        refs = [
            {'number': 1, 'text': 'Author A. Title. DOI: 10.1016/x'},
            {'number': 2, 'text': 'Author B. Title. DOI: 10.1016/y'},
        ]
        assert check_duplicates(refs) == []

    def test_three_refs_two_with_same_pmid(self):
        refs = [
            {'number': 1, 'text': 'Author A. PMID: 99999999'},
            {'number': 2, 'text': 'Author B. PMID: 11111111'},
            {'number': 3, 'text': 'Author C. PMID: 99999999'},
        ]
        dupes = check_duplicates(refs)
        assert len(dupes) == 1
        assert dupes[0]['pmid'] == '99999999'
