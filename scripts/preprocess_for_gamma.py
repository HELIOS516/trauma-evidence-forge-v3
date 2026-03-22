#!/usr/bin/env python3
"""
preprocess_for_gamma.py — Pre-process markdown for Gamma preserve mode.

Usage:
    python3 scripts/preprocess_for_gamma.py project/presentation.md

Applies passes to prepare content for textMode "preserve":
  4. Strip header block (before first ---)
  5. Strip ### SLIDE N: lines
  6. Strip **Gamma instruction: lines
  7. Convert *** to --- (Gamma card separators)
  8. Convert ---* reference lines to standard list items
 9. Extract speaker notes from HTML comments to companion file
10. Normalize first heading per card to ## (Gamma card header)
11. Fix concatenated reference entries (PMID running into next ref number)
 13. Ensure Bottom Line block appears above Sources block within each card

Run AFTER format_citations.py (passes 1-3).
"""

import argparse
import os
import re
import shutil
import sys


def pass4_strip_header(content: str) -> str:
    """Strip header block (before first *** or --- on its own line)."""
    m = re.search(r'^\*\*\*$', content, re.MULTILINE)
    first_break = m.start() if m else -1
    if first_break < 0:
        m2 = re.search(r'^---$', content, re.MULTILINE)
        first_break = m2.start() if m2 else -1
    if first_break > 0:
        content = content[first_break:]
    return content


def pass5_strip_slide_markers(content: str) -> str:
    """Strip ### SLIDE N: and ### FINAL SLIDE: lines."""
    content = re.sub(r'^### SLIDE \d+:.*\n+', '', content, flags=re.MULTILINE)
    content = re.sub(r'^### FINAL SLIDE:.*\n+', '', content, flags=re.MULTILINE)
    return content


def pass6_extract_and_strip_gamma_instructions(content: str, instructions_path: str | None = None) -> str:
    """Extract **Gamma instruction: ...** lines to companion JSON, then strip from content."""
    instructions = {}
    cards = re.split(r'\n---\n', content)
    for i, card in enumerate(cards):
        matches = re.findall(r'\*\*Gamma instruction:\s*(.+?)\*\*', card)
        if matches:
            # Find the card's heading for context
            title_match = re.search(r'^#{1,6}\s+(.+)', card, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else f"Slide {i+1}"
            title = re.sub(r'\s*\[LO:\s*[\d,\s]+\]', '', title).strip()
            instructions[str(i + 1)] = {
                "title": title,
                "instruction": matches[0].strip(),
            }
    if instructions and instructions_path:
        import json
        with open(instructions_path, 'w', encoding='utf-8') as f:
            json.dump(instructions, f, indent=2)
    # Strip the lines from content
    return re.sub(r'^\*\*Gamma instruction:.*\*\*\s*\n+', '', content, flags=re.MULTILINE)


def pass7_convert_separators(content: str) -> str:
    """Convert standalone *** to --- (only on its own line)."""
    return re.sub(r'^\*\*\*$', '---', content, flags=re.MULTILINE)


def pass8_convert_ref_lines(content: str) -> str:
    """Convert ---* reference lines to standard list items."""
    return re.sub(r'^---\* ', '- ', content, flags=re.MULTILINE)


def pass9_extract_and_strip_comments(content: str, notes_path: str | None = None) -> str:
    """Extract HTML comments to companion file, strip from content."""
    comments = re.findall(r'<!--([\s\S]*?)-->', content)
    if comments and notes_path:
        cards = content.split('\n---\n')
        notes_lines = ["# Speaker Notes\n", "# Extracted from gamma-ready markdown\n\n"]
        for i, card in enumerate(cards, 1):
            card_comments = re.findall(r'<!--([\s\S]*?)-->', card)
            if card_comments:
                title_match = re.search(r'^#{1,6}\s+(.+)', card, re.MULTILINE)
                title = title_match.group(1) if title_match else f"Slide {i}"
                notes_lines.append(f"## Slide {i}: {title}\n")
                for c in card_comments:
                    cleaned = re.sub(r'^Speaker Notes:\s*', '', c.strip())
                    notes_lines.append(cleaned + "\n\n")
        with open(notes_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(notes_lines))
    content = re.sub(r'<!--[\s\S]*?-->\s*', '', content)
    return content


def pass10_normalize_headings(content: str) -> str:
    """Normalize first heading after each card separator to ## (Gamma card header)."""
    lines = content.split('\n')
    result = []
    after_separator = True  # First card starts at top
    for line in lines:
        if line.strip() == '---':
            after_separator = True
            result.append(line)
        elif after_separator and re.match(r'^#{1,6}\s', line):
            heading_text = re.sub(r'^#{1,6}\s+', '', line)
            result.append(f'## {heading_text}')
            after_separator = False
        else:
            if line.strip():
                after_separator = False
            result.append(line)
    return '\n'.join(result)


def pass11_fix_concat_refs(content: str) -> str:
    """Split concatenated reference entries where PMID runs into next ref number.

    Scoped to the references section only (after '# References' heading) to avoid
    corrupting numeric data in tables or other content.
    """
    ref_heading = re.search(r'^#\s+References\s*$', content, re.MULTILINE | re.IGNORECASE)
    if not ref_heading:
        return content
    pre = content[:ref_heading.start()]
    refs = content[ref_heading.start():]
    refs = re.sub(r'(\d{7,8})(\d+\.\s+)', lambda m: m.group(1) + '\n' + m.group(2), refs)
    return pre + refs


def pass12_strip_lo_tags(content: str) -> str:
    """Strip [LO: N,M] learning objective tags from content."""
    return re.sub(r'\[LO:\s*[\d,\s]+\]\s*\n?', '', content)


def pass13_bottom_line_above_sources(content: str) -> str:
    """Reorder per-card blocks so Bottom Line is always above Sources."""
    cards = content.split('\n---\n')
    reordered: list[str] = []

    for card in cards:
        sources_match = re.search(
            r'(\*\*Sources?:\*\*\s*\n(?:- \[\d+\].*(?:\n|$))*)',
            card,
            flags=re.MULTILINE,
        )
        bottom_match = re.search(
            r'(>\s*\*\*Bottom Line:\*\*.*(?:\n>\s*.*)*)',
            card,
            flags=re.MULTILINE,
        )

        if not (sources_match and bottom_match):
            reordered.append(card)
            continue

        if bottom_match.start() < sources_match.start():
            reordered.append(card)
            continue

        s_start, s_end = sources_match.span()
        b_start, b_end = bottom_match.span()
        sources_text = sources_match.group(1).strip()
        bottom_text = bottom_match.group(1).strip()

        pre_sources = card[:s_start].rstrip()
        between = card[s_end:b_start].strip()
        post_bottom = card[b_end:].lstrip()

        parts = [pre_sources]
        if between:
            parts.append(between)
        parts.append(bottom_text)
        parts.append(sources_text)
        if post_bottom:
            parts.append(post_bottom.rstrip())

        new_card = '\n\n'.join(p for p in parts if p != '')
        new_card = re.sub(r'\n{3,}', '\n\n', new_card)
        reordered.append(new_card)

    return '\n---\n'.join(reordered)


def main():
    parser = argparse.ArgumentParser(description='Pre-process markdown for Gamma preserve mode.')
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without writing')
    parser.add_argument('--output', '-o', help='Write to specified file instead of in-place')
    parser.add_argument('--notes-output', help='Write speaker notes to specified file (default: auto-generate from input path)')
    args = parser.parse_args()

    filepath = args.input
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    if not args.dry_run and not args.output:
        shutil.copy(filepath, filepath + '.bak')
        print(f"Backup saved to {filepath}.bak")
    original_len = len(content)
    print(f"Read {original_len} chars from {filepath}")

    # Pass 4: Strip header block — skip if content already starts with ---
    if content.startswith('---'):
        print("Pass 4: Already applied, skipping")
    else:
        content = pass4_strip_header(content)
        if content != original_content:
            print("Pass 4: Stripped header block")
        else:
            print("Pass 4: No header block found")

    # Pass 5: Strip SLIDE marker lines — skip if no ### SLIDE lines found
    if not re.search(r'^### SLIDE \d+:', content, re.MULTILINE) and \
       not re.search(r'^### FINAL SLIDE:', content, re.MULTILINE):
        print("Pass 5: Already applied, skipping")
    else:
        content = pass5_strip_slide_markers(content)
        print("Pass 5: Stripped SLIDE marker lines")

    # Pass 6: Extract + strip Gamma instruction lines — skip if none found
    if not re.search(r'^\*\*Gamma instruction:', content, re.MULTILINE):
        print("Pass 6: Already applied, skipping")
    else:
        base, ext = os.path.splitext(args.output if args.output else filepath)
        instr_path = base + '-instructions.json'
        if not args.dry_run:
            instr_count = len(re.findall(r'^\*\*Gamma instruction:', content, re.MULTILINE))
            content = pass6_extract_and_strip_gamma_instructions(content, instr_path)
            print(f"Pass 6: Extracted {instr_count} Gamma instructions to {instr_path}, stripped from content")
        else:
            content = pass6_extract_and_strip_gamma_instructions(content)
            print("Pass 6: [dry-run] Would extract + strip Gamma instruction lines")

    # Pass 7: Convert *** to --- — skip if no *** found
    if '***' not in content:
        print("Pass 7: Already applied, skipping")
    else:
        content = pass7_convert_separators(content)
        print("Pass 7: Converted *** to ---")

    # Pass 8: Convert ---* reference lines to list items — skip if no ---* found
    if not re.search(r'^---\* ', content, re.MULTILINE):
        print("Pass 8: Already applied, skipping")
    else:
        content = pass8_convert_ref_lines(content)
        count_8 = len(re.findall(r'^---\*', content, re.MULTILINE))
        print(f"Pass 8: Converted ---* reference lines to list items ({count_8} remaining)")

    # Pass 9: Extract speaker notes from HTML comments — skip if no comments found
    if '<!--' not in content:
        print("Pass 9: Already applied, skipping")
    else:
        if args.notes_output:
            notes_path = args.notes_output
        else:
            base, ext = os.path.splitext(args.output if args.output else filepath)
            notes_path = base + '-notes' + ext
        comment_count = len(re.findall(r'<!--[\s\S]*?-->', content))
        if not args.dry_run:
            content = pass9_extract_and_strip_comments(content, notes_path)
            print(f"Pass 9: Extracted {comment_count} HTML comments to {notes_path}")
        else:
            content = pass9_extract_and_strip_comments(content, notes_path=None)
            print(f"Pass 9: [dry-run] Would extract {comment_count} HTML comments to {notes_path}")

    # Pass 10: Normalize first heading per card to ## — skip if all already ##
    cards = content.split('\n---\n')
    needs_normalize = False
    for card in cards:
        lines = card.strip().split('\n')
        for line in lines:
            if re.match(r'^#{1,6}\s', line):
                if not line.startswith('## '):
                    needs_normalize = True
                break
    if not needs_normalize:
        print("Pass 10: Already applied, skipping")
    else:
        content = pass10_normalize_headings(content)
        print("Pass 10: Normalized first headings per card to ##")

    # Pass 11: Fix concatenated reference entries — skip if no 9+ digit sequences before ". "
    if not re.search(r'\d{9,}\.\s+', content):
        print("Pass 11: Already applied, skipping")
    else:
        content = pass11_fix_concat_refs(content)
        print("Pass 11: Fixed concatenated reference entries")

    # Pass 12: Strip [LO: N,M] learning objective tags — skip if none found
    if not re.search(r'\[LO:\s*[\d,\s]+\]', content):
        print("Pass 12: Already applied, skipping")
    else:
        lo_count = len(re.findall(r'\[LO:\s*[\d,\s]+\]', content))
        content = pass12_strip_lo_tags(content)
        print(f"Pass 12: Stripped {lo_count} [LO: ...] tags")

    # Pass 13: Ensure Bottom Line appears above Sources
    content_after_13 = pass13_bottom_line_above_sources(content)
    if content_after_13 == content:
        print("Pass 13: Already applied, skipping")
    else:
        content = content_after_13
        print("Pass 13: Reordered Bottom Line above Sources where needed")

    breaks = content.count('\n---\n')
    print(f"\nResult: {len(content)} chars ({original_len - len(content)} removed)")
    print(f"Card breaks: {breaks} (= {breaks + 1} slides)")

    # Verify no leftover meta-lines
    for pattern, label in [
        (r'^### SLIDE', 'SLIDE markers'),
        (r'\*\*Gamma instruction:', 'Gamma instructions'),
        (r'^---\*', '---* reference lines (card break collision)'),
        (r'<!--', 'HTML comments'),
        (r'\d{9,}\.\s+', 'concatenated reference sequences (9+ digits)'),
    ]:
        matches = re.findall(pattern, content, re.MULTILINE)
        if matches:
            print(f"WARNING: {len(matches)} remaining {label}!")
        else:
            print(f"OK: No remaining {label}")

    # Check heading normalization
    cards_check = content.split('\n---\n')
    bad_headings = 0
    for card in cards_check:
        lines = card.strip().split('\n')
        for line in lines:
            if re.match(r'^#{1,6}\s', line):
                if not line.startswith('## '):
                    bad_headings += 1
                break
    if bad_headings:
        print(f"WARNING: {bad_headings} non-## first headings per card!")
    else:
        print("OK: All first headings per card are ##")

    if args.dry_run:
        if content == original_content:
            print("\n[dry-run] No changes detected.")
        else:
            print(f"\n[dry-run] Would write {len(content)} chars ({len(content) - len(original_content):+d} delta)")
            orig_lines = original_content.split('\n')
            new_lines = content.split('\n')
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
        out_path = args.output if args.output else filepath
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Wrote {len(content)} chars to {out_path}")


if __name__ == '__main__':
    main()
