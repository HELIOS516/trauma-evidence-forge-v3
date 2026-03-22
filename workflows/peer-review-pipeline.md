# Peer Review Pipeline

Tri-tier workflow for structured manuscript peer review across 5 domains.

## Review Domains

All tiers evaluate the same 5 domains:

| #   | Domain                | Focus Areas                                              |
| --- | --------------------- | -------------------------------------------------------- |
| 1   | Methodology           | Study design, bias assessment, sample size, confounders  |
| 2   | Statistics            | Correct tests, effect sizes, multiple comparisons, CI    |
| 3   | Reporting             | Checklist compliance (CONSORT/STROBE/PRISMA/SQUIRE/CARE) |
| 4   | Literature            | Citation completeness, missing key references, recency   |
| 5   | Clinical Significance | Beyond statistical significance, generalizability, NNT   |

Severity ratings: **Major** (must fix), **Minor** (should fix), **Optional** (suggestions).

---

## Tier 1: Conversational (claude.ai / Desktop)

No file system or script access. All analysis is conversational.

### Prerequisites

- PubMed connector enabled (claude.ai) or PubMed MCP installed (Desktop)
- Reference: `docs/script-equivalents.md` for manual validation rules

### Step-by-Step

1. **Intake**: User pastes manuscript text or uploads PDF. Confirm receipt and identify:
   - Study type (RCT, observational, systematic review, case report, quality improvement)
   - Target journal (if known)
   - Applicable reporting checklist

2. **Automated Checks (Manual Equivalent)**:
   Apply the validation rules from `docs/script-equivalents.md`:
   - Count IMRAD sections present
   - Check for `[N]` citations in body text
   - Verify PMID/DOI presence in references
   - Flag suspicious PMIDs (all same digits, 00000000, 12345678)
   - Estimate AI detection score across 8 categories
   - Check reference formatting consistency

3. **Domain-by-Domain Review**:
   Work through each domain sequentially:

   **Domain 1 -- Methodology**:
   - Is the study design appropriate for the research question?
   - Are inclusion/exclusion criteria clearly stated?
   - Is the sample size justified (power calculation for RCTs)?
   - Are potential confounders identified and addressed?
   - Is bias risk assessed (selection, performance, detection, attrition, reporting)?

   **Domain 2 -- Statistics**:
   - Are statistical tests appropriate for data type and distribution?
   - Are effect sizes reported (OR, RR, HR, mean difference)?
   - Are 95% confidence intervals provided?
   - Are exact p-values reported (not just "p < 0.05")?
   - Is multiple comparison correction applied where needed?

   **Domain 3 -- Reporting**:
   - Auto-detect study type and select checklist
   - Walk through checklist items (CONSORT 25, STROBE 22, PRISMA 27, SQUIRE 18, CARE 13)
   - Flag missing items with specific locations where they should appear

   **Domain 4 -- Literature**:
   - Are seminal papers in the field cited? (Check against `references/global-surgery-literature.md`)
   - Use PubMed connector to search for missing key references
   - Is the literature current (majority within last 5-10 years)?
   - Are conflicting studies acknowledged?

   **Domain 5 -- Clinical Significance**:
   - Do findings change clinical practice?
   - Is NNT reported where applicable?
   - Are results generalizable to the target population?
   - Are limitations honestly discussed?
   - Is the conclusion supported by the data presented?

4. **Compile Review**: Output structured review report (see Output Format below)

5. **Revision Response** (if requested): Generate point-by-point response letter for reviewer comments

### Output Format

```markdown
## Peer Review: [Manuscript Title]

**Reviewer Role**: [Methodology / Clinical / Editor / Statistician]
**Date**: [Today]
**Study Type**: [Detected type] | **Checklist**: [Applied checklist]

### Summary

[2-3 sentence overview of the manuscript and overall assessment]

### Major Issues

1. [Issue] -- [Location in manuscript] -- [Specific recommendation]

### Minor Issues

1. [Issue] -- [Location] -- [Recommendation]

### Optional Suggestions

1. [Suggestion]

### Automated Check Results

- Validation: [PASS/FAIL] ([N] hard failures, [N] soft warnings)
- AI Detection Score: [0-100] ([interpretation])
- Reference Format: [N issues found]

### Domain Scores

| Domain                | Rating               | Key Finding      |
| --------------------- | -------------------- | ---------------- |
| Methodology           | Strong/Adequate/Weak | [1-line summary] |
| Statistics            | Strong/Adequate/Weak | [1-line summary] |
| Reporting             | [X]% compliant       | [checklist name] |
| Literature            | Complete/Gaps        | [1-line summary] |
| Clinical Significance | High/Moderate/Low    | [1-line summary] |

### Decision

[Accept / Minor Revision / Major Revision / Reject]
[1-2 sentence justification]
```

---

## Tier 2: CLI (Claude Code without OMC)

Script-assisted review with file output.

### Prerequisites

- Python 3.9+ available
- PubMed MCP server installed (see `docs/pubmed-setup.md`)

### Step-by-Step

1. **Setup**:

   ```bash
   # Place manuscript in project directory
   mkdir -p projects/<name>
   cp /path/to/manuscript.md projects/<name>/manuscript.md
   ```

2. **Run Automated Checks**:

   ```bash
   # 16-check validation (10 hard, 6 soft)
   python3 scripts/validate_manuscript.py projects/<name>/manuscript.md --json > projects/<name>/validation.json

   # 8-category AI detection
   python3 scripts/detect_ai_patterns.py projects/<name>/manuscript.md --json > projects/<name>/ai-detection.json

   # Reference format check
   python3 scripts/format_references.py projects/<name>/manuscript.md --style vancouver > projects/<name>/ref-check.txt
   ```

3. **Review Script Results**:
   - Read all three output files
   - Identify hard-gate failures (must be addressed)
   - Note AI detection hotspots (categories scoring > 10)
   - List reference formatting issues

4. **Domain-by-Domain Analysis**:
   - Read `manuscript.md` completely
   - Work through all 5 domains (same criteria as Tier 1 Step 3)
   - For Literature domain: use PubMed MCP to verify citations and find missing references
   - Cross-reference with `references/global-surgery-literature.md`

5. **Write Review Report**:

   ```bash
   # Create structured review file
   # Write to projects/<name>/review.md using the Output Format from Tier 1
   ```

6. **Revision Response** (if requested):
   - Create `projects/<name>/revision-response.md`
   - Point-by-point response with page/line references
   - Evidence-based rebuttals where reviewer comments are addressed or respectfully disagreed with

### Output

Project directory with: `review.md`, `validation.json`, `ai-detection.json`, `ref-check.txt`, optionally `revision-response.md`.

---

## Tier 3: CLI + OMC (Claude Code with oh-my-claudecode)

Parallel review agents with merged results.

### Prerequisites

- OMC agents available (Task tool works)
- PubMed MCP server installed
- Agent definitions loaded from `agents/`

### Pipeline

```
verifier + scripts ─────────────┐
methodology-critic ─────────────┤
quality-reviewer (literature) ──┼──> orchestrator (merge) ──> final review report
quality-reviewer (statistics) ──┤
scientist (clinical sig.) ──────┘
```

**Phase 1 -- Automated Analysis**

1. Spawn `verifier` (sonnet): run all 3 Python scripts, parse results
   ```bash
   python3 scripts/validate_manuscript.py projects/<name>/manuscript.md --json
   python3 scripts/detect_ai_patterns.py projects/<name>/manuscript.md --json
   python3 scripts/format_references.py projects/<name>/manuscript.md --style vancouver
   ```

**Phase 2 -- Domain Reviews (parallel)**
Spawn 3-4 agents simultaneously, each reviewing a subset of domains:

| Agent                | Domains                 | Model  |
| -------------------- | ----------------------- | ------ |
| `methodology-critic` | Methodology + Reporting | opus   |
| `quality-reviewer`   | Statistics + Literature | sonnet |
| `scientist`          | Clinical Significance   | sonnet |

Each agent:

- Reads `projects/<name>/manuscript.md`
- Reads automated check results from Phase 1
- Produces a domain-specific review with Major/Minor/Optional findings
- Uses PubMed MCP for citation verification (Literature domain)

**Phase 3 -- Merge + Decision**

1. Orchestrator collects all domain reviews
2. Deduplicate overlapping findings
3. Assign final severity ratings (if agents disagree, use higher severity)
4. Compile into unified review report using Output Format from Tier 1
5. Determine overall decision:
   - Accept: 0 major issues, <= 3 minor issues
   - Minor Revision: 0 major issues, > 3 minor issues
   - Major Revision: 1-3 major issues
   - Reject: > 3 major issues or fundamental design flaws

**Phase 4 -- Revision Response (optional)**
If reviewing a revision:

1. Spawn `executor` (sonnet): generate point-by-point response letter
2. Spawn `verifier` (sonnet): verify all claimed changes were made
3. Compare before/after validation scores

### Team Composition

See `workflows/team-compositions.md` -- "Peer Review Team".

### Output

Project directory with: `review.md` (unified), domain-specific review files, automated check outputs, optionally `revision-response.md`.
