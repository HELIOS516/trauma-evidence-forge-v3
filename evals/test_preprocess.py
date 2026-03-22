"""Tests for preprocess_for_gamma.py — passes 4-11."""

from preprocess_for_gamma import (
    pass4_strip_header,
    pass5_strip_slide_markers,
    pass6_extract_and_strip_gamma_instructions,
    pass7_convert_separators,
    pass8_convert_ref_lines,
    pass9_extract_and_strip_comments,
    pass10_normalize_headings,
    pass11_fix_concat_refs,
    pass12_strip_lo_tags,
    pass13_bottom_line_above_sources,
)


def full_preprocess(content: str) -> str:
    """Run all 9 preprocessing passes (4-12)."""
    content = pass4_strip_header(content)
    content = pass5_strip_slide_markers(content)
    content = pass6_extract_and_strip_gamma_instructions(content, instructions_path=None)
    content = pass7_convert_separators(content)
    content = pass8_convert_ref_lines(content)
    content = pass9_extract_and_strip_comments(content, notes_path=None)
    content = pass10_normalize_headings(content)
    content = pass11_fix_concat_refs(content)
    content = pass12_strip_lo_tags(content)
    content = pass13_bottom_line_above_sources(content)
    return content


# --- Pass 4: Strip header ---

def test_pass4_strips_header():
    """Pass 4 should remove everything before first *** or ---."""
    content = "Header block\nMeta info\n\n---\n\n# First Slide"
    result = pass4_strip_header(content)
    # Should start at the first ---
    assert result.startswith("---")
    assert "Meta info" not in result


def test_pass4_strips_header_with_stars():
    """Pass 4 should find *** before ---."""
    content = "Header block\n\n***\n\n# First Slide"
    result = pass4_strip_header(content)
    assert result.startswith("***")
    assert "Header block" not in result


def test_pass4_no_header():
    """Pass 4 should leave content unchanged if no separator found."""
    content = "# Just content\nNo separators here"
    result = pass4_strip_header(content)
    assert result == content


def test_pass4_bold_text_not_matched():
    """Pass 4 should NOT treat ***bold*** as a separator."""
    content = "Header with ***bold italic*** text\n\n---\n\n# First Slide"
    result = pass4_strip_header(content)
    # Should strip at ---, not at ***bold***
    assert result.startswith("---")
    assert "bold italic" not in result


# --- Pass 5: Strip SLIDE markers ---

def test_pass5_strips_slide_markers():
    """Pass 5 should remove ### SLIDE N: lines."""
    content = "### SLIDE 1: Introduction\n\n# Title\n\n### SLIDE 2: Overview\n\n# Second"
    result = pass5_strip_slide_markers(content)
    assert "### SLIDE" not in result
    assert "# Title" in result
    assert "# Second" in result


def test_pass5_strips_final_slide():
    """Pass 5 should also remove ### FINAL SLIDE: lines."""
    content = "### FINAL SLIDE: Questions\n\n# Questions & Discussion"
    result = pass5_strip_slide_markers(content)
    assert "### FINAL SLIDE" not in result
    assert "# Questions & Discussion" in result


def test_pass5_preserves_other_headings():
    """Pass 5 should not touch non-SLIDE headings."""
    content = "### Some Other Heading\n\n### SLIDE 1: Title\n\nBody"
    result = pass5_strip_slide_markers(content)
    assert "### Some Other Heading" in result
    assert "### SLIDE" not in result


# --- Pass 6: Strip Gamma instructions ---

def test_pass6_strips_gamma_instructions():
    """Pass 6 should remove **Gamma instruction: ...** lines."""
    content = "# Title\n\n**Gamma instruction: Use professional layout**\n\nBody text"
    result = pass6_extract_and_strip_gamma_instructions(content, instructions_path=None)
    assert "Gamma instruction" not in result
    assert "# Title" in result
    assert "Body text" in result


def test_pass6_preserves_other_bold():
    """Pass 6 should not touch other bold text."""
    content = "**Important:** This is bold\n\n**Gamma instruction: Remove me**\n\nMore text"
    result = pass6_extract_and_strip_gamma_instructions(content, instructions_path=None)
    assert "**Important:** This is bold" in result
    assert "Gamma instruction" not in result


# --- Pass 7: Convert separators ---

def test_pass7_converts_separators():
    """Pass 7 should convert standalone *** to ---."""
    content = "Slide 1 content\n\n***\n\nSlide 2 content\n\n***\n\nSlide 3"
    result = pass7_convert_separators(content)
    assert "\n***\n" not in result
    assert result.count("---") == 2


def test_pass7_no_stars():
    """Pass 7 should leave content unchanged if no standalone *** present."""
    content = "Content with --- already"
    result = pass7_convert_separators(content)
    assert result == content


def test_pass7_bold_text_preserved():
    """Pass 7 should NOT convert ***bold*** inside content to ---bold---."""
    content = "This has ***bold italic*** text\n\n***\n\nNext slide"
    result = pass7_convert_separators(content)
    assert "***bold italic***" in result
    assert "---bold italic---" not in result
    # The standalone *** should be converted
    assert "\n---\n" in result


# --- Pass 8: Convert reference lines ---

def test_pass8_converts_ref_lines():
    """Pass 8 should convert ---* lines to - list items."""
    content = "# References\n\n---* Some ref [1]\n---* Another ref [2]"
    result = pass8_convert_ref_lines(content)
    assert "- Some ref [1]" in result
    assert "- Another ref [2]" in result
    assert "---*" not in result


def test_pass8_preserves_regular_separators():
    """Pass 8 should not touch --- that aren't followed by *."""
    content = "---\n\n# Title\n\n---* Ref [1]"
    result = pass8_convert_ref_lines(content)
    assert result.startswith("---\n")
    assert "- Ref [1]" in result


# --- Pass 9: Extract and strip speaker notes ---

def test_pass9_strips_comments():
    """Pass 9 should remove HTML comments from content."""
    content = "# Title\n\n<!-- Speaker Notes:\n- Note 1\n-->\n\nBody text"
    result = pass9_extract_and_strip_comments(content, notes_path=None)
    assert "<!--" not in result
    assert "-->" not in result
    assert "# Title" in result
    assert "Body text" in result


def test_pass9_preserves_content_without_comments():
    """Pass 9 should leave content unchanged if no comments."""
    content = "# Title\n\nBody text\n\n---\n\n# Slide 2"
    result = pass9_extract_and_strip_comments(content, notes_path=None)
    assert result == content


def test_pass9_handles_multiline_comments():
    """Pass 9 should handle multi-line HTML comments."""
    content = "Before\n\n<!-- Speaker Notes:\n- Line 1\n- Line 2\n- Line 3\n-->\n\nAfter"
    result = pass9_extract_and_strip_comments(content, notes_path=None)
    assert "<!--" not in result
    assert "Before" in result
    assert "After" in result


def test_pass9_strips_multiple_comments():
    """Pass 9 should strip all HTML comments."""
    content = "Slide 1\n<!-- Note 1 -->\n\n---\n\nSlide 2\n<!-- Note 2 -->\n"
    result = pass9_extract_and_strip_comments(content, notes_path=None)
    assert result.count("<!--") == 0


def test_pass9_writes_notes_file(tmp_path):
    """Pass 9 should extract notes to companion file."""
    content = "---\n\n# Title Slide\n\n<!-- Speaker Notes:\n- Key point\n-->\n\n---\n\n# Second\n\nBody"
    notes_file = tmp_path / "notes.md"
    pass9_extract_and_strip_comments(content, notes_path=str(notes_file))
    assert notes_file.exists()
    notes = notes_file.read_text()
    assert "Key point" in notes
    assert "Title Slide" in notes


# --- Pass 10: Normalize headings ---

def test_pass10_h1_to_h2():
    """Pass 10 should convert first H1 per card to H2."""
    content = "---\n\n# Big Title\n\nBody"
    result = pass10_normalize_headings(content)
    assert "## Big Title" in result
    # Verify no standalone H1 remains (## Big Title contains # Big Title as substring)
    assert "\n# Big Title" not in result


def test_pass10_h3_to_h2():
    """Pass 10 should convert first H3 per card to H2."""
    content = "---\n\n### Small Title\n\nBody"
    result = pass10_normalize_headings(content)
    assert "## Small Title" in result
    assert "### Small Title" not in result


def test_pass10_preserves_subheadings():
    """Pass 10 should only normalize the FIRST heading per card."""
    content = "---\n\n# Card Title\n\n### Subheading\n\nBody"
    result = pass10_normalize_headings(content)
    assert "## Card Title" in result
    assert "### Subheading" in result


def test_pass10_first_card():
    """Pass 10 should normalize the first card (before any ---)."""
    content = "# Opening Slide\n\nContent\n\n---\n\n# Second"
    result = pass10_normalize_headings(content)
    assert result.startswith("## Opening Slide")
    assert "## Second" in result


def test_pass10_already_h2():
    """Pass 10 should leave ## headings unchanged."""
    content = "---\n\n## Already H2\n\nBody"
    result = pass10_normalize_headings(content)
    assert "## Already H2" in result


# --- Pass 11: Fix concatenated references ---

def test_pass11_splits_concat_refs():
    """Pass 11 should split PMID running into next ref number."""
    content = "# References\n- Author. Title. PMID: 2198674110. Bulger EM, et al."
    result = pass11_fix_concat_refs(content)
    assert "21986741" in result
    assert "\n10. Bulger EM" in result


def test_pass11_preserves_normal_refs():
    """Pass 11 should not touch properly formatted references."""
    content = "# References\n- Author. PMID: 36652353\n- Next Author. Title."
    result = pass11_fix_concat_refs(content)
    assert result == content


def test_pass11_handles_8digit_pmid():
    """Pass 11 should handle 8-digit PMIDs running into ref numbers."""
    content = "# References\nPMID: 404923075. Smith J, et al."
    result = pass11_fix_concat_refs(content)
    assert "40492307" in result
    assert "\n5. Smith J" in result


def test_pass11_ignores_body_content():
    """Pass 11 should NOT modify content before # References heading."""
    content = "Body with number 2198674110. text here.\n\n# References\n- Normal ref."
    result = pass11_fix_concat_refs(content)
    assert "Body with number 2198674110. text here." in result


# --- Pass 13: Bottom Line above Sources ---

def test_pass13_reorders_bottom_line_and_sources():
    content = (
        "## Slide\n\nText.\n\n**Sources:**\n- [1] A.\n\n"
        "> **Bottom Line:** Key point.\n"
    )
    result = pass13_bottom_line_above_sources(content)
    assert result.find("> **Bottom Line:**") < result.find("**Sources:**")


def test_pass13_no_change_when_already_ordered():
    content = (
        "## Slide\n\nText.\n\n> **Bottom Line:** Key point.\n\n"
        "**Sources:**\n- [1] A.\n"
    )
    result = pass13_bottom_line_above_sources(content)
    assert result == content


# --- Integration ---

def test_full_pipeline_integration(sample_raw, sample_expected):
    """Full pipeline (passes 1-11) should match expected output."""
    from format_citations import (
        build_ref_lookup,
        pass1_clean_titles,
        pass2_expand_sources,
        pass3_superscript,
        pass4_link_reference_pmids,
    )

    content = sample_raw

    # Passes 1-3 (citation formatting)
    refs = build_ref_lookup(content)
    content = pass1_clean_titles(content)
    content = pass2_expand_sources(content, refs)
    content = pass3_superscript(content)
    content = pass4_link_reference_pmids(content)

    # Passes 4-11 (preprocessing)
    content = full_preprocess(content)

    # Normalize whitespace for comparison (trailing newlines, multiple blanks)
    def normalize(text):
        lines = text.strip().split("\n")
        # Collapse multiple blank lines to single
        result = []
        prev_blank = False
        for line in lines:
            is_blank = line.strip() == ""
            if is_blank and prev_blank:
                continue
            result.append(line)
            prev_blank = is_blank
        return "\n".join(result)

    assert normalize(content) == normalize(sample_expected)


def test_idempotent_preprocess_passes(sample_raw):
    """Running preprocess passes 4-11 twice should give the same result.

    Note: The full pipeline (passes 1-11) is NOT idempotent because pass3
    (superscript) will double-wrap <sup>[N]</sup> on second run. This is a
    known limitation — the pipeline is designed to run once. This test verifies
    that the preprocess passes (4-11) alone are idempotent.
    """
    once = full_preprocess(sample_raw)
    twice = full_preprocess(once)
    assert once == twice
