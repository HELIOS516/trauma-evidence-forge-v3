"""Tests for scripts/check_staleness.py"""
import os
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

import pytest

SCRIPT = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'check_staleness.py')

# Import the module under test directly for unit-level tests.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from check_staleness import check_file, check_staleness  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_tree(base: Path, files: dict[str, str]):
    """Create a directory tree from a {relative_path: content} dict."""
    for rel, content in files.items():
        full = base / rel
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content, encoding='utf-8')


# ---------------------------------------------------------------------------
# 1. File with valid recent date passes
# ---------------------------------------------------------------------------

def test_recent_date_is_fresh():
    """A file dated today should be reported as fresh."""
    today = date.today()
    content = f"# Doc\n\nLast updated: {today.strftime('%B %Y')}\n\nSome content here.\n"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False,
                                     encoding='utf-8') as f:
        f.write(content)
        path = f.name
    try:
        result = check_file(path, max_age_days=365, today=today)
        assert result['status'] == 'fresh', f"Expected fresh, got: {result}"
    finally:
        os.unlink(path)


# ---------------------------------------------------------------------------
# 2. File with old date flags as stale
# ---------------------------------------------------------------------------

def test_old_date_is_stale():
    """A file dated more than max_age_days ago should be flagged stale."""
    today = date.today()
    old_date = today - timedelta(days=400)
    content = f"# Doc\n\nLast updated: {old_date.isoformat()}\n\nContent.\n"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False,
                                     encoding='utf-8') as f:
        f.write(content)
        path = f.name
    try:
        result = check_file(path, max_age_days=365, today=today)
        assert result['status'] == 'stale', f"Expected stale, got: {result}"
        assert result['age_days'] == 400
    finally:
        os.unlink(path)


# ---------------------------------------------------------------------------
# 3. File with no date metadata flags as undated
# ---------------------------------------------------------------------------

def test_no_date_metadata_is_undated():
    """A file with no version/date line should be flagged undated."""
    content = "# Module Overview\n\nThis document describes the module.\n"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False,
                                     encoding='utf-8') as f:
        f.write(content)
        path = f.name
    try:
        result = check_file(path, max_age_days=365)
        assert result['status'] == 'undated', f"Expected undated, got: {result}"
        assert result['date'] is None
        assert result['age_days'] is None
    finally:
        os.unlink(path)


# ---------------------------------------------------------------------------
# 4. Custom --max-age-days threshold works
# ---------------------------------------------------------------------------

def test_custom_max_age_days():
    """A file 30 days old should be fresh at 60-day threshold but stale at 20-day threshold."""
    today = date.today()
    file_date = today - timedelta(days=30)
    content = f"# Doc\n\nLast updated: {file_date.isoformat()}\n\nContent.\n"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False,
                                     encoding='utf-8') as f:
        f.write(content)
        path = f.name
    try:
        fresh = check_file(path, max_age_days=60, today=today)
        assert fresh['status'] == 'fresh', f"Expected fresh at 60d threshold: {fresh}"

        stale = check_file(path, max_age_days=20, today=today)
        assert stale['status'] == 'stale', f"Expected stale at 20d threshold: {stale}"
    finally:
        os.unlink(path)


# ---------------------------------------------------------------------------
# 5. Non-markdown files are ignored
# ---------------------------------------------------------------------------

def test_non_markdown_files_ignored():
    """Only .md files should be scanned; .txt, .py, .rst files are ignored."""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        _make_tree(base, {
            'modules/note.txt': 'No date here at all.',
            'modules/script.py': '# python file, no date',
            'modules/readme.rst': 'RST file, no date',
        })
        summary = check_staleness(tmpdir, max_age_days=365)
        assert summary['total'] == 0, f"Expected 0 files scanned, got {summary['total']}"
        assert summary['clean'] is True


# ---------------------------------------------------------------------------
# 6. Empty directory returns clean
# ---------------------------------------------------------------------------

def test_empty_directory_is_clean():
    """A project with no .md files in scan dirs should return clean with total=0."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create the scan dirs but leave them empty
        for d in ('modules', 'templates', 'docs'):
            (Path(tmpdir) / d).mkdir()
        summary = check_staleness(tmpdir, max_age_days=365)
        assert summary['total'] == 0
        assert summary['clean'] is True
        assert summary['stale'] == []
        assert summary['undated'] == []


# ---------------------------------------------------------------------------
# 7. Multiple files with mixed status
# ---------------------------------------------------------------------------

def test_mixed_file_statuses():
    """Directory with fresh, stale, and undated files should report all three."""
    today = date.today()
    recent = today - timedelta(days=10)
    old = today - timedelta(days=500)

    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        _make_tree(base, {
            'modules/fresh.md': f"# Fresh\n\nLast updated: {recent.isoformat()}\n\nContent.\n",
            'modules/stale.md': f"# Stale\n\nLast updated: {old.isoformat()}\n\nContent.\n",
            'modules/undated.md': "# Undated\n\nNo version info here.\n",
        })
        summary = check_staleness(tmpdir, max_age_days=365)

    assert summary['total'] == 3
    assert len(summary['fresh']) == 1
    assert len(summary['stale']) == 1
    assert len(summary['undated']) == 1
    assert summary['clean'] is False
    assert summary['fresh'][0].endswith('fresh.md')
    assert summary['stale'][0].endswith('stale.md')
    assert summary['undated'][0].endswith('undated.md')


# ---------------------------------------------------------------------------
# 8. Date format variations
# ---------------------------------------------------------------------------

def test_date_format_last_updated_month_year():
    """'Last updated: March 2026' should parse to 2026-03-01."""
    today = date(2026, 3, 2)
    content = "# Checklist\n\nLast updated: March 2026\n\nContent.\n"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False,
                                     encoding='utf-8') as f:
        f.write(content)
        path = f.name
    try:
        result = check_file(path, max_age_days=365, today=today)
        assert result['status'] == 'fresh'
        assert result['date'] == date(2026, 3, 1)
    finally:
        os.unlink(path)


def test_date_format_version_with_parens():
    """'Version: 1.0 (March 2026)' should parse the date correctly."""
    today = date(2026, 3, 2)
    content = "# Module\n\nVersion: 1.0 (March 2026)\n\nContent.\n"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False,
                                     encoding='utf-8') as f:
        f.write(content)
        path = f.name
    try:
        result = check_file(path, max_age_days=365, today=today)
        assert result['status'] == 'fresh'
        assert result['date'] == date(2026, 3, 1)
    finally:
        os.unlink(path)


def test_date_format_h2_version_iso():
    """'## Version\\nv1.0 — 2026-03-01' should detect the ISO date."""
    today = date(2026, 3, 2)
    content = "# Module\n\n## Version\nv1.0 — 2026-03-01\n\nContent.\n"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False,
                                     encoding='utf-8') as f:
        f.write(content)
        path = f.name
    try:
        result = check_file(path, max_age_days=365, today=today)
        assert result['status'] == 'fresh'
        assert result['date'] == date(2026, 3, 1)
    finally:
        os.unlink(path)


# ---------------------------------------------------------------------------
# CLI integration tests
# ---------------------------------------------------------------------------

def test_script_exists():
    assert os.path.exists(SCRIPT), f"Script not found: {SCRIPT}"


def test_script_help():
    result = subprocess.run(
        [sys.executable, SCRIPT, '--help'],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert '--max-age-days' in result.stdout


def test_cli_exits_0_on_clean_directory():
    """CLI should exit 0 when all files are fresh."""
    today = date.today()
    recent = today - timedelta(days=10)
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        _make_tree(base, {
            'modules/doc.md': f"# Doc\n\nLast updated: {recent.isoformat()}\n\nContent.\n",
        })
        result = subprocess.run(
            [sys.executable, SCRIPT, tmpdir, '--max-age-days', '365'],
            capture_output=True, text=True,
        )
    assert result.returncode == 0, f"Expected exit 0, stdout: {result.stdout}"


def test_cli_exits_1_on_stale_files():
    """CLI should exit 1 when stale files are found."""
    today = date.today()
    old = today - timedelta(days=400)
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        _make_tree(base, {
            'modules/old.md': f"# Doc\n\nLast updated: {old.isoformat()}\n\nContent.\n",
        })
        result = subprocess.run(
            [sys.executable, SCRIPT, tmpdir, '--max-age-days', '365'],
            capture_output=True, text=True,
        )
    assert result.returncode == 1, f"Expected exit 1, stdout: {result.stdout}"
    assert 'STALE' in result.stdout


def test_cli_missing_directory_exits_1():
    """CLI should exit 1 and print an error for a nonexistent directory."""
    result = subprocess.run(
        [sys.executable, SCRIPT, '/nonexistent/path/that/does/not/exist'],
        capture_output=True, text=True,
    )
    assert result.returncode == 1
    assert 'Error' in result.stderr
