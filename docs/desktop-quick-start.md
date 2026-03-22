# Academic Surgery Forge -- Quick Start Guide

> A research workbench that helps you draft manuscripts, review papers, check for AI-detectable writing patterns, and design capacity assessments for global surgery research.

---

## What This Is

Academic Surgery Forge is a set of tools built into Claude that help you with academic surgical research. You can draft manuscripts in IMRAD format for journals like World Journal of Surgery, get structured peer review feedback, naturalize AI-assisted text so it reads like human-authored prose, and design capacity assessments using the Lancet Commission framework. It handles citation formatting, reporting checklists (CONSORT, STROBE, PRISMA), and statistical reporting standards automatically.

---

## Setup (3 Steps)

### Step 1: Enable the PubMed Connector

This lets Claude search PubMed for real citations instead of guessing.

1. Open **claude.ai** (or the Claude Desktop app)
2. Go to **Settings** (gear icon, bottom-left)
3. Click **Connectors**
4. Find **PubMed** and click **Connect**

No account or API key needed. It is free.

See `pubmed-setup.md` for detailed instructions and verification steps.

### Step 2: Add the Skill to Your Project

1. In Claude, open the conversation sidebar and create a **Project**
2. Name it something like "Surgery Research"
3. In the Project Knowledge section, upload the skill files (your admin will provide these)
4. The skill activates automatically when you mention keywords like "manuscript", "global surgery", "peer review", or "naturalize"

### Step 3: Start Chatting

Use natural language. The examples below show what you can ask.

---

## What You Can Say

### Draft a Manuscript

> "Help me draft a manuscript about surgical capacity in Zambia for World Journal of Surgery"

Claude will walk you through a 5-stage pipeline: outline, draft, validate, polish, and submission prep. It applies the correct reporting checklist and formats references in Vancouver style.

### Review a Paper

> "Review this manuscript for methodological issues"

Paste your manuscript text into the chat. Claude reviews it across 5 domains: methodology, statistics, reporting compliance, literature coverage, and clinical significance. Each issue is rated Major, Minor, or Optional.

### Check for AI Patterns

> "Check this text for AI-detectable patterns and fix them"

Paste your text. Claude scores it on a 0-100 scale across 8 categories (hedging, transitions, sentence uniformity, etc.). If the score is above 30, it rewrites sections to sound more natural while keeping all facts intact.

### Design a Capacity Assessment

> "Design a capacity assessment for Kenya using the Lancet Commission framework"

Claude generates a structured protocol covering all 6 Lancet Commission indicators, data collection instruments, and analysis plans. It fills in country context (WHO region, World Bank income classification, surgeon density).

### Systematic Review

> "Help me do a systematic review on task-shifting for emergency surgery in sub-Saharan Africa"

Claude structures the review using PRISMA guidelines (27-item checklist), helps define inclusion/exclusion criteria, and organizes evidence extraction.

### Cost-Effectiveness Analysis

> "Run a cost-effectiveness analysis for cataract surgery programs in rural India"

Claude sets up a CEA framework with cost inputs, effectiveness measures (DALYs averted), and sensitivity analysis structure. All cost data is tagged with currency, year, and PPP adjustment method.

---

## Tips

- **Verify citations**: Claude can look up real PubMed articles when the connector is enabled. Always ask it to "verify the PMIDs" before finalizing a manuscript. Fabricated citations are the most common AI error.
- **Citation format**: References use numbered `[1], [2], [3]` format in the text. Most target journals use Vancouver style. JAMA Surgery uses AMA style.
- **AI detection target**: Aim for a score below 30. Scores 0-30 are indistinguishable from human-authored surgical academic text.
- **Journal selection**: Tell Claude which journal you are targeting. It adjusts word limits, reference format, and abstract structure automatically. Supported journals: WJS, JSR, JTACS, Annals of Surgery, Surgery, JAMA Surgery, BJS.
- **Reporting checklists**: Claude auto-detects your study type (RCT, observational, systematic review, QI, case report) and applies the right checklist. You can also request a specific one.
- **Default author**: Manuscripts default to "Evan DeCan, MD" as author. Say "use [Name] as author" to change this.

---

## Troubleshooting

**"I pasted my manuscript but Claude did not run the review"**
Try being explicit: "Run a peer review on the following manuscript:" then paste the text. The skill activates on keywords like "review", "manuscript", "peer review".

**"The AI detection score is too high"**
Focus on the Discussion section first -- it has the highest variance. Replace phrases like "It is important to note that" with direct statements. Add field-specific abbreviations (ISS, GCS, MTP). Vary your sentence lengths.

**"Citations look made up"**
Enable the PubMed connector (Step 1 above). Then ask Claude to "verify all PMIDs in this manuscript." If a PMID does not exist, Claude will flag it and suggest a real replacement.

**"Word count is too high for my target journal"**
Tell Claude: "This is for [journal name], which has a [N]-word limit. Help me cut it down." It will prioritize trimming while preserving key findings.

**"I want to use a different reporting checklist"**
Say: "Apply the STROBE checklist to this manuscript" (or CONSORT, PRISMA, SQUIRE, CARE). Claude will switch checklists regardless of auto-detection.
