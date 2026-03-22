# /asf:evidence-review

Domain-aware evidence synthesis with GRADE ratings.

## Usage

```
/asf:evidence-review {topic}
```

## Workflow

1. Identify clinical domain (trauma, EGS, SCC, global surgery) from topic
2. Load domain-specific search strategy from `references/domain-search-strategies.md`
3. Execute 6-category PubMed search (guidelines, RCTs, meta-analyses, recent, epidemiology, landmark)
4. GRADE-rate every piece of evidence
5. Build guideline comparison matrix and severity classification tables
6. Produce evidence synthesis document using `templates/evidence-synthesis.md`

## Output

- GRADE-rated evidence table with PMID for every entry
- Guideline comparison matrix (domain-appropriate societies)
- Statistical summary (95% CI, NNT, ARR, exact p-values)
- Evidence gap analysis
