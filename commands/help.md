# /asf:help

Interactive guide to Academic Surgery Forge.

## Instructions

Present the welcome guide below, then use AskUserQuestion for interactive workflow selection. Adapt to the user's environment.

### Environment Detection

Detect your environment: if the Bash tool is available, you are in Claude Code. If not, you are in Claude Desktop. Adapt guidance accordingly throughout.

### Step 1: Present the Capability Summary

Display this overview to the user:

---

**Academic Surgery Forge** -- Full-Lifecycle Academic Surgery Workbench

**5 Modules | 11 Commands | 13 Scripts | 41+ Tests | 4 Clinical Domains**

**Clinical Domains**

| Domain                        | Societies                                  | Scoring Systems                                                                          |
| ----------------------------- | ------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **Trauma Surgery**            | EAST, WEST, ATLS, ACS-TQIP, AAST           | ISS, GCS, RTS, TRISS, AIS, AAST OIS, ABC Score, FAST                                     |
| **Emergency General Surgery** | WSES, SAGES, AAST, EAST, ASCRS, ACG        | Tokyo TG18, Alvarado, RIPASA, Hinchey, LRINEC, Atlanta/Ranson/BISAP, AAST EGS Grades I-V |
| **Surgical Critical Care**    | SCCM, SSC, ATS, ESICM, SIS, ASPEN          | APACHE, SOFA, qSOFA, CAM-ICU, RASS, CPOT, BPS, NUTRIC, Caprini                           |
| **Global Surgery**            | Lancet Commission, NSOAP, ZAMSAT, WHO-EESC | 6 Lancet Indicators, Bellwether Procedures                                               |

**What ASF Can Do**

- **Evidence & Research** -- PubMed search with domain-specific strategies (6-category structured search), GRADE-rated evidence synthesis (1A through 4), PMID/DOI verification (fabrication detection), guideline comparison matrices across societies, statistical reporting (95% CI, NNT, ARR, exact p-values)
- **Presentations** -- Grand rounds (30+ slides, assertion-evidence format), journal club (9-section critique), chalk talk (interactive teaching), 5-script Gamma.app pipeline, MCQ integration, case-based learning, image generation (imagen-4-pro)
- **Manuscripts** -- IMRAD pipeline (outline, draft, validate, polish, submit-prep), journal-specific profiles (JTACS, Annals, JAMA Surgery, WJS, BJS, CCM, JACS), reporting checklists (CONSORT, STROBE, PRISMA, SQUIRE, CARE), cover letter and submission package
- **Review & Quality** -- 5-domain peer review (methodology, statistics, reporting, literature, clinical), AI text detection and naturalization (4-stage pipeline, gate: score <30), citation validation, manuscript validation (16 checks)
- **Global Surgery Research** -- Lancet Commission capacity assessments, NSOAP gap analyses, cross-sectional facility surveys, cost-effectiveness protocol design
- **Cross-Module Workflows** -- Dual output (same evidence base producing slides AND manuscript), conference-to-publication pipeline, EGS guideline grand rounds, SCC protocol development

**Your Environment**

- **Claude Desktop**: Conversational workflows with manual quality gates. See `docs/desktop-quick-start.md` and `docs/script-equivalents.md` for guided walkthroughs.
- **Claude Code (CLI)**: Full script automation, 8 specialized agents, Git integration. See `CLAUDE.md` for agents, team compositions, and model selection strategy.
- **Claude Code + Agent Teams**: Parallel agent orchestration for maximum throughput. Use `/team` with pre-defined compositions from `CLAUDE.md`.

---

### Step 2: Ask What the User Wants to Do

Use AskUserQuestion with one question and 4 options:

**Question:** "What would you like to work on?"

**Options:**

1. **Synthesize Evidence** -- "PubMed search, GRADE rating, guideline comparison, or global surgery research across trauma, EGS, SCC, or global surgery domains"
2. **Create a Presentation** -- "Grand rounds, journal club, chalk talk, or guideline comparison slides via Gamma.app pipeline"
3. **Write a Manuscript** -- "Original research, systematic review, or QI paper with 5-stage IMRAD pipeline and journal-specific formatting"
4. **Review or Improve Work** -- "Peer review, citation validation, AI text naturalization, or dual output from existing evidence"

### Step 3: Present Specific Workflow Options

Based on the user's choice, use a second AskUserQuestion with specific commands.

**If user chose "Synthesize Evidence":**

Question: "What type of evidence work?"
Options:

1. **Trauma/General Evidence Review** -- "Domain-aware PubMed search with GRADE synthesis. Pick any topic for a broad literature review. Command: `/asf:evidence-review {topic}`"
2. **EGS Guideline Comparison** -- "Multi-society guideline synthesis (WSES, SAGES, AAST, EAST) with severity grading. Command: `/asf:egs-guidelines {condition}`"
3. **Critical Care Protocol** -- "SCC evidence synthesis (SCCM, SSC, ATS) with protocol tables and landmark trial comparison. Command: `/asf:critical-care-protocol {topic}`"
4. **Global Surgery Research** -- "Lancet Commission indicators, NSOAP gap analysis, surgical capacity assessment and research protocol design. Command: `/asf:capacity-assessment {country/region}`"

**If user chose "Create a Presentation":**

Question: "What type of presentation?"
Options:

1. **Grand Rounds** -- "Full evidence-to-slides pipeline with 5-script Gamma automation. 30+ slides, assertion-evidence format. Command: `/asf:grand-rounds {topic}`"
2. **Journal Club** -- "9-section single-article structured critique as presentation slides. Command: `/asf:journal-club {article}`"
3. **Critical Care Education** -- "ICU/nursing education slides with protocol tables and guideline synthesis. Command: `/asf:critical-care-protocol {topic}`"

**If user chose "Write a Manuscript":**

Question: "What type of manuscript work?"
Options:

1. **Draft Paper** -- "5-stage IMRAD pipeline with journal-specific profiles (JTACS, Annals, JAMA Surgery, etc.). Command: `/asf:draft-paper {topic}`"
2. **Dual Output** -- "Same evidence base produces both slides AND manuscript in parallel. Command: `/asf:dual-output {topic}`"
3. **Pre-Submission Review** -- "5-domain peer review before journal submission. Command: `/asf:peer-review {file}`"

**If user chose "Review or Improve Work":**

Question: "What type of review?"
Options:

1. **Peer Review** -- "5-domain structured critique (methodology, statistics, reporting, literature, clinical) with severity ratings. Command: `/asf:peer-review {file}`"
2. **Naturalize Text** -- "AI detection and humanization. 4-stage pipeline: detect, diagnose, rewrite, verify. Gate: score <30. Command: `/asf:naturalize {text}`"
3. **Dual Output** -- "Fork existing evidence into both presentation and manuscript formats. Command: `/asf:dual-output {topic}`"

### Step 4: Launch the Selected Workflow

After the user selects a specific command, ask for the topic or input argument (e.g., "What topic would you like to synthesize evidence on?").

Then adapt to environment:

- **Claude Code**: Execute the chosen `/asf:*` command directly. Scripts run automatically, agents are available for delegation.
- **Claude Desktop**: Walk the user through the workflow conversationally. Reference `docs/script-equivalents.md` for manual quality gates. Perform the same evidence synthesis and content authoring but without script automation -- do quality checks inline instead of via Python scripts.

### Quick Reference (for power users)

If the user already knows what they want, display this table:

| I need to...           | Command                               | What happens                                  |
| ---------------------- | ------------------------------------- | --------------------------------------------- |
| Get oriented           | `/asf:help`                           | This guide                                    |
| Synthesize evidence    | `/asf:evidence-review {topic}`        | Domain-aware PubMed search with GRADE ratings |
| Compare EGS guidelines | `/asf:egs-guidelines {condition}`     | WSES/SAGES/AAST guideline synthesis           |
| Develop ICU protocol   | `/asf:critical-care-protocol {topic}` | SCCM/SSC/PADIS guideline synthesis            |
| Design capacity study  | `/asf:capacity-assessment {country}`  | Lancet Commission/NSOAP research protocol     |
| Make a presentation    | `/asf:grand-rounds {topic}`           | Evidence synthesis then Gamma pipeline        |
| Run journal club       | `/asf:journal-club {article}`         | 9-section structured critique                 |
| Write a paper          | `/asf:draft-paper {topic}`            | Evidence synthesis then IMRAD pipeline        |
| Do both slides + paper | `/asf:dual-output {topic}`            | Single evidence base, forked to both          |
| Review a manuscript    | `/asf:peer-review {file}`             | 5-domain structured critique                  |
| Fix AI-sounding text   | `/asf:naturalize {text}`              | 4-stage AI detection and humanization         |
