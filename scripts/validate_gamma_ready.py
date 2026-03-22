#!/usr/bin/env python3
"""
validate_gamma_ready.py — Pre-submission quality gate for Gamma-ready markdown.

Usage:
    python3 scripts/validate_gamma_ready.py <file.md>

Runs a 17-numbered validation report on a gamma-ready markdown file before Gamma API submission:
  - 11 hard pass/fail gates (reported as pass/fail summary)
  - 5 soft design checks (reported as WARN, not counted as failures)
  - Card count as informational check #6
Exit code 0 if all hard gates pass, 1 if any hard gate fails.
"""

import argparse
import re
import sys

from card_utils import (
    split_cards, classify_card, get_title,
    count_body_words, count_bullets, extract_tables,
    has_bottom_line, has_sources, has_citations, title_has_verb,
    THRESHOLDS, EXEMPT_TYPES, BOTTOM_LINE_REQUIRED,
)


def check_no_html_comments(content: str) -> tuple[bool, str]:
    """Check 1: No HTML comments remain."""
    matches = re.findall(r'<!--.*?-->', content, re.DOTALL)
    if matches:
        return False, f"{len(matches)} HTML comment(s) found"
    return True, ""


def check_no_slide_markers(content: str) -> tuple[bool, str]:
    """Check 2: No ### SLIDE markers remain."""
    matches = re.findall(r'^### SLIDE \d+:', content, re.MULTILINE)
    final = re.findall(r'^### FINAL SLIDE:', content, re.MULTILINE)
    total = len(matches) + len(final)
    if total:
        return False, f"{total} SLIDE marker(s) found"
    return True, ""


def check_no_gamma_instructions(content: str) -> tuple[bool, str]:
    """Check 3: No **Gamma instruction:** lines remain."""
    matches = re.findall(r'^\*\*Gamma instruction:', content, re.MULTILINE)
    if matches:
        return False, f"{len(matches)} remaining"
    return True, ""


def check_no_triple_star_separators(content: str) -> tuple[bool, str]:
    """Check 4: No *** separators (all should be ---)."""
    # Match *** on its own line (not inside bold text)
    matches = re.findall(r'^\*\*\*$', content, re.MULTILINE)
    if matches:
        return False, f"{len(matches)} *** separator(s) found"
    return True, ""


def check_slide_titles_h2(content: str) -> tuple[bool, str]:
    """Check 5: Slide titles are ## (first heading per card is H2)."""
    cards = re.split(r'\n---\n', content)
    bad_cards = []
    for i, card in enumerate(cards, 1):
        lines = card.strip().split('\n')
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#'):
                if stripped.startswith('## '):
                    break  # Good — first heading is H2
                elif stripped.startswith('# ') and not stripped.startswith('## '):
                    bad_cards.append(f"card {i} uses H1")
                    break
                elif stripped.startswith('### '):
                    bad_cards.append(f"card {i} uses H3")
                    break
                else:
                    break
    if bad_cards:
        return False, "; ".join(bad_cards[:5]) + (f" (+{len(bad_cards)-5} more)" if len(bad_cards) > 5 else "")
    return True, ""


def count_cards(content: str) -> int:
    """Count card breaks (--- separators) + 1."""
    return content.count('\n---\n') + 1


def check_no_bare_bracket_refs(content: str) -> tuple[bool, str]:
    """Check 7: No bare [N] in body text (should be <sup>[N]</sup>).
    Excludes headings, Sources lines, References section, and list items starting with [N]."""
    ref_start = content.find('## References')
    if ref_start < 0:
        ref_start = content.find('# References')
    body = content[:ref_start] if ref_start > 0 else content

    bare_count = 0
    for line in body.split('\n'):
        stripped = line.strip()
        # Skip headings
        if stripped.startswith('#'):
            continue
        # Skip Sources lines
        if '**Sources:**' in stripped or stripped.startswith('**Source:**'):
            continue
        # Skip list items that start with [N] (expanded source entries)
        if re.match(r'^- \[\d+\]', stripped):
            continue
        # Find bare [N] not wrapped in <sup>
        bare = re.findall(r'(?<!<sup>)\[(\d+)\](?!</sup>)', line)
        bare_count += len(bare)

    if bare_count:
        return False, f"{bare_count} bare [N] reference(s) found (need <sup>)"
    return True, ""


def check_sources_expanded(content: str) -> tuple[bool, str]:
    """Check 8: Sources blocks are expanded (no compact **Sources:** [1][2])."""
    # Compact format: **Sources:** [1][2][3] all on one line
    compact = re.findall(r'^\*\*Sources?:\*\*\s*(\[\d+\])+', content, re.MULTILINE)
    if compact:
        return False, f"{len(compact)} compact Sources line(s) (should be multi-line with full citations)"
    return True, ""


def check_no_concatenated_refs(content: str) -> tuple[bool, str]:
    """Check 9: No concatenated reference entries (no 16+ digit number sequences)."""
    # PMIDs are 8 digits; concatenated = two or more run together = 16+ digits
    matches = re.findall(r'\b\d{16,}\b', content)
    if matches:
        examples = [m[:20] + "..." if len(m) > 20 else m for m in matches[:3]]
        return False, f"{len(matches)} concatenated number sequence(s): {', '.join(examples)}"
    return True, ""


def check_file_size(content: str) -> tuple[bool, str]:
    """Check 10: File size under 100K tokens (~400K chars)."""
    max_chars = 400_000
    if len(content) > max_chars:
        return False, f"{len(content):,} chars exceeds {max_chars:,} limit"
    return True, ""


CHECKS = [
    ("No HTML comments", check_no_html_comments),
    ("No SLIDE markers", check_no_slide_markers),
    ("No Gamma instructions", check_no_gamma_instructions),
    ("No *** separators", check_no_triple_star_separators),
    ("Slide titles are H2", check_slide_titles_h2),
    # Check 6 (card count) is informational, not pass/fail
    ("No bare [N] in body text", check_no_bare_bracket_refs),
    ("Sources blocks expanded", check_sources_expanded),
    ("No concatenated references", check_no_concatenated_refs),
    ("File size under 100K tokens", check_file_size),
]



def check_word_density(content: str) -> tuple[bool, str]:
    """Check 11: Word density per card (WARN only — soft gate)."""
    cards = split_cards(content)
    warnings = []
    for i, card in enumerate(cards):
        card_type = classify_card(card, i, len(cards))
        if card_type in EXEMPT_TYPES:
            continue
        thresholds = THRESHOLDS.get(card_type, THRESHOLDS["Content"])
        body = count_body_words(card)
        if thresholds["body_max"] is not None and body > thresholds["body_max"]:
            title = get_title(card)
            warnings.append(f"card {i+1} ({card_type}): {body} body words > {thresholds['body_max']} max — \"{title[:30]}\"")
    if warnings:
        return True, f"[WARN] {len(warnings)} card(s) exceed body word limits: " + "; ".join(warnings[:3])
    return True, ""


def check_bullet_count(content: str) -> tuple[bool, str]:
    """Check 12: Bullet count per card (WARN only — soft gate)."""
    cards = split_cards(content)
    warnings = []
    for i, card in enumerate(cards):
        card_type = classify_card(card, i, len(cards))
        if card_type in EXEMPT_TYPES:
            continue
        thresholds = THRESHOLDS.get(card_type, THRESHOLDS["Content"])
        bullets = count_bullets(card)
        if thresholds["bullets_max"] is not None and bullets > thresholds["bullets_max"]:
            title = get_title(card)
            warnings.append(f"card {i+1} ({card_type}): {bullets} bullets > {thresholds['bullets_max']} max — \"{title[:30]}\"")
    if warnings:
        return True, f"[WARN] {len(warnings)} card(s) exceed bullet limits: " + "; ".join(warnings[:3])
    return True, ""


def check_table_dimensions(content: str) -> tuple[bool, str]:
    """Check 13: Table dimensions (WARN only — soft gate)."""
    cards = split_cards(content)
    warnings = []
    for i, card in enumerate(cards):
        card_type = classify_card(card, i, len(cards))
        if card_type in EXEMPT_TYPES:
            continue
        thresholds = THRESHOLDS.get(card_type, THRESHOLDS["Content"])
        tables = extract_tables(card)
        for t_idx, table in enumerate(tables):
            if thresholds["table_rows_max"] is not None and table["rows"] > thresholds["table_rows_max"]:
                warnings.append(f"card {i+1} table {t_idx+1}: {table['rows']} rows > {thresholds['table_rows_max']} max")
            if thresholds["table_cols_max"] is not None and table["cols"] > thresholds["table_cols_max"]:
                warnings.append(f"card {i+1} table {t_idx+1}: {table['cols']} cols > {thresholds['table_cols_max']} max")
    if warnings:
        return True, f"[WARN] {len(warnings)} table dimension issue(s): " + "; ".join(warnings[:3])
    return True, ""


def check_bottom_line_presence(content: str) -> tuple[bool, str]:
    """Check 14: Bottom Line on content slides (FAIL — hard gate)."""
    cards = split_cards(content)
    missing = []
    for i, card in enumerate(cards):
        card_type = classify_card(card, i, len(cards))
        if card_type not in BOTTOM_LINE_REQUIRED:
            continue
        if not has_bottom_line(card):
            title = get_title(card)
            missing.append(f"card {i+1} ({card_type}): missing Bottom Line — \"{title[:30]}\"")
    if missing:
        return False, f"{len(missing)} content card(s) missing Bottom Line: " + "; ".join(missing[:3])
    return True, ""


def check_sources_on_evidence(content: str) -> tuple[bool, str]:
    """Check 15: Sources on slides with citations (WARN only — soft gate)."""
    cards = split_cards(content)
    warnings = []
    for i, card in enumerate(cards):
        card_type = classify_card(card, i, len(cards))
        if card_type in EXEMPT_TYPES:
            continue
        if has_citations(card) and not has_sources(card):
            title = get_title(card)
            warnings.append(f"card {i+1}: has citations but no Sources block — \"{title[:30]}\"")
    if warnings:
        return True, f"[WARN] {len(warnings)} card(s) have citations without Sources: " + "; ".join(warnings[:3])
    return True, ""


def check_assertion_titles(content: str) -> tuple[bool, str]:
    """Check 16: Assertion-evidence titles (WARN only — soft gate)."""
    cards = split_cards(content)
    exempt = EXEMPT_TYPES | {"Learning Objectives", "MCQ", "Case"}
    topic_titles = []
    for i, card in enumerate(cards):
        card_type = classify_card(card, i, len(cards))
        if card_type in exempt:
            continue
        title = get_title(card)
        if title == "(untitled)":
            continue
        if not title_has_verb(title):
            topic_titles.append(f"card {i+1}: topic-label (no verb) — \"{title[:40]}\"")
    if topic_titles:
        return True, f"[WARN] {len(topic_titles)} non-assertion title(s): " + "; ".join(topic_titles[:3])
    return True, ""


def check_unfilled_placeholders(content: str) -> tuple[bool, str]:
    """Check 17: No unfilled [PLACEHOLDER]/[TOPIC]/[TODO] (FAIL — hard gate)."""
    placeholders = re.findall(r'\[(?:PLACEHOLDER|TOPIC|TODO)[^\]]*\]', content, re.IGNORECASE)
    if placeholders:
        return False, f"{len(placeholders)} unfilled placeholder(s): " + ", ".join(placeholders[:3])
    return True, ""


def check_presentation_word_count(content: str) -> tuple[bool, str]:
    """Check 18: Presentation-level projected word count (WARN only — soft gate)."""
    cards = split_cards(content)
    total_words = sum(count_body_words(card) for card in cards)
    if total_words > 1600:
        return True, f"[WARN] {total_words} total body words > 1600 (long presentation)"
    if total_words > 1200:
        return True, f"[WARN] {total_words} total body words > 1200 (medium-long presentation)"
    if total_words > 800:
        return True, f"[WARN] {total_words} total body words > 800 (compact limit)"
    return True, f"{total_words} total body words"


def check_speaker_notes_presence(content: str) -> tuple[bool, str]:
    """Check 19: Speaker notes presence — >50% of content/trial/data/guideline slides should have speaker notes."""
    NOTES_REQUIRED_TYPES = {"Content", "Trial", "Data/Table", "Guideline"}
    cards = split_cards(content)
    eligible = 0
    with_notes = 0
    for i, card in enumerate(cards):
        card_type = classify_card(card, i, len(cards))
        if card_type not in NOTES_REQUIRED_TYPES:
            continue
        eligible += 1
        if re.search(r'<!--.*?-->', card, re.DOTALL):
            with_notes += 1
    if eligible == 0:
        return True, ""
    ratio = with_notes / eligible
    if ratio < 0.50:
        return True, f"[WARN] {with_notes}/{eligible} eligible slides ({ratio:.0%}) have speaker notes (target >50%)"
    return True, f"{with_notes}/{eligible} eligible slides have speaker notes"


# Hard checks (checks 14, 17) — cause failure
HARD_DESIGN_CHECKS = [
    ("Bottom Line on content slides", check_bottom_line_presence),
    ("No unfilled placeholders", check_unfilled_placeholders),
]

# Soft checks (checks 11-13, 15-16, 18-19) — print WARN but don't fail
SOFT_DESIGN_CHECKS = [
    ("Word density per card", check_word_density),
    ("Bullet count per card", check_bullet_count),
    ("Table dimensions", check_table_dimensions),
    ("Sources on cited slides", check_sources_on_evidence),
    ("Assertion-evidence titles", check_assertion_titles),
    ("Presentation word count", check_presentation_word_count),
    ("Speaker notes presence", check_speaker_notes_presence),
]


def validate(content: str) -> tuple[int, int, int]:
    """Run all checks and print results. Returns (passed, failed, card_count)."""
    passed = 0
    failed = 0

    for i, (label, check_fn) in enumerate(CHECKS, 1):
        # Adjust display number: checks 7-10 map to display positions 7-10
        # but check 6 (card count) is inserted between 5 and 7
        display_num = i if i <= 5 else i + 1
        ok, detail = check_fn(content)
        if ok:
            print(f"[PASS] {display_num:2d}. {label}")
            passed += 1
        else:
            print(f"[FAIL] {display_num:2d}. {label} ({detail})")
            failed += 1

    card_count = count_cards(content)

    # Hard design checks (11+)
    check_num = 11
    for label, check_fn in HARD_DESIGN_CHECKS:
        ok, detail = check_fn(content)
        if ok:
            print(f"[PASS] {check_num:2d}. {label}")
            passed += 1
        else:
            print(f"[FAIL] {check_num:2d}. {label} ({detail})")
            failed += 1
        check_num += 1

    # Soft design checks (WARN only, don't count as failures)
    for label, check_fn in SOFT_DESIGN_CHECKS:
        ok, detail = check_fn(content)
        if detail:
            print(f"[WARN] {check_num:2d}. {label} ({detail})")
        else:
            print(f"[PASS] {check_num:2d}. {label}")
        check_num += 1

    return passed, failed, card_count


def main():
    parser = argparse.ArgumentParser(
        description='Pre-submission quality gate for Gamma-ready markdown.'
    )
    parser.add_argument('input', help='Gamma-ready markdown file to validate')
    args = parser.parse_args()

    filepath = args.input
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    char_count = len(content)
    print(f"Validating: {filepath} ({char_count} chars)")
    print("\u2501" * 42)

    passed, failed, card_count = validate(content)

    # Insert card count report at position 6
    print(f"       6. Card count: {card_count} slides")

    print("\u2501" * 42)
    total = passed + failed
    print(f"Result: {passed}/{total} PASSED, {failed} FAILED")
    print(f"Card count: {card_count} slides")

    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
