"""Shared pytest fixtures for medical evidence presenter tests."""

import sys
from pathlib import Path

import pytest

# Add scripts/ to path so we can import the modules
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

FILES_DIR = Path(__file__).resolve().parent / "files"
PROJECT_DIR = REPO_ROOT / "projects"


@pytest.fixture
def sample_raw():
    """Raw markdown before any processing."""
    return (FILES_DIR / "sample_raw.md").read_text()


@pytest.fixture
def sample_expected():
    """Expected markdown after full pipeline."""
    return (FILES_DIR / "sample_expected.md").read_text()


@pytest.fixture
def presentation_md():
    """The actual presentation.md content."""
    path = PROJECT_DIR / "presentation.md"
    if not path.exists():
        pytest.skip("project/presentation.md not found")
    return path.read_text()


@pytest.fixture
def sample_refs():
    """Reference lookup dict matching sample_raw.md.

    Note: build_ref_lookup includes the '- ' list prefix because the strip
    regex only removes leading asterisks. This matches actual behavior.
    """
    return {
        "1": "- Eastern Association for Surgery of Trauma. VTE in Trauma. https://www.east.org/",
        "2": "- Geerts WH, et al. Prevention of venous thromboembolism. Chest. 2008;133:381S-453S.",
        "3": "- Wu X, et al. Early VTE prophylaxis in severe TBI. J Trauma Acute Care Surg. 2023;95:94-104.",
        "4": "- Kerwin AJ, et al. Ann Surg. 2025;282(3):382-388. PMID: 40492307",
    }
