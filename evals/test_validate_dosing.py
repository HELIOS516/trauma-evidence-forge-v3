"""Tests for validate_dosing.py"""
import json
import os
import subprocess
import sys
import tempfile

import pytest

SCRIPT = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'validate_dosing.py')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from validate_dosing import extract_dosing_claims, validate_dose, validate_document


# ---------------------------------------------------------------------------
# extract_dosing_claims
# ---------------------------------------------------------------------------

def test_extract_weight_based_dose():
    claims = extract_dosing_claims('Ketamine 1.5 mg/kg was administered.')
    assert any(c['drug'] == 'ketamine' for c in claims)
    match = next(c for c in claims if c['drug'] == 'ketamine')
    assert match['value'] == 1.5
    assert match['unit'] == 'mg/kg'


def test_extract_infusion_rate():
    claims = extract_dosing_claims('Norepinephrine infusion at 8 mcg/min titrated.')
    assert any(c['drug'] == 'norepinephrine' for c in claims)
    match = next(c for c in claims if c['drug'] == 'norepinephrine')
    assert match['value'] == 8.0
    assert match['unit'] == 'mcg/min'


def test_extract_no_space_unit():
    """Handles dosing written without space between value and unit."""
    claims = extract_dosing_claims('Tranexamic acid 1 g IV push.')
    drugs = [c['drug'] for c in claims]
    assert 'tranexamic_acid' in drugs


def test_extract_multiple_drugs():
    text = (
        'Norepinephrine 10 mcg/min and vasopressin 0.03 units/min '
        'were both running on admission.'
    )
    claims = extract_dosing_claims(text)
    drugs = [c['drug'] for c in claims]
    assert 'norepinephrine' in drugs
    assert 'vasopressin' in drugs


def test_extract_empty_text_returns_empty():
    claims = extract_dosing_claims('')
    assert claims == []


def test_extract_no_drug_mentions_returns_empty():
    claims = extract_dosing_claims(
        'The patient was admitted to the ICU with hemodynamic instability.'
    )
    # No dosing pattern — should return empty or only unknowns
    for c in claims:
        assert c['drug'] is None


# ---------------------------------------------------------------------------
# validate_dose
# ---------------------------------------------------------------------------

def test_within_range_returns_ok():
    result = validate_dose('norepinephrine', 8.0, 'mcg/min')
    assert result['status'] == 'OK'
    assert '[OK]' in result['message']
    assert result['ratio'] is None


def test_slightly_above_max_returns_warning():
    # propofol max is 80 mcg/kg/min; 120 is 1.5x — WARNING territory (<=5x)
    result = validate_dose('propofol', 120.0, 'mcg/kg/min')
    assert result['status'] == 'WARNING'
    assert '[WARNING]' in result['message']
    assert result['ratio'] is not None
    assert result['ratio'] <= 5


def test_way_above_max_returns_danger():
    # vasopressin max is 0.04 units/min; 0.5 is 12.5x — DANGER
    result = validate_dose('vasopressin', 0.5, 'units/min')
    assert result['status'] == 'DANGER'
    assert '[DANGER]' in result['message']
    assert result['ratio'] > 5


def test_below_min_returns_warning():
    # norepinephrine min is 1 mcg/min; 0.4 is 2.5x below — WARNING
    result = validate_dose('norepinephrine', 0.4, 'mcg/min')
    assert result['status'] == 'WARNING'
    assert result['ratio'] is not None


def test_below_min_extreme_returns_danger():
    # norepinephrine min is 1 mcg/min; 0.05 is 20x below — DANGER
    result = validate_dose('norepinephrine', 0.05, 'mcg/min')
    assert result['status'] == 'DANGER'


def test_unknown_drug_is_skipped():
    result = validate_dose(None, 500.0, 'mg')
    assert result['status'] == 'UNKNOWN'
    assert '[SKIP]' in result['message']


def test_unknown_drug_name_string_is_skipped():
    result = validate_dose('cephalexin', 500.0, 'mg')
    assert result['status'] == 'UNKNOWN'


def test_unit_mismatch_is_skipped():
    # ketamine expects mg/kg; passing mg/min is a mismatch
    result = validate_dose('ketamine', 1.0, 'mg/min')
    assert result['status'] == 'UNIT_MISMATCH'
    assert '[SKIP]' in result['message']


def test_at_boundary_min_is_ok():
    result = validate_dose('fentanyl', 25.0, 'mcg/hr')
    assert result['status'] == 'OK'


def test_at_boundary_max_is_ok():
    result = validate_dose('fentanyl', 200.0, 'mcg/hr')
    assert result['status'] == 'OK'


# ---------------------------------------------------------------------------
# validate_document (integration)
# ---------------------------------------------------------------------------

def test_document_multiple_drugs_mixed_results():
    text = (
        'We started norepinephrine 8 mcg/min and vasopressin 0.03 units/min. '
        'Propofol sedation was at 120 mcg/kg/min. '
        'Mannitol 0.5 g/kg was given for ICP.'
    )
    report = validate_document(text)
    statuses = {r['status'] for r in report['results']}
    assert 'OK' in statuses          # norepinephrine and/or vasopressin
    assert 'WARNING' in statuses     # propofol 120


def test_document_clean_text_no_danger():
    text = 'Ketamine 1 mg/kg was used for induction before intubation.'
    report = validate_document(text)
    assert not report['has_danger']


def test_document_danger_sets_flag():
    # vasopressin 2.0 units/min is 50x above max — DANGER
    text = 'Vasopressin was infusing at 2.0 units/min on arrival.'
    report = validate_document(text)
    assert report['has_danger']


def test_document_no_drug_mentions_clean():
    text = 'The patient had an exploratory laparotomy for hemorrhage control.'
    report = validate_document(text)
    assert not report['has_danger']
    assert not report['has_warning']


# ---------------------------------------------------------------------------
# CLI integration
# ---------------------------------------------------------------------------

def _run_script(content: str, extra_args: list[str] | None = None) -> subprocess.CompletedProcess:
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.md', delete=False, encoding='utf-8'
    ) as f:
        f.write(content)
        fname = f.name
    try:
        cmd = [sys.executable, SCRIPT, fname] + (extra_args or [])
        return subprocess.run(cmd, capture_output=True, text=True)
    finally:
        os.unlink(fname)


def test_cli_exits_0_on_clean_document():
    result = _run_script('Ketamine 1 mg/kg induction dose given.')
    assert result.returncode == 0


def test_cli_exits_1_on_danger():
    result = _run_script('Vasopressin running at 2.0 units/min.')
    assert result.returncode == 1


def test_cli_json_output_is_valid():
    result = _run_script(
        'Norepinephrine 8 mcg/min and propofol 120 mcg/kg/min.',
        extra_args=['--json'],
    )
    assert result.returncode == 0  # no DANGER here
    data = json.loads(result.stdout)
    assert 'results' in data
    assert 'has_danger' in data
    assert 'summary' in data


def test_cli_missing_file_exits_nonzero():
    result = subprocess.run(
        [sys.executable, SCRIPT, '/tmp/nonexistent_dosing_file_xyz.md'],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
