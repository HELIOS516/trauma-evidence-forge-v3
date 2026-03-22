# Academic Surgery Forge -- Workflow Guide

> Complete guide to using the academic-surgery-forge skill for manuscript drafting, peer review, capacity assessments, and text naturalization.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Module 1: Global Surgery Analysis](#module-1-global-surgery-analysis)
3. [Module 2: Manuscript Forge](#module-2-manuscript-forge)
4. [Module 3: Peer Review Engine](#module-3-peer-review-engine)
5. [Module 4: Text Naturalizer](#module-4-text-naturalizer)
6. [Shared Infrastructure](#shared-infrastructure)
7. [Slash Commands](#slash-commands)
8. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Prerequisites

- Python 3.10+ (for validation scripts)
- pytest (for running test suite)

### Quick Start

1. Choose your entry point based on task:
   - **Capacity assessment** → `/asf:assess-capacity`
   - **Draft a paper** → `/asf:draft-paper`
   - **Review a manuscript** → `/asf:review-paper`
   - **Naturalize AI text** → `/asf:naturalize`
   - **New project workspace** → `/asf:new-project`

2. Each command creates a project directory under `projects/<name>/` with the appropriate structure.

### Project Directory Structure

```
projects/<project-name>/
  PROJECT.md          # Project metadata (topic, journal, status)
  data/               # Raw data, survey results, cost tables
  literature/         # Reference PDFs, citation database
  drafts/             # Manuscript drafts (draft-v1.md, draft-v2.md)
  reviews/            # Peer review reports, revision letters
  output/             # Final submission-ready files
  logs/               # Session logs, validation reports
```

## Platform-Specific Setup

### claude.ai / Desktop Users

1. **Enable PubMed**: Settings > Connectors > PubMed > Connect (free)
2. **Upload skill**: Settings > Capabilities > Skills > Upload `academic-surgery-forge.zip`
3. **Start chatting**: Type any of the example prompts below
4. See `docs/desktop-quick-start.md` for detailed guide

### Claude Code CLI Users

1. **Install skill**: `/plugin install academic-surgery-forge` or unzip to `~/.claude/skills/`
2. **Install PubMed MCP** (optional): See `docs/pubmed-setup.md`
3. **Use slash commands**: `/asf:draft-paper`, etc.

### Claude Code + OMC Users

All CLI features plus:

- Parallel agent workflows from `workflows/`
- Team compositions from `workflows/team-compositions.md`
- Specialized subagents in `agents/`

---

## Module 1: Global Surgery Analysis

### When to Use

- Designing a **capacity assessment** for a country or region
- Building a study around the **Lancet Commission 6 indicators**
- Developing or evaluating a **National Surgical, Obstetric, and Anesthesia Plan (NSOAP)**
- Performing **cost-effectiveness analysis** for surgical interventions
- Conducting **facility-level assessments** (ZAMSAT, WHO-EESC, SAT)

### Workflow: Capacity Assessment

```
Step 1: Select country/region
  └── Load context (WHO region, World Bank income, surgeon density)

Step 2: Choose framework
  ├── Lancet Commission 6 Indicators (comprehensive)
  ├── NSOAP Evaluation (national planning)
  ├── Facility Assessment (ZAMSAT/WHO-EESC)
  └── Custom cross-sectional survey

Step 3: Generate protocol
  ├── Study design + sampling strategy
  ├── Data collection instruments
  ├── Analysis plan (with indicator definitions)
  └── Ethical considerations

Step 4: Populate with data
  └── Fill in country-specific data from literature/surveys

Step 5: Generate output
  ├── Structured research protocol
  ├── Data collection forms
  └── Analysis framework
```

### Lancet Commission 6 Indicators

Every capacity assessment must address these or explicitly justify their exclusion:

| #   | Indicator                                    | Target by 2030                 | Measurement            |
| --- | -------------------------------------------- | ------------------------------ | ---------------------- |
| 1   | Access to timely essential surgery           | ≥80% population within 2 hours | GIS modeling           |
| 2   | Specialist surgical workforce density        | ≥20 per 100,000                | Registry/survey        |
| 3   | Surgical volume                              | ≥5,000 per 100,000/year        | Theatre logbooks       |
| 4   | Perioperative mortality rate                 | Track and report               | Theatre + ward linkage |
| 5   | Protection against impoverishing expenditure | 100%                           | Household survey       |
| 6   | Protection against catastrophic expenditure  | 100%                           | Household survey       |

### Quality Gates

- [ ] All 6 indicators addressed or excluded with justification
- [ ] Country context complete (WHO region, World Bank income, surgeon density)
- [ ] Cost data specifies currency, year, and PPP adjustment method
- [ ] Bellwether procedure capability assessed (C-section, laparotomy, open fracture)
- [ ] Sampling methodology documented

### Key References

- **frameworks/lancet-commission.md** -- Detailed indicator definitions, measurement methodology, data collection instruments
- **frameworks/nsoap-template.md** -- NSOAP development guide with domain templates
- **frameworks/facility-assessment.md** -- ZAMSAT/WHO-EESC tool adaptations
- **templates/capacity-assessment.md** -- Protocol template
- **templates/cost-effectiveness.md** -- CEA framework
- **templates/cross-sectional-survey.md** -- Survey design template

---

## Module 2: Manuscript Forge

### When to Use

- Drafting an **original research manuscript** (IMRAD format)
- Writing a **systematic review** or meta-analysis
- Preparing a **case report** or brief communication
- Formatting for a **specific journal** (WJS, JSR, JTACS, Annals, Surgery, JAMA Surgery, BJS)
- Ensuring **reporting checklist compliance** (CONSORT, STROBE, PRISMA, SQUIRE, CARE)

### IMRAD Pipeline (5 Stages)

```
Stage 1: OUTLINE
  ├── Hypothesis formulation
  ├── Section structure
  ├── Key references identification
  └── Target journal selection

Stage 2: DRAFT
  ├── Section-by-section writing
  ├── Evidence integration with [N] citations
  ├── Table/figure planning
  └── Statistical results formatting

Stage 3: VALIDATE
  ├── Run validate_manuscript.py (16 checks)
  ├── Reporting checklist compliance (≥90%)
  ├── Citation verification (all PMIDs/DOIs)
  └── Word count check against journal limits

Stage 4: POLISH
  ├── Language and flow refinement
  ├── Journal-specific style adaptation
  ├── AI detection check (score must be <30)
  └── Final formatting pass

Stage 5: SUBMIT-PREP
  ├── Cover letter generation
  ├── Highlights/key points
  ├── Structured abstract formatting
  ├── Author contributions (CRediT)
  └── Conflict of interest declarations
```

### Manuscript Templates

| Template                     | Study Type                       | Location     |
| ---------------------------- | -------------------------------- | ------------ |
| `imrad-original-research.md` | RCT, cohort, case-control        | `templates/` |
| `imrad-systematic-review.md` | Systematic review, meta-analysis | `templates/` |
| `case-report.md`             | Case report                      | `templates/` |
| `brief-communication.md`     | Short format                     | `templates/` |

### Journal Profiles

Pre-configured formatting for 7 target journals. See `references/journal-styles.md` for complete details:

| Journal                      | Abbreviation | Reference Style | Word Limit |
| ---------------------------- | ------------ | --------------- | ---------- |
| World Journal of Surgery     | WJS          | Vancouver       | 4000       |
| Journal of Surgical Research | JSR          | Vancouver       | 5000       |
| J Trauma Acute Care Surg     | JTACS        | Vancouver       | 3500       |
| Annals of Surgery            | Ann Surg     | Vancouver       | 4000       |
| Surgery                      | Surgery      | Vancouver       | 4000       |
| JAMA Surgery                 | JAMA Surg    | AMA             | 3000       |
| British Journal of Surgery   | BJS          | Vancouver       | 4000       |

### Reporting Checklists

Auto-detected based on study type via `detect_study_type()` in `research_utils.py`:

| Study Type          | Checklist | Items | Location                |
| ------------------- | --------- | ----- | ----------------------- |
| RCT                 | CONSORT   | 25    | `checklists/consort.md` |
| Observational       | STROBE    | 22    | `checklists/strobe.md`  |
| Systematic Review   | PRISMA    | 27    | `checklists/prisma.md`  |
| Quality Improvement | SQUIRE    | 18    | `checklists/squire.md`  |
| Case Report         | CARE      | 13    | `checklists/care.md`    |

### Validation Pipeline

Run the manuscript validator after Stage 3:

```bash
python3 scripts/validate_manuscript.py projects/<name>/drafts/draft.md --json
```

**16 Checks (10 hard, 6 soft):**

Hard gates (any failure = FAIL):

1. IMRAD sections present (Abstract, Introduction, Methods, Results, Discussion, References)
2. At least 1 citation in body text
3. All body citations have corresponding references
4. At least 1 PMID or DOI in references
5. No fabricated PMID patterns detected
6. Abstract present
7. Results section contains statistical data
8. Methods section present and non-empty
9. Discussion section present and non-empty
10. References section has ≥5 entries

Soft gates (warnings only): 11. Word count within journal limits 12. Reporting checklist compliance ≥90% 13. Statistical claims have 95% CI 14. All references have PMID or DOI 15. GRADE ratings are valid 16. GRADE plausibility (cross-check grade vs study type)

### Quality Gates

- [ ] Reporting checklist compliance ≥ 90%
- [ ] All citations verified (PMID/DOI present)
- [ ] Word count within journal limits
- [ ] Reference format matches target journal (Vancouver/AMA)
- [ ] IMRAD sections all present
- [ ] Statistical claims have 95% CI and effect sizes

---

## Module 3: Peer Review Engine

### When to Use

- **Reviewing a manuscript** for journal submission
- Preparing a **revision response** letter to reviewer comments
- **Self-reviewing** your own manuscript before submission
- Conducting structured **methodology critique**

### Review Workflow

```
Step 1: Load manuscript
  └── Auto-detect study type and apply appropriate checklist

Step 2: Domain-by-domain review
  ├── Methodology (study design, bias, sample size)
  ├── Statistics (correct tests, effect sizes, multiple comparisons)
  ├── Reporting (checklist compliance, missing items)
  ├── Literature (citation completeness, missing key refs)
  └── Clinical Significance (beyond statistical significance)

Step 3: Generate review report
  ├── Summary assessment
  ├── Major issues (must address)
  ├── Minor issues (should address)
  ├── Optional suggestions
  └── Recommendation (accept/minor revision/major revision/reject)

Step 4: Revision response (if revising)
  ├── Point-by-point response letter
  ├── Change tracking with page/line references
  └── Evidence-based rebuttals for disagreements
```

### Severity Ratings

| Rating       | Meaning                             | Action Required                |
| ------------ | ----------------------------------- | ------------------------------ |
| **Major**    | Fundamental flaw affecting validity | Must address before acceptance |
| **Minor**    | Important but not invalidating      | Should address in revision     |
| **Optional** | Suggestions for improvement         | Author discretion              |

### Review Report Format

```markdown
## Peer Review Report

### Summary

[2-3 sentence overall assessment]

### Recommendation: [Accept / Minor Revision / Major Revision / Reject]

### Major Issues

1. **[Domain]: [Issue title]** (Severity: Major)
   - Finding: [What the problem is]
   - Impact: [Why this matters]
   - Recommendation: [How to fix it]

### Minor Issues

1. **[Domain]: [Issue title]** (Severity: Minor)
   ...

### Optional Suggestions

1. ...
```

### Revision Response Format

```markdown
## Response to Reviewers

Dear Editor and Reviewers,

Thank you for the thorough review...

### Reviewer 1

**Comment 1.1**: [Reviewer's comment]
**Response**: [Your response]
**Changes**: [Page/line references to changes made]

**Comment 1.2**: ...
```

---

## Module 4: Text Naturalizer

### When to Use

- **Detecting AI patterns** in a manuscript draft
- **Naturalizing** AI-assisted text to sound human-authored
- **Pre-submission quality check** for AI detection
- Achieving target AI detection score **< 30**

### Detection + Naturalization Pipeline

```
Stage 1: DETECT
  └── Score text across 8 categories (0-100 scale)

Stage 2: DIAGNOSE
  └── Identify specific triggering phrases and patterns

Stage 3: REWRITE
  ├── Section-by-section naturalization
  ├── Prioritize: Discussion > Introduction > Results > Methods
  └── Preserve 100% factual claims

Stage 4: VERIFY
  └── Re-score to confirm improvement (target: <30)
```

### 8 Detection Categories

| Category              | Weight | What It Detects                               |
| --------------------- | ------ | --------------------------------------------- |
| Hedging Clusters      | 15     | "It is important to note that..."             |
| Transition Density    | 15     | Excessive "Furthermore," "Moreover,"          |
| Sentence Uniformity   | 15     | Low variation in sentence length (CV < 0.35)  |
| Over-qualification    | 10     | "This comprehensive analysis demonstrates..." |
| Missing Jargon        | 10     | Absence of field-specific abbreviations       |
| Repetitive Structure  | 10     | Rigid claim-evidence-interpretation loops     |
| Passive Voice Density | 10     | Excessive passive voice (>60%)                |
| Enumeration Patterns  | 15     | "First,...Second,...Third,...Finally,..."     |

### Running AI Detection

```bash
python3 scripts/detect_ai_patterns.py path/to/text.md --json
```

### Score Interpretation

| Score  | Interpretation                  | Action                         |
| ------ | ------------------------------- | ------------------------------ |
| 0-20   | Definitively human-authored     | None needed                    |
| 21-30  | Likely human, minor AI elements | Spot-check only                |
| 31-45  | Uncertain, may be AI-assisted   | Review high-scoring categories |
| 46-60  | Likely AI-generated             | Comprehensive naturalization   |
| 61-100 | Definitively AI-generated       | Complete rewrite               |

### Quality Gate

Naturalized text must score **< 30** on AI detection while preserving **100%** of factual claims.

---

## Shared Infrastructure

### Citation Verification Protocol

Every clinical claim must have a PMID or DOI. See `references/citation-standards.md`.

**3-Pass Protocol:**

1. **Extract**: Pull all [N] citations and PMID/DOI identifiers
2. **Verify**: Check PMIDs exist (pattern validation, not API call)
3. **Report**: Flag missing, fabricated, or orphaned references

### GRADE Evidence Ratings

| Grade | Recommendation | Evidence Quality                 |
| ----- | -------------- | -------------------------------- |
| 1A    | Strong         | High (well-designed RCTs)        |
| 1B    | Strong         | Moderate (RCTs with limitations) |
| 1C    | Strong         | Low (observational studies)      |
| 2A    | Weak           | High (uncertain balance)         |
| 2B    | Weak           | Moderate (important limitations) |
| 2C    | Weak           | Low (observational)              |
| 3     | Expert opinion | Consensus/case series            |
| 4     | Insufficient   | Anecdotal/case reports           |

### Statistical Reporting Standards

- Report **95% confidence intervals** for all effect estimates
- Include **NNT** (number needed to treat) when available
- Report **absolute risk reduction** alongside relative risk
- Include **exact p-values** (not just "p < 0.05")
- Format: `VTE rate: 5.3% vs 8.1% (OR 0.63, 95% CI 0.45-0.88, p=0.007; ARR 2.8%, NNT 36)`

### Python Scripts

| Script                   | Purpose                                                   | Usage                                                              |
| ------------------------ | --------------------------------------------------------- | ------------------------------------------------------------------ |
| `research_utils.py`      | Shared utilities (citation extraction, GRADE, study type) | Imported by other scripts                                          |
| `validate_manuscript.py` | 16-check quality gate                                     | `python3 scripts/validate_manuscript.py <file> [--json]`           |
| `detect_ai_patterns.py`  | 8-category AI text scoring                                | `python3 scripts/detect_ai_patterns.py <file> [--json]`            |
| `format_references.py`   | Vancouver/AMA reference formatting                        | `python3 scripts/format_references.py <file> [--style vancouver]`  |
| `check_staleness.py`     | Reference staleness detection                             | `python3 scripts/check_staleness.py <dir> [--json]`                |
| `validate_dosing.py`     | Drug dosing validation                                    | `python3 scripts/validate_dosing.py <file> [--json]`               |
| `verify_citations.py`    | Citation verification + cross-check                       | `python3 scripts/verify_citations.py <file> [--cross-check file2]` |

---

## Slash Commands

| Command                | Purpose                            |
| ---------------------- | ---------------------------------- |
| `/asf:new-project`     | Initialize a new project workspace |
| `/asf:draft-paper`     | Start manuscript drafting pipeline |
| `/asf:review-paper`    | Run peer review engine             |
| `/asf:naturalize`      | Detect and fix AI patterns         |
| `/asf:assess-capacity` | Run capacity assessment framework  |

---

## Troubleshooting

### Common Issues

**"Missing IMRAD sections"**

- Ensure section headers use `## Abstract`, `## Introduction`, etc.
- Headers must be level 2 (`##`) or level 3 (`###`)

**"No PMIDs found"**

- Format: `PMID: 12345678` (with or without space after colon)
- PMIDs must be 7-8 digits

**"AI detection score too high"**

- Focus on Discussion section first (highest variance)
- Replace hedging phrases with direct statements
- Add field-specific abbreviations (ISS, GCS, MTP, etc.)
- Vary sentence length (mix 5-word and 30-word sentences)

**"Reporting checklist below 90%"**

- Load the appropriate checklist from `modules/manuscript-forge/checklists/`
- Address each item or mark as N/A with justification
- Re-run validation after changes

### Running Tests

```bash
cd skills/academic-surgery-forge
python3 -m pytest evals/ -v
```

### Platform-Specific Notes

**claude.ai/Desktop:**

- Scripts can't run directly unless Code Interpreter is enabled. Use `docs/script-equivalents.md` instead.
- PubMed connector provides real citation verification — enable it for best results.
- Claude Research feature (paid plans) enables comprehensive literature discovery.

**Claude Code CLI:**

- All Python scripts require Python 3.10+
- PubMed MCP gives the same verification as the claude.ai connector
- Scripts are stdlib-only — no pip install needed
