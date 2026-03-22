"""Tests for detect_ai_patterns.py"""
import subprocess
import sys
import os
import tempfile
import pytest

SCRIPT = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'detect_ai_patterns.py')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


def test_script_exists():
    assert os.path.exists(SCRIPT)


def test_script_runs():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write('This is a test sentence for analysis.')
        f.flush()
        result = subprocess.run([sys.executable, SCRIPT, f.name, '--json'], capture_output=True, text=True)
    os.unlink(f.name)
    assert result.returncode == 0


def test_detects_ai_hedging():
    from detect_ai_patterns import score_hedging
    ai_text = ('It is important to note that the results show improvement. '
               'It should be noted that further research is needed. '
               'It is worth mentioning that outcomes varied.')
    result = score_hedging(ai_text)
    assert result['score'] > 0
    assert result['count'] >= 2


def test_detects_transitions():
    from detect_ai_patterns import score_transitions
    text = ('Furthermore, results improved. Moreover, outcomes were better. '
            'Additionally, costs decreased. Nevertheless, challenges remained.')
    result = score_transitions(text)
    assert result['score'] > 0
    assert result['count'] >= 3


def test_sentence_uniformity():
    from detect_ai_patterns import score_sentence_uniformity
    uniform = ('The study showed significant results in the population. '
               'The analysis revealed important findings for patients. '
               'The data demonstrated meaningful improvements in outcomes. '
               'The research indicated substantial changes in metrics. '
               'The investigation uncovered notable patterns in data. '
               'The evaluation confirmed positive trends in treatment. ')
    result_uniform = score_sentence_uniformity(uniform)

    varied = ('Results improved. '
              'The comprehensive retrospective analysis of 847 trauma patients enrolled between '
              'January 2020 and December 2023 at our Level 1 trauma center demonstrated a '
              'statistically significant reduction in 28-day mortality. '
              'We found no difference. '
              'Importantly, the subgroup with ISS greater than 25 showed the most dramatic benefit. '
              'TXA worked.')
    result_varied = score_sentence_uniformity(varied)

    assert result_uniform['score'] >= result_varied['score']


def test_natural_surgical_text():
    from detect_ai_patterns import analyze
    text = (
        'We enrolled 847 trauma patients (ISS > 15) between Jan 2020 and Dec 2023. '
        'Blunt mechanism predominated (n=612, 72%). The primary endpoint -- 28-day '
        'mortality -- was 11.2% in the intervention arm vs 18.7% in controls '
        '(OR 0.55, 95% CI 0.38-0.79, p=0.001). Three patients developed ARDS '
        'requiring ECMO cannulation. Given the retrospective design, our findings '
        'should be interpreted with caution. TXA was administered within 3 hours of injury '
        'per our MTP protocol. MAP targets were maintained above 65 mmHg.'
    )
    result = analyze(text)
    assert result['overall_score'] < 40


def test_ai_generated_text():
    from detect_ai_patterns import analyze
    text = (
        'It is important to note that this comprehensive analysis demonstrates significant '
        'findings regarding surgical outcomes. Furthermore, the robust methodology employed '
        'in this study provides valuable insights into the complex interplay between various '
        'clinical factors. Moreover, these results have important implications for clinical '
        'practice. Additionally, the data suggest that further research is needed to fully '
        'understand the multifaceted nature of surgical care delivery. It should be noted '
        'that several key factors contribute to these outcomes. The results indicate that '
        'a comprehensive approach is essential for optimal patient care. Furthermore, the '
        'findings highlight the critical importance of evidence-based decision-making.'
    )
    result = analyze(text)
    assert result['overall_score'] > 40
