#!/usr/bin/env python3
"""Shared research utilities for academic-surgery-forge skill."""

import re


def extract_pmids(text: str) -> list[str]:
    """Extract all PMID numbers from text."""
    return re.findall(r'PMID:?\s*(\d{7,8})', text)


def extract_dois(text: str) -> list[str]:
    """Extract all DOI strings from text."""
    return re.findall(r'(?:DOI:?\s*|doi\.org/)(10\.\d{4,}/[^\s,;)\]]+)', text)


def extract_citations(text: str) -> list[int]:
    """Extract [N] citation numbers from body text (before References section)."""
    refs_match = re.search(r'^#{1,3}\s*references', text, re.MULTILINE | re.IGNORECASE)
    body = text[:refs_match.start()] if refs_match else text
    return sorted(set(int(n) for n in re.findall(r'\[(\d+)\]', body)))


def extract_reference_numbers(text: str) -> list[int]:
    """Extract citation numbers from the References section."""
    refs_match = re.search(r'^#{1,3}\s*References', text, re.MULTILINE | re.IGNORECASE)
    if not refs_match:
        return []
    refs_section = text[refs_match.end():]
    # Match [N] bracket format or N. numbered list format
    bracket_nums = set(int(n) for n in re.findall(r'\[(\d+)\]', refs_section))
    list_nums = set(int(n) for n in re.findall(r'^\s*(\d+)\.\s+\w', refs_section, re.MULTILINE))
    return sorted(bracket_nums | list_nums)


def check_citation_coverage(text: str) -> dict:
    """Check that all body citations have corresponding reference entries."""
    body_citations = set(extract_citations(text))
    ref_numbers = set(extract_reference_numbers(text))
    return {
        'body_citations': sorted(body_citations),
        'reference_entries': sorted(ref_numbers),
        'missing_references': sorted(body_citations - ref_numbers),
        'orphan_references': sorted(ref_numbers - body_citations),
        'coverage_complete': body_citations <= ref_numbers,
    }


def count_words(text: str) -> int:
    """Count words in text, excluding markdown syntax."""
    clean = re.sub(r'[#*_`\[\]()>|]', ' ', text)
    clean = re.sub(r'<[^>]+>', '', clean)
    clean = re.sub(r'---+', '', clean)
    return len(clean.split())


def detect_study_type(text: str) -> str:
    """Heuristic detection of study type from manuscript text."""
    text_lower = text.lower()
    patterns = {
        'RCT': [r'randomi[zs]ed', r'randomly\s+assigned', r'random\s+allocation'],
        'systematic_review': [r'systematic\s+review', r'meta-analysis', r'prisma'],
        'cohort': [r'cohort\s+study', r'prospective\s+cohort', r'retrospective\s+cohort'],
        'case_control': [r'case-control', r'case\s+control', r'matched\s+controls'],
        'cross_sectional': [r'cross-sectional', r'cross\s+sectional', r'prevalence\s+study'],
        'case_report': [r'case\s+report', r'single\s+patient', r'we\s+present\s+a\s+case'],
        'quality_improvement': [r'quality\s+improvement', r'pdsa', r'plan-do-study-act'],
    }
    for study_type, regexes in patterns.items():
        for pattern in regexes:
            if re.search(pattern, text_lower):
                return study_type
    return 'unknown'


def get_checklist_for_study_type(study_type: str) -> str:
    """Return the appropriate reporting checklist for a study type."""
    mapping = {
        'RCT': 'CONSORT',
        'systematic_review': 'PRISMA',
        'cohort': 'STROBE',
        'case_control': 'STROBE',
        'cross_sectional': 'STROBE',
        'case_report': 'CARE',
        'quality_improvement': 'SQUIRE',
    }
    return mapping.get(study_type, 'unknown')


VALID_GRADES = {'1A', '1B', '1C', '2A', '2B', '2C', '3', '4',
                'High', 'Moderate', 'Low', 'Very Low'}

# Approximate bidirectional mapping between CEBM levels and GRADE certainty.
CEBM_TO_GRADE = {
    '1A': 'High', '1B': 'High',
    '1C': 'Moderate',
    '2A': 'Moderate', '2B': 'Low', '2C': 'Very Low',
    '3': 'Very Low', '4': 'Very Low',
}
GRADE_TO_CEBM = {
    'High': ['1A', '1B'],
    'Moderate': ['1C', '2A'],
    'Low': ['2B'],
    'Very Low': ['2C', '3', '4'],
}


def is_valid_grade(grade: str) -> bool:
    """Check if a GRADE rating string is valid."""
    return grade.strip() in VALID_GRADES


def map_cebm_to_grade(code: str) -> str | None:
    """Map a CEBM level code to approximate GRADE certainty term."""
    return CEBM_TO_GRADE.get(code.strip().upper())


def map_grade_to_cebm(term: str) -> list[str]:
    """Map a GRADE certainty term to approximate CEBM level codes."""
    return GRADE_TO_CEBM.get(term.strip().title(), [])


def extract_grades(text: str) -> list[str]:
    """Extract GRADE ratings from text (both CEBM codes and GRADE-system terms)."""
    return re.findall(
        r'GRADE[:\s]+(High|Moderate|Very\s+Low|Low|[12][ABC]|[34])',
        text, re.IGNORECASE,
    )


def validate_grade_plausibility(grade: str, study_type: str) -> list[str]:
    """Check if a GRADE rating is plausible for the given study type.

    Handles both CEBM codes (1A, 2B, etc.) and GRADE-system terms
    (High, Moderate, Low, Very Low). Returns a list of warning strings.
    """
    warnings = []
    study_lower = study_type.lower()
    grade_clean = grade.strip()

    # Normalize to GRADE certainty term for uniform comparison
    grade_upper = grade_clean.upper()
    if grade_upper in CEBM_TO_GRADE:
        grade_term = CEBM_TO_GRADE[grade_upper]
    else:
        grade_term = grade_clean.title()

    low_quality_types = {'cohort', 'case_control', 'case-control', 'case series', 'case_series'}
    high_quality_types = {'rct', 'systematic_review', 'meta-analysis', 'meta_analysis'}

    is_low_quality = any(t in study_lower for t in low_quality_types)
    is_high_quality = any(t in study_lower for t in high_quality_types)

    if is_low_quality and grade_term == 'High':
        warnings.append(
            f"GRADE '{grade_clean}' (High certainty) is suspicious for study type '{study_type}': "
            f"observational studies rarely achieve High certainty without strong evidence."
        )
    if is_high_quality and grade_term in ('Very Low', 'Low'):
        warnings.append(
            f"GRADE '{grade_clean}' ({grade_term} certainty) is suspicious for study type '{study_type}': "
            f"RCTs/meta-analyses rarely have {grade_term} certainty unless quality is very poor."
        )
    return warnings


def find_statistical_claims(text: str) -> list[dict]:
    """Find statistical claims and check for proper reporting."""
    claims = []
    for match in re.finditer(r'(\d+\.?\d*)\s*%', text):
        line_start = text.rfind('\n', 0, match.start()) + 1
        line_end = text.find('\n', match.end())
        line = text[line_start:line_end if line_end > 0 else len(text)]
        has_ci = bool(re.search(r'(?:95%?\s*CI|confidence\s+interval)', line, re.IGNORECASE))
        has_p = bool(re.search(r'p\s*[=<>]\s*\d', line, re.IGNORECASE))
        has_citation = bool(re.search(r'\[\d+\]', line))
        claims.append({
            'value': match.group(),
            'line': line.strip(),
            'has_ci': has_ci,
            'has_p_value': has_p,
            'has_citation': has_citation,
        })
    return claims


def detect_imrad_sections(text: str) -> dict:
    """Detect presence of IMRAD sections."""
    sections = {
        'abstract': bool(re.search(r'^#{1,3}\s*abstract', text, re.IGNORECASE | re.MULTILINE)),
        'introduction': bool(re.search(r'^#{1,3}\s*introduction', text, re.IGNORECASE | re.MULTILINE)),
        'methods': bool(re.search(r'^#{1,3}\s*methods', text, re.IGNORECASE | re.MULTILINE)),
        'results': bool(re.search(r'^#{1,3}\s*results', text, re.IGNORECASE | re.MULTILINE)),
        'discussion': bool(re.search(r'^#{1,3}\s*discussion', text, re.IGNORECASE | re.MULTILINE)),
        'references': bool(re.search(r'^#{1,3}\s*references', text, re.IGNORECASE | re.MULTILINE)),
    }
    sections['complete'] = all(sections.values())
    return sections
