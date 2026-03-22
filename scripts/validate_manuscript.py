#!/usr/bin/env python3
"""Manuscript validation with 16 checks (10 hard, 6 soft).

Hard gates cause FAIL; soft gates produce warnings.
"""

import argparse
import json
import os
import sys

from research_utils import (
    extract_pmids, extract_dois, extract_citations, extract_reference_numbers,
    check_citation_coverage, count_words, detect_study_type,
    get_checklist_for_study_type, detect_imrad_sections, find_statistical_claims,
    extract_grades, is_valid_grade, validate_grade_plausibility,
)


def validate(text: str) -> dict:
    """Run all 16 validation checks on manuscript text."""
    checks = []
    hard_fail = 0
    soft_fail = 0

    sections = detect_imrad_sections(text)
    pmids = extract_pmids(text)
    dois = extract_dois(text)
    body_citations = extract_citations(text)
    ref_numbers = extract_reference_numbers(text)
    coverage = check_citation_coverage(text)
    word_count = count_words(text)
    study_type = detect_study_type(text)
    stats = find_statistical_claims(text)
    grades = extract_grades(text)

    # --- HARD GATES (1-10) ---

    # 1. IMRAD sections present
    missing = [s for s in ['abstract', 'introduction', 'methods', 'results', 'discussion', 'references']
               if not sections.get(s)]
    passed = len(missing) == 0
    checks.append({'id': 1, 'name': 'IMRAD sections', 'hard': True, 'passed': passed,
                   'detail': f'Missing: {", ".join(missing)}' if missing else 'All present'})
    if not passed:
        hard_fail += 1

    # 2. At least 1 citation in body
    passed = len(body_citations) > 0
    checks.append({'id': 2, 'name': 'Body citations exist', 'hard': True, 'passed': passed,
                   'detail': f'{len(body_citations)} citations found'})
    if not passed:
        hard_fail += 1

    # 3. All body citations have references
    passed = coverage['coverage_complete']
    checks.append({'id': 3, 'name': 'Citation coverage', 'hard': True, 'passed': passed,
                   'detail': f'Missing refs: {coverage["missing_references"]}' if not passed else 'Complete'})
    if not passed:
        hard_fail += 1

    # 4. At least 1 PMID or DOI
    passed = len(pmids) > 0 or len(dois) > 0
    checks.append({'id': 4, 'name': 'PMID/DOI present', 'hard': True, 'passed': passed,
                   'detail': f'{len(pmids)} PMIDs, {len(dois)} DOIs'})
    if not passed:
        hard_fail += 1

    # 5. No fabricated PMID patterns
    fabricated = []
    for pmid in pmids:
        if pmid == '00000000' or pmid == '12345678' or len(set(pmid)) == 1:
            fabricated.append(pmid)
    passed = len(fabricated) == 0
    checks.append({'id': 5, 'name': 'No fabricated PMIDs', 'hard': True, 'passed': passed,
                   'detail': f'Suspicious: {fabricated}' if fabricated else 'None detected'})
    if not passed:
        hard_fail += 1

    # 6. Abstract present
    passed = sections.get('abstract', False)
    checks.append({'id': 6, 'name': 'Abstract present', 'hard': True, 'passed': passed,
                   'detail': 'Found' if passed else 'Missing'})
    if not passed:
        hard_fail += 1

    # 7. Results has statistical data
    results_start = text.lower().find('## results')
    results_end = text.lower().find('## discussion')
    if results_start >= 0 and results_end > results_start:
        results_text = text[results_start:results_end]
    elif results_start >= 0:
        results_text = text[results_start:]
    else:
        results_text = ''
    has_stats = bool(results_text and (
        '%' in results_text or
        'p=' in results_text.lower() or
        'p<' in results_text.lower() or
        'CI' in results_text or
        'OR ' in results_text
    ))
    passed = has_stats
    checks.append({'id': 7, 'name': 'Results has statistics', 'hard': True, 'passed': passed,
                   'detail': 'Statistical data found' if passed else 'No statistical data in Results'})
    if not passed:
        hard_fail += 1

    # 8. Methods non-empty
    methods_start = text.lower().find('## methods')
    methods_end = text.lower().find('## results')
    if methods_start >= 0 and methods_end > methods_start:
        methods_text = text[methods_start:methods_end].strip()
    elif methods_start >= 0:
        methods_text = text[methods_start:].strip()
    else:
        methods_text = ''
    passed = len(methods_text) > 50
    checks.append({'id': 8, 'name': 'Methods non-empty', 'hard': True, 'passed': passed,
                   'detail': f'{count_words(methods_text)} words' if methods_text else 'Missing'})
    if not passed:
        hard_fail += 1

    # 9. Discussion non-empty
    disc_start = text.lower().find('## discussion')
    disc_end = text.lower().find('## references')
    if disc_start >= 0 and disc_end > disc_start:
        disc_text = text[disc_start:disc_end].strip()
    elif disc_start >= 0:
        disc_text = text[disc_start:].strip()
    else:
        disc_text = ''
    passed = len(disc_text) > 50
    checks.append({'id': 9, 'name': 'Discussion non-empty', 'hard': True, 'passed': passed,
                   'detail': f'{count_words(disc_text)} words' if disc_text else 'Missing'})
    if not passed:
        hard_fail += 1

    # 10. References >= 5
    passed = len(ref_numbers) >= 5
    checks.append({'id': 10, 'name': 'References >= 5', 'hard': True, 'passed': passed,
                   'detail': f'{len(ref_numbers)} references found'})
    if not passed:
        hard_fail += 1

    # --- SOFT GATES (11-15) ---

    # 11. Word count within limits (default 4000)
    passed = word_count <= 5000
    checks.append({'id': 11, 'name': 'Word count', 'hard': False, 'passed': passed,
                   'detail': f'{word_count} words'})
    if not passed:
        soft_fail += 1

    # 12. Study type detected
    passed = study_type != 'unknown'
    checklist = get_checklist_for_study_type(study_type)
    checks.append({'id': 12, 'name': 'Study type detected', 'hard': False, 'passed': passed,
                   'detail': f'{study_type} -> {checklist}' if passed else 'Could not detect study type'})
    if not passed:
        soft_fail += 1

    # 13. Statistical claims have CI
    claims_with_ci = [c for c in stats if c['has_ci']]
    ci_ratio = len(claims_with_ci) / len(stats) if stats else 1.0
    passed = ci_ratio >= 0.5
    checks.append({'id': 13, 'name': 'Stats have CI', 'hard': False, 'passed': passed,
                   'detail': f'{len(claims_with_ci)}/{len(stats)} claims have 95% CI'})
    if not passed:
        soft_fail += 1

    # 14. All references have PMID or DOI
    total_refs = len(ref_numbers)
    total_identifiers = len(pmids) + len(dois)
    passed = total_identifiers >= total_refs * 0.8 if total_refs > 0 else True
    checks.append({'id': 14, 'name': 'Refs have identifiers', 'hard': False, 'passed': passed,
                   'detail': f'{total_identifiers} identifiers for {total_refs} refs'})
    if not passed:
        soft_fail += 1

    # 15. GRADE ratings valid
    invalid = [g for g in grades if not is_valid_grade(g)]
    passed = len(invalid) == 0
    checks.append({'id': 15, 'name': 'GRADE ratings valid', 'hard': False, 'passed': passed,
                   'detail': f'Invalid: {invalid}' if invalid else f'{len(grades)} valid ratings'})
    if not passed:
        soft_fail += 1

    # 16. GRADE plausibility (cross-check grade vs study type)
    grade_warnings = []
    for g in grades:
        grade_warnings.extend(validate_grade_plausibility(g, study_type))
    passed = len(grade_warnings) == 0
    checks.append({'id': 16, 'name': 'GRADE plausibility', 'hard': False, 'passed': passed,
                   'detail': '; '.join(grade_warnings[:3]) if grade_warnings else 'All ratings plausible'})
    if not passed:
        soft_fail += 1

    overall = 'PASS' if hard_fail == 0 else 'FAIL'

    return {
        'overall': overall,
        'hard_fail': hard_fail,
        'soft_fail': soft_fail,
        'total_checks': len(checks),
        'word_count': word_count,
        'study_type': study_type,
        'checklist': get_checklist_for_study_type(study_type),
        'checks': checks,
    }


def main():
    parser = argparse.ArgumentParser(description='Validate manuscript against 16-check quality gate')
    parser.add_argument('file', help='Manuscript markdown file')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f'Error: File not found: {args.file}', file=sys.stderr)
        sys.exit(1)

    with open(args.file, encoding='utf-8') as f:
        text = f.read()

    result = validate(text)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f'Overall: {result["overall"]}')
        print(f'Hard failures: {result["hard_fail"]}')
        print(f'Soft failures: {result["soft_fail"]}')
        print(f'Word count: {result["word_count"]}')
        print(f'Study type: {result["study_type"]} -> {result["checklist"]}')
        print()
        for check in result['checks']:
            status = 'PASS' if check['passed'] else ('FAIL' if check['hard'] else 'WARN')
            print(f'  [{status}] {check["id"]}. {check["name"]}: {check["detail"]}')

    sys.exit(0 if result['overall'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
