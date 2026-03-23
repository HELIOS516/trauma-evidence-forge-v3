# V3 Presentation Handoffs — 5 Cloud Sessions

> Generated 2026-03-23. Each section is a self-contained prompt for a cloud Claude Code session.
> Run sequentially (1→5). All output goes to `skills/trauma-evidence-forge-v3/projects/Pending/{topic}/`.
>
> **All 5 follow V3 conventions** (not V1/V2). See V3 rules summary below.

---

## V3 Rules Summary (embed in every session)

**Keyword-only slides:**
- Max 50 words/slide body, 3-7 words per bullet
- No full sentences in slide body — sentences go in speaker notes only
- Assertion titles with verbs (not topic labels)

**Required elements on every content slide:**
- `> **Bottom Line:** [max 12 words]`
- `**[KEY STAT: ...]**` — one bold number
- `**Sources:** [N][M]` at bottom
- Speaker notes in `<!-- Speaker Notes: ... -->` (150-250 words)

**Gamma:**
- Marine theme locked: `themeId: "marine"`
- `textMode: "preserve"`, `cardSplit: "auto"`, `imagen-4-pro`
- Per-slide-type Gamma instructions (see templates)

**MCQs:** 2 per presentation (medium), 4 per presentation (long)

**Pipeline (5 scripts, run in order):**
```bash
cd ~/claude-skills  # or repo root
python skills/trauma-evidence-forge-v3/scripts/format_citations.py <input.md>
python skills/trauma-evidence-forge-v3/scripts/preprocess_for_gamma.py <output>
python skills/trauma-evidence-forge-v3/scripts/audit_slide_design.py <output>
python skills/trauma-evidence-forge-v3/scripts/validate_gamma_ready.py <output>
python skills/trauma-evidence-forge-v3/scripts/generate_gamma_params.py <output>
```
Fix any FAIL issues and re-run until all checks pass.

**Templates (copy structure exactly):**
- Medium: `skills/trauma-evidence-forge-v3/templates/presentation-medium.md` (18-22 slides)
- Long: `skills/trauma-evidence-forge-v3/templates/presentation-long.md` (24-30 slides)
- Evidence: `skills/trauma-evidence-forge-v3/templates/evidence-synthesis.md` (11 modules)

**Reference files to read first:**
- `skills/trauma-evidence-forge-v3/SKILL.md`
- `skills/trauma-evidence-forge-v3/CLAUDE.md`
- `skills/trauma-evidence-forge-v3/references/slide-design-principles.md`
- `skills/trauma-evidence-forge-v3/references/evidence-quality-framework.md`
- `skills/trauma-evidence-forge-v3/config/gamma-medical-profile.json`

**Gold standard example:** `skills/trauma-evidence-forge-v3/projects/Pending/xabcde-primary-survey/` (has evidence-synthesis, presentation-medium, presentation-long, all pipeline outputs)

**Presenter:** Evan DeCan, MD, Division of Acute Care Surgery, University of Virginia

---

## Handoff 1: Hemorrhagic Shock & Resuscitation

**Priority:** Highest (most content exists, closest to completion)

**Source material (REUSE — do NOT start from scratch):**
- Branch `origin/claude/setup-trauma-forge-8P07M` contains:
  - `evidence-synthesis.md` (226 lines, real PMIDs, real trial data for PROPPR/CRASH-2/PAMPer/Bickell)
  - `presentation-medium.md` (361 lines, V2-ish format — needs V3 keyword conversion)
- V3 stub already on main: `projects/Pending/hemorrhagic-shock-resuscitation/README.md` + empty `evidence-synthesis.md`

**Output directory:** `skills/trauma-evidence-forge-v3/projects/Pending/hemorrhagic-shock-resuscitation/`

### Steps

1. **Read V3 references first:** SKILL.md, CLAUDE.md, templates/presentation-medium.md, templates/presentation-long.md, references/slide-design-principles.md, config/gamma-medical-profile.json

2. **Cherry-pick evidence from branch:**
   ```bash
   cd ~/claude-skills
   git show origin/claude/setup-trauma-forge-8P07M:skills/trauma-evidence-forge-v3/projects/Pending/hemorrhagic-shock-resuscitation/evidence-synthesis.md > /tmp/hs-evidence-branch.md
   git show origin/claude/setup-trauma-forge-8P07M:skills/trauma-evidence-forge-v3/projects/Pending/hemorrhagic-shock-resuscitation/presentation-medium.md > /tmp/hs-medium-branch.md
   ```

3. **Rewrite evidence-synthesis.md** following the V3 template (11 modules). Use the branch evidence as your data source — it has verified PMIDs and real trial data. Expand to fill all 11 modules. Key trials to include: PROPPR (2015), CRASH-2 (2010), PAMPer (2018), Bickell (1994), PROMMTT (2013). Target ~500-700 lines.

4. **Author presentation-medium.md** (20-22 slides, 30-35 min). The branch has a V2-format medium presentation — **do NOT copy it verbatim**. Convert to V3 keyword-only format:
   - Every bullet = 3-7 words max
   - Every slide body ≤ 50 words
   - Assertion titles (e.g., "PROPPR Proved 1:1:1 Reduces 24-Hour Mortality" not "PROPPR Trial")
   - Add `**Gamma instruction:**` line at top of each slide section
   - 2 MCQ checkpoints
   - Follow templates/presentation-medium.md structure exactly

5. **Author presentation-long.md** (28-30 slides, 45-50 min). Expand from medium:
   - Add slides on: whole blood, prehospital plasma (PAMPer deep dive), TEG/ROTEM guided resuscitation, MTP activation criteria (ABC score), calcium replacement, fibrinogen replacement
   - 4 MCQ checkpoints
   - Add shelf exam tips in speaker notes
   - Follow templates/presentation-long.md structure exactly

6. **Run 5-script pipeline on BOTH presentations.** Fix any FAIL issues until all checks pass.

7. **Git add, commit with message `[TEFv3] hemorrhagic-shock: evidence + medium + long presentations`, push.**

### Validation targets
- evidence-synthesis.md: ≥20 verified PMIDs, all 11 modules populated, GRADE ratings on all treatment recs
- presentation-medium.md: 20-22 slides, avg ≤45 words/slide body, 2 MCQs, all checks pass
- presentation-long.md: 28-30 slides, avg ≤45 words/slide body, 4 MCQs, all checks pass

---

## Handoff 2: Spinal Injuries, Shock, and Fractures

**Priority:** High (rich evidence exists on branch, needs V3 migration)

**Source material (REUSE):**
- Branch `origin/claude/setup-spinal-injuries-project-v7idJ` contains:
  - `skills/trauma-evidence-forge/projects/Pending/spinal-injuries-shock-fractures/README.md` (134 lines — rich outline with NEXUS, CCR, ASIA, TLICS frameworks)
  - `skills/trauma-evidence-forge/projects/Pending/spinal-injuries-shock-fractures/evidence-synthesis.md` (283 lines — verified PMIDs for NEXUS 10891516, CCR 14695411, Stiell 11597285, EAST obtunded 25757133, Panczykowski 21619408, etc.)
- **NOTE:** This is in the V1 location (`trauma-evidence-forge/`). Must be migrated to V3 location.
- V3 does NOT have a stub for this topic yet — create directory and README.

**Output directory:** `skills/trauma-evidence-forge-v3/projects/Pending/spinal-injuries-shock-fractures/`

### Steps

1. **Read V3 references first** (same as Handoff 1).

2. **Create project directory and extract branch content:**
   ```bash
   cd ~/claude-skills
   mkdir -p skills/trauma-evidence-forge-v3/projects/Pending/spinal-injuries-shock-fractures/
   git show origin/claude/setup-spinal-injuries-project-v7idJ:skills/trauma-evidence-forge/projects/Pending/spinal-injuries-shock-fractures/evidence-synthesis.md > /tmp/spinal-evidence-branch.md
   git show origin/claude/setup-spinal-injuries-project-v7idJ:skills/trauma-evidence-forge/projects/Pending/spinal-injuries-shock-fractures/README.md > /tmp/spinal-readme-branch.md
   ```

3. **Write README.md** following V3 project README format (see hemorrhagic-shock README as example). MS3 clerkship level. Include: Learning Objectives, Key Frameworks (NEXUS, CCR, ASIA, TLICS, neurogenic vs spinal shock), slide outline, status checklist.

4. **Write evidence-synthesis.md** following V3 template (11 modules). Use branch evidence as data source — it has verified PMIDs for:
   - NEXUS criteria (Hoffman 2000, PMID 10891516)
   - Canadian C-Spine Rule (Stiell 2001, PMID 11597285; Stiell 2003, PMID 14695411)
   - Obtunded patient clearance (Patel 2015, PMID 25757133)
   - TLICS scoring (Vaccaro 2005)
   - Neurogenic shock management
   Expand to fill all 11 modules. Do web-search-backed PubMed verification for any new PMIDs.

5. **Author presentation-medium.md** (20-22 slides, 30-35 min). V3 keyword-only format. Subtopics: c-spine clearance (NEXUS vs CCR), obtunded patient clearance, neurogenic shock vs spinal shock, ASIA scale, TLICS scoring, thoracolumbar fracture management. 2 MCQ checkpoints.

6. **Author presentation-long.md** (28-30 slides, 45 min). Expand with: detailed NEXUS vs CCR comparison table, obtunded patient algorithm, vasopressor selection in neurogenic shock, ASIA grading with prognosis, TLICS scoring worked example, MRI indications, steroid controversy (NASCIS legacy), shelf exam tips. 4 MCQ checkpoints.

7. **Run 5-script pipeline on BOTH.** Fix FAILs.

8. **Git add, commit `[TEFv3] spinal-injuries: new V3 project with evidence + presentations`, push.**

---

## Handoff 3: Spinal Cord Injury Management

**Priority:** Medium (V2 content exists with real slides, needs V3 conversion + citation renumber)

**Source material (REUSE):**
- On main branch at `skills/trauma-evidence-forge-v2/projects/Pending/spinal-cord-injury-management/`:
  - `spinal-cord-injury-management.md` — 24-slide LONG version with clinical content and citations [32]-[36]
  - `README.md`
- **CRITICAL: Citation renumbering required:**
  - [32] → [1] Froedtert protocol
  - [33] → [2] ENLS v5.0
  - [34] → [3] PMC11840280
  - [35] → [4] ACS CPG Sage 2023
  - [36] → [5] Acute phase tSCI 2024
- This is a **Resident/Fellow-level** presentation (not MS3). Adjust depth accordingly.
- V3 does NOT have a stub for this topic — create directory.

**Output directory:** `skills/trauma-evidence-forge-v3/projects/Pending/spinal-cord-injury-management/`

### Steps

1. **Read V3 references first** (same as Handoff 1).

2. **Read source material:**
   ```bash
   cat skills/trauma-evidence-forge-v2/projects/Pending/spinal-cord-injury-management/spinal-cord-injury-management.md
   cat skills/trauma-evidence-forge-v2/projects/Pending/spinal-cord-injury-management/README.md
   ```

3. **Create project directory:**
   ```bash
   mkdir -p skills/trauma-evidence-forge-v3/projects/Pending/spinal-cord-injury-management/
   ```

4. **Write README.md** in V3 format. Target audience: Residents/Fellows. Include: overview, learning objectives, key frameworks (ASIA, neurogenic shock MAP targets, vasopressor selection, steroid controversy), slide outline, status checklist.

5. **Write evidence-synthesis.md** following V3 template (11 modules). Use the V2 content as your evidence base and EXPAND significantly with web-search-backed PubMed evidence. Renumber all citations starting from [1]. Key topics:
   - SCI epidemiology (54/million/year US)
   - Neurogenic shock recognition and differentiation from spinal shock
   - MAP targets (>85 mmHg x 7 days)
   - Vasopressor selection (norepinephrine first-line for cervical SCI)
   - Steroid controversy (NASCIS II/III legacy, current guidelines against routine use)
   - Surgical timing (<24h decompression evidence)
   - DVT prophylaxis in SCI
   - Autonomic dysreflexia
   - Rehabilitation and prognostication
   Target ≥25 verified PMIDs.

6. **Author presentation-medium.md** (20-22 slides, 35 min). V3 keyword-only. Resident/fellow depth — include more nuanced vasopressor dosing, MAP augmentation trial data, surgical timing evidence, and complications management. 2 MCQ checkpoints.

7. **Author presentation-long.md** (28-30 slides, 50 min). Expand: detailed neurogenic shock hemodynamics, vasopressor comparison table, NASCIS controversy deep dive, surgical decompression timing evidence, autonomic dysreflexia management, SCI rehabilitation milestones, ASIA-based prognosis. 4 MCQ checkpoints.

8. **Run 5-script pipeline on BOTH.** Fix FAILs.

9. **Git add, commit `[TEFv3] spinal-cord-injury: V2-to-V3 migration with expanded evidence`, push.**

---

## Handoff 4: Thoracic Trauma — Chest Tubes & Thoracotomies

**Priority:** Medium (V3 stub exists but evidence-synthesis.md is empty scaffold)

**Source material:**
- V3 main has: `projects/Pending/thoracic-trauma/README.md` (60 lines — full outline with learning objectives, slide outline for 20 slides)
- V3 main has: `projects/Pending/thoracic-trauma/evidence-synthesis.md` (empty scaffold — headers only)
- Branch `origin/claude/review-documentation-YXNIt` has: only a V1-format README.md (21 lines) — minimal value, V3 README is better
- **Must build evidence synthesis from scratch via web search**

**Output directory:** `skills/trauma-evidence-forge-v3/projects/Pending/thoracic-trauma/`

### Steps

1. **Read V3 references first** (same as Handoff 1).

2. **Read existing README.md for slide outline and learning objectives:**
   ```bash
   cat skills/trauma-evidence-forge-v3/projects/Pending/thoracic-trauma/README.md
   ```

3. **Write evidence-synthesis.md** following V3 template (11 modules). Do web-search-backed evidence synthesis with verified PMIDs. Cover 8 subtopics:
   - Tension pneumothorax (diagnosis, needle vs finger decompression)
   - Hemothorax (simple vs massive, chest tube thresholds for OR: >1500 mL initial or >200 mL/hr x 2-4h)
   - Cardiac tamponade (Beck triad, pericardiocentesis vs pericardial window)
   - Flail chest and pulmonary contusion (PPV, rib fixation evidence)
   - Aortic injury (AAST grading, endovascular vs open repair)
   - ED thoracotomy indications (EAST guidelines, survival by mechanism)
   - Chest tube management (size, placement, removal criteria)
   - Rib fracture scoring and elderly mortality
   Key PMIDs to find/verify: EAST EDT guidelines, AAST aortic grading, EAST chest tube guidelines. Target ≥20 verified PMIDs.

4. **Author presentation-medium.md** (20-22 slides, 35 min). Follow V3 keyword-only format. Use the README slide outline as guide. MS3 level. 2 MCQ checkpoints.

5. **Author presentation-long.md** (28-30 slides, 45 min). Expand: add slides for aortic injury, retained hemothorax (VATS vs fibrinolytics), rib fixation evidence, tracheobronchial injury, esophageal injury, diaphragmatic injury, shelf exam tips. 4 MCQ checkpoints.

6. **Run 5-script pipeline on BOTH.** Fix FAILs.

7. **Git add, commit `[TEFv3] thoracic-trauma: evidence synthesis + medium + long presentations`, push.**

---

## Handoff 5: Traumatic Brain Injury — GCS to the OR

**Priority:** Standard (V3 stub exists but evidence-synthesis.md is empty scaffold)

**Source material:**
- V3 main has: `projects/Pending/traumatic-brain-injury/README.md` (64 lines — full outline with learning objectives, slide outline for 22 slides)
- V3 main has: `projects/Pending/traumatic-brain-injury/evidence-synthesis.md` (empty scaffold — headers only)
- A prior cloud session attempted a full clone-and-build from `HELIOS516/trauma-evidence-forge-v3` repo — status unknown, likely incomplete
- **Must build evidence synthesis from scratch via web search**

**Output directory:** `skills/trauma-evidence-forge-v3/projects/Pending/traumatic-brain-injury/`

### Steps

1. **Read V3 references first** (same as Handoff 1).

2. **Read existing README.md for slide outline and learning objectives:**
   ```bash
   cat skills/trauma-evidence-forge-v3/projects/Pending/traumatic-brain-injury/README.md
   ```

3. **Write evidence-synthesis.md** following V3 template (11 modules). Do web-search-backed evidence synthesis with verified PMIDs. Cover subtopics:
   - GCS scoring (eyes, verbal, motor — reliability, pitfalls)
   - TBI classification (mild 13-15, moderate 9-12, severe ≤8)
   - Monroe-Kellie doctrine and ICP physiology
   - Epidural vs subdural hematoma (CT appearance, surgical thresholds)
   - Herniation syndromes (uncal vs central — CNIII palsy, Cushing triad)
   - ICP management (BTF 4th Edition tiered algorithm: Tier 1 basics → Tier 2 osmotherapy → Tier 3 decompressive craniectomy)
   - Secondary injury prevention (hypotension SBP <90 doubles mortality, hypoxia)
   - Anticoagulation reversal in TBI
   - Concussion and return-to-play guidelines
   Key PMIDs to find/verify: BTF 4th Edition (Carney 2017), DECRA trial, RESCUEicp trial, BEST-TRIP trial. Target ≥20 verified PMIDs.

4. **Author presentation-medium.md** (20-22 slides, 40 min). V3 keyword-only. Use README slide outline as guide. MS3 level. Include GCS component scoring table slide, epidural vs subdural comparison table slide. 2 MCQ checkpoints.

5. **Author presentation-long.md** (28-30 slides, 45 min). Expand: dedicated GCS component scoring table, epidural vs subdural comparison table, herniation syndrome comparison, BTF tier-by-tier deep dive, DECRA/RESCUEicp trial slides, pediatric TBI (non-accidental trauma), anticoagulation reversal protocols, "Your Role as MS3" slide, shelf exam tips. 4 MCQ checkpoints. Define ALL abbreviations on first use.

6. **Run 5-script pipeline on BOTH.** Fix FAILs.

7. **Git add, commit `[TEFv3] traumatic-brain-injury: evidence synthesis + medium + long presentations`, push.**

---

## Branch Strategy

All 5 handoffs should work on a single feature branch from main:
```bash
git checkout main && git pull
git checkout -b feature/v3-five-presentations
```
Commit after each topic completes. When all 5 are done, merge to main.

Alternatively, each cloud session can create its own branch:
```bash
git checkout -b claude/v3-{topic-slug}
```
Then merge sequentially after each completes.

## Gamma Submission (after all pipeline checks pass)

Use MCP tool `GAMMA_GENERATE_GAMMA` or the Gamma API directly:

```bash
curl -X POST https://gamma.app/api/generate \
  -H "Authorization: Bearer sk-gamma-eR7jhlp5wTrR02mAzXKwhIqw1DRXYhc5vsMpJfpxZKM" \
  -H "Content-Type: application/json" \
  -d @<generated-gamma-api.json>
```

The `generate_gamma_params.py` script produces the API JSON. Always verify Marine theme is set.

## Post-Completion

After all 5 topics complete:
1. Move completed projects from `Pending/` to `Complete/`
2. Update `SKILL.md` and `CLAUDE.md` project tables
3. Delete stale remote branches:
   ```bash
   git push origin --delete claude/setup-spinal-injuries-project-v7idJ
   git push origin --delete claude/review-documentation-YXNIt
   git push origin --delete claude/setup-trauma-forge-8P07M
   git push origin --delete claude/review-project-docs-eyfCf
   ```
