#!/usr/bin/env python3
"""AI text detection for academic surgical writing.

Scores text across 8 categories (0-100 scale).
Higher scores indicate greater likelihood of AI generation.
"""

import argparse
import json
import os
import re
import sys


HEDGING_PHRASES = [
    r'it is important to note that',
    r'it should be noted that',
    r'it is worth mentioning that',
    r'it is interesting to observe that',
    r'it is essential to understand that',
    r'one must consider that',
    r'it cannot be overstated that',
    r'it bears mentioning that',
]

TRANSITION_WORDS = [
    r'^furthermore,',
    r'^moreover,',
    r'^additionally,',
    r'^in addition,',
    r'^similarly,',
    r'^consequently,',
    r'^nevertheless,',
    r'^nonetheless,',
    r'^accordingly,',
    r'^conversely,',
]

OVERQUALIFICATION_PHRASES = [
    r'comprehensive analysis',
    r'robust study',
    r'thorough investigation',
    r'rigorous examination',
    r'extensive research',
    r'groundbreaking study',
    r'novel approach',
    r'significant finding',
    r'important contribution',
    r'valuable insights',
]

ENUMERATION_PATTERNS = [
    r'(?:^|\.\s+)first(?:ly)?,.*(?:^|\.\s+)second(?:ly)?,',
    r'(?:^|\.\s+)first,.*second,.*third,',
    r'there are (?:several|three|four|five) (?:key |main |important )?(?:factors|reasons|aspects|points)',
    r'the following (?:points|factors|aspects) are',
]


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 5]


def score_hedging(text: str) -> dict:
    """Score hedging cluster density (weight: 15/100)."""
    text_lower = text.lower()
    word_count = len(text.split())
    count = 0
    matches = []
    for phrase in HEDGING_PHRASES:
        found = re.findall(phrase, text_lower)
        count += len(found)
        if found:
            matches.append(phrase.replace(r'\b', ''))

    per_1000 = (count / max(word_count, 1)) * 1000
    if per_1000 <= 3:
        score = 0
    elif per_1000 <= 6:
        score = 5
    elif per_1000 <= 9:
        score = 10
    else:
        score = 15

    return {'score': score, 'count': count, 'per_1000_words': round(per_1000, 2), 'matches': matches}


def score_transitions(text: str) -> dict:
    """Score transition word density (weight: 15/100)."""
    sentences = _split_sentences(text)
    if not sentences:
        return {'score': 0, 'count': 0, 'percentage': 0}

    count = 0
    for sentence in sentences:
        for pattern in TRANSITION_WORDS:
            if re.search(pattern, sentence.strip(), re.IGNORECASE):
                count += 1
                break

    percentage = (count / len(sentences)) * 100
    if percentage <= 2:
        score = 0
    elif percentage <= 5:
        score = 5
    elif percentage <= 8:
        score = 10
    else:
        score = 15

    return {'score': score, 'count': count, 'percentage': round(percentage, 2)}


def score_sentence_uniformity(text: str) -> dict:
    """Score sentence length uniformity (weight: 15/100)."""
    sentences = _split_sentences(text)
    if len(sentences) < 5:
        return {'score': 0, 'cv': 0, 'mean_length': 0, 'std_length': 0}

    lengths = [len(s.split()) for s in sentences]
    mean = sum(lengths) / len(lengths)
    variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
    std = variance ** 0.5
    cv = std / mean if mean > 0 else 0

    if cv > 0.45:
        score = 0
    elif cv > 0.35:
        score = 5
    elif cv > 0.25:
        score = 10
    else:
        score = 15

    return {'score': score, 'cv': round(cv, 3), 'mean_length': round(mean, 1), 'std_length': round(std, 1)}


def score_overqualification(text: str) -> dict:
    """Score over-qualification phrases (weight: 10/100)."""
    text_lower = text.lower()
    word_count = len(text.split())
    count = 0
    matches = []
    for phrase in OVERQUALIFICATION_PHRASES:
        found = re.findall(phrase, text_lower)
        count += len(found)
        if found:
            matches.append(phrase)

    per_1000 = (count / max(word_count, 1)) * 1000
    if per_1000 <= 1:
        score = 0
    elif per_1000 <= 3:
        score = 3
    elif per_1000 <= 5:
        score = 7
    else:
        score = 10

    return {'score': score, 'count': count, 'matches': matches}


def score_missing_jargon(text: str) -> dict:
    """Score absence of field-specific abbreviations (weight: 10/100)."""
    abbreviations = [
        r'\bISS\b', r'\bGCS\b', r'\bFAST\b', r'\bREBOA\b', r'\bMTP\b',
        r'\bDCR\b', r'\bDCS\b', r'\bMAP\b', r'\bCVP\b', r'\bECMO\b',
        r'\bPRBC\b', r'\bFFP\b', r'\bPLT\b', r'\bTXA\b', r'\bASA\b',
        r'\bICU\b', r'\bOR\b', r'\bED\b', r'\bSBP\b', r'\bUOP\b',
        r'\bACS\b', r'\bTBI\b', r'\bARDS\b', r'\bDVT\b', r'\bVTE\b',
        r'\bPE\b', r'\bINR\b', r'\bPOMR\b', r'\bNSOAP\b', r'\bLCoGS\b',
    ]
    word_count = len(text.split())
    count = sum(1 for abbr in abbreviations if re.search(abbr, text))
    per_1000 = (count / max(word_count, 1)) * 1000

    if count >= 15:
        score = 0
    elif count >= 10:
        score = 3
    elif count >= 5:
        score = 7
    else:
        score = 10

    return {'score': score, 'abbreviation_count': count}


def score_repetitive_structure(text: str) -> dict:
    """Score repetitive paragraph structure (weight: 10/100)."""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip() and len(p.strip()) > 50]
    if len(paragraphs) < 3:
        return {'score': 0, 'template_paragraphs': 0}

    template_count = 0
    for para in paragraphs[:10]:
        sentences = _split_sentences(para)
        if len(sentences) >= 3:
            lengths = [len(s.split()) for s in sentences]
            if len(lengths) >= 3:
                diffs = [abs(lengths[i] - lengths[i + 1]) for i in range(len(lengths) - 1)]
                avg_diff = sum(diffs) / len(diffs) if diffs else 0
                if avg_diff < 5:
                    template_count += 1

    analyzed = min(len(paragraphs), 10)
    ratio = template_count / analyzed if analyzed > 0 else 0
    if ratio <= 0.2:
        score = 0
    elif ratio <= 0.4:
        score = 5
    else:
        score = 10

    return {'score': score, 'template_paragraphs': template_count, 'analyzed': analyzed}


def score_passive_voice(text: str) -> dict:
    """Score passive voice density (weight: 10/100)."""
    sentences = _split_sentences(text)
    if not sentences:
        return {'score': 0, 'passive_count': 0, 'percentage': 0}

    passive_patterns = [
        r'\b(?:was|were|is|are|been|being)\s+\w+ed\b',
        r'\b(?:was|were|is|are|been|being)\s+\w+en\b',
        r'\b(?:was|were|is|are|been|being)\s+(?:found|shown|seen|given|made|done|taken)\b',
    ]
    passive_count = 0
    for sentence in sentences:
        for pattern in passive_patterns:
            if re.search(pattern, sentence, re.IGNORECASE):
                passive_count += 1
                break

    percentage = (passive_count / len(sentences)) * 100
    if percentage <= 50:
        score = 0
    elif percentage <= 60:
        score = 5
    else:
        score = 10

    return {'score': score, 'passive_count': passive_count, 'percentage': round(percentage, 1)}


def score_enumeration(text: str) -> dict:
    """Score explicit enumeration patterns (weight: 15/100)."""
    text_lower = text.lower()
    count = 0
    for pattern in ENUMERATION_PATTERNS:
        count += len(re.findall(pattern, text_lower, re.MULTILINE | re.DOTALL))

    # Also check for simple first/second/third at sentence starts
    sentences = _split_sentences(text)
    enum_starts = 0
    for s in sentences:
        if re.match(r'(?:first|second|third|fourth|finally|lastly),', s.strip(), re.IGNORECASE):
            enum_starts += 1
    if enum_starts >= 3:
        count += 1

    if count == 0:
        score = 0
    elif count == 1:
        score = 5
    elif count == 2:
        score = 10
    else:
        score = 15

    return {'score': score, 'enumeration_count': count}


def analyze(text: str) -> dict:
    """Run full AI detection analysis across all 8 categories."""
    results = {
        'hedging': score_hedging(text),
        'transitions': score_transitions(text),
        'sentence_uniformity': score_sentence_uniformity(text),
        'overqualification': score_overqualification(text),
        'missing_jargon': score_missing_jargon(text),
        'repetitive_structure': score_repetitive_structure(text),
        'passive_voice': score_passive_voice(text),
        'enumeration': score_enumeration(text),
    }

    overall = sum(r['score'] for r in results.values())

    if overall <= 20:
        interpretation = 'Likely human-authored'
    elif overall <= 30:
        interpretation = 'Likely human, minor AI elements possible'
    elif overall <= 45:
        interpretation = 'Uncertain, may be AI-assisted'
    elif overall <= 60:
        interpretation = 'Likely AI-generated'
    else:
        interpretation = 'Definitively AI-generated'

    return {
        'overall_score': overall,
        'interpretation': interpretation,
        'categories': results,
        'word_count': len(text.split()),
    }


def main():
    parser = argparse.ArgumentParser(description='Detect AI patterns in academic text')
    parser.add_argument('file', help='Text file to analyze')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f'Error: File not found: {args.file}', file=sys.stderr)
        sys.exit(1)

    with open(args.file, encoding='utf-8') as f:
        text = f.read()

    result = analyze(text)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f'AI Detection Score: {result["overall_score"]}/100')
        print(f'Interpretation: {result["interpretation"]}')
        print(f'Word count: {result["word_count"]}')
        print()
        for name, data in result['categories'].items():
            print(f'  {name}: {data["score"]} points')

    sys.exit(0)


if __name__ == '__main__':
    main()
