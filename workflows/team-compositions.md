# Agent Team Compositions

Workflow team definitions for Claude Code Agent Teams. Each composition defines roles, models, and coordination patterns.

## Availability

| Environment                  | Team Support   | Fallback                                  |
| ---------------------------- | -------------- | ----------------------------------------- |
| Claude Desktop (claude.ai)   | No             | Sequential workflow, manual quality gates |
| Claude Code (single session) | Subagents only | Delegate to subagents sequentially        |
| Claude Code + Agent Teams    | Full teams     | Parallel execution with shared task list  |

Enable Agent Teams: add `"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"` to settings.json env.

## Team: Grand Rounds Pipeline

**Purpose:** Parallel evidence-to-presentation
**Lead:** Orchestrator (sonnet)
**Teammates:**

- evidence-researcher (sonnet): PubMed search, GRADE rating
- slide-designer (sonnet): Template selection, content authoring, 5-script pipeline
- citation-validator (haiku): PMID verification in parallel

**Task Flow:**

1. Lead decomposes topic into search strategy
2. evidence-researcher produces evidence-synthesis.md
3. citation-validator verifies PMIDs in parallel
4. slide-designer receives verified synthesis, authors slides
5. Lead reviews final output

## Team: Manuscript Pipeline

**Purpose:** Parallel evidence-to-publication
**Lead:** Orchestrator (opus, delegate mode)
**Teammates:**

- evidence-researcher (sonnet): PubMed search and GRADE
- manuscript-drafter (opus): IMRAD stages 1-4
- peer-reviewer (opus): Self-review after draft
- text-naturalizer (sonnet): AI detection and humanization
- citation-validator (haiku): Continuous PMID verification

**Task Flow:**

1. evidence-researcher produces synthesis
2. manuscript-drafter runs IMRAD stages 1-4
3. peer-reviewer critiques draft
4. manuscript-drafter incorporates revisions
5. text-naturalizer runs 4-stage pipeline
6. citation-validator verifies throughout
7. Lead assembles submission package

## Team: Dual Output

**Purpose:** Same evidence base, two output tracks (max parallelism)
**Lead:** Orchestrator (opus, delegate mode)
**Teammates:**

- evidence-researcher (sonnet): Shared evidence synthesis
- slide-designer (sonnet): Presentation track
- manuscript-drafter (opus): Manuscript track
- citation-validator (haiku): Shared PMID verification

**Task Flow:**

1. evidence-researcher produces evidence-synthesis.md
2. FORK: slide-designer AND manuscript-drafter both receive synthesis
3. Parallel execution: slides and manuscript authored simultaneously
4. citation-validator runs against both outputs
5. Lead reconciles consistent evidence references

## Team: EGS Guideline Synthesis

**Purpose:** Multi-society guideline comparison
**Lead:** Orchestrator (sonnet)
**Teammates:**

- evidence-researcher (sonnet): Multi-society search (WSES, SAGES, AAST, EAST)
- methodology-critic (opus): Evidence quality assessment
- slide-designer (sonnet): Guideline comparison presentation

## Team: SCC Protocol Development

**Purpose:** Critical care evidence synthesis with protocol generation
**Lead:** Orchestrator (opus, delegate mode)
**Teammates:**

- evidence-researcher (sonnet): Guideline search (SCCM, SSC, ATS, EAST) + landmark trial identification
- methodology-critic (opus): Trial quality assessment
- manuscript-drafter (opus): Protocol document writing
- slide-designer (sonnet): Educational presentation authoring

**Task Flow:**

1. evidence-researcher searches guidelines and identifies landmark trials
2. methodology-critic evaluates landmark trials
3. Lead synthesizes into protocol framework
4. manuscript-drafter writes protocol document (SQUIRE if QI)
5. slide-designer authors educational presentation from protocol data

## Desktop Fallback

When Agent Teams are not available, run the same workflows sequentially:

1. Run evidence synthesis first (complete before proceeding)
2. Run citation verification on the synthesis
3. Author the presentation OR manuscript (one at a time)
4. Run quality checks (audit/validate scripts)
5. For dual output: complete presentation first, then manuscript

The quality gates and validation requirements are identical regardless of environment.
