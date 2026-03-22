# Academic Surgery Forge: Workflow Guide

## What This Is

Academic Surgery Forge transforms clinical topics into professional, citation-verified slide presentations via Gamma.app. You give it a topic ("DVT Prophylaxis in Trauma"), and it produces a complete markdown deck that passes through a 5-script pipeline, emerges Gamma-ready, and uploads to create professionally designed slides with images.

Gamma parameter contracts are inherited from `../gamma-presentation-core`:

- `../gamma-presentation-core/references/gamma-canonical-spec.md`
- `../gamma-presentation-core/references/gamma-mcp-tool-contracts.md`
- `../gamma-presentation-core/references/gamma-local-vs-official-delta.md`

## Quick Start

```bash
# Create a new topic and run the full pipeline
/full-pipeline "DVT Prophylaxis in Trauma Patients"

# This will:
# 1. Create project directory structure
# 2. Guide evidence gathering (search, PMID collection, GRADE rating)
# 3. Synthesize evidence into narrative summaries
# 4. Author presentation-long.md with proper formatting
# 5. Run 5-script pipeline (format → preprocess → audit → validate → generate)
# 6. Produce Gamma-ready files: *-gamma.md, *-gamma-api.json, *-gamma-web.md
# 7. Upload to Gamma.app via API or web guide
```

**Result:** Polished 16:9 presentation with assertion-evidence slides, full citations, speaker notes, and AI-generated medical images.

## How It Works

```
1. Evidence Gathering
   ├─ Systematic PubMed search (RCTs, SRs, guidelines)
   ├─ PMID/DOI verification (fabricated PMIDs are common)
   └─ GRADE rating (1A-4 scale)

2. Evidence Synthesis
   ├─ evidence-synthesis.md (narrative + statistical summaries)
   ├─ Guideline comparison tables
   └─ Study characteristic tables

3. Slide Authoring
   ├─ presentation-long.md (80-100 slides, full case-based)
   ├─ Specific formatting rules (see Authoring Conventions)
   └─ Citations: [N] in body, **Sources:** [N][M] blocks

4. Pipeline Processing (5 scripts, run in order)
   ├─ 1. format_citations.py → presentation-long-gamma.md
   ├─ 2. preprocess_for_gamma.py → *-gamma.md + *-instructions.json + *-notes.md
   ├─ 3. audit_slide_design.py → audit_output.txt
   ├─ 4. validate_gamma_ready.py → validation_report.txt
   └─ 5. generate_gamma_params.py → *-gamma-api.json + *-gamma-web.md

5. Gamma Submission
   ├─ API: POST with *-gamma-api.json params + *-gamma.md content
   ├─ Web: Paste *-gamma.md + follow *-gamma-web.md instructions
   └─ Settings: preserve mode, numCards exact, imagen-4-pro
```

## The Pipeline

### Script 1: `format_citations.py`

**Purpose:** Convert author-friendly `[N]` citations to Gamma-ready superscripts and expand Sources blocks.

**3 Passes:**

- **Pass 1:** Strip `[N]` from headings (Gamma card titles should be clean)
- **Pass 2:** Expand `**Sources:** [1][2]` to full citation lines by looking up in References section
- **Pass 3:** Convert body `[N]` to `<sup>[N]</sup>` for superscript rendering

**Input:** `presentation-long.md`
**Output:** `presentation-long-gamma.md`

**Example:**

```markdown
# BEFORE (authored)

## Early Prophylaxis Reduces VTE by 40%[1]

Trauma patients benefit from early chemical prophylaxis[1][2].
**Sources:** [1][2]

# AFTER (formatted)

## Early Prophylaxis Reduces VTE by 40%

Trauma patients benefit from early chemical prophylaxis<sup>[1]</sup><sup>[2]</sup>.
**Sources:**

- Geerts et al. Prevention of venous thromboembolism. Chest. 2008;133:381S-453S. PMID: 18574271 [1]
- Rogers et al. EAST DVT prophylaxis guideline. J Trauma. 2002;53:142-164. PMID: 12131409 [2]
```

### Script 2: `preprocess_for_gamma.py`

**Purpose:** Strip all meta-content Gamma shouldn't see and extract companion files.

**9 Passes (numbered 4-12 to continue from format_citations):**

- **Pass 4:** Strip header block before first `---` (project metadata, presenter, date)
- **Pass 5:** Strip `### SLIDE N: LABEL` marker lines (authoring scaffolding)
- **Pass 6:** Extract `**Gamma instruction: ...**` lines to `*-gamma-instructions.json`, then remove
- **Pass 7:** Convert `***` to `---` card separators (some templates use triple asterisk)
- **Pass 8:** Convert `---*` reference lines to standard list items (`- Author...`)
- **Pass 9:** Extract `<!-- Speaker Notes: -->` to `*-gamma-notes.md`, then remove
- **Pass 10:** Normalize slide title headings to `##` (Gamma expects H2 for cards)
- **Pass 11:** Fix concatenated reference entries (regex splits accidentally joined lines)
- **Pass 12:** Strip `LO1:`, `LO2:` prefixes from learning objective bullets

**Inputs:** `presentation-long-gamma.md`
**Outputs:**

- `presentation-long-gamma.md` (overwritten, cleaned)
- `presentation-long-gamma-instructions.json` (per-slide design guidance)
- `presentation-long-gamma-notes.md` (speaker notes for rehearsal)

**Why This Exists:** Gamma renders markdown literally. If `### SLIDE 23: DATA SLIDE` appears in your .md, it appears on the slide. Meta-content must be stripped.

### Script 3: `audit_slide_design.py`

**Purpose:** Quality gate for slide design principles before validation.

**8 Checks:**

1. **Assertion-Evidence Titles** — Titles should be claims with verbs, not topic labels
2. **Bottom Line Presence** — Every content/data/trial/guideline slide needs `> **Bottom Line:**`
3. **Bullet Density** — Max 7 bullets per slide (7x7 rule)
4. **Word Count per Slide** — Target ≤140 words/slide (20 words/min × 7 min)
5. **Consecutive Text Slides** — Max 3 text-heavy slides in a row (audience fatigue)
6. **MCQ Frequency** — MCQs should appear every 7-10 slides (active learning)
7. **Case Integration** — Case-based structure: Case → Evidence → Application → Resolution
8. **Gamma Instruction Coverage** — Every slide should have design guidance

**Output:** `audit_output.txt` with FAIL/WARN/ADVISORY per check

**Thresholds by Slide Type:**

- Title slides: exempt from density checks
- Data/table slides: relaxed word count (tables are dense)
- MCQ slides: exempt from bullet density
- Case slides: higher word count allowed (clinical narrative)

### Script 4: `validate_gamma_ready.py`

**Purpose:** Final quality gate before Gamma submission. Must pass 11/11 hard checks.

**17 Checks (11 hard gates + 5 soft design + 1 info):**

**Hard Gates (MUST PASS):**

1. File exists
2. Non-empty content
3. H2 headers present (`##` for card titles)
4. Card separators (`---`) present
5. No meta-lines (`### SLIDE`, `**Gamma instruction:`, `<!-- Speaker Notes`)
6. No orphaned citations (`**Sources:** [N]` without expansion)
7. Card count matches header declaration
8. Well-formed superscripts (`<sup>[N]</sup>`, not `[N]` in body)
9. No empty cards (every `---` section has content)
10. No duplicate card titles
11. References section exists

**Soft Design Checks (WARN only):** 12. Assertion-evidence title format 13. Bottom Line presence on content slides 14. Bullet density (≤7 per slide) 15. Word count (≤140/slide average) 16. MCQ frequency (every 7-10 slides)

**Info:** 17. Card count report

**Output:** `validation_report.txt`

**Pass Criteria:** `11/11 PASSED, 0 FAILED` (soft checks can WARN)

### Script 5: `generate_gamma_params.py`

**Purpose:** Generate submission files for API and web workflows.

**Dual Output:**

**1. `*-gamma-api.json`** (API submission)

```json
{
  "inputText": "...",
  "textMode": "preserve",
  "numCards": 87,
  "imageOptions": {
    "source": "aiGenerated",
    "model": "imagen-4-pro",
    "style": "photorealistic medical photography..."
  },
  "cardOptions": { "dimensions": "16x9" },
  "additionalInstructions": "Slide-specific design template (max 2000 chars)"
}
```

**2. `*-gamma-web.md`** (Web submission guide)

- Unlimited instructions (no 2000-char limit)
- Per-slide design directives from `*-gamma-instructions.json`
- Step-by-step paste/configure/generate workflow

**Why Two Files:** API has 2000-char `additionalInstructions` limit. Web form allows unlimited pasting of per-slide guidance.

## Authoring Conventions

### Required Formatting

**Every slide MUST have:**

```markdown
### SLIDE 23: DATA SLIDE

## Assertion-Evidence Title With Verb

**Gamma instruction: Design guidance for this specific slide**

Body content with [N] citations...

**Sources:** [1][2][3]

> **Bottom Line:** One-sentence takeaway for this slide.

<!-- Speaker Notes: What to say when presenting this slide -->

---
```

### Slide Title Format (Assertion-Evidence)

**WRONG (topic label):**

```markdown
## DVT Prophylaxis Timing
```

**RIGHT (claim with verb):**

```markdown
## Early Prophylaxis Reduces VTE by 40%
```

### Citation Format

**In body text:** Use `[N]` numbered citations (NOT parenthetical)

```markdown
Trauma patients benefit from early prophylaxis[1][2]. LMWH reduces DVT by 50%[3].
```

**Sources block:** At bottom of content slides

```markdown
**Sources:** [1][2][3]
```

**References section:** At end of presentation

```markdown
## References

Geerts et al. Prevention of venous thromboembolism. Chest. 2008;133:381S-453S. PMID: 18574271 [1]
Rogers et al. EAST DVT prophylaxis guideline. J Trauma. 2002;53:142-164. PMID: 12131409 [2]
```

**CRITICAL:** `[N]` MUST be at END of reference line (regex depends on it).

### Bottom Line

Every content/data/trial/guideline slide needs:

```markdown
> **Bottom Line:** One-sentence clinical takeaway.
```

Exempt: title slides, section dividers, MCQ slides.

### Gamma Instructions

Every slide needs design guidance:

```markdown
**Gamma instruction: Medical image showing ICU patient with DVT prophylaxis devices, professional photography**
```

Or for data slides:

```markdown
**Gamma instruction: Preserve table exactly as formatted, use blue color theme, high contrast**
```

### Speaker Notes

```markdown
<!-- Speaker Notes: Emphasize the 40% relative risk reduction. Mention that timing matters—within 24 hours is ideal. Ask audience if they've encountered delays in their practice. -->
```

### Card Separators

Three hyphens between slides:

```markdown
---
```

### Slide Types and Design Rules

| Type       | Max Words | Max Bullets | Bottom Line | Notes                       |
| ---------- | --------- | ----------- | ----------- | --------------------------- |
| Title      | 30        | 0           | No          | Clean, minimal              |
| Content    | 140       | 7           | Yes         | One message                 |
| Data/Table | 200       | 10          | Yes         | Tables preferred over prose |
| MCQ        | 100       | 5           | No          | Question + 4-5 options      |
| Case       | 180       | 7           | Yes         | Clinical narrative          |
| Reference  | Unlimited | Unlimited   | No          | Dense by nature             |

## Evidence Standards

### GRADE Rating System

Every piece of evidence must be rated:

| Grade  | Recommendation | Quality  | Example                            |
| ------ | -------------- | -------- | ---------------------------------- |
| **1A** | Strong         | High     | Systematic review of RCTs          |
| **1B** | Strong         | Moderate | Individual RCT                     |
| **1C** | Strong         | Low      | Strong observational evidence      |
| **2A** | Weak           | High     | RCT with uncertainty               |
| **2B** | Weak           | Moderate | Observational with strong evidence |
| **2C** | Weak           | Low      | Case series                        |
| **3**  | Expert opinion | Very low | Consensus statement                |
| **4**  | Insufficient   | N/A      | No reliable data                   |

### Citation Verification Protocol

**NEVER trust AI-generated PMIDs.** This is the #1 source of errors.

**Verification workflow:**

1. Search PubMed manually for the study
2. Copy exact PMID from PubMed result
3. Verify author, journal, year match
4. If no PMID, use DOI instead
5. Run `scripts/verify_citations.py presentation-long.md` before pipeline

**Common fabrication patterns:**

- Plausible but wrong PMID (off by 1-2 digits)
- Real author + real journal + fake PMID
- Old PMID for a different paper by same author

**Fix:** Cross-reference every single PMID before authoring.

### Statistical Reporting

All effect estimates require:

- **95% CI** (not just p-value)
- **NNT** (number needed to treat) for interventions
- **ARR** (absolute risk reduction), not just RRR
- **Exact p-values** (p=0.03, not p<0.05)

**Example:**

```markdown
LMWH reduced DVT from 15% to 8% (ARR 7%, NNT 14, 95% CI 4-11%, p=0.001)[1].
```

## Slide Design Rules

### Assertion-Evidence Format

**Assertion:** Slide title is a claim with a verb
**Evidence:** Body provides data/visuals supporting the claim

**Example:**

```markdown
## Early Prophylaxis Reduces VTE by 40%

| Timing | VTE Rate | RR (95% CI)      |
| ------ | -------- | ---------------- |
| <24h   | 8%       | 0.60 (0.45-0.80) |
| 24-48h | 12%      | 0.85 (0.70-1.03) |
| >48h   | 15%      | Reference        |

> **Bottom Line:** Start within 24 hours for maximum benefit.
```

### One Message Per Slide

Bad slide (3 messages):

```markdown
## DVT Prophylaxis in Trauma

- Timing matters
- LMWH is better than UFH
- Contraindications include active bleeding
```

Good slides (3 separate):

```markdown
## Slide 1: Early Prophylaxis Reduces VTE by 40%

## Slide 2: LMWH Reduces DVT by 50% vs UFH

## Slide 3: Active Bleeding Is an Absolute Contraindication
```

### 7x7 Rule

- Max 7 bullets per slide
- Max 7 words per bullet
- Relaxed for data tables (tables are inherently dense)

### 20 Words Per Minute

Target: 140 words/slide (7-minute talk pace)

**Check:** `scripts/audit_slide_design.py` calculates word count per slide.

### CRAP Principles

- **Contrast:** High contrast text/background (black on white, white on dark blue)
- **Repetition:** Consistent formatting (same bullet style, same heading hierarchy)
- **Alignment:** Everything lines up (tables, bullets, images)
- **Proximity:** Related items grouped together

### Case-Based Structure

**Flow:**

```
1. Case Introduction (2-3 slides)
2. Clinical Question (1 slide)
3. Evidence Review (10-15 slides)
4. Application to Case (2-3 slides)
5. Case Resolution (1-2 slides)
6. Key Takeaways (1 slide)
```

### MCQ Frequency

Insert MCQ every 7-10 slides for active learning.

**Format:**

```markdown
## MCQ: Which timing maximizes VTE reduction?

A. <24 hours
B. 24-48 hours
C. 48-72 hours
D. >72 hours

**Correct:** A

**Explanation:** Early prophylaxis (<24h) reduces VTE by 40% compared to delayed initiation.
```

## Gamma Submission

### API Workflow

**1. Generate API parameters:**

```bash
python scripts/generate_gamma_params.py \
  projects/dvt-prophylaxis-trauma/presentation-long-gamma.md \
  projects/dvt-prophylaxis-trauma/
```

**2. Submit via Gamma MCP:**

```bash
# Load Gamma API key
export GAMMA_API_KEY="your_key"

# Submit
curl -X POST https://api.gamma.app/api/v1/generate \
  -H "Authorization: Bearer $GAMMA_API_KEY" \
  -H "Content-Type: application/json" \
  -d @projects/dvt-prophylaxis-trauma/presentation-long-gamma-api.json \
  --data-urlencode "text@projects/dvt-prophylaxis-trauma/presentation-long-gamma.md"
```

**3. Check result:**

- Response includes `presentationId`
- Open: `https://gamma.app/docs/{presentationId}`

### Web Workflow

**1. Open Gamma.app**
**2. Click "New" → "Paste"**
**3. Paste entire `*-gamma.md` content**
**4. Follow `*-gamma-web.md` instructions for settings:**

- Mode: "Format my text"
- Image generation: On, Imagen 4 Pro, photorealistic medical
- Length: Exact (numCards from web guide)
- Theme: Blues-dominant, professional

**5. Paste per-slide design instructions** (from web guide)
**6. Generate**

### Key Settings

| Setting                | Value                               | Why                                        |
| ---------------------- | ----------------------------------- | ------------------------------------------ |
| textMode               | `preserve`                          | Don't condense or rewrite authored content |
| numCards               | Exact count                         | Slide count must match (count `---` + 1)   |
| imageOptions.model     | `imagen-4-pro`                      | Best medical image quality                 |
| imageOptions.style     | `photorealistic, medical education` | Professional aesthetic                     |
| cardOptions.dimensions | `16x9`                              | Standard presentation format               |
| additionalInstructions | Per-slide design template           | Custom guidance per card                   |

### What to Check

After generation:

- [ ] Slide count matches authored count
- [ ] Citations rendered as superscripts
- [ ] No meta-lines visible (`### SLIDE`, `**Gamma instruction:`)
- [ ] Tables formatted correctly
- [ ] Images match slide content (no generic stock photos)
- [ ] Bottom Line boxes visible and formatted
- [ ] Speaker notes NOT visible on slides (extracted to companion file)

## Starting a New Topic

### Step-by-Step

**1. Create project directory:**

```bash
/new-topic "DVT Prophylaxis in Trauma Patients"
```

**Output:**

```
projects/dvt-prophylaxis-trauma/
  evidence-synthesis.md
  presentation-long.md
  notes.md
```

**2. Evidence gathering:**

- Search PubMed: `(DVT OR venous thromboembolism) AND (trauma OR injury) AND (prophylaxis OR prevention)`
- Collect PMIDs (verify each one)
- Rate evidence (GRADE 1A-4)
- Fill `evidence-synthesis.md`

**3. Author presentation:**

- Open `presentation-long.md`
- Follow authoring conventions (see above)
- Use `templates/presentation-long.md` as scaffold
- Write 80-100 slides (case-based structure)

**4. Run pipeline:**

```bash
cd projects/dvt-prophylaxis-trauma
python ../../scripts/format_citations.py presentation-long.md
python ../../scripts/preprocess_for_gamma.py presentation-long-gamma.md .
python ../../scripts/audit_slide_design.py presentation-long-gamma.md
python ../../scripts/validate_gamma_ready.py presentation-long-gamma.md
python ../../scripts/generate_gamma_params.py presentation-long-gamma.md .
```

**5. Check validation:**

```bash
cat validation_report.txt
# Must show: 11/11 PASSED, 0 FAILED
```

**6. Submit to Gamma:**

- API: Use `presentation-long-gamma-api.json`
- Web: Follow `presentation-long-gamma-web.md`

**7. Review and iterate:**

- Check generated slides
- Fix any design issues
- Re-run pipeline if content changes

### Project Structure

```
projects/your-topic/
  evidence-synthesis.md          # Literature review, GRADE ratings
  presentation-long.md           # Authored presentation (80-100 slides)
  presentation-long-gamma.md     # After format_citations.py
  presentation-long-gamma-instructions.json  # After preprocess_for_gamma.py
  presentation-long-gamma-notes.md          # After preprocess_for_gamma.py
  audit_output.txt               # After audit_slide_design.py
  validation_report.txt          # After validate_gamma_ready.py
  presentation-long-gamma-api.json  # After generate_gamma_params.py
  presentation-long-gamma-web.md    # After generate_gamma_params.py
  notes.md                       # Working notes, search terms, ideas
```

## Troubleshooting

### Pipeline Failures

**Problem:** `validate_gamma_ready.py` fails with "Orphaned Sources blocks"
**Cause:** `**Sources:** [N]` not expanded to full citations
**Fix:** Check References section has `[N]` at END of each line, re-run `format_citations.py`

---

**Problem:** `validate_gamma_ready.py` fails with "Meta-lines still present"
**Cause:** `### SLIDE N:` or `**Gamma instruction:**` still in file
**Fix:** Re-run `preprocess_for_gamma.py`, check output for leftover markers

---

**Problem:** `audit_slide_design.py` reports high word count
**Cause:** Too much text per slide
**Fix:** Split dense slides into 2-3 slides, move details to speaker notes

---

**Problem:** Gamma generates wrong number of slides
**Cause:** `numCards` mismatch (counted wrong, or `---` separators missing)
**Fix:** Count `---` in `*-gamma.md` manually, update header, re-run `generate_gamma_params.py`

---

**Problem:** Citations show as `[N]` instead of superscripts
**Cause:** `format_citations.py` not run, or references missing `[N]` suffix
**Fix:** Add `[N]` to END of reference lines, re-run `format_citations.py`

---

**Problem:** Gamma shows meta-content on slides
**Cause:** `preprocess_for_gamma.py` failed to strip markers
**Fix:** Check regex patterns in script, ensure `### SLIDE` lines have exact format

---

**Problem:** Fabricated PMID in References
**Cause:** AI generated plausible but wrong PMID
**Fix:** Verify EVERY PMID via PubMed, use `scripts/verify_citations.py`

---

**Problem:** Bottom Line missing on content slide
**Cause:** Forgot to add during authoring
**Fix:** Add `> **Bottom Line:** ...` before `---` separator, re-run pipeline

---

**Problem:** Gamma images don't match slide content
**Cause:** Generic `**Gamma instruction:**` (e.g., "medical image")
**Fix:** Be specific (e.g., "ICU trauma patient with mechanical DVT prophylaxis devices, lower extremity compression sleeves visible"), re-generate

---

**Problem:** Pipeline is not idempotent (running twice breaks it)
**Cause:** Superscript double-wrapping (`<sup><sup>[N]</sup></sup>`)
**Fix:** Only run `format_citations.py` once per authoring cycle, work from `presentation-long.md` source

### Common Authoring Mistakes

| Mistake                      | Example                   | Fix                                         |
| ---------------------------- | ------------------------- | ------------------------------------------- |
| Topic-label titles           | `## DVT Prophylaxis`      | `## Early Prophylaxis Reduces VTE by 40%`   |
| Parenthetical citations      | `(Smith 2020)`            | `[N]` numbered citations                    |
| Missing Sources block        | No `**Sources:**` line    | Add at bottom of content slides             |
| `[N]` in middle of reference | `[1] Smith et al. Title.` | Move to END: `Smith et al. Title. [1]`      |
| Missing Gamma instruction    | No design guidance        | Add `**Gamma instruction:**` to every slide |
| Missing Bottom Line          | No takeaway               | Add `> **Bottom Line:**` blockquote         |
| Dense text slides            | 300 words/slide           | Split into 2-3 slides, 140 words each       |
| No MCQs                      | 40 slides, zero questions | Insert MCQ every 7-10 slides                |

## File Map

```
academic-surgery-forge/
├── SKILL.md                  # Skill documentation (entry points, workflow)
├── CLAUDE.md                 # Project context (this is read by Claude)
├── verification.md           # Domain verification commands
│
├── agents/
│   └── evidence-reviewer.md  # Sub-agent for evidence quality review
│
├── commands/
│   ├── full-pipeline.md      # End-to-end: evidence → Gamma
│   ├── generate-presentation.md  # Pipeline only (slides exist)
│   ├── verify-citations.md   # Citation verification only
│   └── new-topic.md          # Directory scaffold
│
├── docs/
│   └── workflow-guide.md     # This file
│
├── evals/                    # Pytest test suite
│   ├── conftest.py
│   ├── test_format_citations.py
│   ├── test_preprocess.py
│   ├── test_card_utils.py
│   ├── test_audit.py
│   ├── test_validate_new.py
│   └── files/                # Test fixtures
│
├── projects/                 # Per-topic working directories
│   ├── dvt-prophylaxis-trauma/
│   ├── xabcde-hemorrhage-control/
│   ├── incentive-spirometry-trauma/
│   ├── padis-delirium-update/
│   ├── spinal-fracture-management/
│   └── penetrating-pancreaticoduodenal-trauma/
│
├── references/               # Reference documentation
│   ├── gamma-api-guide.md    # Gamma API settings, limitations
│   ├── citation-standards.md # PMID/DOI formatting rules
│   ├── slide-design-principles.md  # CRAP, assertion-evidence, 7x7
│   └── evidence-quality-framework.md  # GRADE rating system
│
├── scripts/                  # The 5-script pipeline + utilities
│   ├── card_utils.py         # Shared parsing (card classification, word count)
│   ├── format_citations.py   # Script 1: Citation formatter (3 passes)
│   ├── preprocess_for_gamma.py  # Script 2: Meta-content stripper (9 passes)
│   ├── audit_slide_design.py    # Script 3: Design quality audit (8 checks)
│   ├── validate_gamma_ready.py  # Script 4: Quality gate (17 checks)
│   ├── generate_gamma_params.py # Script 5: API/web submission files
│   ├── convert_inline_citations.py  # Utility: Convert parenthetical to numbered
│   └── verify_citations.py      # Utility: PMID verification via PubMed
│
└── templates/                # Reusable templates
    ├── evidence-synthesis.md
    ├── presentation-long.md  # 80-100 slides, case-based
    ├── presentation-medium.md  # 40-50 slides, condensed
    ├── journal-club.md       # Critical appraisal format
    ├── chalk-talk.md         # Whiteboard-style teaching
    └── mcq-case-pairs.md     # MCQ + case discussion pairs
```

### What Lives Where

| File Type           | Location                                                     | Purpose                   |
| ------------------- | ------------------------------------------------------------ | ------------------------- |
| Authored slides     | `projects/{topic}/presentation-long.md`                      | Source of truth           |
| Formatted slides    | `projects/{topic}/presentation-long-gamma.md`                | After citation formatting |
| Gamma-ready slides  | `projects/{topic}/presentation-long-gamma.md`                | After preprocessing       |
| API submission      | `projects/{topic}/presentation-long-gamma-api.json`          | API parameters            |
| Web submission      | `projects/{topic}/presentation-long-gamma-web.md`            | Web paste guide           |
| Speaker notes       | `projects/{topic}/presentation-long-gamma-notes.md`          | Rehearsal reference       |
| Design instructions | `projects/{topic}/presentation-long-gamma-instructions.json` | Per-slide Gamma guidance  |
| Evidence synthesis  | `projects/{topic}/evidence-synthesis.md`                     | Literature review         |
| Working notes       | `projects/{topic}/notes.md`                                  | Search terms, ideas       |
| Audit report        | `projects/{topic}/audit_output.txt`                          | Design quality results    |
| Validation report   | `projects/{topic}/validation_report.txt`                     | Quality gate results      |

---

## Key Lessons Learned

1. **AI fabricates PMIDs constantly.** Verify every single one via PubMed before authoring.
2. **Gamma supports cardSplit in MCP.** Use `cardSplit: auto` + `numCards` for deterministic counts, or `cardSplit: inputTextBreaks` to honor authored `---` boundaries.
3. **Meta-lines appear verbatim on slides** if not stripped by preprocessor.
4. **Pipeline is NOT idempotent end-to-end.** Superscripts double-wrap if run twice. Work from source.
5. **`[N]` must be at END of reference lines.** Regex depends on it for extraction.
6. **Gamma instruction extraction** (Pass 6) feeds `generate_gamma_params.py` for per-slide design.
7. **Web guide vs API params** serve different submission workflows (unlimited vs 2000-char limit).
8. **Assertion-evidence titles** dramatically improve slide clarity and retention.
9. **Bottom Line boxes** force you to synthesize the takeaway (better teaching).
10. **Case-based structure** beats pure didactic (application beats memorization).

---

**Default Presenter:** Evan DeCan, MD
**System Version:** 2.0 (pipeline-based, Gamma-native)
**Last Updated:** February 14, 2026
