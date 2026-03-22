#!/usr/bin/env python3
"""Reference formatting and validation for manuscripts."""

import argparse
import os
import re
import sys


def extract_references(text: str) -> list[dict]:
    """Extract reference entries from the References section."""
    refs_match = re.search(r'^#{1,3}\s*References\s*$', text, re.MULTILINE | re.IGNORECASE)
    if not refs_match:
        return []

    refs_text = text[refs_match.end():]
    refs = []
    for line in refs_text.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        # Try [N] bracket format first, then N. numbered list format
        num_match = re.match(r'\[(\d+)\]', line)
        if not num_match:
            num_match = re.match(r'(\d+)\.\s+', line)
        if num_match:
            ref_num = int(num_match.group(1))
            ref_text = line[num_match.end():].strip()
            refs.append({
                'number': ref_num,
                'text': ref_text or line,
                'has_pmid': bool(re.search(r'PMID', line)),
                'has_doi': bool(re.search(r'DOI|doi\.org', line)),
            })
    return sorted(refs, key=lambda r: r['number'])


def check_format(refs: list[dict], style: str = 'vancouver') -> list[dict]:
    """Check reference formatting issues."""
    issues = []
    for idx, ref in enumerate(refs):
        expected = idx + 1
        if ref['number'] != expected:
            issues.append({'ref': ref['number'], 'issue': f'Expected [{expected}], got [{ref["number"]}]'})
        if not ref['has_pmid'] and not ref['has_doi']:
            issues.append({'ref': ref['number'], 'issue': 'Missing PMID and DOI'})
        if not re.search(r'\.\s+\w+.*\.\s+\d{4}', ref['text']):
            issues.append({'ref': ref['number'], 'issue': 'Format may not match Vancouver/AMA style'})
    return issues


def check_duplicates(refs: list[dict]) -> list[dict]:
    """Find duplicate references."""
    seen_pmids = {}
    duplicates = []
    for ref in refs:
        pmid_match = re.search(r'PMID:?\s*(\d+)', ref['text'])
        if pmid_match:
            pmid = pmid_match.group(1)
            if pmid in seen_pmids:
                duplicates.append({'refs': [seen_pmids[pmid], ref['number']], 'pmid': pmid})
            seen_pmids[pmid] = ref['number']
    return duplicates


def main():
    parser = argparse.ArgumentParser(description='Format and validate references')
    parser.add_argument('file', help='Manuscript markdown file')
    parser.add_argument('--style', choices=['vancouver', 'ama'], default='vancouver')
    parser.add_argument('--check-only', action='store_true', help='Only check, do not modify')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f'Error: File not found: {args.file}', file=sys.stderr)
        sys.exit(1)

    with open(args.file, encoding='utf-8') as f:
        text = f.read()

    refs = extract_references(text)
    print(f'Found {len(refs)} references')

    issues = check_format(refs, args.style)
    duplicates = check_duplicates(refs)

    if issues:
        print(f'\nFormat issues ({len(issues)}):')
        for issue in issues:
            print(f'  [{issue["ref"]}] {issue["issue"]}')

    if duplicates:
        print(f'\nDuplicate references ({len(duplicates)}):')
        for dup in duplicates:
            print(f'  PMID {dup["pmid"]} appears in refs {dup["refs"]}')

    if not issues and not duplicates:
        print('All references formatted correctly.')

    sys.exit(1 if issues else 0)


if __name__ == '__main__':
    main()
