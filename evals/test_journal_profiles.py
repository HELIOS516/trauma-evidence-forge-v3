"""Tests for config/journal-profiles.json correctness and completeness."""

import json
import pathlib
import pytest

PROFILES_PATH = pathlib.Path(__file__).parent.parent / "config" / "journal-profiles.json"

REQUIRED_FIELDS = {
    "id",
    "name",
    "abbreviation",
    "publisher",
    "citation_style",
    "max_abstract_words",
    "max_manuscript_words",
    "max_references",
    "structured_abstract",
    "abstract_sections",
    "requires_checklist",
    "accepted_checklists",
    "reference_format",
    "doi_required",
    "pmid_preferred",
    "open_access_option",
    "level_of_evidence_required",
    "study_type_in_title",
}

EXPECTED_JOURNAL_IDS = {
    "jtacs",
    "jacs",
    "annals",
    "surgery",
    "ajs",
    "jsr",
    "tsaco",
    "wjes",
    "injury",
    "ccm",
}

VALID_CITATION_STYLES = {"vancouver", "apa", "harvard"}
VALID_REFERENCE_FORMATS = {"numbered", "author-date"}


@pytest.fixture(scope="module")
def profiles_data():
    with open(PROFILES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def journals(profiles_data):
    return profiles_data["journals"]


def test_json_file_is_valid_and_parseable():
    """JSON file must exist and parse without errors."""
    assert PROFILES_PATH.exists(), f"File not found: {PROFILES_PATH}"
    with open(PROFILES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, dict)
    assert "journals" in data


def test_all_10_journals_present(journals):
    """All 10 required journals must be present."""
    found_ids = {j["id"] for j in journals}
    missing = EXPECTED_JOURNAL_IDS - found_ids
    assert not missing, f"Missing journal IDs: {missing}"
    assert len(journals) == 10, f"Expected 10 journals, found {len(journals)}"


@pytest.mark.parametrize("journal_id", sorted(EXPECTED_JOURNAL_IDS))
def test_each_profile_has_required_fields(journals, journal_id):
    """Every profile must contain all required fields."""
    journal = next((j for j in journals if j["id"] == journal_id), None)
    assert journal is not None, f"Journal '{journal_id}' not found"
    missing = REQUIRED_FIELDS - set(journal.keys())
    assert not missing, f"Journal '{journal_id}' missing fields: {missing}"


def test_no_duplicate_ids(journals):
    """Journal IDs must be unique."""
    ids = [j["id"] for j in journals]
    duplicates = {id_ for id_ in ids if ids.count(id_) > 1}
    assert not duplicates, f"Duplicate journal IDs: {duplicates}"


@pytest.mark.parametrize("journal_id", sorted(EXPECTED_JOURNAL_IDS))
def test_citation_style_is_valid(journals, journal_id):
    """citation_style must be one of the accepted values."""
    journal = next(j for j in journals if j["id"] == journal_id)
    assert journal["citation_style"] in VALID_CITATION_STYLES, (
        f"Journal '{journal_id}' has invalid citation_style: '{journal['citation_style']}'. "
        f"Must be one of {VALID_CITATION_STYLES}"
    )


@pytest.mark.parametrize("journal_id", sorted(EXPECTED_JOURNAL_IDS))
def test_abstract_word_limit_is_reasonable(journals, journal_id):
    """max_abstract_words must be between 100 and 1000."""
    journal = next(j for j in journals if j["id"] == journal_id)
    limit = journal["max_abstract_words"]
    assert isinstance(limit, int), f"Journal '{journal_id}' max_abstract_words must be int"
    assert 100 <= limit <= 1000, (
        f"Journal '{journal_id}' max_abstract_words={limit} is outside range [100, 1000]"
    )


@pytest.mark.parametrize("journal_id", sorted(EXPECTED_JOURNAL_IDS))
def test_manuscript_word_limit_is_reasonable(journals, journal_id):
    """max_manuscript_words must be between 2000 and 10000."""
    journal = next(j for j in journals if j["id"] == journal_id)
    limit = journal["max_manuscript_words"]
    assert isinstance(limit, int), f"Journal '{journal_id}' max_manuscript_words must be int"
    assert 2000 <= limit <= 10000, (
        f"Journal '{journal_id}' max_manuscript_words={limit} is outside range [2000, 10000]"
    )


@pytest.mark.parametrize("journal_id", sorted(EXPECTED_JOURNAL_IDS))
def test_reference_format_is_valid(journals, journal_id):
    """reference_format must be one of the accepted values."""
    journal = next(j for j in journals if j["id"] == journal_id)
    assert journal["reference_format"] in VALID_REFERENCE_FORMATS, (
        f"Journal '{journal_id}' has invalid reference_format: '{journal['reference_format']}'. "
        f"Must be one of {VALID_REFERENCE_FORMATS}"
    )


@pytest.mark.parametrize("journal_id", sorted(EXPECTED_JOURNAL_IDS))
def test_boolean_fields_are_bool(journals, journal_id):
    """All boolean fields must be actual booleans, not strings or integers."""
    bool_fields = {
        "structured_abstract",
        "requires_checklist",
        "doi_required",
        "pmid_preferred",
        "open_access_option",
        "level_of_evidence_required",
        "study_type_in_title",
    }
    journal = next(j for j in journals if j["id"] == journal_id)
    for field in bool_fields:
        val = journal[field]
        assert isinstance(val, bool), (
            f"Journal '{journal_id}' field '{field}' must be bool, got {type(val).__name__}"
        )


@pytest.mark.parametrize("journal_id", sorted(EXPECTED_JOURNAL_IDS))
def test_abstract_sections_consistent_with_structured(journals, journal_id):
    """If structured_abstract is True, abstract_sections must be non-empty, and vice versa."""
    journal = next(j for j in journals if j["id"] == journal_id)
    structured = journal["structured_abstract"]
    sections = journal["abstract_sections"]
    assert isinstance(sections, list), (
        f"Journal '{journal_id}' abstract_sections must be a list"
    )
    if structured:
        assert len(sections) > 0, (
            f"Journal '{journal_id}' has structured_abstract=true but empty abstract_sections"
        )
    else:
        assert len(sections) == 0, (
            f"Journal '{journal_id}' has structured_abstract=false but non-empty abstract_sections: {sections}"
        )


@pytest.mark.parametrize("journal_id", sorted(EXPECTED_JOURNAL_IDS))
def test_accepted_checklists_is_non_empty_list(journals, journal_id):
    """accepted_checklists must be a non-empty list of strings."""
    journal = next(j for j in journals if j["id"] == journal_id)
    checklists = journal["accepted_checklists"]
    assert isinstance(checklists, list), (
        f"Journal '{journal_id}' accepted_checklists must be a list"
    )
    assert len(checklists) > 0, (
        f"Journal '{journal_id}' accepted_checklists must not be empty"
    )
    for item in checklists:
        assert isinstance(item, str), (
            f"Journal '{journal_id}' accepted_checklists entries must be strings, got {type(item).__name__}"
        )


@pytest.mark.parametrize("journal_id", sorted(EXPECTED_JOURNAL_IDS))
def test_max_references_positive(journals, journal_id):
    """max_references must be a positive integer."""
    journal = next(j for j in journals if j["id"] == journal_id)
    refs = journal["max_references"]
    assert isinstance(refs, int), f"Journal '{journal_id}' max_references must be int"
    assert refs > 0, f"Journal '{journal_id}' max_references must be positive"
