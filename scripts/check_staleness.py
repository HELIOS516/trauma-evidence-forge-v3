#!/usr/bin/env python3
"""Check reference file freshness for academic-surgery-forge.

Walks .md files under modules/, templates/, and docs/ directories.
Flags files with no staleness metadata or dates older than max_age_days.
"""

import argparse
import os
import re
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Optional


# Patterns to extract a date from a markdown file.
# Covers:
#   ## Version\nv1.0 — 2026-03-01
#   Last updated: March 2026
#   Last updated: 2026-03-01
#   Version: 1.0 (March 2026)
#   Version: 1.0 (2026-03-01)
_DATE_PATTERNS = [
    # ISO date: 2026-03-01
    re.compile(r'\b(20\d{2}-\d{2}-\d{2})\b'),
    # Month Year: March 2026 / Mar 2026
    re.compile(
        r'\b(January|February|March|April|May|June|July|August|September|'
        r'October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
        r'\s+(20\d{2})\b',
        re.IGNORECASE,
    ),
]

_MONTH_MAP = {
    'january': 1, 'jan': 1,
    'february': 2, 'feb': 2,
    'march': 3, 'mar': 3,
    'april': 4, 'apr': 4,
    'may': 5,
    'june': 6, 'jun': 6,
    'july': 7, 'jul': 7,
    'august': 8, 'aug': 8,
    'september': 9, 'sep': 9,
    'october': 10, 'oct': 10,
    'november': 11, 'nov': 11,
    'december': 12, 'dec': 12,
}

_STALENESS_TRIGGER_PATTERNS = [
    re.compile(r'^##\s+version\b', re.IGNORECASE),
    re.compile(r'\blast\s+updated\s*:', re.IGNORECASE),
    re.compile(r'\bversion\s*:', re.IGNORECASE),
    re.compile(r'\bversion\s+\d', re.IGNORECASE),
]

SCAN_DIRS = ('modules', 'templates', 'docs')


def _parse_date_from_text(text: str) -> Optional[date]:
    """Return the first recognisable date found in text, or None."""
    for line in text.splitlines():
        # ISO date match
        m = _DATE_PATTERNS[0].search(line)
        if m:
            try:
                return datetime.strptime(m.group(1), '%Y-%m-%d').date()
            except ValueError:
                pass
        # Month Year match
        m = _DATE_PATTERNS[1].search(line)
        if m:
            month_name = m.group(1).lower()
            year = int(m.group(2))
            month = _MONTH_MAP.get(month_name)
            if month:
                return date(year, month, 1)
    return None


def _has_staleness_marker(text: str) -> bool:
    """Return True if the file contains a version/last-updated marker line."""
    for line in text.splitlines():
        for pat in _STALENESS_TRIGGER_PATTERNS:
            if pat.search(line):
                return True
    return False


def check_file(filepath: str, max_age_days: int, today: Optional[date] = None) -> dict:
    """Check a single file for staleness metadata.

    Returns a dict with keys:
        path        - absolute path
        status      - 'fresh' | 'stale' | 'undated'
        date        - date object or None
        age_days    - int or None
        detail      - human-readable description
    """
    if today is None:
        today = date.today()

    with open(filepath, encoding='utf-8') as f:
        text = f.read()

    has_marker = _has_staleness_marker(text)
    found_date = _parse_date_from_text(text) if has_marker else None

    if not has_marker and found_date is None:
        # Try parsing a date even without a marker line (bare date anywhere)
        found_date = _parse_date_from_text(text)

    if found_date is None:
        return {
            'path': filepath,
            'status': 'undated',
            'date': None,
            'age_days': None,
            'detail': 'no staleness metadata found',
        }

    age_days = (today - found_date).days
    if age_days > max_age_days:
        return {
            'path': filepath,
            'status': 'stale',
            'date': found_date,
            'age_days': age_days,
            'detail': f'last updated {found_date} ({age_days} days ago, threshold {max_age_days})',
        }

    return {
        'path': filepath,
        'status': 'fresh',
        'date': found_date,
        'age_days': age_days,
        'detail': f'last updated {found_date} ({age_days} days ago)',
    }


def check_staleness(directory: str, max_age_days: int = 365) -> dict:
    """Walk scan directories under `directory` and check each .md file.

    Returns:
        {
            'results': list of per-file dicts from check_file(),
            'stale': [paths],
            'undated': [paths],
            'fresh': [paths],
            'total': int,
            'clean': bool,
        }
    """
    base = Path(directory).resolve()
    results = []

    for subdir in SCAN_DIRS:
        scan_path = base / subdir
        if not scan_path.exists():
            continue
        for md_file in sorted(scan_path.rglob('*.md')):
            result = check_file(str(md_file), max_age_days)
            results.append(result)

    stale = [r['path'] for r in results if r['status'] == 'stale']
    undated = [r['path'] for r in results if r['status'] == 'undated']
    fresh = [r['path'] for r in results if r['status'] == 'fresh']

    return {
        'results': results,
        'stale': stale,
        'undated': undated,
        'fresh': fresh,
        'total': len(results),
        'clean': len(stale) == 0 and len(undated) == 0,
    }


def main():
    parser = argparse.ArgumentParser(
        description='Check reference file freshness for academic-surgery-forge.'
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help='Project root directory to scan (default: current directory)',
    )
    parser.add_argument(
        '--max-age-days',
        type=int,
        default=365,
        metavar='N',
        help='Maximum allowed age in days before a file is flagged stale (default: 365)',
    )
    args = parser.parse_args()

    directory = os.path.abspath(args.directory)
    if not os.path.isdir(directory):
        print(f'Error: directory not found: {directory}', file=sys.stderr)
        sys.exit(1)

    summary = check_staleness(directory, args.max_age_days)

    print(f'Staleness check: {directory}')
    print(f'Threshold: {args.max_age_days} days')
    print(f'Files scanned: {summary["total"]}')
    print()

    if summary['total'] == 0:
        print('No .md files found in modules/, templates/, or docs/.')
        sys.exit(0)

    # Print stale files
    if summary['stale']:
        print(f'STALE ({len(summary["stale"])} files):')
        for r in summary['results']:
            if r['status'] == 'stale':
                print(f'  [STALE]   {r["path"]}')
                print(f'            {r["detail"]}')
        print()

    # Print undated files
    if summary['undated']:
        print(f'UNDATED ({len(summary["undated"])} files):')
        for r in summary['results']:
            if r['status'] == 'undated':
                print(f'  [UNDATED] {r["path"]}')
                print(f'            {r["detail"]}')
        print()

    # Print fresh files
    if summary['fresh']:
        print(f'FRESH ({len(summary["fresh"])} files):')
        for r in summary['results']:
            if r['status'] == 'fresh':
                print(f'  [FRESH]   {r["path"]}')
                print(f'            {r["detail"]}')
        print()

    if summary['clean']:
        print('All files are fresh.')
        sys.exit(0)
    else:
        issues = len(summary['stale']) + len(summary['undated'])
        print(f'{issues} file(s) require attention.')
        sys.exit(1)


if __name__ == '__main__':
    main()
