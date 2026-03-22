"""Integration tests for the 5-script Gamma pipeline.

Tests the full pipeline on evals/files/sample_raw.md:
    format_citations.py -> preprocess_for_gamma.py -> audit_slide_design.py -> validate_gamma_ready.py

generate_gamma_params.py is skipped because it depends on the optional
gamma-presentation-core sibling skill.
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / 'scripts'
FILES_DIR = Path(__file__).resolve().parent / 'files'
SAMPLE_RAW = FILES_DIR / 'sample_raw.md'
PYTHON = sys.executable


def run_script(script_name: str, *args) -> subprocess.CompletedProcess:
    """Run a pipeline script and return the CompletedProcess."""
    script = str(SCRIPTS_DIR / script_name)
    return subprocess.run(
        [PYTHON, script] + list(args),
        capture_output=True,
        text=True,
    )


class TestPipelineIntegration:
    """Run the 4-script pipeline end-to-end on sample_raw.md."""

    def test_sample_raw_fixture_exists(self):
        assert SAMPLE_RAW.exists(), f"Test fixture not found: {SAMPLE_RAW}"

    def test_format_citations_runs(self):
        """format_citations.py should process sample_raw.md without error."""
        with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as tmp:
            tmp_path = tmp.name
        try:
            result = run_script(
                'format_citations.py',
                str(SAMPLE_RAW),
                '--output', tmp_path,
            )
            assert result.returncode == 0, (
                f"format_citations.py failed:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
            )
            output = Path(tmp_path).read_text(encoding='utf-8')
            assert len(output) > 0, "format_citations.py produced empty output"
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_preprocess_accepts_format_citations_output(self):
        """preprocess_for_gamma.py should accept format_citations.py output."""
        with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as tmp1:
            fc_out = tmp1.name
        with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as tmp2:
            pp_out = tmp2.name
        try:
            # Step 1: format_citations
            r1 = run_script('format_citations.py', str(SAMPLE_RAW), '--output', fc_out)
            assert r1.returncode == 0, f"format_citations.py failed: {r1.stderr}"

            # Step 2: preprocess_for_gamma
            r2 = run_script('preprocess_for_gamma.py', fc_out, '--output', pp_out)
            assert r2.returncode == 0, (
                f"preprocess_for_gamma.py failed:\nSTDOUT: {r2.stdout}\nSTDERR: {r2.stderr}"
            )
            output = Path(pp_out).read_text(encoding='utf-8')
            assert len(output) > 0, "preprocess_for_gamma.py produced empty output"
            # Should have removed *** separators
            assert '***' not in output, "preprocess_for_gamma.py should remove *** separators"
            # Should have no SLIDE markers
            assert '### SLIDE' not in output, "preprocess_for_gamma.py should remove SLIDE markers"
        finally:
            Path(fc_out).unlink(missing_ok=True)
            Path(pp_out).unlink(missing_ok=True)

    def test_audit_accepts_preprocess_output(self):
        """audit_slide_design.py should run on preprocessed output without crashing."""
        with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as tmp1:
            fc_out = tmp1.name
        with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as tmp2:
            pp_out = tmp2.name
        try:
            r1 = run_script('format_citations.py', str(SAMPLE_RAW), '--output', fc_out)
            assert r1.returncode == 0, f"format_citations.py failed: {r1.stderr}"

            r2 = run_script('preprocess_for_gamma.py', fc_out, '--output', pp_out)
            assert r2.returncode == 0, f"preprocess_for_gamma.py failed: {r2.stderr}"

            # audit_slide_design has its own exit codes — just check it doesn't crash (exit 2+)
            r3 = run_script('audit_slide_design.py', pp_out)
            assert r3.returncode < 2, (
                f"audit_slide_design.py crashed (exit {r3.returncode}):\n"
                f"STDOUT: {r3.stdout}\nSTDERR: {r3.stderr}"
            )
        finally:
            Path(fc_out).unlink(missing_ok=True)
            Path(pp_out).unlink(missing_ok=True)

    def test_validate_accepts_preprocess_output(self):
        """validate_gamma_ready.py should accept preprocessed output (exit code 0 or 1, not crash)."""
        with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as tmp1:
            fc_out = tmp1.name
        with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as tmp2:
            pp_out = tmp2.name
        try:
            r1 = run_script('format_citations.py', str(SAMPLE_RAW), '--output', fc_out)
            assert r1.returncode == 0, f"format_citations.py failed: {r1.stderr}"

            r2 = run_script('preprocess_for_gamma.py', fc_out, '--output', pp_out)
            assert r2.returncode == 0, f"preprocess_for_gamma.py failed: {r2.stderr}"

            r4 = run_script('validate_gamma_ready.py', pp_out)
            # Exit 0 = all gates pass, exit 1 = soft warnings — both are acceptable for pipeline
            # Exit 2+ would indicate a crash
            assert r4.returncode <= 1, (
                f"validate_gamma_ready.py crashed (exit {r4.returncode}):\n"
                f"STDOUT: {r4.stdout}\nSTDERR: {r4.stderr}"
            )
        finally:
            Path(fc_out).unlink(missing_ok=True)
            Path(pp_out).unlink(missing_ok=True)

    def test_full_pipeline_no_html_comments_remain(self):
        """After preprocessing, no HTML comments should remain in output."""
        with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as tmp1:
            fc_out = tmp1.name
        with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as tmp2:
            pp_out = tmp2.name
        try:
            r1 = run_script('format_citations.py', str(SAMPLE_RAW), '--output', fc_out)
            assert r1.returncode == 0

            r2 = run_script('preprocess_for_gamma.py', fc_out, '--output', pp_out)
            assert r2.returncode == 0

            content = Path(pp_out).read_text(encoding='utf-8')
            import re
            html_comments = re.findall(r'<!--.*?-->', content, re.DOTALL)
            assert html_comments == [], f"HTML comments remain after preprocessing: {html_comments}"
        finally:
            Path(fc_out).unlink(missing_ok=True)
            Path(pp_out).unlink(missing_ok=True)

    def test_full_pipeline_has_card_separators(self):
        """After preprocessing, content should use --- as card separators."""
        with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as tmp1:
            fc_out = tmp1.name
        with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as tmp2:
            pp_out = tmp2.name
        try:
            r1 = run_script('format_citations.py', str(SAMPLE_RAW), '--output', fc_out)
            assert r1.returncode == 0

            r2 = run_script('preprocess_for_gamma.py', fc_out, '--output', pp_out)
            assert r2.returncode == 0

            content = Path(pp_out).read_text(encoding='utf-8')
            assert '\n---\n' in content, "Preprocessed output should contain --- card separators"
        finally:
            Path(fc_out).unlink(missing_ok=True)
            Path(pp_out).unlink(missing_ok=True)
