#!/usr/bin/env python3
"""
convert_inline_citations.py — Convert parenthetical citations to [N] numbered format.

Usage:
    python3 scripts/convert_inline_citations.py <file.md> [--dry-run]

One-time migration tool for legacy content. Finds inline parenthetical citations
like (Author et al., Year; PMID: XXXXXXXX) and converts them to numbered [N]
references with per-slide Sources blocks and a References section.
"""

import argparse
import re
import shutil
import sys


# Patterns for inline parenthetical citations
CITATION_PATTERNS = [
    # (Author et al., Year; PMID: 12345678)
    re.compile(
        r'\(([A-Z][A-Za-z\'-]+(?:\s+(?:et\s+al\.))?),?\s*(\d{4});?\s*PMID:\s*(\d+)\)'
    ),
    # (Author et al., Year; DOI: 10.xxxx/...)
    re.compile(
        r'\(([A-Z][A-Za-z\'-]+(?:\s+(?:et\s+al\.))?),?\s*(\d{4});?\s*DOI:\s*(10\.\S+)\)'
    ),
    # (Author, Year; PMID: 12345678) — single author without "et al."
    re.compile(
        r'\(([A-Z][A-Za-z\'-]+),?\s*(\d{4});?\s*PMID:\s*(\d+)\)'
    ),
    # (Author et al., Year) — no identifier
    re.compile(
        r'\(([A-Z][A-Za-z\'-]+(?:\s+(?:et\s+al\.))?),?\s*(\d{4})\)'
    ),
]


def extract_citations(content: str) -> list[dict]:
    """Extract all parenthetical citations from content.

    Returns list of dicts with keys: match_text, author, year, pmid, doi.
    """
    citations = []
    seen_spans = set()

    for pattern in CITATION_PATTERNS:
        for m in pattern.finditer(content):
            span = (m.start(), m.end())
            # Avoid overlapping matches from multiple patterns
            if any(s[0] <= span[0] < s[1] or s[0] < span[1] <= s[1] for s in seen_spans):
                continue
            seen_spans.add(span)

            groups = m.groups()
            author = groups[0]
            year = groups[1]
            identifier = groups[2] if len(groups) > 2 else None

            cite = {
                'match_text': m.group(0),
                'author': author,
                'year': year,
                'pmid': None,
                'doi': None,
                'span': span,
            }

            if identifier:
                if identifier.startswith('10.'):
                    cite['doi'] = identifier
                else:
                    cite['pmid'] = identifier

            citations.append(cite)

    # Sort by position in text
    citations.sort(key=lambda c: c['span'][0])
    return citations


def dedup_key(cite: dict) -> str:
    """Generate deduplication key for a citation.

    Two citations are the same if they have identical PMID or identical (author, year).
    """
    if cite['pmid']:
        return f"pmid:{cite['pmid']}"
    return f"{cite['author'].lower()}:{cite['year']}"


def assign_numbers(citations: list[dict]) -> dict[str, int]:
    """Assign sequential [N] numbers to unique citations. Returns key -> number mapping."""
    mapping = {}
    counter = 1
    for cite in citations:
        key = dedup_key(cite)
        if key not in mapping:
            mapping[key] = counter
            counter += 1
    return mapping


def build_reference_entry(cite: dict, num: int) -> str:
    """Build a reference line like: Author et al., Year. PMID: 12345678 [N]

    The [N] must be at the END of the line for format_citations.py's
    build_ref_lookup() to find it (matches trailing [N] on each line).
    """
    parts = [f"{cite['author']},", cite['year'] + "."]
    if cite['pmid']:
        parts.append(f"PMID: {cite['pmid']}")
    elif cite['doi']:
        parts.append(f"DOI: {cite['doi']}")
    parts.append(f"[{num}]")
    return " ".join(parts)


def convert_citations(content: str) -> tuple[str, int, int]:
    """Convert inline parenthetical citations to [N] format.

    Returns (modified_content, unique_count, replacement_count).
    """
    citations = extract_citations(content)
    if not citations:
        return content, 0, 0

    number_map = assign_numbers(citations)

    # Build reference entries (one per unique citation, preserving first-seen order)
    seen_keys = {}
    ref_entries = []
    for cite in citations:
        key = dedup_key(cite)
        if key not in seen_keys:
            num = number_map[key]
            seen_keys[key] = cite
            ref_entries.append(build_reference_entry(cite, num))

    # Replace citations in reverse order to preserve positions
    sorted_cites = sorted(citations, key=lambda c: c['span'][0], reverse=True)
    replacement_count = 0
    for cite in sorted_cites:
        key = dedup_key(cite)
        num = number_map[key]
        start, end = cite['span']
        content = content[:start] + f"[{num}]" + content[end:]
        replacement_count += 1

    # Add per-slide Sources blocks
    content = _add_per_slide_sources(content)

    # Add or update References section
    content = _update_references_section(content, ref_entries)

    return content, len(ref_entries), replacement_count


def _add_per_slide_sources(content: str) -> str:
    """Add **Sources:** [N][M] blocks at the bottom of each slide."""
    cards = content.split('\n---\n')
    new_cards = []

    for card in cards:
        # Find all [N] references in this card
        refs_in_card = sorted(set(int(n) for n in re.findall(r'\[(\d+)\]', card)))
        if refs_in_card:
            # Check if there's already a Sources block
            if '**Sources:**' not in card:
                refs_str = ''.join(f'[{n}]' for n in refs_in_card)
                card = card.rstrip() + f'\n\n**Sources:** {refs_str}\n'
        new_cards.append(card)

    return '\n---\n'.join(new_cards)


def _update_references_section(content: str, ref_entries: list[str]) -> str:
    """Add or replace the References section at the end."""
    # Remove existing References section if present
    ref_markers = ['## References', '# References']
    for marker in ref_markers:
        idx = content.find(marker)
        if idx >= 0:
            # Find the preceding card separator
            before_ref = content[:idx].rstrip()
            content = before_ref + '\n'
            break

    # Build new References section
    ref_section = '\n---\n\n## References\n\n'
    for entry in ref_entries:
        ref_section += f'- {entry}\n'

    content = content.rstrip() + ref_section
    return content


def main():
    parser = argparse.ArgumentParser(
        description='Convert parenthetical citations to [N] numbered format.'
    )
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without writing')
    parser.add_argument('--output', '-o', help='Write to specified file instead of in-place')
    parser.add_argument('--keep-backup', action='store_true', help='Preserve .bak file after successful write')
    args = parser.parse_args()

    filepath = args.input
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    print(f"Read {len(content)} chars from {filepath}")

    converted, unique_count, replacement_count = convert_citations(content)

    if unique_count == 0:
        print("No parenthetical citations found.")
        sys.exit(0)

    print(f"Found {unique_count} unique citations, {replacement_count} replacements made")

    if args.dry_run:
        if converted == original_content:
            print("\n[dry-run] No changes detected.")
        else:
            print(f"\n[dry-run] Would write {len(converted)} chars ({len(converted) - len(original_content):+d} delta)")
            orig_lines = original_content.split('\n')
            new_lines = converted.split('\n')
            changed = 0
            for i, (o, n) in enumerate(zip(orig_lines, new_lines)):
                if o != n:
                    changed += 1
                    if changed <= 10:
                        print(f"  L{i+1}: - {o[:80]}")
                        print(f"  L{i+1}: + {n[:80]}")
            length_diff = len(new_lines) - len(orig_lines)
            if length_diff != 0:
                changed += abs(length_diff)
            if changed > 10:
                print(f"  ... and {changed - 10} more changed lines")
            print("[dry-run] No files modified.")
    else:
        if not args.output:
            shutil.copy(filepath, filepath + '.bak')
            print(f"Backup saved to {filepath}.bak")

        out_path = args.output if args.output else filepath
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(converted)
        print(f"Wrote {len(converted)} chars to {out_path}")
        # Clean up backup file unless --keep-backup was specified
        if not args.output and not args.keep_backup:
            from pathlib import Path
            bak = Path(filepath + '.bak')
            bak.unlink(missing_ok=True)


if __name__ == '__main__':
    main()
