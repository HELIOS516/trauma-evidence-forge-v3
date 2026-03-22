"""Tests for verify_citations.py — PMID extraction, DOI validation, orphan/duplicate detection."""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from verify_citations import (
    extract_pmid,
    extract_doi,
    extract_body_citations,
    extract_references,
    validate_doi,
    verify,
    cross_check_citations,
)


class TestExtractPmid:
    def test_standard_colon_space(self):
        assert extract_pmid('PMID: 12345678') == '12345678'

    def test_no_space(self):
        assert extract_pmid('PMID:12345678') == '12345678'

    def test_space_no_colon(self):
        assert extract_pmid('PMID 12345678') == '12345678'

    def test_7_digit(self):
        assert extract_pmid('PMID: 1234567') == '1234567'

    def test_8_digit(self):
        assert extract_pmid('PMID: 40492307') == '40492307'

    def test_6_digit_rejected(self):
        # 6-digit PMIDs should NOT match (standardized to \d{7,8})
        assert extract_pmid('PMID: 123456') is None

    def test_9_digit_not_fully_matched(self):
        # \d{7,8} matches the first 8 digits of a 9-digit string — result is first 8 chars
        # This documents actual regex behavior (greedy leftmost match)
        result = extract_pmid('PMID: 123456789')
        assert result == '12345678'  # matches first 8 digits

    def test_no_pmid(self):
        assert extract_pmid('No identifier here') is None

    def test_in_full_reference(self):
        ref = '- Kerwin AJ, et al. Ann Surg. 2025;282(3):382-388. PMID: 40492307 [4]'
        assert extract_pmid(ref) == '40492307'


class TestExtractDoi:
    def test_doi_prefix(self):
        doi = extract_doi('DOI: 10.1016/j.jss.2024.01.001')
        assert doi == '10.1016/j.jss.2024.01.001'

    def test_doi_lowercase(self):
        doi = extract_doi('doi: 10.1001/jamasurg.2024.1234')
        assert doi == '10.1001/jamasurg.2024.1234'

    def test_doi_url(self):
        doi = extract_doi('https://doi.org/10.1097/SLA.0000000000005123')
        assert doi == '10.1097/SLA.0000000000005123'

    def test_no_doi(self):
        assert extract_doi('No DOI here, just text') is None


class TestValidateDoi:
    def test_valid_doi(self):
        assert validate_doi('10.1016/j.jss.2024.01.001') is True

    def test_valid_doi_with_parens(self):
        assert validate_doi('10.1002/bjs.1234(2024)') is True

    def test_invalid_doi_wrong_prefix(self):
        assert validate_doi('11.1016/j.jss.2024.01.001') is False

    def test_invalid_doi_null_byte(self):
        # Null bytes and non-ASCII should be rejected
        assert validate_doi('10.1016/j.jss\x00evil') is False

    def test_invalid_doi_spaces(self):
        assert validate_doi('10.1016/j.jss 2024') is False

    def test_invalid_doi_empty(self):
        assert validate_doi('') is False

    def test_invalid_doi_shell_injection(self):
        # Semicolons are excluded from allowed chars to prevent shell injection
        assert validate_doi('10.1016/j.jss;rm') is False


class TestExtractBodyCitations:
    def test_basic(self):
        content = 'Results showed [1] and [2] improvements.\n# References\n'
        result = extract_body_citations(content)
        assert result == {'1', '2'}

    def test_ignores_references_section(self):
        content = 'Body [1].\n# References\n[1] Some paper [1]\n[2] Another [2]\n'
        result = extract_body_citations(content)
        assert result == {'1'}

    def test_no_citations(self):
        assert extract_body_citations('No citations here.') == set()


class TestExtractReferences:
    def test_bracket_format(self):
        content = '# References\n- Author. Title. PMID: 12345678 [1]\n'
        refs = extract_references(content)
        assert '1' in refs

    def test_numbered_list_format(self):
        content = '# References\n1. Author. Title. PMID: 12345678\n'
        refs = extract_references(content)
        assert '1' in refs

    def test_dash_bracket_format(self):
        content = '# References\n- [1] Author. Title. PMID: 12345678\n'
        refs = extract_references(content)
        assert '1' in refs

    def test_no_references_section(self):
        assert extract_references('No references here.') == {}


class TestVerify:
    SAMPLE = (
        'Body cites [1] and [2].\n'
        '# References\n'
        '- Author A. Title A. PMID: 12345678 [1]\n'
        '- Author B. Title B. DOI: 10.1016/j.jss.2024.01.001 [2]\n'
    )

    def test_pass_all_verified(self):
        report = verify(self.SAMPLE)
        text = '\n'.join(report)
        assert 'PASS' in text

    def test_detects_missing_pmid_and_doi(self):
        content = (
            'Body [1].\n'
            '# References\n'
            '- Author. Title. [1]\n'
        )
        report = verify(content)
        text = '\n'.join(report)
        assert '[NEEDS VERIFICATION]' in text

    def test_detects_orphan_citation(self):
        content = (
            'Body [1] and [3].\n'
            '# References\n'
            '- Author A. PMID: 12345678 [1]\n'
            '- Author B. PMID: 87654321 [2]\n'
        )
        report = verify(content)
        text = '\n'.join(report)
        assert '[ORPHAN CITATION]' in text
        assert '3' in text

    def test_detects_duplicate_pmid(self):
        content = (
            'Body [1] and [2].\n'
            '# References\n'
            '- Author A. PMID: 12345678 [1]\n'
            '- Author B. PMID: 12345678 [2]\n'
        )
        report = verify(content)
        text = '\n'.join(report)
        assert '[DUPLICATE PMID]' in text

    def test_detects_uncited_reference(self):
        content = (
            'Body [1].\n'
            '# References\n'
            '- Author A. PMID: 12345678 [1]\n'
            '- Author B. PMID: 87654321 [2]\n'
        )
        report = verify(content)
        text = '\n'.join(report)
        assert '[UNCITED REFERENCE]' in text

    def test_no_references_section(self):
        report = verify('Just body text [1] [2].')
        text = '\n'.join(report)
        assert 'WARNING' in text

    def test_doi_url_in_report(self):
        content = (
            'Body [1].\n'
            '# References\n'
            '- Author. Title. DOI: 10.1016/j.jss.2024.01.001 [1]\n'
        )
        report = verify(content)
        text = '\n'.join(report)
        assert 'doi.org' in text

    def test_invalid_doi_flagged(self):
        content = (
            'Body [1].\n'
            '# References\n'
            '- Author. Title. DOI: 10.1016/j.jss;rm -rf / [1]\n'
        )
        report = verify(content)
        text = '\n'.join(report)
        assert '[INVALID DOI]' in text


class TestCrossCheckCitations:
    CONTENT_A = (
        'Body [1] and [2].\n'
        '# References\n'
        '- [1] Author A. PMID: 12345678\n'
        '- [2] Author B. DOI: 10.1016/j.jss.2024.01.001\n'
    )
    CONTENT_B = (
        'Body [1] and [2].\n'
        '# References\n'
        '- [1] Author A. PMID: 12345678\n'
        '- [2] Author B. DOI: 10.1016/j.jss.2024.01.001\n'
    )

    def test_identical_citations_no_divergence(self):
        report = cross_check_citations(self.CONTENT_A, self.CONTENT_B)
        text = '\n'.join(report)
        assert 'Divergent: 0' in text
        assert 'Shared PMIDs: 1' in text

    def test_header_includes_filenames(self):
        report = cross_check_citations(self.CONTENT_A, self.CONTENT_B, name_a='pres.md', name_b='ms.md')
        assert report[0] == '=== Cross-Check: pres.md vs ms.md ==='

    def test_divergent_pmids(self):
        content_b = (
            'Body [1].\n'
            '# References\n'
            '- [1] Author C. PMID: 87654321\n'
        )
        report = cross_check_citations(self.CONTENT_A, content_b, name_a='a.md', name_b='b.md')
        text = '\n'.join(report)
        # PMID 12345678 only in A, 87654321 only in B
        assert '12345678' in text
        assert '87654321' in text
        assert 'Divergent: 0' not in text

    def test_divergent_dois(self):
        content_a = (
            'Body [1].\n'
            '# References\n'
            '- [1] Author A. DOI: 10.1016/j.jss.2024.01.001\n'
        )
        content_b = (
            'Body [1].\n'
            '# References\n'
            '- [1] Author B. DOI: 10.1001/jamasurg.2024.9999\n'
        )
        report = cross_check_citations(content_a, content_b, name_a='a.md', name_b='b.md')
        text = '\n'.join(report)
        assert '10.1016/j.jss.2024.01.001' in text
        assert '10.1001/jamasurg.2024.9999' in text
        assert 'Divergent: 0' not in text

    def test_one_file_no_references(self):
        content_empty = 'Just body text with no references section.\n'
        report = cross_check_citations(self.CONTENT_A, content_empty, name_a='a.md', name_b='empty.md')
        text = '\n'.join(report)
        # All PMIDs/DOIs from A are divergent; B has none
        assert '12345678' in text
        assert 'Divergent: 0' not in text
        assert 'Shared PMIDs: 0' in text
