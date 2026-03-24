---
name: trauma-evidence-forge-v3
category: medical
description: >
  Gamma-optimized medical education presentation system for trauma surgery,
  emergency general surgery (EGS), and surgical critical care. Produces
  keyword-only slides with robust speaker notes targeting <15 min post-Gamma
  editing. Includes 10 medical student presentation stubs (6 Trauma + 4 EGS)
  mapped to Surgery Shelf Exam high-yield topics. Evidence synthesis with
  GRADE ratings, 5-script Gamma pipeline, chalk talk and MCQ templates.
  Marine theme locked for all presentations.
argument-hint: "<topic or workflow: grand-rounds, chalk-talk, evidence-review, full-pipeline>"
disable-model-invocation: false
---

# Trauma Evidence Forge v3

> Gamma-optimized evidence-to-presentation system for medical student education in Trauma/ACS/EGS.

## What's New in v3

| Feature | v1/v2 | v3 |
|---------|-------|-----|
| Words per slide | ~110 | ~45 (keyword-only) |
| Post-Gamma editing | 45-60 min | <15 min target |
| Speaker notes | ~30% of slides | 100% of content slides |
| MCQ checkpoints | 1 per talk | 2 per talk |
| Gamma theme | Varies | Marine (locked) |
| Audit checks | 8 (D1-D8) | 13 (D1-D13) |
| Validation checks | 17 | 19 |
| Presentation templates | 2 (medium, long) | 3 (compact, medium, long) |
| Medical student topics | 0 | 10 stubs (6 Trauma + 4 EGS) |

## Quick Start

| I need to... | Command | Template |
|-------------|---------|----------|
| Build a presentation | `/tef:grand-rounds {topic}` | medium (18-22 slides) |
| Quick didactic | `/tef:chalk-talk {topic}` | compact (12-16 slides) |
| Evidence review only | `/tef:evidence-review {topic}` | N/A (markdown output) |
| Full pipeline | `/tef:full-pipeline {topic}` | Evidence -> Slides -> Gamma |
| Run pipeline on existing | `/tef:generate-presentation {file}` | 5-script pipeline + submit |

## Design Philosophy

### Keyword Slides, Narrative Notes

**The presenter is the presentation.** Slides reinforce what you say, not replace you.

- **Slide body:** 3-7 word keyword phrases, max 50 words/slide
- **Speaker notes:** 150-250 words/slide — the full narrative
- **Key stat:** One bold number per content slide (NNT, HR, mortality %)
- **Bottom Line:** Every content slide ends with <=12-word takeaway

### Marine Theme

All presentations use Gamma **Marine** theme (`themeId: "marine"`):
- Dark navy/blue backgrounds, white text, high contrast
- Professional, bold, classic tone
- Consistent across all presentations

### Per-Slide-Type Directives

Each slide type gets specific Gamma layout instructions, reducing manual reformatting.

## 10 Presentation Topics

| # | Topic | Type | Duration | Shelf % |
|---|-------|------|----------|---------|
| 1 | xABCDE: The Trauma Primary Survey | Trauma | 35 min | 20-25% |
| 2 | Hemorrhagic Shock & Resuscitation | Trauma | 40 min | 20-25% |
| 3 | Blunt Abdominal Trauma: FAST and Beyond | Trauma | 35 min | 20-25% |
| 4 | Traumatic Brain Injury: GCS to the OR | Trauma | 40 min | 5-10% |
| 5 | Thoracic Trauma: Chest Tubes & Thoracotomies | Trauma | 35 min | 8-12% |
| 6 | Burns: Assessment & Resuscitation | Trauma | 35 min | 5-10% |
| 7 | Acute Abdomen: A Systematic Approach | EGS | 40 min | 30-35% |
| 8 | Acute Cholecystitis & Biliary Emergencies | EGS | 35 min | 30-35% |
| 9 | Small Bowel Obstruction: Watch vs Cut | EGS | 35 min | 30-35% |
| 10 | Post-Op Complications: What Students Must Know | Periop | 35 min | ~15% |

**Coverage:** ~40-50% of NBME Surgery Shelf Exam

## Workflow Phases

| Phase | Scripts |
|-------|---------|
| 1-3. Evidence Gathering/Grading/Synthesis | Manual |
| 4. Slide Authoring (keyword body + notes) | Manual |
| 5. Citation Formatting | `format_citations.py` |
| 6. Gamma Preprocessing | `preprocess_for_gamma.py` |
| 6.5. Design Audit (13 checks) | `audit_slide_design.py` |
| 7. Validation (19 checks) | `validate_gamma_ready.py` |
| 8. Gamma Submission (Marine + per-type) | `generate_gamma_params.py` |

## Evidence Standards

- Every clinical claim needs PMID or DOI
- `[N]` format → pipeline converts to `<sup>[N]</sup>`
- `**Sources:** [N][M]` at bottom of content slides
- GRADE ratings 1A through 4

## Gamma Integration

Uses `gamma-presentation-core` adapter pattern:
- Payload validation via core scripts
- Marine theme locked: `themeId: "marine"`
- MCP tools: `GAMMA_GENERATE_GAMMA`, `GAMMA_LIST_THEMES`, `GAMMA_GET_GAMMA_FILE_URLS`

## Templates

| Template | Slides | Duration | Use Case |
|----------|--------|----------|----------|
| `presentation-compact.md` | 12-16 | 15-20 min | Quick didactics |
| `presentation-medium.md` | 18-22 | 30-35 min | Standard lectures |
| `presentation-long.md` | 24-30 | 40-50 min | Grand rounds |
| `chalk-talk.md` | N/A | 45 min | Whiteboard teaching |
| `mcq-case-pairs.md` | N/A | Variable | Question bank |
| `evidence-synthesis.md` | N/A | N/A | Evidence template |

## File Structure

```
trauma-evidence-forge-v3/
  SKILL.md / CLAUDE.md / verification.md
  agents/          # Subagent definitions
  commands/        # Slash commands
  config/          # Gamma profile + journal profiles
  docs/            # Pipeline documentation
  evals/           # Test suite (pytest)
  projects/        # Complete/ and Pending/ (10 stubs)
  references/      # Evidence guides, design principles
  research/        # Shelf exam research archive (4 files)
  scripts/         # 7 Python scripts
  templates/       # 6 templates
```

## Defaults

**Author:** Evan DeCan, MD, Division of Acute Care Surgery, University of Virginia
**Theme:** Marine | **Image model:** imagen-4-pro
