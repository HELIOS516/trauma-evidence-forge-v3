# Academic Surgery Forge -- How It Works

> Architecture overview and design rationale for the academic-surgery-forge skill.

---

## Problem Statement

Academic surgical research involves several distinct but interconnected workflows:

1. **Research Design**: Capacity assessments, cost-effectiveness analyses, and survey design require domain-specific frameworks (Lancet Commission, NSOAP, ZAMSAT) that most researchers reference manually.

2. **Manuscript Writing**: IMRAD papers require journal-specific formatting, reporting checklist compliance (CONSORT/STROBE/PRISMA/SQUIRE/CARE), and rigorous citation management.

3. **Peer Review**: Structured critique across methodology, statistics, reporting, literature, and clinical significance domains -- with severity-rated feedback.

4. **AI Text Detection**: AI-assisted drafting produces detectable patterns (hedging clusters, transition density, sentence uniformity) that must be naturalized before submission.

These workflows share common infrastructure: citation verification, GRADE evidence grading, and statistical reporting standards. This skill unifies them into a single modular system.

---

## Architecture

### 4-Module Design

```
academic-surgery-forge/
├── modules/
│   ├── global-surgery-analysis/   ← Research design + frameworks
│   ├── manuscript-forge/          ← Paper drafting pipeline
│   ├── peer-review-engine/        ← Structured critique
│   └── text-naturalizer/          ← AI detection + humanization
├── scripts/                       ← Shared Python automation
├── references/                    ← Shared reference docs
├── projects/                      ← Per-project workspaces
├── commands/                      ← Slash commands (entry points)
├── agents/                        ← Specialized sub-agents
└── evals/                         ← Test suite (pytest)
```

**Why 4 modules?** Each module represents a distinct workflow that can operate independently. A researcher might only need the manuscript forge (drafting), or only the peer review engine (reviewing someone else's paper). Modules share infrastructure but don't require each other.

**Why not combine into fewer modules?** Separation keeps each module focused and prevents feature creep. The manuscript forge doesn't need to know about capacity assessment frameworks, and the text naturalizer doesn't need journal style profiles.

### Shared Infrastructure

Three components are shared across all modules:

1. **Citation Verification** (`references/citation-standards.md`, `scripts/research_utils.py`)
   - PMID/DOI extraction and validation
   - Fabricated PMID detection (patterns like sequential numbers, round numbers)
   - Citation coverage checking (body citations ↔ reference entries)

2. **GRADE Evidence Grading** (`references/evidence-quality-framework.md`, `scripts/research_utils.py`)
   - 1A-4 scale validation
   - Study type → evidence level mapping
   - Quality of evidence assessment

3. **Statistical Reporting** (`modules/manuscript-forge/references/statistical-reporting.md`)
   - Effect size measures (OR, RR, HR, ARR, NNT)
   - Confidence interval requirements
   - Multiple comparison corrections

---

## Module Deep Dives

### Global Surgery Analysis

**Purpose**: Provide structured frameworks for global surgery research design.

**Core Framework**: The Lancet Commission on Global Surgery (2015) defined 6 indicators that are the standard for measuring surgical capacity worldwide. This module provides:

- Detailed indicator definitions with measurement methodology
- Data collection instruments for each indicator
- Country context templates (WHO region, World Bank classification, surgeon density)
- NSOAP development guides
- Facility assessment tools (ZAMSAT, WHO-EESC)

**Design Decision**: Templates use fill-in-the-blank format with `{{VARIABLE}}` placeholders rather than generating content, because research protocols require human judgment about study design choices.

### Manuscript Forge

**Purpose**: Guide researchers through the complete manuscript drafting pipeline.

**5-Stage Pipeline**: OUTLINE → DRAFT → VALIDATE → POLISH → SUBMIT-PREP

Each stage has explicit quality gates:

- Stage 3 (VALIDATE) runs the 16-check automated validator
- Stage 4 (POLISH) includes AI detection scoring
- Stage 5 (SUBMIT-PREP) generates journal-specific submission materials

**Study Type Auto-Detection**: The `detect_study_type()` function in `research_utils.py` uses regex heuristics to identify study design from manuscript text, then auto-applies the appropriate reporting checklist.

**Journal Profiles**: Pre-configured formatting for 7 major surgical journals. Each profile specifies word limits, reference format (Vancouver vs AMA), structured abstract requirements, and author guideline URLs.

### Peer Review Engine

**Purpose**: Provide structured, reproducible manuscript critique.

**5 Review Domains**:

1. **Methodology**: Study design appropriateness, bias assessment, sample size adequacy
2. **Statistics**: Correct test selection, effect sizes, multiple comparisons handling
3. **Reporting**: Checklist compliance (auto-detected), missing required items
4. **Literature**: Citation completeness, missing key references, recency of evidence
5. **Clinical Significance**: Beyond statistical significance -- does this matter clinically?

**Severity System**: Major (must fix) / Minor (should fix) / Optional (suggestions). This maps to standard journal review terminology.

**Revision Response**: Point-by-point response letter generation with change tracking and evidence-based rebuttals.

### Text Naturalizer

**Purpose**: Detect and remediate AI-generated patterns in academic text.

**8-Category Scoring System**: Each category scores 0-15 points (total 0-100). Categories were designed based on common AI writing patterns that differ from natural surgical academic prose:

| Pattern              | Why AI Does This                       | What Humans Do Instead              |
| -------------------- | -------------------------------------- | ----------------------------------- |
| Hedging clusters     | AI adds meta-commentary                | Surgeons state findings directly    |
| Transition density   | AI uses formulaic connectors           | Surgeons use content-specific links |
| Sentence uniformity  | AI generates 15-25 word sentences      | Surgeons mix 5-word and 30-word     |
| Over-qualification   | AI self-congratulates                  | Surgeons let data speak             |
| Missing jargon       | AI avoids abbreviations                | Surgeons use ISS, GCS, MTP freely   |
| Repetitive structure | AI loops claim→evidence→interpretation | Surgeons vary paragraph structure   |
| Passive voice        | AI overuses passive                    | Surgeons use active in Discussion   |
| Enumeration          | AI lists "First,...Second,..."         | Surgeons embed items in prose       |

**Target Score**: < 30 after naturalization. This threshold was chosen because scores 0-30 are indistinguishable from human-authored surgical academic text in blind testing.

---

## Python Scripts

### research_utils.py

Shared utility library imported by all other scripts. Provides:

- `extract_pmids(text)` / `extract_dois(text)` -- citation extraction
- `extract_citations(text)` -- body citation [N] extraction
- `check_citation_coverage(text)` -- body ↔ reference matching
- `count_words(text)` -- markdown-aware word counting
- `detect_study_type(text)` -- heuristic study type detection
- `get_checklist_for_study_type(type)` -- checklist mapping
- `is_valid_grade(grade)` -- GRADE validation
- `detect_imrad_sections(text)` -- section presence detection
- `find_statistical_claims(text)` -- statistical claim extraction
- `extract_grades(text)` -- GRADE rating extraction (CEBM + GRADE terms)
- `validate_grade_plausibility(grade, study_type)` -- cross-check grade vs study type
- `map_cebm_to_grade(code)` -- CEBM to GRADE mapping
- `map_grade_to_cebm(term)` -- GRADE to CEBM mapping

### validate_manuscript.py

16-check quality gate (10 hard, 6 soft). Hard gates cause FAIL; soft gates produce warnings.

**Usage**: `python3 scripts/validate_manuscript.py manuscript.md --json`

**Output**: JSON with per-check results, overall PASS/FAIL, hard_fail count, soft_fail count.

### detect_ai_patterns.py

8-category AI text detection with weighted scoring.

**Usage**: `python3 scripts/detect_ai_patterns.py text.md --json`

**Output**: JSON with per-category scores, overall score (0-100), interpretation.

### format_references.py

Reference extraction and format validation.

**Usage**: `python3 scripts/format_references.py manuscript.md --style vancouver`

**Output**: Format issues, duplicate detection, sequential numbering check.

---

## Design Decisions

### Why Not Use External APIs for PMID Verification?

The scripts use regex-based pattern validation rather than PubMed API calls because:

1. Offline operation is important (hospital networks may restrict external API access)
2. Pattern detection catches common fabrication (sequential PMIDs, round numbers)
3. Full verification can be added later as an optional flag

### Why Separate Module Directories Instead of a Single Config?

Each module has its own `templates/`, `checklists/`, and `references/` directories because:

1. Modules operate independently -- you don't need manuscript-forge loaded to do peer review
2. File discovery is intuitive (look in the module you're using)
3. New modules can be added without modifying existing ones

### Why Vancouver as Default Reference Format?

6 of 7 target journals use Vancouver style. Only JAMA Surgery uses AMA. Vancouver is the safer default.

### Why GRADE Instead of Oxford/CEBM?

GRADE is the international standard used by WHO, Cochrane, and most surgical societies. The Lancet Commission framework references GRADE explicitly.

---

## Version History

This skill was previously named `global-surgery-researcher` and has been renamed to `academic-surgery-forge` to better reflect its scope across all academic surgical research workflows (not limited to global surgery topics).

- **v1.0** (February 2026): Initial release as `global-surgery-researcher` — 4 modules, 4 scripts, 3 test files
- **v2.0** (March 2026): Renamed to `academic-surgery-forge`; added check 16 (GRADE plausibility), 3 new scripts (`check_staleness.py`, `validate_dosing.py`, `verify_citations.py`), 4 new `research_utils.py` functions for CEBM/GRADE mapping

---

## Testing

```bash
# Run all tests
cd skills/academic-surgery-forge
python3 -m pytest evals/ -v

# Test specific module
python3 -m pytest evals/test_research_utils.py -v
python3 -m pytest evals/test_detect_ai_patterns.py -v
python3 -m pytest evals/test_validate_manuscript.py -v
```
