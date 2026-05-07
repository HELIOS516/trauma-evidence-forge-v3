# Claude Code Configuration — Trauma Evidence Forge v3

> Claude Code-specific instructions. Loaded automatically on session start.

## v3 Optimization Philosophy

- **Keyword slides** (max 50 words/slide body), full narrative in speaker notes
- **Marine theme** locked (`themeId: "marine"`) for all presentations
- **Per-slide-type Gamma directives** — each slide type gets explicit layout instructions
- **Target: <15 min post-Gamma editing** (down from 45-60 min in v1/v2)
- **2 MCQ checkpoints** per 30-min presentation

## Model Selection

| Task | Model | Rationale |
|------|-------|-----------|
| PubMed search, citation verification | sonnet | Fast, repetitive |
| Evidence synthesis, slide authoring | sonnet | Good balance |
| GRADE rating decisions | opus | Nuanced clinical judgment |
| Slide design audit (scripts) | sonnet | Deterministic |
| Guideline comparison tables | sonnet | Structured extraction |
| Statistical reporting validation | opus | Study design implications |
| Citation format conversion | haiku | Mechanical transformation |

## Subagent Definitions

| Agent | Model | Purpose |
|-------|-------|---------|
| evidence-researcher | sonnet | PubMed search, GRADE rating, landmark trials |
| slide-designer | sonnet | 5-script Gamma pipeline, design audit |
| methodology-critic | opus | Study design assessment, bias evaluation |
| citation-validator | haiku | PMID/DOI verification |

## Team: Grand Rounds Pipeline

```
Lead: Orchestrator (sonnet)
  Teammates:
    - evidence-researcher (sonnet): PubMed search, GRADE, comparison tables
    - slide-designer (sonnet): Template selection, keyword authoring, 5-script pipeline
    - citation-validator (haiku): PMID verification in parallel
  Workflow:
    1. Lead decomposes topic into search strategy
    2. evidence-researcher produces evidence-synthesis.md
    3. citation-validator runs verify_citations.py in parallel
    4. slide-designer authors keyword slides + speaker notes, runs pipeline
    5. Lead reviews, generates Gamma params with Marine theme
    6. Submit to Gamma, verify output quality
```

## Team: Evidence Review

```
Lead: Orchestrator (sonnet)
  Teammates:
    - evidence-researcher (sonnet): Multi-society guideline search
    - methodology-critic (opus): Evidence quality + GRADE validation
  Workflow:
    1. evidence-researcher searches each society in parallel
    2. methodology-critic evaluates evidence, assigns GRADE
    3. Lead builds comparison matrix and synthesis document
```

## Project Conventions

- Evidence synthesis: `projects/{status}/{topic}/evidence-synthesis.md`
- Presentations: `projects/{status}/{topic}/presentation-*.md`
- Status: `Pending/` (in progress) or `Complete/` (finished)
- Commit messages: `[TEFv3] {phase}: {description}`
- Gamma theme: Always Marine — never override

## Gamma Optimization Notes

When authoring slides, enforce these rules:
1. **Title = assertion** with a verb (not a topic label)
2. **Body = keyword bullets** (3-7 words each, max 3-4 bullets)
3. **Bold one KEY STAT** per content slide
4. **Bottom Line blockquote** on every content/data/trial/guideline slide
5. **Speaker Notes** (150-250 words) below every content slide in HTML comments
6. **Sources block** (`**Sources:** [N][M]`) at bottom of content slides
7. **No full sentences** in slide body — sentences go in speaker notes only

## Quick Reference

```bash
# Run full pipeline on a presentation
python scripts/format_citations.py projects/Pending/{topic}/presentation.md
python scripts/preprocess_for_gamma.py <output>
python scripts/audit_slide_design.py <output>
python scripts/validate_gamma_ready.py <output>
python scripts/generate_gamma_params.py <output>

# Run tests
python -m pytest evals/ -v

# Verify citations
python scripts/verify_citations.py projects/Pending/{topic}/evidence-synthesis.md
```

## Second Brain Integration

Evidence wiki pages for rapid topic lookup during presentation authoring:

| Wiki Page | Presentation Domain | Key Evidence |
|-----------|---------------------|--------------|
| [BCVI Management](../second-brain/wiki/bcvi-management.md) | Vascular trauma | BIFFL grading, antithrombotic selection, SEH coexistence |
| [DVT Prophylaxis](../second-brain/wiki/dvt-prophylaxis-trauma.md) | ICU/VTE | 2025 meta-analysis N=87K; early initiation reduces VTE 62% |
| [Antibiotic Prophylaxis](../second-brain/wiki/antibiotic-prophylaxis-trauma.md) | Perioperative | Universal ≤24h rule; agent selection by site/flora |
| [Hemorrhage + Resuscitation](../second-brain/wiki/hemorrhage-resuscitation.md) | Trauma resus | xABCDE, DCR, DCS, TXA timing window, 1:1:1 ratio |
| [Stress Ulcer Prophylaxis](../second-brain/wiki/stress-ulcer-prophylaxis.md) | ICU | REVISE trial: PPI reduces GI bleeding 70%, NNT=40 |
| [Spinal Cord Injury](../second-brain/wiki/spinal-cord-injury.md) | Neuro-critical | MAP >85 x7 days, early decompression <24h |
| [PSH Management](../second-brain/wiki/psh-management.md) | Neuro-critical | Meyfroidt 2017 (Lancet Neurol), EIR model, propranolol + clonidine |
| [Rib Fracture Fixation](../second-brain/wiki/rib-fracture-fixation.md) | Thoracic trauma | VATS vs open ORIF equivalent outcomes, 2025 landmark study |
| [Pancreaticoduodenal Trauma](../second-brain/wiki/pancreaticoduodenal-trauma.md) | Abdominal trauma | AAST grading, DCS approach, Kocher/Cattell-Braasch anatomy |

Pressure-test a slide claim against vault evidence:
```bash
/vault-challenge "claim to test"
```

Full wiki index: `../second-brain/wiki/index.md`

## DO NOT

- Do not commit `.env` files or hardcoded secrets — use 1Password (`helios516-automation` vault) + `op://` references
- Do not bypass tests or pre-commit hooks (`--no-verify`)
- Do not push directly to `main` for breaking changes without review
- Do not commit PHI or identifiable patient case details

## Related repos

Part of the HELIOS516 second-brain ecosystem (`~/Documents/GITHUB_HELIOS516/own/second-brain/`). Generated EDOPs / Gamma slides live here; `automation/private_vault_pipeline/` (non-clinical content) is a sibling pipeline. Same egress filter (`automation/lib/egress_filter.py`) governs both.

---

_Canonical template v1 (2026-05-02). See `~/Documents/GitHub/.CLAUDE_TEMPLATE.md`._
