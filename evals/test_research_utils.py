"""Tests for research_utils.py"""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from research_utils import (
    extract_pmids, extract_dois, extract_citations, extract_reference_numbers,
    check_citation_coverage, count_words, detect_study_type,
    get_checklist_for_study_type, is_valid_grade, detect_imrad_sections,
    find_statistical_claims, extract_grades, validate_grade_plausibility,
    map_cebm_to_grade, map_grade_to_cebm,
)


class TestExtractPmids:
    def test_standard_format(self):
        assert extract_pmids('PMID: 12345678') == ['12345678']

    def test_no_space(self):
        assert extract_pmids('PMID:12345678') == ['12345678']

    def test_multiple(self):
        text = 'PMID: 12345678 and PMID: 87654321'
        assert extract_pmids(text) == ['12345678', '87654321']

    def test_no_pmids(self):
        assert extract_pmids('No PMIDs here') == []


class TestExtractDois:
    def test_standard(self):
        dois = extract_dois('DOI: 10.1016/j.jss.2024.01.001')
        assert len(dois) == 1
        assert '10.1016/j.jss.2024.01.001' in dois[0]

    def test_url_format(self):
        dois = extract_dois('doi.org/10.1001/jamasurg.2024.1234')
        assert len(dois) == 1


class TestCitations:
    def test_extract_body_citations(self):
        text = 'Results[1] showed improvement[2].\n## References\nRef [1]\nRef [2]\n'
        assert extract_citations(text) == [1, 2]

    def test_coverage_complete(self):
        text = 'Claim[1].\n## References\nAuthor. Title. PMID: 123 [1]\n'
        result = check_citation_coverage(text)
        assert result['coverage_complete']

    def test_coverage_missing(self):
        text = 'Claim[1] and claim[2].\n## References\nAuthor. Title. PMID: 123 [1]\n'
        result = check_citation_coverage(text)
        assert not result['coverage_complete']
        assert 2 in result['missing_references']


class TestWordCount:
    def test_simple(self):
        assert count_words('This is a test with seven words.') == 7

    def test_strips_markdown(self):
        assert count_words('## Heading\n**bold** text') > 0


class TestStudyType:
    def test_rct(self):
        assert detect_study_type('Patients were randomized to groups') == 'RCT'

    def test_systematic_review(self):
        assert detect_study_type('This systematic review and meta-analysis') == 'systematic_review'

    def test_cohort(self):
        assert detect_study_type('In this retrospective cohort study') == 'cohort'

    def test_case_report(self):
        assert detect_study_type('We present a case report of a patient') == 'case_report'

    def test_unknown(self):
        assert detect_study_type('The sky is blue') == 'unknown'


class TestChecklist:
    def test_rct_consort(self):
        assert get_checklist_for_study_type('RCT') == 'CONSORT'

    def test_cohort_strobe(self):
        assert get_checklist_for_study_type('cohort') == 'STROBE'

    def test_systematic_prisma(self):
        assert get_checklist_for_study_type('systematic_review') == 'PRISMA'


class TestGrade:
    def test_valid_grades(self):
        for g in ['1A', '1B', '1C', '2A', '2B', '2C', '3', '4']:
            assert is_valid_grade(g), f'{g} should be valid'

    def test_invalid(self):
        assert not is_valid_grade('5A')
        assert not is_valid_grade('1D')


class TestImradSections:
    def test_complete(self):
        text = '## Abstract\n\n## Introduction\n\n## Methods\n\n## Results\n\n## Discussion\n\n## References\n'
        sections = detect_imrad_sections(text)
        assert sections['complete']

    def test_missing_methods(self):
        text = '## Abstract\n\n## Introduction\n\n## Results\n\n## Discussion\n\n## References\n'
        sections = detect_imrad_sections(text)
        assert not sections['methods']
        assert not sections['complete']


class TestExtractGrades:
    def test_cebm_code(self):
        assert extract_grades('GRADE: 1A') == ['1A']

    def test_grade_term_high(self):
        assert extract_grades('GRADE: High') == ['High']

    def test_grade_term_moderate(self):
        assert extract_grades('GRADE: Moderate') == ['Moderate']

    def test_grade_term_very_low(self):
        result = extract_grades('GRADE: Very Low')
        assert len(result) == 1
        assert result[0].replace(' ', ' ') == 'Very Low'

    def test_mixed_cebm_and_term(self):
        text = 'Evidence rated GRADE: 1B for the primary outcome and GRADE: Low for secondary.'
        result = extract_grades(text)
        assert '1B' in result
        assert 'Low' in result

    def test_case_insensitive(self):
        result = extract_grades('grade: high')
        assert len(result) == 1
        assert result[0].lower() == 'high'

    def test_no_matches(self):
        assert extract_grades('no grade here') == []


class TestGradeTerms:
    def test_valid_high(self):
        assert is_valid_grade('High')

    def test_valid_moderate(self):
        assert is_valid_grade('Moderate')

    def test_valid_low(self):
        assert is_valid_grade('Low')

    def test_valid_very_low(self):
        assert is_valid_grade('Very Low')

    def test_invalid_medium(self):
        assert not is_valid_grade('Medium')

    def test_invalid_none_string(self):
        assert not is_valid_grade('None')

    def test_invalid_very_high(self):
        assert not is_valid_grade('Very High')


class TestMapCebmToGrade:
    def test_1a_high(self):
        assert map_cebm_to_grade('1A') == 'High'

    def test_1b_high(self):
        assert map_cebm_to_grade('1B') == 'High'

    def test_1c_moderate(self):
        assert map_cebm_to_grade('1C') == 'Moderate'

    def test_2a_moderate(self):
        assert map_cebm_to_grade('2A') == 'Moderate'

    def test_2b_low(self):
        assert map_cebm_to_grade('2B') == 'Low'

    def test_2c_very_low(self):
        assert map_cebm_to_grade('2C') == 'Very Low'

    def test_3_very_low(self):
        assert map_cebm_to_grade('3') == 'Very Low'

    def test_4_very_low(self):
        assert map_cebm_to_grade('4') == 'Very Low'

    def test_invalid_code(self):
        assert map_cebm_to_grade('5A') is None


class TestMapGradeToCebm:
    def test_high(self):
        assert map_grade_to_cebm('High') == ['1A', '1B']

    def test_moderate(self):
        assert map_grade_to_cebm('Moderate') == ['1C', '2A']

    def test_low(self):
        assert map_grade_to_cebm('Low') == ['2B']

    def test_very_low(self):
        assert map_grade_to_cebm('Very Low') == ['2C', '3', '4']

    def test_invalid_term(self):
        assert map_grade_to_cebm('Excellent') == []


class TestValidateGradePlausibility:
    def test_high_with_cohort_warns(self):
        warnings = validate_grade_plausibility('High', 'cohort')
        assert len(warnings) > 0

    def test_1a_with_case_control_warns(self):
        warnings = validate_grade_plausibility('1A', 'case_control')
        assert len(warnings) > 0

    def test_low_with_rct_warns(self):
        warnings = validate_grade_plausibility('Low', 'RCT')
        assert len(warnings) > 0

    def test_moderate_with_rct_no_warn(self):
        warnings = validate_grade_plausibility('Moderate', 'RCT')
        assert len(warnings) == 0

    def test_low_with_cohort_no_warn(self):
        warnings = validate_grade_plausibility('Low', 'cohort')
        assert len(warnings) == 0

    def test_high_with_systematic_review_no_warn(self):
        warnings = validate_grade_plausibility('High', 'systematic_review')
        assert len(warnings) == 0


class TestFindStatisticalClaims:
    def test_with_ci_and_p_value(self):
        text = 'The mortality rate was 5.3% (95% CI 3.1-7.5, p=0.007) in the treatment group.'
        claims = find_statistical_claims(text)
        assert len(claims) >= 1
        primary = next(c for c in claims if '5.3' in c['value'])
        assert primary['has_ci'] is True
        assert primary['has_p_value'] is True

    def test_with_citation_no_ci(self):
        text = 'Studies show a 23% reduction [1] in complication rates.'
        claims = find_statistical_claims(text)
        assert len(claims) >= 1
        primary = next(c for c in claims if '23' in c['value'])
        assert primary['has_citation'] is True
        assert primary['has_ci'] is False

    def test_no_percentages(self):
        text = 'The study found no significant difference between groups.'
        claims = find_statistical_claims(text)
        assert claims == []
