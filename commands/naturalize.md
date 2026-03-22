# /asf:naturalize

AI detection and humanization of academic text.

## Usage

```
/asf:naturalize {text or file}
```

## Workflow

1. DETECT: Score text 0-100 per section (scripts/detect_ai_patterns.py)
2. DIAGNOSE: Identify triggering patterns
3. REWRITE: Section-by-section naturalization
4. VERIFY: Re-score, gate: <30 while preserving 100% factual claims
