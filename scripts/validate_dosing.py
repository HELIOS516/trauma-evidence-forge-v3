#!/usr/bin/env python3
"""Drug dosing validation for critical-care medical documents.

Parses text for drug dosing claims and checks physiologic plausibility
against known ranges for common critical care medications.
"""

import argparse
import json
import os
import re
import sys


DOSE_RANGES = {
    'norepinephrine': {'unit': 'mcg/min', 'min': 1, 'max': 50},
    'vasopressin': {'unit': 'units/min', 'min': 0.01, 'max': 0.04},
    'epinephrine': {'unit': 'mcg/min', 'min': 1, 'max': 20},
    'phenylephrine': {'unit': 'mcg/min', 'min': 40, 'max': 360},
    'propofol': {'unit': 'mcg/kg/min', 'min': 5, 'max': 80},
    'fentanyl': {'unit': 'mcg/hr', 'min': 25, 'max': 200},
    'ketamine': {'unit': 'mg/kg', 'min': 0.1, 'max': 2.0},
    'tranexamic_acid': {'unit': 'g', 'min': 1, 'max': 2},
    'mannitol': {'unit': 'g/kg', 'min': 0.25, 'max': 1.5},
    'heparin': {'unit': 'units/kg', 'min': 60, 'max': 100},
}

# Aliases map variant names to canonical DOSE_RANGES keys
DRUG_ALIASES = {
    'txa': 'tranexamic_acid',
    'tranexamic acid': 'tranexamic_acid',
    'norepi': 'norepinephrine',
    'levophed': 'norepinephrine',
    'epi': 'epinephrine',
    'adrenaline': 'epinephrine',
    'neo': 'phenylephrine',
    'diprivan': 'propofol',
}

# Numeric value pattern: integers, decimals, ranges (captures first number of a range)
_NUM = r'(\d+(?:\.\d+)?)'
_RANGE_NUM = r'(\d+(?:\.\d+)?)(?:\s*[-\u2013]\s*\d+(?:\.\d+)?)?'

# Unit alternatives — order matters: longer/more-specific units first
_UNITS = (
    r'mcg/kg/min',
    r'mcg/kg/hr',
    r'mcg/min',
    r'mcg/hr',
    r'mg/kg/min',
    r'mg/kg/hr',
    r'mg/kg',
    r'mg/min',
    r'mg/hr',
    r'units/min',
    r'units/hr',
    r'units/kg',
    r'g/kg',
    r'g',
    r'mg',
    r'mcg',
)

_UNIT_PATTERN = '|'.join(_UNITS)

# Main extraction regex: drug-name  optional-space  number  optional-space  unit
# Allows "mg" with no preceding space (e.g. "500mg")
_DOSE_RE = re.compile(
    r'(?P<drug>[a-zA-Z][a-zA-Z0-9_ ]{1,30}?)'    # drug name (greedy up to 30 chars)
    r'\s+'                                          # whitespace separator
    r'(?P<value>' + _RANGE_NUM + r')'              # numeric value (first of range)
    r'\s*'                                          # optional space before unit
    r'(?P<unit>' + _UNIT_PATTERN + r')'            # unit
    r'(?:\s*/\s*(?:IV|IM|SQ|PO|PR|SL|INH))?',     # optional route suffix
    re.IGNORECASE,
)


def _normalize_drug(name: str) -> str | None:
    """Resolve a raw drug name string to a DOSE_RANGES key, or None if unknown."""
    name_clean = name.strip().lower().rstrip('s')  # simple depluralize
    # Direct match
    if name_clean in DOSE_RANGES:
        return name_clean
    # Alias match
    if name_clean in DRUG_ALIASES:
        return DRUG_ALIASES[name_clean]
    # Partial / substring match against canonical names and aliases
    for canonical in DOSE_RANGES:
        if canonical in name_clean or name_clean in canonical:
            return canonical
    for alias, canonical in DRUG_ALIASES.items():
        if alias in name_clean or name_clean in alias:
            return canonical
    return None


def _normalize_unit(unit: str) -> str:
    """Return a lowercase, whitespace-collapsed unit string."""
    return re.sub(r'\s+', '', unit.lower())


def extract_dosing_claims(text: str) -> list[dict]:
    """Extract drug dosing claims from text.

    Returns a list of dicts with keys:
        drug_raw   - raw matched drug name string
        drug       - canonical drug name (None if unknown)
        value      - float dose value
        unit       - normalized unit string
        match_text - full matched substring
    """
    claims = []
    for m in _DOSE_RE.finditer(text):
        drug_raw = m.group('drug').strip()
        value_str = m.group('value').strip()
        unit_raw = m.group('unit').strip()

        try:
            value = float(value_str)
        except ValueError:
            continue

        canonical = _normalize_drug(drug_raw)
        unit = _normalize_unit(unit_raw)

        claims.append({
            'drug_raw': drug_raw,
            'drug': canonical,
            'value': value,
            'unit': unit,
            'match_text': m.group(0).strip(),
        })

    return claims


def validate_dose(drug: str | None, value: float, unit: str) -> dict:
    """Validate a single dose against DOSE_RANGES.

    Returns a dict with keys:
        status    - 'OK', 'WARNING', 'DANGER', 'UNKNOWN', or 'UNIT_MISMATCH'
        drug      - canonical drug name or None
        value     - the dose value
        unit      - the unit string
        message   - human-readable result line
        ratio     - how many times outside range (None if within range)
    """
    if drug is None:
        return {
            'status': 'UNKNOWN',
            'drug': drug,
            'value': value,
            'unit': unit,
            'message': f'[SKIP] unknown drug — {value} {unit}',
            'ratio': None,
        }

    if drug not in DOSE_RANGES:
        return {
            'status': 'UNKNOWN',
            'drug': drug,
            'value': value,
            'unit': unit,
            'message': f'[SKIP] {drug} not in reference table — {value} {unit}',
            'ratio': None,
        }

    ref = DOSE_RANGES[drug]
    expected_unit = _normalize_unit(ref['unit'])
    given_unit = _normalize_unit(unit)

    if given_unit != expected_unit:
        return {
            'status': 'UNIT_MISMATCH',
            'drug': drug,
            'value': value,
            'unit': unit,
            'message': (
                f'[SKIP] {drug} unit mismatch: got {unit}, expected {ref["unit"]}'
            ),
            'ratio': None,
        }

    lo = ref['min']
    hi = ref['max']
    range_str = f'{lo}-{hi} {ref["unit"]}'

    if lo <= value <= hi:
        return {
            'status': 'OK',
            'drug': drug,
            'value': value,
            'unit': unit,
            'message': f'[OK] {drug} {value} {unit} (range: {range_str})',
            'ratio': None,
        }

    # Determine how far outside range
    if value > hi:
        ratio = round(value / hi, 1)
        direction = f'exceeds max by {ratio}x'
    else:
        ratio = round(lo / value, 1)
        direction = f'below min by {ratio}x'

    if ratio <= 5:
        status = 'WARNING'
        tag = 'WARNING'
    else:
        status = 'DANGER'
        tag = 'DANGER'

    return {
        'status': status,
        'drug': drug,
        'value': value,
        'unit': unit,
        'message': f'[{tag}] {drug} {value} {unit} (range: {range_str}) \u2014 {direction}',
        'ratio': ratio,
    }


def validate_document(text: str) -> dict:
    """Run full dosing validation on a document.

    Returns:
        claims   - list of raw extracted claims
        results  - list of validation result dicts
        has_danger  - bool
        has_warning - bool
        summary  - brief counts string
    """
    claims = extract_dosing_claims(text)
    results = []
    for claim in claims:
        result = validate_dose(claim['drug'], claim['value'], claim['unit'])
        result['drug_raw'] = claim['drug_raw']
        result['match_text'] = claim['match_text']
        results.append(result)

    has_danger = any(r['status'] == 'DANGER' for r in results)
    has_warning = any(r['status'] == 'WARNING' for r in results)

    counts = {s: sum(1 for r in results if r['status'] == s)
              for s in ('OK', 'WARNING', 'DANGER', 'UNKNOWN', 'UNIT_MISMATCH')}

    summary = (
        f'{counts["OK"]} OK, {counts["WARNING"]} WARNING, '
        f'{counts["DANGER"]} DANGER, '
        f'{counts["UNKNOWN"] + counts["UNIT_MISMATCH"]} skipped'
    )

    return {
        'claims': claims,
        'results': results,
        'has_danger': has_danger,
        'has_warning': has_warning,
        'summary': summary,
        'counts': counts,
    }


def main():
    parser = argparse.ArgumentParser(
        description='Validate drug dosing claims in a medical document'
    )
    parser.add_argument('file', help='Markdown or text file to check')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f'Error: File not found: {args.file}', file=sys.stderr)
        sys.exit(1)

    with open(args.file, encoding='utf-8') as f:
        text = f.read()

    report = validate_document(text)

    if args.json:
        # Remove non-serialisable internals if any; all fields are primitives
        print(json.dumps(report, indent=2))
    else:
        if not report['results']:
            print('No dosing claims detected.')
        else:
            for r in report['results']:
                print(r['message'])
            print()
            print(f'Summary: {report["summary"]}')

    sys.exit(1 if report['has_danger'] else 0)


if __name__ == '__main__':
    main()
