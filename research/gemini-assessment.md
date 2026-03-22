# Gemini 2.5 Pro Assessment: trauma-evidence-forge-v3

**Model:** gemini-2.5-pro via Vertex AI (with thinking)
**Date:** 2026-03-22

---

As an expert software architect, I have completed a thorough review of the `trauma-evidence-forge-v3` skill. The system demonstrates a high degree of maturity, a sophisticated design philosophy, and a robust implementation strategy.

Here is my detailed assessment:

---

## Scores (1-10)

*   **Architecture Quality:** 9/10. The system employs a well-defined pipeline architecture with excellent separation of concerns (content, configuration, scripts, templates). The use of subagents (`CLAUDE.md`) and a shared utility library (`card_utils.py`) demonstrates mature design patterns.
*   **Gamma Optimization Effectiveness:** 10/10. This is the system's most impressive feature. The combination of `gamma-medical-profile.json` with its `slideTypeDirectives` and `typeImageStyles` (including `NO_IMAGE` rules) is a masterclass in prompt engineering for a specific output target. It minimizes ambiguity and dramatically reduces the need for post-generation editing.
*   **Template Design Quality:** 9/10. The `presentation-medium.md` and `presentation-compact.md` templates are exceptionally well-designed. They are not just skeletons but prescriptive guides that enforce the core design philosophy (keyword slides, narrative notes, key stats) and include embedded Gamma instructions, ensuring consistency.
*   **Research Archive Completeness:** 9/10. The `shelf-exam-content-analysis.md` file is a significant asset. It provides a strong, evidence-based rationale for the topic selection, grounding the educational product in real-world high-stakes exam requirements. This elevates the project from a simple tool to a targeted educational system.
*   **Topic Selection Appropriateness:** 9/10. Directly derived from the research in `shelf-exam-content-analysis.md`, the 10 topics are high-yield and perfectly aligned with the target audience (medical students on a surgery rotation). The estimated coverage of 40-50% of the shelf exam is a compelling value proposition.
*   **Script Modification Quality:** 8/10. The Python scripts are well-structured and serve a critical quality assurance function. The `audit_slide_design.py` script is essential for enforcing design rules automatically. The abstraction of common logic into `card_utils.py` is a good practice. The score is not a 10 due to the brittleness of the heuristic-based `classify_card` function (see Weaknesses).
*   **Test Coverage Adequacy:** 5/10. The `CLAUDE.md` file mentions a `pytest evals/` command, which implies a testing framework exists. However, without seeing the test files, I cannot assess their quality or coverage. The complex logic in `card_utils.py`, particularly `classify_card`, is not something that should be trusted without extensive unit tests. The audit script acts as a form of integration testing, but it's not a substitute for unit-level validation.
*   **Overall Readiness for Production Use:** 9/10. The system is very close to being production-ready. The architecture is robust, the workflow is clear, and the output is highly optimized. The few identified weaknesses are addressable and do not fundamentally undermine the core value.

## Top 5 Strengths

1.  **Hyper-Specific Output Optimization:** The `gamma-medical-profile.json` is the system's crown jewel. By defining explicit layout and image generation instructions for each slide type (e.g., `Case`, `Trial`, `Disclosures`), it transforms Gamma from a creative partner into a deterministic layout engine. This is the primary driver for achieving the sub-15-minute editing target.
2.  **Automated Design Governance:** The `audit_slide_design.py` script acts as an automated "design linter." By programmatically enforcing rules like word count, bullet limits, and the presence of a "Bottom Line," the system guarantees a high degree of consistency and adherence to its pedagogical philosophy, independent of the author.
3.  **Pedagogically Sound Architecture:** The "Keyword Slides, Narrative Notes" philosophy is a modern and effective approach to medical presentations. The entire system, from the templates to the audit scripts, is built to enforce this principle, ensuring the presenter, not the slide, is the focus.
4.  **Evidence-Based Content Strategy:** The inclusion of `shelf-exam-content-analysis.md` demonstrates a commitment to educational effectiveness. Content is not chosen arbitrarily but is strategically mapped to high-yield topics for the NBME Surgery Shelf Exam, providing clear value to the target user (medical students).
5.  **Sophisticated AI Agent Delegation:** The `CLAUDE.md` configuration shows an advanced understanding of AI workforce management. Assigning different models (Opus, Sonnet, Haiku) to tasks based on their complexity and cost is highly efficient. Defining explicit "Team" pipelines (e.g., `Grand Rounds Pipeline`) ensures repeatable and predictable results.

## Top 5 Weaknesses or Gaps

1.  **Brittle Heuristic-Based Slide Classification:** The `classify_card` function in `card_utils.py` uses regular expressions and keyword searching to determine a slide's type. This is fragile and prone to error. For example, a content slide that happens to mention "a 45-year-old man" in its notes could be misclassified as a "Case" slide, leading to incorrect audit checks and Gamma directives.
2.  **Manual Bottleneck in Core Workflow:** As noted in `SKILL.md`, phases 1-4 (Evidence Gathering, Grading, Synthesis, and Slide Authoring) are "Manual." While AI-assisted, this remains a significant chokepoint that introduces variability and is labor-intensive. The system excels at validating and formatting, but the initial creation process is not fully systematized.
3.  **Lack of Visible Unit Testing:** While `pytest` is mentioned, no unit test files are provided in the manifest. The logic within `card_utils.py` is sufficiently complex (e.g., parsing, counting, classifying) that it absolutely requires a dedicated suite of unit tests to prevent regressions and validate edge cases.
4.  **Inflexible Theme Configuration:** The "Marine theme locked for all presentations" (`SKILL.md`) ensures consistency but sacrifices flexibility. A user might want to present on pediatric trauma with a slightly less severe theme, or align the presentation with their institution's branding. This hardcoded constraint limits adaptability.
5.  **Minor Documentation Drift:** There is a discrepancy between `SKILL.md`, which states v3 has "13 (D1-D13)" audit checks, and the docstring of the provided `audit_slide_design.py`, which mentions "8 design checks." While the file is truncated, this points to a potential for documentation to fall out of sync with the implementation.

## Specific Recommendations for Improvement

1.  **Implement Declarative Slide Typing:** Replace the heuristic-based `classify_card` function. The best practice would be to use YAML frontmatter at the top of each slide in the markdown.
    *   **Before (Heuristic):** `## [Patient demographic]: [Chief complaint]`
    *   **After (Declarative):**
        ```markdown
        ---
        type: Case
        ---
        ## [Patient demographic]: [Chief complaint]
        ```
    This would make classification 100% reliable and simplify the `card_utils.py` logic immensely.

2.  **Develop AI-Powered Authoring Assistants:** To address the manual bottleneck in Phase 4, create a dedicated subagent or script that takes an `evidence-synthesis.md` file and a template (e.g., `presentation-medium.md`) and generates a first-draft `presentation.md`. This draft would still require human review but would accelerate the most time-consuming manual step.

3.  **Build and Include a Unit Test Suite:** Create a `tests/` directory with `test_card_utils.py`. This file should include specific tests for the `classify_card` function with tricky examples, as well as tests for word counting and other parsing logic to ensure they handle edge cases correctly.

4.  **Make Theme Configurable:** In `gamma-medical-profile.json`, the `themeId` should be a parameter that can be overridden, not a hardcoded value. The `generate_gamma_params.py` script could accept a `--theme` argument, with "marine" as the default if not provided.

5.  **Synchronize Documentation:** Perform a full audit of all documentation (`SKILL.md`, script docstrings, `README.md` files) to ensure that numbers, feature lists, and workflow descriptions are consistent with the latest implementation.

## Bugs, Errors, or Issues Found

1.  **Latent Misclassification Bug:** The `classify_card` function in `card_utils.py` represents a significant latent bug. Its reliance on keyword heuristics (e.g., `re.search(r'\d+[\s-]*(year|yo|y/?o|month)', lower)`) is not robust. A content slide discussing epidemiological data for a specific age group could easily be misclassified as a "Case" slide, causing it to be subjected to the wrong validation rules and sent to Gamma with the wrong layout directive.
2.  **Documentation Discrepancy:** As noted, `SKILL.md` claims 13 audit checks for v3, while the `audit_slide_design.py` docstring mentions 8. This is a clear documentation error that needs correction.
3.  **Potential Regex Over-matching:** The regex for identifying an MCQ slide (`re.search(r'\n\s*(\*\*)?[A-D][\.\)]', text)`) is broad. If a content slide included a list formatted as "A. [text] B. [text]", it could be misclassified as an MCQ. The check should be more specific, requiring a "question" or "mcq" keyword in the header as well, which the code does attempt to do, but the logic could still be fragile.

## Assessment: Can the <15 min post-Gamma editing target be achieved?

**Yes, absolutely.** The system is exceptionally well-architected to achieve this specific goal. The likelihood of success is very high for the following reasons:

1.  **Directive-Driven Layout:** The `slideTypeDirectives` in `gamma-medical-profile.json` are the most critical factor. By telling Gamma *exactly* how to lay out each type of slide ("Split layout: clinical scene imagery left, structured case text right"), the system preempts the most common and time-consuming manual edits: reformatting cards, changing layouts, and adjusting text hierarchy.
2.  **Controlled Image Generation:** The combination of a highly specific default image prompt and the `typeImageStyles` (especially the `NO_IMAGE` directive for slides like "Disclosures" and "References") prevents Gamma from adding irrelevant or distracting visuals that the user would have to manually find and delete.
3.  **Preservation of Content:** The use of `textMode: "preserve"` and `safetyConstraints` ensures that the carefully authored keyword-based content, tables, and citations are not altered by Gamma's generative text models. The editing process is therefore focused on visual polish, not content correction.

The `<15 min` of editing will likely be spent on fine-tuning, such as swapping an AI-generated image for a more specific one, adjusting a minor line break, or confirming the visual flow, rather than wholesale reconstruction of slides. The system intelligently front-loads the effort into the structured markdown creation, making the final step in Gamma a quick validation and polish phase.