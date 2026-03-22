#!/usr/bin/env python3
"""
verify_citations.py — Automated citation verification for medical presentations.

Usage:
    python3 scripts/verify_citations.py project/presentation.md
    python3 scripts/verify_citations.py project/presentation.md --dry-run
    python3 scripts/verify_citations.py project/presentation.md --output report.txt

Checks:
  - Extracts PMIDs and DOIs from References section
  - Generates verification URLs (PubMed, DOI.org)
  - Flags: [NEEDS VERIFICATION], [DUPLICATE PMID], [ORPHAN CITATION], [UNCITED REFERENCE]

Run AFTER format_citations.py (passes 1-3).
"""

import argparse
import re
from urllib.parse import quote as _url_quote


def extract_body_citations(content: str) -> set:
    """Find all [N] citation numbers used in body text (before References)."""
    ref_start = content.find('# References')
    body = content[:ref_start] if ref_start > 0 else content
    return set(re.findall(r'\[(\d+)\]', body))


def extract_references(content: str) -> dict:
    """Extract reference number -> full line text from References section."""
    refs = {}
    ref_start = content.find('# References')
    if ref_start < 0:
        return refs

    ref_section = content[ref_start:]
    for line in ref_section.split('\n'):
        line = line.strip()
        if not line:
            continue
        # Match [N] at end of line or start patterns like "1. " or "[1]"
        m = re.search(r'\[(\d+)\]\s*$', line)
        if m:
            refs[m.group(1)] = line
            continue
        m2 = re.match(r'^(\d+)\.\s+', line)
        if m2:
            refs[m2.group(1)] = line
            continue
        # Also handle "- [N] Citation text" format
        m3 = re.match(r'^-\s*\[(\d+)\]\s+', line)
        if m3:
            refs[m3.group(1)] = line
            continue
        # Handle "[N] Citation text" at start of line (Vancouver format)
        m4 = re.match(r'^\[(\d+)\]\s+', line)
        if m4:
            refs[m4.group(1)] = line
    return refs


_DOI_STRICT_RE = re.compile(r'^10\.\d{4,9}/[A-Za-z0-9.\-_/()\[\]:!@#$%&*+=?~,]+$')


def extract_pmid(text: str) -> str | None:
    """Extract PMID from reference text."""
    m = re.search(r'PMID[:\s]+(\d{7,8})', text)
    return m.group(1) if m else None


def extract_doi(text: str) -> str | None:
    """Extract DOI from reference text."""
    m = re.search(r'(?:DOI[:\s]+|doi[:\s]+|https?://doi\.org/)(10\.\d{4,}/[^\s\]]+)', text)
    return m.group(1) if m else None


def validate_doi(doi: str) -> bool:
    """Return True if DOI matches strict safe pattern."""
    return bool(_DOI_STRICT_RE.match(doi))


def verify(content: str) -> list:
    """Run all verification checks. Returns list of report lines."""
    report = []
    body_cites = extract_body_citations(content)
    refs = extract_references(content)

    if not refs:
        report.append("WARNING: No References section found.")
        if body_cites:
            report.append(f"  Body contains citations: {sorted(body_cites, key=int)}")
        return report

    report.append(f"Found {len(refs)} references, {len(body_cites)} body citations.\n")

    # Track PMIDs for duplicate detection
    seen_pmids = {}
    ref_nums = set(refs.keys())

    # Per-reference verification
    report.append("=== Reference Verification ===\n")
    for num in sorted(refs.keys(), key=int):
        line = refs[num]
        pmid = extract_pmid(line)
        doi = extract_doi(line)
        flags = []

        if pmid:
            url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            if pmid in seen_pmids:
                flags.append(f"[DUPLICATE PMID] same as [{seen_pmids[pmid]}]")
            seen_pmids[pmid] = num
            report.append(f"  [{num}] PMID {pmid} -> {url}")
        elif doi:
            if validate_doi(doi):
                safe_doi = _url_quote(doi, safe='/:.-_()[]@!$&*+=?~,;')
                url = f"https://doi.org/{safe_doi}"
            else:
                flags.append(f"[INVALID DOI] rejected: {doi[:60]}")
                url = None
            if url:
                report.append(f"  [{num}] DOI -> {url}")
        else:
            flags.append("[NEEDS VERIFICATION]")
            # Truncate line for display
            display = line[:100] + ('...' if len(line) > 100 else '')
            report.append(f"  [{num}] {display}")

        for flag in flags:
            report.append(f"       {flag}")

    # Orphan citations: cited in body but no matching reference
    orphans = sorted(body_cites - ref_nums, key=int) if body_cites - ref_nums else []
    if orphans:
        report.append(f"\n=== Orphan Citations ({len(orphans)}) ===")
        report.append("  Body cites these numbers but no matching reference exists:")
        for n in orphans:
            report.append(f"  [{n}] [ORPHAN CITATION]")

    # Uncited references: in References but never cited in body
    uncited = sorted(ref_nums - body_cites, key=int) if ref_nums - body_cites else []
    if uncited:
        report.append(f"\n=== Uncited References ({len(uncited)}) ===")
        report.append("  These references are never cited in body text:")
        for n in uncited:
            display = refs[n][:80] + ('...' if len(refs[n]) > 80 else '')
            report.append(f"  [{n}] [UNCITED REFERENCE] {display}")

    # Summary
    needs_verify = sum(1 for num in refs if not extract_pmid(refs[num]) and not extract_doi(refs[num]))
    # Count PMIDs that appear in more than one reference
    pmid_counts = {}
    for num in refs:
        pmid = extract_pmid(refs[num])
        if pmid:
            pmid_counts[pmid] = pmid_counts.get(pmid, 0) + 1
    dupes = sum(1 for count in pmid_counts.values() if count > 1)
    report.append(f"\n=== Summary ===")
    report.append(f"  Total references:    {len(refs)}")
    report.append(f"  With PMID:           {len(seen_pmids)}")
    report.append(f"  With DOI only:       {sum(1 for n in refs if not extract_pmid(refs[n]) and extract_doi(refs[n]))}")
    report.append(f"  Needs verification:  {needs_verify}")
    report.append(f"  Duplicate PMIDs:     {dupes}")
    report.append(f"  Orphan citations:    {len(orphans)}")
    report.append(f"  Uncited references:  {len(uncited)}")

    if needs_verify == 0 and dupes == 0 and not orphans and not uncited:
        report.append("\n  PASS: All citations verified.")
    else:
        report.append(f"\n  ISSUES: {needs_verify + dupes + len(orphans) + len(uncited)} total issues found.")

    return report


def cross_check_citations(content_a: str, content_b: str, name_a: str = 'file_a', name_b: str = 'file_b') -> list:
    """Compare citations between two content strings. Returns list of report lines."""
    report = []

    def _pmids_from_content(content: str) -> set:
        refs = extract_references(content)
        result = set()
        for line in refs.values():
            pmid = extract_pmid(line)
            if pmid:
                result.add(pmid)
        return result

    def _dois_from_content(content: str) -> set:
        refs = extract_references(content)
        result = set()
        for line in refs.values():
            doi = extract_doi(line)
            if doi:
                result.add(doi)
        return result

    pmids_a = _pmids_from_content(content_a)
    pmids_b = _pmids_from_content(content_b)
    dois_a = _dois_from_content(content_a)
    dois_b = _dois_from_content(content_b)

    only_a_pmids = sorted(pmids_a - pmids_b)
    only_b_pmids = sorted(pmids_b - pmids_a)
    only_a_dois = sorted(dois_a - dois_b)
    only_b_dois = sorted(dois_b - dois_a)
    shared_pmids = pmids_a & pmids_b
    divergent = len(only_a_pmids) + len(only_b_pmids) + len(only_a_dois) + len(only_b_dois)

    report.append(f"=== Cross-Check: {name_a} vs {name_b} ===")
    report.append(f"PMIDs only in {name_a}: {only_a_pmids if only_a_pmids else []}")
    report.append(f"PMIDs only in {name_b}: {only_b_pmids if only_b_pmids else []}")
    report.append(f"DOIs only in {name_a}: {only_a_dois if only_a_dois else []}")
    report.append(f"DOIs only in {name_b}: {only_b_dois if only_b_dois else []}")
    report.append(f"Shared PMIDs: {len(shared_pmids)}, Divergent: {divergent}")

    return report


def main():
    parser = argparse.ArgumentParser(description='Automated citation verification for medical presentations.')
    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('--dry-run', action='store_true', help='Report only, do not write output file')
    parser.add_argument('--output', '-o', help='Write verification report to file')
    parser.add_argument('--check-links', action='store_true', help='Verify URLs are reachable (requires network)')
    parser.add_argument('--cross-check', metavar='FILE', help='Second markdown file to cross-check citation consistency')
    args = parser.parse_args()

    filepath = args.input
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Read {len(content)} chars from {filepath}")

    report_lines = verify(content)

    if not args.check_links:
        print("\nWARNING: Running without --check-links. URLs are generated but not verified.")
        print("  Use --check-links to confirm PubMed/DOI URLs are reachable.")
    else:
        print("\n--check-links: URL verification requires network access.")
        print("Verifying PubMed/DOI URLs (rate limited)...")
        import urllib.request
        import urllib.error
        import time
        refs = extract_references(content)
        for num in sorted(refs.keys(), key=int):
            pmid = extract_pmid(refs[num])
            doi = extract_doi(refs[num])
            url = None
            if pmid:
                url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                time.sleep(0.5)
            elif doi:
                if validate_doi(doi):
                    safe_doi = _url_quote(doi, safe='/:.-_()[]@!$&*+=?~,;')
                    url = f"https://doi.org/{safe_doi}"
                    time.sleep(0.5)
                else:
                    report_lines.append(f"  [{num}] [INVALID DOI] skipped: {doi[:60]}")
            if url:
                try:
                    req = urllib.request.Request(url, method='HEAD')
                    req.add_header('User-Agent', 'citation-verifier/1.0')
                    resp = urllib.request.urlopen(req, timeout=10)
                    status = resp.getcode()
                    report_lines.append(f"  [{num}] {url} -> HTTP {status}")
                except (urllib.error.URLError, urllib.error.HTTPError) as e:
                    report_lines.append(f"  [{num}] {url} -> FAILED: {e}")

    report_text = '\n'.join(report_lines)
    print(report_text)

    if args.output and not args.dry_run:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report_text + '\n')
        print(f"\nReport written to {args.output}")

    cross_check_divergent = False
    if args.cross_check:
        with open(args.cross_check, 'r', encoding='utf-8') as f:
            content_b = f.read()
        import os
        name_a = os.path.basename(filepath)
        name_b = os.path.basename(args.cross_check)
        cc_lines = cross_check_citations(content, content_b, name_a=name_a, name_b=name_b)
        cc_text = '\n'.join(cc_lines)
        print('\n' + cc_text)
        if args.output and not args.dry_run:
            with open(args.output, 'a', encoding='utf-8') as f:
                f.write('\n' + cc_text + '\n')
        # Determine divergence from last summary line
        last_line = cc_lines[-1] if cc_lines else ''
        if 'Divergent: 0' not in last_line:
            cross_check_divergent = True

    if args.cross_check:
        raise SystemExit(1 if cross_check_divergent else 0)


if __name__ == '__main__':
    main()
