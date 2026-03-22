"""Tests for validate_manuscript.py"""
import subprocess
import sys
import os
import json
import tempfile
import pytest

SCRIPT = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'validate_manuscript.py')


def test_script_exists():
    assert os.path.exists(SCRIPT)


def test_help():
    result = subprocess.run([sys.executable, SCRIPT, '--help'], capture_output=True, text=True)
    assert result.returncode == 0


def test_complete_manuscript_passes():
    """A well-formed manuscript should pass all hard gates."""
    manuscript = """# Early VTE Prophylaxis in Trauma

## Abstract
Background: VTE is common in trauma. Methods: We randomized 200 patients.
Results: VTE rate was lower. Conclusions: Early prophylaxis works.

## Introduction
Venous thromboembolism affects 20% of trauma patients[1]. Current guidelines
recommend early prophylaxis[2]. The knowledge gap is timing optimization[3].

## Methods
This was a randomized controlled trial at a Level 1 trauma center. Patients with
ISS > 15 were enrolled between Jan 2020 and Dec 2023. Sample size was calculated
assuming 40% VTE reduction with alpha 0.05 and power 0.80.

## Results
VTE rate was 5.3% vs 8.1% (OR 0.63, 95% CI 0.45-0.88, p=0.007)[1]. GRADE: 1B.
Secondary endpoints showed reduced PE (1.2% vs 3.4%, p=0.02)[2].

## Discussion
Our findings support early prophylaxis in trauma patients. These results align
with prior work from Level I centers[2]. The magnitude of effect suggests
clinical relevance beyond statistical significance[3]. Limitations include
single-center design and retrospective data collection.

## References
O'Toole RV, et al. PREVENT CLOT. N Engl J Med. 2023. PMID: 36652353 [1]
Wu X, et al. Early VTE in TBI. J Trauma. 2023. PMID: 36626625 [2]
Knudson MM, et al. VTE Prophylaxis. J Trauma. 2022. PMID: 35100156 [3]
Geerts WH, et al. DVT Prevention. Chest. 2008. PMID: 18574271 [4]
Rappold JF, et al. VTE in Trauma. J Trauma. 2021. PMID: 33060495 [5]
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(manuscript)
        f.flush()
        result = subprocess.run([sys.executable, SCRIPT, f.name, '--json'], capture_output=True, text=True)
    os.unlink(f.name)
    data = json.loads(result.stdout)
    assert data['overall'] == 'PASS'
    assert data['hard_fail'] == 0


def test_missing_sections_fails():
    """A manuscript missing key sections should fail."""
    manuscript = """# Some Paper

## Introduction
This is the intro with a citation[1].

## References
Ref Author. Title. Journal. 2023. PMID: 12345678 [1]
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(manuscript)
        f.flush()
        result = subprocess.run([sys.executable, SCRIPT, f.name, '--json'], capture_output=True, text=True)
    os.unlink(f.name)
    data = json.loads(result.stdout)
    assert data['hard_fail'] > 0
