#!/usr/bin/env python3
"""card_utils.py — Shared card parsing utilities for presentation pipeline."""

import re


# ---------------------------------------------------------------------------
# Shared constants — single source of truth for both audit and validate scripts
# ---------------------------------------------------------------------------

# Type-specific thresholds: {card_type: {body_max, bullets_max, table_rows_max, table_cols_max, total_max}}
THRESHOLDS = {
    "Content": {"body_max": 50, "bullets_max": 6, "table_rows_max": 6, "table_cols_max": 4, "total_max": 280},
    "Case": {"body_max": 60, "bullets_max": 8, "table_rows_max": None, "table_cols_max": None, "total_max": 300},
    "Data/Table": {"body_max": 25, "bullets_max": 3, "table_rows_max": 8, "table_cols_max": 5, "total_max": 350},
    "Trial": {"body_max": 50, "bullets_max": 4, "table_rows_max": 7, "table_cols_max": 5, "total_max": 300},
    "Guideline": {"body_max": 20, "bullets_max": 2, "table_rows_max": 10, "table_cols_max": 6, "total_max": 400},
    "MCQ": {"body_max": 80, "bullets_max": 5, "table_rows_max": None, "table_cols_max": None, "total_max": 250},
    "Learning Objectives": {"body_max": 60, "bullets_max": 6, "table_rows_max": None, "table_cols_max": None, "total_max": 200},
    "References": {"body_max": None, "bullets_max": None, "table_rows_max": None, "table_cols_max": None, "total_max": None},
    "Title": {"body_max": None, "bullets_max": None, "table_rows_max": None, "table_cols_max": None, "total_max": None},
    "Disclosures": {"body_max": None, "bullets_max": None, "table_rows_max": None, "table_cols_max": None, "total_max": None},
    "Q&A": {"body_max": None, "bullets_max": None, "table_rows_max": None, "table_cols_max": None, "total_max": None},
    "Take-Home": {"body_max": 80, "bullets_max": 10, "table_rows_max": None, "table_cols_max": None, "total_max": 300},
}

# Card types exempt from content density checks
EXEMPT_TYPES = {"Title", "Disclosures", "References", "Q&A"}

# Card types that require a Bottom Line blockquote
BOTTOM_LINE_REQUIRED = {"Content", "Data/Table", "Trial", "Guideline", "Case", "Take-Home"}


def split_cards(content: str) -> list[str]:
    """Split markdown content on \n---\n card separators."""
    return re.split(r'\n---\n', content)


def classify_card(card: str, index: int, total: int, presenter: str = "") -> str:
    """Classify a card by type using content heuristics.

    Returns one of: Title, Disclosures, Learning Objectives, Case, Data/Table,
    MCQ, Content, References, Q&A, Take-Home, Guideline, Trial
    """
    text = card.strip()
    lower = text.lower()

    if index == 0:
        return "Title"
    if presenter and presenter.lower().split(',')[0] in lower and index <= 2:
        return "Title"

    if 'disclosure' in lower or 'financial' in lower or 'conflicts of interest' in lower:
        return "Disclosures"

    if 'learning objective' in lower and index <= 5:
        return "Learning Objectives"

    if re.search(r'\n\s*(\*\*)?[A-D][\.\)]', text) and (
        re.search(r'question', lower) or 'mcq' in lower or 'knowledge check' in lower
    ):
        return "MCQ"

    if re.search(r'\d+[\s-]*(year|yo|y/?o|month)', lower) and (
        'present' in lower or 'arrive' in lower or 'brought' in lower
    ):
        return "Case"

    # Check for tables — classify by heading context, not cell content
    if ('|---|' in text or '|:--|' in text or '|--:|' in text):
        heading = get_title(card).lower()
        if 'guideline' in heading or 'society' in heading or 'recommendation' in heading:
            return "Guideline"
        if 'trial' in heading or 'rct' in heading or 'pico' in heading:
            return "Trial"
        return "Data/Table"

    # Check first heading for special types
    for line in text.split('\n'):
        stripped = line.strip()
        if stripped.startswith('#'):
            heading_lower = stripped.lower()
            if 'reference' in heading_lower:
                return "References"
            if 'question' in heading_lower or 'q&a' in heading_lower:
                return "Q&A"
            if 'take-home' in heading_lower or 'take home' in heading_lower or 'summary' in heading_lower:
                return "Take-Home"
            if 'guideline' in heading_lower and ('comparison' in heading_lower or 'versus' in heading_lower):
                return "Guideline"
            if 'emerging' in heading_lower or 'future' in heading_lower:
                return "Content"
            break

    return "Content"


def get_title(card: str) -> str:
    """Extract the first main heading from a card, skipping slide markers."""
    for line in card.strip().split('\n'):
        stripped = line.strip()
        if stripped.startswith('#'):
            # Skip slide markers like "### SLIDE 1: TITLE"
            if re.search(r'###\s*SLIDE\s*\d+:', stripped, re.IGNORECASE):
                continue
            return re.sub(r'^#{1,6}\s+', '', stripped).strip()
    return "(untitled)"


def count_body_words(card: str) -> int:
    """Count words in card body, excluding tables, headings, blockquotes, sources, and speaker notes."""
    word_counts: list[int] = []
    in_table = False
    in_notes = False
    for line in card.strip().split('\n'):
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        if stripped.startswith('>'):
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
        clean = re.sub(r'\*\*.*?\*\*', lambda m: m.group(0).replace('**', ''), clean)
        word_counts.append(len(clean.split()))
    return sum(word_counts)


def count_table_words(card: str) -> int:
    """Count words inside table rows (| ... | lines)."""
    word_counts: list[int] = []
    for line in card.strip().split('\n'):
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|'):
            if re.match(r'^\|[\s:-]+\|', stripped):
                continue
            parts = stripped.split('|')
            if len(parts) > 2:
                # Use explicit range to aid static analysis
                start = 1
                stop = len(parts) - 1
                cells = [parts[i] for i in range(start, stop)]
                for cell in cells:
                    clean = cell.strip()
                    clean = re.sub(r'<sup>\[\d+\]</sup>', '', clean)
                    clean = re.sub(r'\*\*', '', clean)
                    word_counts.append(len(clean.split()))
    return sum(word_counts)


def count_bullets(card: str) -> int:
    """Count list items, excluding source lines and speaker notes."""
    bullet_marks: list[int] = []
    in_notes = False
    for line in card.strip().split('\n'):
        stripped = line.strip()
        if '<!--' in stripped:
            if '-->' not in stripped:
                in_notes = True
            continue
        if '-->' in stripped:
            in_notes = False
            continue
        if in_notes:
            continue
            
        if stripped.startswith('- ') or stripped.startswith('* ') or re.match(r'^\d+\.\s', stripped):
            # Exclude source citation lines like "- [1] Author..."
            if re.match(r'^- \[\d+\]', stripped):
                continue
            bullet_marks.append(1)
    return sum(bullet_marks)


def extract_tables(card: str) -> list[dict]:
    """Extract table dimensions from card. Returns list of {rows, cols, words}."""
    tables = []
    current_rows = []
    max_cols = 0
    in_notes = False

    def process_table(rows: list[str], total_cols: int) -> dict:
        table_word_counts = []
        for row in rows:
            parts = row.split('|')
            if len(parts) > 2:
                # Use explicit range to aid static analysis
                start = 1
                stop = len(parts) - 1
                cells = [parts[i] for i in range(start, stop)]
                for cell in cells:
                    clean = re.sub(r'<sup>\[\d+\]</sup>', '', cell.strip())
                    clean = re.sub(r'\*\*', '', clean)
                    table_word_counts.append(len(clean.split()))
        return {
            'rows': len(rows),
            'cols': total_cols,
            'words': sum(table_word_counts)
        }

    for line in card.strip().split('\n'):
        stripped = line.strip()
        if '<!--' in stripped:
            if '-->' not in stripped: in_notes = True
            continue
        if '-->' in stripped:
            in_notes = False
            continue
        if in_notes: continue

        if stripped.startswith('|') and stripped.endswith('|'):
            parts = stripped.split('|')
            if re.match(r'^\|[\s:-]+\|', stripped):
                num_cells = len(parts) - 2
                if num_cells > max_cols: max_cols = num_cells
                continue
            current_rows.append(stripped)
            num_cells = len(parts) - 2
            if num_cells > max_cols: max_cols = num_cells
        else:
            if current_rows:
                tables.append(process_table(current_rows, max_cols))
                current_rows = []
                max_cols = 0

    if current_rows:
        tables.append(process_table(current_rows, max_cols))

    return tables


def has_bottom_line(card: str) -> bool:
    """Check if card has a Bottom Line blockquote."""
    return bool(re.search(r'>\s*\*\*Bottom Line:\*\*', card))


def has_sources(card: str) -> bool:
    """Check if card has a Sources block or citation list."""
    if re.search(r'\*\*Sources?:\*\*', card):
        return True
    # Check for numbered citation list
    if re.search(r'^- \[\d+\]', card, re.MULTILINE):
        return True
    return False


def has_citations(card: str) -> bool:
    """Check if card body references citations via <sup>[N]</sup> or [N]."""
    if re.search(r'<sup>\[\d+\]</sup>', card):
        return True
    # Check for [N] refs but not inside Sources blocks or citation list lines
    for line in card.strip().split('\n'):
        stripped = line.strip()
        if stripped.startswith('**Sources:**') or stripped.startswith('**Source:**'):
            continue
        if re.match(r'^- \[\d+\]', stripped):
            continue
        if re.search(r'\[\d+\]', stripped):
            return True
    return False


_VERB_SET = frozenset({
    'account', 'accounts', 'achieve', 'achieves', 'activate', 'activates',
    'address', 'addresses', 'adjust', 'adjusts', 'affect', 'affects',
    'aim', 'aims', 'align', 'applies', 'apply', 'are', 'associates',
    'attenuates', 'avoid', 'avoids', 'blocks', 'brace', 'braces',
    'can', 'capture', 'captures', 'causes', 'change', 'changes',
    'check', 'checks', 'choose', 'combine', 'combines', 'compare',
    'compares', 'confirm', 'confirms', 'continue', 'correlates',
    'decompress', 'decompresses', 'decrease', 'decreases', 'define',
    'defines', 'demonstrate', 'demonstrates', 'describe', 'describes',
    'determine', 'determines', 'differ', 'differs', 'discuss',
    'distinguish', 'distinguishes', 'document', 'documents', 'doubles',
    'drive', 'drives', 'elevates', 'enables', 'enhance', 'enhances',
    'escalate', 'escalates', 'establish', 'evaluate', 'evaluates',
    'evacuate', 'evacuates', 'exceed', 'exceeds', 'explain', 'explains',
    'fail', 'fails', 'favor', 'favors', 'focus', 'focuses',
    'guide', 'guides', 'had', 'halves', 'has', 'have', 'identify',
    'identifies', 'illustrate', 'illustrates', 'implement', 'implements',
    'improve', 'improves', 'include', 'includes', 'increase', 'increases',
    'influence', 'influences', 'inhibits', 'incorporate', 'incorporates',
    'is', 'lack', 'lacks', 'leads', 'limit', 'limits', 'list',
    'lower', 'lowers', 'maintain', 'maintains', 'map', 'maps',
    'maximize', 'maximizes', 'may', 'measure', 'measures', 'minimize',
    'minimizes', 'modify', 'modifies', 'monitor', 'must',
    'operationalize', 'operationalizes', 'optimize', 'optimizes',
    'outline', 'outlines', 'outperform', 'outperforms',
    'potentiates', 'predicts', 'present', 'presents', 'prevent',
    'prevents', 'prioritize', 'prioritizes', 'provides',
    'raise', 'raises', 'recognize', 'recognizes', 'recommend',
    'recommends', 'reduce', 'reduces', 'remain', 'remains', 'replace',
    'replaces', 'require', 'requires', 'resolve', 'resolves', 'return',
    'review', 'reviews', 'screen', 'screens', 'select', 'selects',
    'separate', 'separates', 'should', 'shows', 'specify', 'specifies',
    'stagger', 'staggers', 'standardize', 'start', 'stop', 'substitute',
    'substitutes', 'suggests', 'support', 'supports', 'suppress',
    'suppresses', 'summarize', 'summarizes', 'tailor', 'tailors',
    'target', 'targets', 'test', 'tests', 'track', 'tracks', 'transfers',
    'trigger', 'triggers', 'triples', 'use', 'used', 'uses',
    'utilize', 'utilizes', 'vary', 'varies', 'verify', 'verifies',
    'warrant', 'warrants', 'was', 'were', 'will',
})


def title_has_verb(title: str) -> bool:
    """Heuristic: check if title contains a verb (assertion-evidence style)."""
    title_lower = title.lower()
    title_clean = re.sub(r'\([^)]*\)', '', title_lower)
    words = title_clean.split()
    return any(w in _VERB_SET for w in words)
