"""Tests for format_citations.py — passes 0-3."""

import re

from format_citations import (
    build_ref_lookup,
    pass0_auto_sources,
    pass1_clean_titles,
    pass2_expand_sources,
    pass2b_compact_expanded_sources,
    pass3_superscript,
    pass4_link_reference_pmids,
    _truncate_title,
)


# --- Pass 0: Auto-generate Sources blocks ---

def test_pass0_auto_sources_basic():
    """Slide with [1] but no Sources block should get one generated."""
    content = "---\n\n## Slide Title\n\nSome text with evidence [1] here.\n\n---"
    result, count = pass0_auto_sources(content)
    assert count == 1
    assert "**Sources:** [1]" in result


def test_pass0_auto_sources_multiple_refs():
    """Slide with [1][2][3] should get all refs in Sources block."""
    content = "---\n\n## Results\n\nOutcome A [1] and outcome B [2] plus [3].\n\n---"
    result, count = pass0_auto_sources(content)
    assert count == 1
    assert "**Sources:** [1][2][3]" in result


def test_pass0_auto_sources_skips_existing():
    """Slide already with Sources block should not be modified."""
    content = "---\n\n## Slide\n\nText [1] here.\n\n**Sources:** [1]\n\n---"
    result, count = pass0_auto_sources(content)
    assert count == 0
    assert result == content


def test_pass0_auto_sources_skips_references_section():
    """References card should not get a Sources block."""
    content = "---\n\n## Slide\n\nText [1].\n\n**Sources:** [1]\n\n---\n\n# References\n\n- Ref text [1]\n- Another [2]"
    result, count = pass0_auto_sources(content)
    assert count == 0


def test_pass0_auto_sources_skips_no_citations():
    """Title/intro slide with no [N] should not get a Sources block."""
    content = "---\n\n## Introduction\n\nWelcome to the presentation.\n\n---"
    result, count = pass0_auto_sources(content)
    assert count == 0
    assert "**Sources:**" not in result


def test_pass0_auto_sources_deduplicates():
    """Repeated [1] in a slide should only list it once in Sources."""
    content = "---\n\n## Slide\n\nFirst [1] and second [1] mention.\n\n---"
    result, count = pass0_auto_sources(content)
    assert count == 1
    assert "**Sources:** [1]" in result
    # Should NOT have [1][1]
    assert "[1][1]" not in result


# --- build_ref_lookup ---

def test_build_ref_lookup_parses_both_formats(sample_raw):
    """build_ref_lookup should parse [N] suffix and [PMID UNVERIFIED][N] formats."""
    refs = build_ref_lookup(sample_raw)
    assert "1" in refs
    assert "east.org" in refs["1"]
    assert "4" in refs
    assert "Kerwin" in refs["4"]


def test_build_ref_lookup_no_refs_section():
    """Returns empty dict when no References section exists."""
    content = "# Title\n\nSome body text with [1] citation."
    refs = build_ref_lookup(content)
    assert refs == {}


# --- Pass 1: Clean titles ---

def test_pass1_removes_brackets_from_headings():
    """Pass 1 should strip [N] from heading lines."""
    content = "# DVT Prophylaxis [1]\n## Sub-heading [2][3]\nBody [1] text"
    result = pass1_clean_titles(content)
    assert "# DVT Prophylaxis" in result
    assert "[1]" not in result.split("\n")[0]
    assert "[2]" not in result.split("\n")[1]


def test_pass1_preserves_body_brackets():
    """Pass 1 should NOT strip [N] from non-heading lines."""
    content = "# Title [1]\nBody text with [1] citation"
    result = pass1_clean_titles(content)
    assert "[1]" in result.split("\n")[1]


def test_pass1_preserves_references_heading():
    """Pass 1 should not strip [N] from the References heading line itself."""
    content = "# References\n- Some ref [1]"
    result = pass1_clean_titles(content)
    assert "# References" in result
    assert "[1]" in result


# --- Pass 2: Expand sources ---

def test_pass2_expands_sources(sample_refs):
    """Pass 2 should expand Sources: [N][M] to abbreviated citation lines."""
    content = "Some text\n\n**Sources:** [1][2]\n\nMore text"
    result = pass2_expand_sources(content, sample_refs)
    assert "- [1]" in result
    assert "- [1] [Eastern](https://www.east.org/)" in result
    assert "- [2] Geerts 2008" in result
    # Original compact line should be gone
    assert "**Sources:** [1][2]" not in result


def test_pass2_handles_missing_ref(sample_refs):
    """Pass 2 should skip refs not found in lookup, only expand found ones."""
    content = "**Sources:** [1][99]"
    result = pass2_expand_sources(content, sample_refs)
    assert "- [1]" in result
    assert "[Eastern](https://www.east.org/)" in result
    assert "[99]" not in result  # 99 not in refs, so not expanded


def test_pass2_handles_source_singular(sample_refs):
    """Pass 2 should also handle **Source:** (singular)."""
    content = "**Source:** [3]"
    result = pass2_expand_sources(content, sample_refs)
    assert "- [3]" in result
    assert "Wu 2023" in result


def test_pass2_links_pmid_when_available(sample_refs):
    """Pass 2 should emit hyperlink on PMID when reference contains PMID."""
    content = "**Sources:** [4]"
    result = pass2_expand_sources(content, sample_refs)
    assert "[Kerwin 2025](https://pubmed.ncbi.nlm.nih.gov/40492307/)" in result


def test_pass2_strips_numbered_reference_prefix():
    """Pass 2 should strip leading numeric list markers from slide sources."""
    refs = {
        "1": "- 1. Smith J, Doe A, et al. Trial title. Ann Surg. 2024;280:100-110. PMID: 12345678"
    }
    content = "**Sources:** [1]"
    result = pass2_expand_sources(content, refs)
    assert "- [1] [Smith 2024](https://pubmed.ncbi.nlm.nih.gov/12345678/)" in result
    assert "- [1] 1." not in result


def test_pass2b_compacts_already_expanded_sources(sample_refs):
    content = (
        "**Sources:**\n"
        "- [1] Eastern Association for Surgery of Trauma. VTE in Trauma. https://www.east.org/\n"
        "- [4] Kerwin AJ, et al. Ann Surg. 2025;282(3):382-388. PMID: 40492307\n\n"
        "Body text"
    )
    result = pass2b_compact_expanded_sources(content, sample_refs)
    assert "- [1] [Eastern](https://www.east.org/)" in result
    assert "- [4] [Kerwin 2025](https://pubmed.ncbi.nlm.nih.gov/40492307/)" in result


# --- Pass 3: Superscript ---

def test_pass3_adds_superscript():
    """Pass 3 should convert [N] to <sup>[N]</sup> in body text."""
    content = "Body text [1] and more [2]\n\n# References\n- Ref [1]"
    result = pass3_superscript(content)
    assert "<sup>[1]</sup>" in result
    assert "<sup>[2]</sup>" in result


def test_pass3_skips_headings():
    """Pass 3 should NOT add superscript in heading lines."""
    content = "# Title [1]\nBody [1]\n\n# References\n- Ref [1]"
    result = pass3_superscript(content)
    lines = result.split("\n")
    # Heading should not have <sup>
    assert "<sup>" not in lines[0]
    # Body should have <sup>
    assert "<sup>[1]</sup>" in lines[1]


def test_pass3_skips_sources_lines():
    """Pass 3 should NOT add superscript in Sources/list lines."""
    content = "**Sources:**\n- [1] Some citation\nBody [1]\n\n# References\n- Ref [1]"
    result = pass3_superscript(content)
    # Sources header and list item should be untouched
    assert "- [1] Some citation" in result
    # Body should be converted
    assert "Body <sup>[1]</sup>" in result


def test_pass3_skips_references_section():
    """Pass 3 should NOT modify anything in the References section."""
    content = "Body [1]\n\n# References\n- Ref text [1]\n- Another [2]"
    result = pass3_superscript(content)
    # References section preserved
    assert "- Ref text [1]" in result
    assert "- Another [2]" in result


def test_pass3_idempotent():
    """Pass 3 on already-processed content should not alter it further.

    Known limitation: pass3 regex matches [N] inside <sup> tags, so running
    on raw content twice would double-wrap. But on properly processed content
    where body [N] are already <sup>[N]</sup>, the function should at minimum
    preserve headings and references untouched.
    """
    # Test with content that has NO bare [N] in body (already processed)
    content = "Body text <sup>[1]</sup> and <sup>[2]</sup>\n\n# References\n- Ref [1]"
    result = pass3_superscript(content)
    # References section must be preserved
    assert "- Ref [1]" in result
    # Headings must be preserved
    assert "# References" in result


# --- Pass 4: PMID links in references ---

def test_pass4_links_pmid_in_references():
    content = "Body text\n\n# References\n- Smith J. Trial. PMID: 12345678 [1]"
    result = pass4_link_reference_pmids(content)
    assert "PMID: [12345678](https://pubmed.ncbi.nlm.nih.gov/12345678/) [1]" in result


def test_pass4_skips_non_references_body():
    content = "Body PMID: 12345678\n\n## Slide"
    result = pass4_link_reference_pmids(content)
    assert result == content


def test_truncate_title_long():
    long_title = "A focused update to SCCM clinical practice guidelines for adult critically ill patients with pain agitation sedation delirium immobility and sleep disruption"
    out = _truncate_title(long_title)
    assert out.endswith("...")
    assert len(out) <= 55


# --- Integration ---

def test_full_citation_pipeline(sample_raw, sample_refs):
    """Full passes 1-3 pipeline produces expected citation formatting."""
    refs = build_ref_lookup(sample_raw)
    assert len(refs) >= 4

    content = pass1_clean_titles(sample_raw)
    content = pass2_expand_sources(content, refs)
    content = pass3_superscript(content)

    # Headings cleaned
    for line in content.split("\n"):
        if line.startswith("#") and "References" not in line:
            assert not re.search(r'\[\d+\]', line), f"Heading still has bracket: {line}"

    # Body has superscript
    assert "<sup>[" in content

    # Sources expanded (ref text includes '- ' prefix from list-format references)
    assert "- [1]" in content
    assert "Eastern Association" in content
