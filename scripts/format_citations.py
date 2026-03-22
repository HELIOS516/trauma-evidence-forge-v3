#!/usr/bin/env python3
"""
format_citations.py — 5-pass citation formatter for medical presentations.

Usage:
    python3 scripts/format_citations.py project/presentation.md

Applies five formatting passes:
  0. Auto-generate missing Sources blocks for slides with [N] citations
  1. Remove [N] from slide titles
  2. Expand Sources: lines to abbreviated citations
  3. Convert in-text [N] to <sup>[N]</sup>
  4. Hyperlink PMID values in final References section
"""

import argparse
import re
import shutil


def _extract_first_url(text: str) -> str | None:
    """Return first URL found in text (raw or markdown link target)."""
    md_link = re.search(r'\]\((https?://[^\s)]+)\)', text)
    if md_link:
        return md_link.group(1)
    raw = re.search(r'(https?://[^\s\])]+)', text)
    if raw:
        return raw.group(1)
    return None


def _truncate_title(title: str, max_words: int = 6, max_chars: int = 52) -> str:
    """Trim long titles for slide footers while preserving meaning."""
    if not title:
        return title
    words = title.split()
    if len(words) > max_words:
        title = ' '.join(words[:max_words]).rstrip(' ,;:.') + '...'
    if len(title) > max_chars:
        title = title[:max_chars].rstrip(' ,;:.') + '...'
    return title


def _abbrev_slide_source(citation: str) -> str:
    """Build ultra-compact slide citation token: LastName Year (linked)."""
    cleaned = citation.strip()
    cleaned = re.sub(r'^\-\s*', '', cleaned)

    pmid_match = re.search(r'PMID[:\s]+(\d+)', cleaned, flags=re.IGNORECASE)
    pmid = pmid_match.group(1) if pmid_match else None
    url = _extract_first_url(cleaned)

    # Remove URL/PMID noise for segment parsing
    parse_text = re.sub(r'\]\((https?://[^\s)]+)\)', '', cleaned)
    parse_text = re.sub(r'https?://[^\s\])]+', '', parse_text)
    parse_text = re.sub(r'PMID[:\s]+\d+', '', parse_text, flags=re.IGNORECASE)
    parse_text = re.sub(r'\s+', ' ', parse_text).strip(' .;')
    parse_text = re.sub(r'^\d+\.\s*', '', parse_text)
    segments = [s.strip(' .;') for s in re.split(r'\.\s+', parse_text) if s.strip(' .;')]

    author = segments[0] if segments else ''
    author = re.sub(r'^\d+\.\s*', '', author)
    if ',' in author:
        author = author.split(',', 1)[0].strip()
    title = segments[1] if len(segments) > 1 else ''
    title = _truncate_title(title)

    year_match = re.search(r'\b(19|20)\d{2}\b', parse_text)
    year = year_match.group(0) if year_match else ''

    journal = ''
    if len(segments) > 2:
        journal_candidate = segments[2]
        journal_candidate = re.sub(r';\s*\d.*$', '', journal_candidate).strip(' ,;.')
        journal_candidate = re.sub(r'\b(19|20)\d{2}\b.*$', '', journal_candidate).strip(' ,;.')
        journal = journal_candidate

    label_parts: list[str] = []
    if author:
        surname = re.sub(r'[^A-Za-z0-9\-].*$', '', author).strip()
        label_parts.append(surname if surname else author.split()[0])
    elif title:
        label_parts.append(title.split()[0])
    elif journal:
        label_parts.append(journal.split()[0])

    if year:
        label_parts.append(year)

    if not label_parts:
        return cleaned

    label = ' '.join(label_parts)
    if pmid:
        return f"[{label}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)"
    if url:
        return f"[{label}]({url})"
    return label


def pass0_auto_sources(content: str) -> tuple[str, int]:
    """Auto-generate missing **Sources:** blocks for slides with [N] citations.

    Returns (modified_content, count_of_slides_fixed).
    """
    # Split on slide delimiters (*** or --- on their own line)
    parts = re.split(r'(^(?:\*\*\*|---)$)', content, flags=re.MULTILINE)

    # Reassemble into slides: [slide_content, separator, slide_content, ...]
    slides: list[str] = []
    current: str = ''
    for part in parts:
        if re.match(r'^(?:\*\*\*|---)$', part):
            slides.append(current)
            slides.append(part)  # separator
            current = ''
        else:
            current += part
    slides.append(current)

    in_references: bool = False
    fixed_count: int = 0

    for i in range(len(slides)):
        slide: str = slides[i]

        # Skip separators
        if re.match(r'^(?:\*\*\*|---)$', slide.strip()):
            continue

        # Detect References section
        if '# References' in slide:
            in_references = True
        if in_references:
            continue

        # Skip if slide already has a Sources block
        if re.search(r'\*\*Sources?:\*\*', slide):
            continue

        # Find all [N] citations in non-heading lines
        lines: list[str] = slide.split('\n')
        citation_nums = set()
        for line in lines:
            if line.startswith('#'):
                continue
            for m in re.finditer(r'\[(\d+)\]', line):
                citation_nums.add(int(m.group(1)))

        if not citation_nums:
            continue

        # Build the Sources block
        sorted_nums = sorted(citation_nums)
        refs_str = ''.join(f'[{n}]' for n in sorted_nums)
        sources_block = f'\n\n**Sources:** {refs_str}'

        # Append before trailing whitespace
        slides[i] = slide.rstrip() + sources_block + '\n'
        fixed_count += 1

    return ''.join(slides), fixed_count


def build_ref_lookup(content: str) -> dict[str, str]:
    """Extract reference number → citation text mapping from References section."""
    refs: dict[str, str] = {}
    ref_start = content.find('# References')
    if ref_start < 0:
        return refs

    start_idx: int = ref_start
    ref_section = content[start_idx:]
    for line in ref_section.split('\n'):
        # Match: **** Citation text [N]
        m = re.search(r'\[(\d+)\]\s*$', line.strip())
        if m:
            num = m.group(1)
            cite = re.sub(r'^\*+\s*', '', line.strip())
            cite = re.sub(r'\[\d+\]\s*$', '', cite).strip()
            refs[num] = cite
        
        # Match: 1. Citation text or [1] Citation text
        if not m:
            m_prefix = re.match(r'^(?:\[(\d+)\]|(\d+)\.)\s+(.*)', line.strip())
            if m_prefix:
                num = m_prefix.group(1) or m_prefix.group(2)
                if num is None:
                    continue
                cite = m_prefix.group(3).strip()
                refs[num] = cite

        # Also handle [PMID UNVERIFIED] tagged refs
        m2 = re.search(r'\[PMID UNVERIFIED[^\]]*\]\[(\d+)\]', line.strip())
        if m2:
            num = m2.group(1)
            cite = re.sub(r'^\*+\s*', '', line.strip())
            cite = re.sub(r'\[PMID UNVERIFIED[^\]]*\]\[\d+\]', '', cite).strip()
            refs[num] = cite

    return refs


def pass1_clean_titles(content: str) -> str:
    """Remove [N] from heading lines."""
    lines = content.split('\n')
    result = []
    for line in lines:
        if line.startswith('#') and not line.startswith('# References'):
            line = re.sub(r'\[(\d+)\]', '', line).strip()
        result.append(line)
    return '\n'.join(result)


def pass2_expand_sources(content: str, refs: dict[str, str]) -> str:
    """Replace compact Sources: [N][M] with abbreviated, linked citation lines."""
    lines = content.split('\n')
    result = []
    for line in lines:
        if '**Sources:**' in line or line.strip().startswith('**Source:**'):
            ref_nums = re.findall(r'\[(\d+)\]', line)
            if ref_nums:
                expanded = []
                for n in ref_nums:
                    if n in refs:
                        expanded.append(f"[{n}] {_abbrev_slide_source(refs[n])}")
                if expanded:
                    result.append('')
                    result.append('**Sources:**')
                    for exp in expanded:
                        result.append(f'- {exp}')
                    continue
        result.append(line)
    return '\n'.join(result)


def pass2b_compact_expanded_sources(content: str, refs: dict[str, str]) -> str:
    """Rewrite full Sources bullets to compact format.

    Handles already-expanded blocks like:
      **Sources:**
      - [1] Very long citation...
    """
    lines = content.split('\n')
    out: list[str] = []
    in_sources = False

    for line in lines:
        stripped = line.strip()
        if re.match(r'^\*\*Sources?:\*\*', stripped):
            in_sources = True
            out.append(line)
            continue

        if in_sources:
            m = re.match(r'^- \[(\d+)\]\s+(.*)$', stripped)
            if m:
                n = m.group(1)
                original_cite = m.group(2).strip()
                cite = refs.get(n, original_cite)
                out.append(f"- [{n}] {_abbrev_slide_source(cite)}")
                continue
            # End Sources block when bullets stop
            if stripped and not stripped.startswith('- '):
                in_sources = False

        out.append(line)

    return '\n'.join(out)


def pass2c_limit_sources_per_slide(content: str, max_sources: int = 4) -> str:
    """Limit number of source bullets shown per slide to reduce visual overload."""
    lines = content.split('\n')
    out: list[str] = []
    in_sources = False
    source_count = 0

    for line in lines:
        stripped = line.strip()
        if re.match(r'^\*\*Sources?:\*\*', stripped):
            in_sources = True
            source_count = 0
            out.append(line)
            continue

        if in_sources:
            if re.match(r'^- \[\d+\]\s+', stripped):
                source_count += 1
                if source_count <= max_sources:
                    out.append(line)
                continue

            in_sources = False
            source_count = 0

        out.append(line)

    return '\n'.join(out)


def pass3_superscript(content: str) -> str:
    """Convert in-text [N] to <sup>[N]</sup>, excluding titles/sources/refs."""
    ref_start = content.find('# References')
    start_idx: int = ref_start
    before = content[:start_idx] if ref_start > 0 else content
    after = content[start_idx:] if ref_start > 0 else ''

    lines = before.split('\n')
    result = []
    for line in lines:
        if line.startswith('#') or '**Sources:**' in line or line.startswith('- ['):
            result.append(line)
        else:
            line = re.sub(r'(?<!<sup>)\[(\d+)\](?!</sup>)', r'<sup>[\1]</sup>', line)
            result.append(line)
    
    combined = '\n'.join(result)
    return combined + after


def pass4_link_reference_pmids(content: str) -> str:
    """Hyperlink PMID identifiers in the final References section."""
    ref_start = content.find('# References')
    if ref_start < 0:
        return content

    before = content[:ref_start]
    after = content[ref_start:]

    # Link only plain PMID numbers that are not already markdown-linked.
    after = re.sub(
        r'PMID:\s*(\d+)(?!\]\()',
        lambda m: f"PMID: [{m.group(1)}](https://pubmed.ncbi.nlm.nih.gov/{m.group(1)}/)",
        after,
    )
    return before + after


def main():
    parser = argparse.ArgumentParser(description='3-pass citation formatter for medical presentations.')
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without writing')
    parser.add_argument('--output', '-o', help='Write to specified file instead of in-place')
    parser.add_argument('--keep-backup', action='store_true', help='Preserve .bak file after successful write')
    args = parser.parse_args()

    filepath = args.input
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    if not args.dry_run and not args.output:
        shutil.copy(filepath, filepath + '.bak')
        print(f"Backup saved to {filepath}.bak")
    print(f"Read {len(content)} chars from {filepath}")

    refs = build_ref_lookup(content)
    print(f"Found {len(refs)} references")

    # Pass 0: Auto-generate missing Sources blocks
    content, pass0_count = pass0_auto_sources(content)
    if pass0_count > 0:
        print(f"Pass 0: Auto-generated Sources blocks for {pass0_count} slides")
    else:
        print("Pass 0: All slides with citations already have Sources blocks, skipping")

    # Pass 1: Clean titles — skip if no headings contain bare [N] (not already superscripted)
    headings = [l for l in content.split('\n') if l.startswith('#') and not l.startswith('# References')]
    bare_refs_in_headings = any(re.search(r'\[\d+\]', h) for h in headings)
    if bare_refs_in_headings:
        content = pass1_clean_titles(content)
        print("Pass 1: Cleaned slide titles")
    else:
        print("Pass 1: Already applied, skipping")

    # Pass 2: Expand sources — skip if no compact Sources: lines with [N] remain
    compact_sources = re.findall(r'^\*\*Sources?:\*\*.*\[\d+\]', content, re.MULTILINE)
    if compact_sources:
        content = pass2_expand_sources(content, refs)
        print("Pass 2: Expanded sources lines")
    else:
        print("Pass 2: Already applied, skipping")

    # Pass 2b: Compact already-expanded Sources bullets
    content = pass2b_compact_expanded_sources(content, refs)
    print("Pass 2b: Compacted expanded Sources bullets")

    # Pass 2c: Limit number of source lines per slide
    content = pass2c_limit_sources_per_slide(content, max_sources=4)
    print("Pass 2c: Limited Sources bullets per slide (max 4)")

    # Pass 3: Superscript — skip if all [N] in body text are already wrapped in <sup>
    ref_start = content.find('# References')
    start_idx: int = ref_start
    body = content[:start_idx] if ref_start > 0 else content
    body_lines = [l for l in body.split('\n')
                  if not l.startswith('#') and '**Sources:**' not in l and not l.startswith('- [')]
    body_text = '\n'.join(body_lines)
    bare_refs_in_body = re.search(r'(?<!<sup>)\[(\d+)\](?!</sup>)', body_text)
    if bare_refs_in_body:
        content = pass3_superscript(content)
        print("Pass 3: Applied superscript citations")
    else:
        print("Pass 3: Already applied, skipping")

    # Pass 4: Link PMIDs in final references
    content = pass4_link_reference_pmids(content)
    print("Pass 4: Linked PMID entries in references")

    if args.dry_run:
        if content == original_content:
            print("\n[dry-run] No changes detected.")
        else:
            print(f"\n[dry-run] Would write {len(content)} chars ({len(content) - len(original_content):+d} delta)")
            # Show a summary of changed lines
            orig_lines = original_content.split('\n')
            new_lines = content.split('\n')
            changed: int = 0
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
        # Clean up backup file unless --keep-backup was specified
        if not args.output and not args.keep_backup:
            from pathlib import Path
            bak = Path(filepath + '.bak')
            bak.unlink(missing_ok=True)


if __name__ == '__main__':
    main()
