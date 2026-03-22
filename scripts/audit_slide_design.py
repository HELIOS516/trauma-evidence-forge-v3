#!/usr/bin/env python3
"""
audit_slide_design.py — Evaluate presentation quality against design principles.

Usage:
    python3 scripts/audit_slide_design.py <file.md> [--strict] [--json]

Runs 8 design checks per card against type-specific thresholds.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Import from shared card utilities
from card_utils import (
    split_cards,
    classify_card,
    get_title,
    count_body_words,
    count_table_words,
    count_bullets,
    extract_tables,
    has_bottom_line,
    has_sources,
    has_citations,
    title_has_verb,
    THRESHOLDS,
    EXEMPT_TYPES,
    BOTTOM_LINE_REQUIRED,
)

# Severity levels
PASS = "PASS"
ADVISORY = "ADVISORY"
WARN = "WARN"
FAIL = "FAIL"


def check_d1_word_density(card: str, card_type: str) -> tuple[str, str]:
    """D1: One Idea / Cognitive Load — word density per card."""
    if card_type in EXEMPT_TYPES:
        return PASS, ""

    thresholds = THRESHOLDS.get(card_type, THRESHOLDS["Content"])
    body = count_body_words(card)
    table = count_table_words(card)
    total = body + table

    issues = []
    if thresholds["body_max"] is not None and body > thresholds["body_max"]:
        issues.append(f"{body} body words > {thresholds['body_max']} max for {card_type}")
    if thresholds["total_max"] is not None and total > thresholds["total_max"]:
        issues.append(f"{total} total words > {thresholds['total_max']} max")

    if issues:
        return WARN, "; ".join(issues)
    return PASS, f"{body}w body, {total}w total"


def check_d2_chunking(card: str, card_type: str) -> tuple[str, str]:
    """D2: Chunking / 7x7 Rule — bullet count per card."""
    if card_type in EXEMPT_TYPES:
        return PASS, ""

    thresholds = THRESHOLDS.get(card_type, THRESHOLDS["Content"])
    bullets = count_bullets(card)

    if thresholds["bullets_max"] is not None and bullets > thresholds["bullets_max"]:
        return WARN, f"{bullets} bullets > {thresholds['bullets_max']} max for {card_type}"
    return PASS, f"{bullets} bullets"


def check_d3_table_dimensions(card: str, card_type: str) -> tuple[str, str]:
    """D3: Clinical Adaptations — table dimensions."""
    if card_type in EXEMPT_TYPES:
        return PASS, ""

    thresholds = THRESHOLDS.get(card_type, THRESHOLDS["Content"])
    tables = extract_tables(card)

    if not tables:
        return PASS, "no tables"

    issues = []
    for i, table in enumerate(tables):
        if thresholds["table_rows_max"] is not None and table["rows"] > thresholds["table_rows_max"]:
            issues.append(f"table {i+1}: {table['rows']} rows > {thresholds['table_rows_max']} max")
        if thresholds["table_cols_max"] is not None and table["cols"] > thresholds["table_cols_max"]:
            issues.append(f"table {i+1}: {table['cols']} cols > {thresholds['table_cols_max']} max")

    if issues:
        return WARN, "; ".join(issues)
    return PASS, f"{len(tables)} table(s)"


def check_d4_bottom_line(card: str, card_type: str) -> tuple[str, str]:
    """D4: 'So What?' Rule — Bottom Line presence on content slides."""
    if card_type not in BOTTOM_LINE_REQUIRED:
        return PASS, ""

    if has_bottom_line(card):
        return PASS, "present"
    return FAIL, f"missing on {card_type} slide"


def check_d5_citations(card: str, card_type: str) -> tuple[str, str]:
    """D5: Citation Standards — Sources block when citations present."""
    if card_type in EXEMPT_TYPES:
        return PASS, ""

    if has_citations(card) and not has_sources(card):
        return WARN, "has citations but no Sources block"
    return PASS, ""


def check_d6_assertion_title(card: str, card_type: str) -> tuple[str, str]:
    """D6: Assertion-Evidence — title format check."""
    if card_type in EXEMPT_TYPES | {"Learning Objectives", "MCQ", "Case"}:
        return PASS, ""

    title = get_title(card)
    if title == "(untitled)":
        return PASS, ""

    if title_has_verb(title):
        return PASS, "assertion-style"
    return ADVISORY, f"topic-label title (no verb): \"{title[:50]}\""


def check_d7_mcq_spacing(cards: list[str], card_types: list[str]) -> list[int]:
    """D7: Active Learning — MCQ spacing check. Returns indices of cards in long gaps."""
    # Check for gaps > 12 consecutive non-MCQ cards
    non_mcq_run = 0
    gap_cards = []
    for i, card_type in enumerate(card_types):
        if card_type == "MCQ":
            non_mcq_run = 0
        else:
            non_mcq_run += 1
            if non_mcq_run > 12:
                gap_cards.append(i)

    return gap_cards


def check_d8_placeholders(card: str) -> tuple[str, str]:
    """D8: Completeness — unfilled placeholders."""
    placeholders = re.findall(r'\[(?:PLACEHOLDER|TOPIC|TODO)[^\]]*\]', card, re.IGNORECASE)
    if placeholders:
        return FAIL, f"{len(placeholders)} unfilled: {', '.join(placeholders[:3])}"
    return PASS, ""


def check_d9_sentence_detection(card: str, card_type: str) -> tuple[str, str]:
    """D9: Sentence detection — flag body lines with >12 words (WARN severity)."""
    if card_type in EXEMPT_TYPES:
        return PASS, ""
    long_lines = []
    in_table = False
    in_notes = False
    for line in card.strip().split('\n'):
        stripped = line.strip()
        if stripped.startswith('#') or stripped.startswith('>'):
            continue
        if '<!--' in stripped:
            if '-->' not in stripped:
                in_notes = True
            continue
        if '-->' in stripped:
            in_notes = False
            continue
        if in_notes:
            continue
        if stripped.startswith('|') and stripped.endswith('|'):
            in_table = True
            continue
        if in_table and not stripped:
            in_table = False
            continue
        if in_table:
            continue
        if stripped.startswith('**Sources:**') or stripped.startswith('**Source:**'):
            continue
        if re.match(r'^- \[\d+\]', stripped):
            continue
        clean = re.sub(r'<sup>\[\d+\]</sup>', '', stripped)
        clean = re.sub(r'\*\*', '', clean)
        word_count = len(clean.split())
        if word_count > 12:
            long_lines.append(word_count)
    if long_lines:
        return WARN, f"{len(long_lines)} line(s) with >{12} words ({max(long_lines)} words max)"
    return PASS, ""


def check_d10_object_count(card: str, card_type: str) -> tuple[str, str]:
    """D10: Object count per slide — count title, bullets, tables, images, blockquotes."""
    if card_type in EXEMPT_TYPES:
        return PASS, ""
    title_count = 1 if get_title(card) != "(untitled)" else 0
    bullet_count = count_bullets(card)
    tables = extract_tables(card)
    table_count = len(tables)
    # Blockquotes (bottom-line, callouts)
    blockquote_count = sum(1 for line in card.strip().split('\n') if line.strip().startswith('>'))
    # Image markers (Gamma uses ![...] syntax)
    image_count = len(re.findall(r'!\[', card))
    total = title_count + min(bullet_count, 1) + table_count + image_count + min(blockquote_count, 1)
    if total > 8:
        return FAIL, f"{total} objects on slide (title:{title_count} bullets:{bullet_count} tables:{table_count} images:{image_count} bqs:{blockquote_count}) > 8 max"
    if total > 6:
        return WARN, f"{total} objects on slide > 6 recommended"
    return PASS, f"{total} objects"


def check_d11_speaker_notes_ratio(card: str, card_type: str) -> tuple[str, str]:
    """D11: Speaker notes ratio — body words should be <30% of (body + notes) combined."""
    if card_type in EXEMPT_TYPES:
        return PASS, ""
    body_words = count_body_words(card)
    # Extract speaker notes (content inside <!-- ... --> comments)
    notes_text = " ".join(re.findall(r'<!--(.*?)-->', card, re.DOTALL))
    notes_words = len(notes_text.split()) if notes_text.strip() else 0
    total = body_words + notes_words
    if total == 0:
        return PASS, ""
    ratio = body_words / total
    if ratio >= 0.30 and notes_words > 0:
        return ADVISORY, f"body {body_words}w is {ratio:.0%} of combined {total}w (target <30%)"
    return PASS, f"body {body_words}w / total {total}w = {ratio:.0%}"


def check_d12_key_highlight(card: str, card_type: str) -> tuple[str, str]:
    """D12: Key highlight detection — Content/Trial/Data slides should have ** bold stat marker."""
    if card_type not in {"Content", "Trial", "Data/Table"}:
        return PASS, ""
    # Look for a bold stat: **number** or **XX%** or **bold phrase**
    has_bold = bool(re.search(r'\*\*[^*]+\*\*', card))
    if not has_bold:
        return ADVISORY, f"no ** bold stat/highlight marker found on {card_type} slide"
    return PASS, "bold highlight present"


def check_d13_presentation_word_budget(cards: list[str], card_types: list[str]) -> tuple[str, str]:
    """D13: Presentation word budget — total projected words across all slides."""
    total_words = 0
    for card, card_type in zip(cards, card_types):
        total_words += count_body_words(card)
    if total_words > 1600:
        return WARN, f"{total_words} total body words > 1600 (long presentation)"
    if total_words > 1200:
        return WARN, f"{total_words} total body words > 1200 (medium-long presentation)"
    if total_words > 800:
        return WARN, f"{total_words} total body words > 800 (compact limit)"
    return PASS, f"{total_words} total body words"


def audit_presentation(content: str, presenter: str = "") -> dict:
    """Run full design audit on presentation content. Returns audit results."""
    cards = split_cards(content)
    num_cards = len(cards)

    # Classify all cards
    card_types = []
    for i, card in enumerate(cards):
        card_type = classify_card(card, i, num_cards, presenter)
        card_types.append(card_type)

    # Check D7 (MCQ spacing) globally
    mcq_gap_cards = check_d7_mcq_spacing(cards, card_types)

    # Check D13 (presentation word budget) globally
    d13_sev, d13_detail = check_d13_presentation_word_budget(cards, card_types)

    # Per-card checks
    results = []
    for i, (card, card_type) in enumerate(zip(cards, card_types)):
        card_results = {
            "card": i + 1,
            "type": card_type,
            "title": get_title(card),
            "checks": {},
            "severity": PASS,  # Will be upgraded
        }

        # D1: Word density
        sev, detail = check_d1_word_density(card, card_type)
        card_results["checks"]["D1"] = {"severity": sev, "detail": detail}

        # D2: Bullet count
        sev, detail = check_d2_chunking(card, card_type)
        card_results["checks"]["D2"] = {"severity": sev, "detail": detail}

        # D3: Table dimensions
        sev, detail = check_d3_table_dimensions(card, card_type)
        card_results["checks"]["D3"] = {"severity": sev, "detail": detail}

        # D4: Bottom Line
        sev, detail = check_d4_bottom_line(card, card_type)
        card_results["checks"]["D4"] = {"severity": sev, "detail": detail}

        # D5: Citations
        sev, detail = check_d5_citations(card, card_type)
        card_results["checks"]["D5"] = {"severity": sev, "detail": detail}

        # D6: Assertion title
        sev, detail = check_d6_assertion_title(card, card_type)
        card_results["checks"]["D6"] = {"severity": sev, "detail": detail}

        # D7: MCQ spacing (only flag cards in gap)
        if i in mcq_gap_cards:
            card_results["checks"]["D7"] = {"severity": ADVISORY, "detail": ">12 consecutive non-MCQ cards"}
        else:
            card_results["checks"]["D7"] = {"severity": PASS, "detail": ""}

        # D8: Placeholders
        sev, detail = check_d8_placeholders(card)
        card_results["checks"]["D8"] = {"severity": sev, "detail": detail}

        # D9: Sentence detection
        sev, detail = check_d9_sentence_detection(card, card_type)
        card_results["checks"]["D9"] = {"severity": sev, "detail": detail}

        # D10: Object count
        sev, detail = check_d10_object_count(card, card_type)
        card_results["checks"]["D10"] = {"severity": sev, "detail": detail}

        # D11: Speaker notes ratio
        sev, detail = check_d11_speaker_notes_ratio(card, card_type)
        card_results["checks"]["D11"] = {"severity": sev, "detail": detail}

        # D12: Key highlight detection
        sev, detail = check_d12_key_highlight(card, card_type)
        card_results["checks"]["D12"] = {"severity": sev, "detail": detail}

        # D13: Presentation word budget (attached to first card only as presentation-level result)
        if i == 0:
            card_results["checks"]["D13"] = {"severity": d13_sev, "detail": d13_detail}
        else:
            card_results["checks"]["D13"] = {"severity": PASS, "detail": ""}

        # Store metrics for reporting
        card_results["body_words"] = count_body_words(card)
        card_results["bullets"] = count_bullets(card)

        # Compute overall severity for this card
        severities = [c["severity"] for c in card_results["checks"].values()]
        if FAIL in severities:
            card_results["severity"] = FAIL
        elif WARN in severities:
            card_results["severity"] = WARN
        elif ADVISORY in severities:
            card_results["severity"] = ADVISORY

        results.append(card_results)

    return {
        "file": "",
        "num_cards": num_cards,
        "cards": results,
    }


def print_report(audit: dict) -> None:
    """Print human-readable audit report."""
    print(f"\n=== Slide Design Audit ===")
    print(f"File: {audit['file']} ({audit['num_cards']} cards)\n")

    counts = {PASS: 0, ADVISORY: 0, WARN: 0, FAIL: 0}

    for card in audit["cards"]:
        status = card["severity"]
        counts[status] = counts.get(status, 0) + 1

        type_label = card["type"]

        # Find worst check details to display
        worst_checks = []
        for check_id, check in card["checks"].items():
            if check["severity"] in (WARN, FAIL, ADVISORY) and check["detail"]:
                worst_checks.append(f"{check_id}: {check['detail']}")

        pad = "." * max(1, 42 - len(f"Card {card['card']:2d}: {type_label}"))

        if worst_checks:
            check_str = " | ".join(worst_checks[:2])
            print(f"Card {card['card']:2d}: {type_label:20s} {pad} {status} [{check_str}]")
        else:
            print(f"Card {card['card']:2d}: {type_label:20s} {pad} {status} ({card['body_words']}w, {card['bullets']} bullets)")

    print(f"\nSummary: {counts[PASS]} PASS | {counts[WARN]} WARN | {counts[FAIL]} FAIL | {counts[ADVISORY]} ADVISORY")


def main():
    parser = argparse.ArgumentParser(
        description='Evaluate presentation quality against design principles.'
    )
    parser.add_argument('input', help='Markdown file to audit')
    parser.add_argument('--strict', action='store_true', help='Exit 1 on any WARN or FAIL')
    parser.add_argument('--json', action='store_true', help='Output JSON instead of text report')
    parser.add_argument('--presenter', default='', help='Presenter name for card classification')
    args = parser.parse_args()

    filepath = args.input
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    audit = audit_presentation(content, args.presenter)
    audit["file"] = filepath

    if args.json:
        print(json.dumps(audit, indent=2))
    else:
        print_report(audit)

    # Exit code logic
    has_fail = any(c["severity"] == FAIL for c in audit["cards"])
    has_warn = any(c["severity"] == WARN for c in audit["cards"])

    if has_fail:
        sys.exit(1)
    if args.strict and has_warn:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
