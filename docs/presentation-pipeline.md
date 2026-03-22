# Academic Surgery Forge: From PubMed to Grand Rounds in Hours, Not Days

> An AI-powered system that transforms clinical topics into complete, citation-verified, professionally designed medical presentations — built for Level 1 Trauma Centers and academic medical education.

---

## The Problem

Creating a high-quality grand rounds presentation is a time-intensive process that demands clinical expertise, research skills, and presentation design:

- **3-4 hours** searching PubMed, reading papers, extracting key data
- **2-3 hours** synthesizing evidence, building comparison tables, rating evidence quality
- **2-3 hours** authoring slides in PowerPoint, structuring the narrative
- **1-2 hours** formatting citations, cross-checking PMIDs, ensuring reference accuracy

**Total: 8-12 hours of work** — and that's for an experienced clinician-educator.

The rise of AI tools promised to accelerate this workflow, but introduced a critical vulnerability: **fabricated citations**. A single AI-hallucinated PMID can destroy academic credibility. Many educators have abandoned AI assistance entirely rather than risk citing nonexistent papers.

**Academic Surgery Forge solves both problems:** it reduces presentation development time to 2-3 hours while enforcing citation integrity through systematic PubMed verification.

---

## What It Produces

From a topic like **"DVT Prophylaxis in Trauma Patients"** or **"PADIS Delirium Guidelines Update,"** the system generates:

### 1. Evidence Synthesis Documents

- **GRADE-rated evidence tables** (1A = strong recommendation + high-quality evidence → 4 = insufficient evidence)
- **Multi-society guideline comparison matrices** (EAST, WEST, ACCP, SCCM, ACS-TQIP, etc.)
- **Statistical summaries** with 95% CI, NNT, absolute risk reduction, exact p-values
- **Bias assessment** using CONSORT/STROBE/PRISMA checklists

### 2. Professional Slide Decks (30-45 slides)

- **Assertion-evidence format titles** — titles are claims with verbs ("Early Prophylaxis Reduces VTE by 40%"), not topic labels ("DVT Prophylaxis Timing")
- **Numbered citations** verified against PubMed, with full bibliographic entries expanded at the bottom of each slide
- **Speaker notes** extracted for the presenter (preserved, but not shown on slides)
- **"Bottom Line" callouts** on every data slide — the clinical takeaway, not just the numbers
- **Interactive MCQs** every 7-10 minutes for audience engagement
- **Case-based learning structure** (Case → Evidence → Application → Resolution)
- **Professional design** via Gamma.app with AI-generated medical imagery (16:9 format, blues-dominant color palette)

### 3. Teaching Supplements

- **Chalk talk modules** (whiteboard-style interactive sessions for small groups)
- **MCQ/case pairs** for formative assessment

**Every clinical claim is backed by a verified citation.** Every slide follows evidence-based design principles. Every presentation is ready to deliver.

---

## How It Works

The system orchestrates a 7-phase workflow:

### **Phase 1: Evidence Gathering**

Systematic PubMed search across six categories:

- Clinical practice guidelines
- Randomized controlled trials
- Meta-analyses and systematic reviews
- Recent evidence (last 5 years)
- Epidemiology and prevalence data
- Landmark studies

**Target: 15-25 verified references per presentation**

Every PMID is verified against PubMed's database. AI models routinely fabricate plausible-looking PMIDs (e.g., "PMID 38243640" might sound legitimate, but points to an unrelated study). Verification catches these before they enter the presentation.

---

### **Phase 2: Evidence Grading**

Using the **GRADE framework**, evidence is classified:

- **1A** = Strong recommendation + high-quality evidence
- **1B/1C** = Strong recommendation + moderate/low-quality evidence
- **2A/2B/2C** = Weak recommendation + varying quality
- **3** = Conflicting evidence
- **4** = Insufficient evidence

Statistical reporting standards:

- 95% confidence intervals
- Number needed to treat (NNT)
- Absolute risk reduction (ARR)
- Exact p-values (never "p < 0.05")

---

### **Phase 3: Evidence Synthesis**

Narrative integration with structured data:

- **Comparison tables** for RCT head-to-head data
- **Multi-society guideline matrices** showing agreement/divergence
- **Controversy identification** where guidelines conflict
- **Evidence gap analysis** for future research directions

---

### **Phase 4: Slide Authoring**

Markdown-based slides with strict formatting:

- **One key message per slide** (cognitive load theory)
- **Assertion-evidence titles** with active verbs
- **Numbered citations** in body text: `[1][2][3]`
- **Per-slide source blocks**: `**Sources:** [1][2]` (expanded to full citations by the pipeline)
- **Bottom Line boxes** on every data/trial/guideline slide
- **Speaker notes** below each slide (stripped before Gamma submission)
- **Case-based structure** for narrative flow

Design follows:

- **CRAP principles** (Contrast, Repetition, Alignment, Proximity)
- **Cognitive Load Theory** (Sweller) — minimize extraneous cognitive load
- **Dual Coding Theory** (Paivio) — pair visual and verbal information
- **7×7 rule** — max 7 bullets per slide, max 7 words per bullet

---

### **Phase 5: Pipeline Processing**

Five Python scripts run sequentially:

#### 1. **Citation Formatting** (`format_citations.py`)

- Converts `[N]` to `<sup>[N]</sup>` superscript
- Expands per-slide `**Sources:** [N][M]` blocks to full bibliographic entries
- Validates all PMIDs against a reference database

#### 2. **Gamma Preprocessing** (`preprocess_for_gamma.py`)

Nine transformation passes:

- Strip authoring markers (slide type tags, TODO comments)
- Extract speaker notes → companion file (`*-gamma-notes.md`)
- Extract design instructions → JSON file (`*-gamma-instructions.json`)
- Normalize headings (H2 → H1 for Gamma's parser)
- Strip learning objective tags
- Clean whitespace and formatting artifacts

**Passes 4-12 are idempotent** (safe to run multiple times). The full pipeline is not, due to superscript wrapping.

#### 3. **Design Quality Audit** (`audit_slide_design.py`)

Eight design checks against type-specific thresholds:

- Word density (max 20 projected words/minute)
- Bullet count (max 7 per slide)
- Table presence on data/guideline slides
- Bottom Line boxes on data/trial/guideline slides
- Assertion-evidence title structure
- Image presence on title/visual slides
- Nested list depth
- Emoji/casual language detection

#### 4. **Validation** (`validate_gamma_ready.py`)

Quality gate with **17 checks** (11 must pass):

- No leftover authoring markers
- No orphaned speaker notes
- Citations properly formatted
- Bottom Line boxes present where required
- Slide type balance (not all text)
- Design quality metrics pass
- No empty slides

**If validation fails, the pipeline stops.** Issues must be fixed before Gamma submission.

#### 5. **Gamma Parameter Generation** (`generate_gamma_params.py`)

Produces:

- API call parameters (theme, textMode: "preserve", per-slide design hints)
- Web submission guide (for manual upload if API is unavailable)

Gamma contract source of truth for parameter semantics:

- `../gamma-presentation-core/references/gamma-canonical-spec.md`
- `../gamma-presentation-core/references/gamma-mcp-tool-contracts.md`

---

### **Phase 6: Gamma Submission**

Upload to **Gamma.app** with:

- `textMode: "preserve"` — Gamma designs slides around the exact content, no rewriting
- AI-generated medical imagery (using Google's Imagen-4-Pro model)
- Per-slide design instructions (e.g., "two-column layout," "full-bleed image," "data table focus")

Gamma returns a shareable URL and an editable web-based presentation.

---

### **Phase 7: Teaching Supplements**

- **Chalk talks** for small-group interactive teaching
- **MCQ/case pairs** for audience assessment

---

## The Citation Integrity Problem

Academic medicine lives or dies by citation accuracy. A single fabricated reference can:

- Destroy the presenter's credibility
- Undermine institutional trust in AI-assisted workflows
- Propagate misinformation if unchecked

### The "Reference [16] Incident"

During development of the DVT Prophylaxis presentation, the system flagged **PMID 38243640** as suspicious. The AI had generated this PMID to cite a meta-analysis on DVT prophylaxis timing.

**Verification revealed:**

- PMID 38243640 was a real paper
- But it was about **cardiac arrest outcomes**, not DVT prophylaxis
- The claimed meta-analysis **did not exist**

This was a **semantic hallucination** — the AI fabricated a plausible study, then assigned it a real (but unrelated) PMID to make it look legitimate.

### Five Known Hallucination Patterns

The system documents and checks for:

1. **Plausible PMID, wrong topic** (like Reference [16])
2. **Nonexistent PMID** (numerically valid but not in PubMed)
3. **Real paper, fabricated findings** (correct citation, wrong statistics)
4. **Misattributed author** (correct PMID, wrong first author)
5. **Date/journal mismatch** (PMID from 2018 claimed as 2023 study)

### How the System Solves It

**Mandatory PubMed verification for every PMID:**

- Before a citation enters the presentation, it's checked against PubMed's API
- Title, authors, journal, and publication year are extracted
- If any field mismatches the AI's claim, the citation is flagged
- The presenter reviews flagged citations before finalizing

**Result:** Zero fabricated citations in six completed projects (150+ total references).

---

## Engineering Under the Hood

For the technically curious, here's what makes the system robust:

### **Companion File Architecture**

Rather than destroying information during preprocessing, the system **extracts** it:

- Speaker notes → `*-gamma-notes.md` (preserved for the presenter)
- Design instructions → `*-gamma-instructions.json` (fed into Gamma API)
- The Gamma-ready markdown is clean for submission, but **nothing is lost**

This design enables:

- Version control for presenter notes
- Reusable design templates
- Debugging (comparing raw vs. processed files)

### **Idempotent vs. Non-Idempotent Design**

- **Passes 4-12** (preprocessing) are idempotent — safe to run repeatedly
- **The full pipeline** is not, because citation superscript conversion would double-wrap `<sup>` tags
- The system is designed to **run once end-to-end** from raw markdown to Gamma upload

### **Test Coverage**

**41+ pytest tests** covering:

- Citation formatting (superscript conversion, source block expansion)
- Preprocessing (marker stripping, note extraction, heading normalization)
- Card classification (slide type detection)
- Design audit (word density, bullet count, Bottom Line presence)
- Validation (quality gate checks)

**Why tests matter:** A single regression in citation formatting could introduce fabricated PMIDs. Tests prevent that.

### **Technology Stack**

| Component          | Technology             |
| ------------------ | ---------------------- |
| AI Orchestration   | Claude Code (Opus 4.6) |
| Evidence Gathering | PubMed API             |
| Pipeline Scripts   | Python 3.13            |
| Slide Design       | Gamma.app API          |
| Evidence Rating    | GRADE Framework        |
| Image Generation   | Google Imagen-4-Pro    |
| Testing            | pytest                 |
| Version Control    | Git                    |

---

## Slide Design Philosophy

The system doesn't just automate — it **encodes pedagogy**.

### **Assertion-Evidence Format**

Traditional slide titles are topic labels:

- ❌ "DVT Prophylaxis Timing"
- ❌ "Meta-Analysis Results"

Assertion-evidence titles are **claims**:

- ✅ "Early Prophylaxis Reduces VTE by 40%"
- ✅ "Enoxaparin Outperforms UFH in High-Risk Trauma"

**Why it matters:** Assertion titles tell the audience what to think, not just what the slide is about. This improves retention and reduces cognitive load.

### **Cognitive Load Theory**

Every slide is designed to minimize **extraneous cognitive load**:

- One key message per slide
- Maximum 20 projected words per minute
- Data in tables, not paragraphs
- Visual reinforcement of key statistics

### **Case-Based Learning**

Presentations follow a clinical narrative:

1. **Case Introduction** — real patient scenario
2. **Evidence Review** — what does the literature say?
3. **Application** — how does this change practice?
4. **Case Resolution** — outcome with evidence-based care
5. **Interactive MCQ** — audience checkpoint

**Research shows** case-based learning improves knowledge retention by 30-40% compared to didactic lectures.

### **The "So What?" Rule**

Every data slide includes a **Bottom Line** blockquote:

> **Bottom Line:** Early chemical prophylaxis (within 24 hours) reduces VTE by 40% (NNT = 25) without increasing bleeding risk in hemodynamically stable trauma patients.

This forces the presenter to **interpret** the data, not just present it.

---

## Projects Built With This System

Completed presentations spanning multiple specialties:

1. **DVT Prophylaxis in Trauma Patients** — 42 slides, 23 citations
2. **XABCDE Approach to Hemorrhage Control** — 38 slides, 19 citations
3. **Incentive Spirometry in Surgical/Trauma Patients** — 35 slides, 21 citations
4. **PADIS Delirium Guidelines Update** — 40 slides, 18 citations
5. **Spinal Fracture Management** — 36 slides, 20 citations
6. **Penetrating Pancreaticoduodenal Trauma** — 33 slides, 17 citations

**Total: 224 slides, 118 verified citations**

**Zero fabricated PMIDs.**

---

## What's Next

### **Immediate Roadmap**

- **Presentation analytics** — track time-per-slide, audience engagement, MCQ performance
- **Collaborative editing** — multi-author workflow with conflict resolution
- **Citation auto-update** — detect when cited papers are retracted or updated

### **Expansion Opportunities**

- **Specialty templates** — cardiology, neurology, oncology-specific evidence structures
- **Morbidity & Mortality format** — root cause analysis, systems review, learning points
- **Journal club automation** — critical appraisal, bias assessment, clinical applicability

### **Integration Targets**

- **Epic EHR** — pull real patient data for case studies (de-identified)
- **PubMed Central** — full-text access for deeper evidence extraction
- **UpToDate** — cross-reference clinical recommendations with evidence base

---

## About the Author

**Evan DeCan, MD** is an attending physician at a Level 1 Trauma Center specializing in evidence-based medical education. This system was built to solve a personal problem: creating high-quality grand rounds presentations without sacrificing citation integrity or spending entire weekends in PubMed.

---

## Getting Started

The system is built on **Claude Code** with Python 3.13 and the Gamma.app API. The full workflow documentation is in `SKILL.md`.

**Core principle:** Trust, but verify. AI accelerates the work — human expertise ensures accuracy.

---

_Last updated: February 14, 2026_
