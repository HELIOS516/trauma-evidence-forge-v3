# Shelf Exam Review Presentation Template

<!-- 36-48 slides | 55-60 minute rapid-fire review -->

## Gamma Submission Parameters

```json
{
  "format": "presentation",
  "textMode": "preserve",
  "themeId": "marine",
  "numCards": "<count --- separators + 1>",
  "cardSplit": "auto",
  "cardOptions": { "dimensions": "16x9" },
  "imageOptions": {
    "source": "aiGenerated",
    "model": "imagen-4-pro",
    "style": "ultra-detailed photorealistic medical photography, surgical suite and trauma bay realism, 50mm lens depth, high dynamic range, anatomical accuracy, no illustrations or cartoons"
  }
}
```

## How to Use This Template

**Purpose:** Comprehensive shelf exam review covering multiple domains in rapid-fire format. Designed for pre-exam review sessions, not grand rounds teaching.

**Differences from Long Format:**

- 36-48 slides across 6-10 clinical domains (vs 24-30 slides on one topic)
- Table-dominant: every domain opens with a classification/comparison table
- No recurring case thread: each MCQ is a standalone clinical vignette
- No trial PICO slides: trials referenced in speaker notes, not slide body
- No guideline comparison slides: classifications and thresholds instead
- 6 MCQ pairs testing shelf question PATTERNS (vs 3 MCQs testing clinical reasoning depth)
- Speaker notes include explicit `Shelf Tip` callouts

**V3 Rules Apply to Every Slide:**

1. Keyword-only body text (3-7 words per bullet, max 50 words/slide)
2. Assertion-evidence title on every slide (verb, not topic label)
3. `> **Bottom Line:** [max 12 words]` on every content/data slide
4. `**[KEY STAT: ...]**` on every content/data slide
5. `**Sources:** [N][M]` at bottom of content/data slides
6. Speaker notes in `<!-- Speaker Notes: ... -->` (150-250 words)
7. `<!-- type: TYPE -->` tag on every slide
8. `**Gamma instruction:**` line at top of every slide section
9. Marine theme locked. No full sentences in slide body.

**Speaker Notes — Shelf Tip Format:**

Speaker notes follow standard V3 format (150-250 words narrative) and include:
```
> **Shelf Tip:** [How the shelf tests this concept — question stem pattern, common distractors, or "most commonly tested fact"]
```

**MCQ Strategy:**

- 6 MCQ pairs, placed at the end of each major domain section
- Each MCQ tests a shelf question PATTERN (not just a clinical fact)
- MCQ answer speaker notes explain: "The shelf asks this by..."
- Bloom's progression: Application (MCQs 1-3) -> Analysis (MCQ 4) -> Application (MCQ 5) -> Evaluation (MCQ 6)
- Final MCQ is a multi-domain integration question

**Slide Type Distribution Target:**

- DATA_TABLE: 40-50% (the defining feature of this format)
- CONTENT: 25-35%
- MCQ + MCQ_ANSWER: ~25% (6 pairs = 12 slides)
- TITLE + LEARNING_OBJECTIVES + TAKE_HOME + REFERENCES: 4 slides

---

## TEMPLATE STRUCTURE — Copy and Adapt

### SLIDE 1: TITLE

**Gamma instruction: Full-bleed medical hero image, white title 48pt centered, presenter name 24pt below, no bullets**

## [TOPIC] Shelf Review: [Subtitle Framing the Scope]

Evan DeCan, MD
Division of Acute Care Surgery | University of Virginia
[Date]

---

### SLIDE 2: LEARNING_OBJECTIVES

**Gamma instruction: Solid dark bg, numbered list 24pt, no images, 6 items max**

## Learning Objectives

1. **[Bloom's verb]** [objective mapped to Domain 1, 5-8 words]
2. **[Bloom's verb]** [objective mapped to Domain 2, 5-8 words]
3. **[Bloom's verb]** [objective mapped to Domain 3, 5-8 words]
4. **[Bloom's verb]** [objective mapped to Domain 4, 5-8 words]
5. **[Bloom's verb]** [objective mapped to Domain 5, 5-8 words]
6. **[Bloom's verb]** [objective mapped to Domain 6, 5-8 words]

<!-- Speaker Notes:
Overview of the review session. This is a rapid-fire shelf exam review
covering [N] domains. Each domain opens with a classification or comparison
table — the highest-yield format for exam review. [N] MCQ checkpoints test
common shelf question patterns. Cross-reference the [FOUNDATIONAL DECK] for
topics already covered there. (~150 words)
-->

---

### DOMAIN SECTION PATTERN (repeat for each domain):

### SLIDE N: DATA_TABLE — Domain Classification/Comparison

**Gamma instruction: Table dominates 70%, key row highlighted accent, title = assertion, Bottom Line box**

## [Assertion: Key Classification or Comparison — Sentence With Distinguishing Feature]

| [Category] | [Type A] | [Type B] | [Type C] |
|------------|----------|----------|----------|
| [Feature 1] | [Value] | [Value] | [Value] |
| [Feature 2] | [Value] | **[Key value]** | [Value] |
| [Feature 3] | [Value] | [Value] | [Value] |
| **Management** | [Action] | **[Action]** | [Action] |

> **Bottom Line:** [Max 12 words — the discriminating feature for the exam]

**Sources:** [N][M]

<!-- Speaker Notes:
Walk through the table systematically. Highlight the key discriminating
feature that the shelf tests. Explain the clinical significance of each
row. Cross-reference [FOUNDATIONAL DECK] if relevant.

> **Shelf Tip:** [How the shelf tests this — "The stem will show you X
> and ask you to identify Y. The distractor is always Z."]

(~200 words)
-->

---

### SLIDE N+1: CONTENT — Domain Key Concept

**Gamma instruction: Dark bg, assertion title 28pt bold, 2-3 keyword bullets 20pt, ONE key stat 36pt accent, Bottom Line box**

## [Assertion: Key Clinical Concept — Sentence With Number or Threshold]

- [Keyword phrase 1, 3-7 words]
- [Keyword phrase 2, 3-7 words]
- **[KEY STAT: specific number, threshold, or mortality figure]**

> **Bottom Line:** [Max 12 words]

**Sources:** [N][M]

<!-- Speaker Notes:
Expand on the assertion. Connect to the classification table from the
previous slide. Include the clinical reasoning chain.

> **Shelf Tip:** [Pattern description — "If the stem says X, the
> answer is always Y. Common wrong answer is Z because..."]

(~200 words)
-->

---

### SLIDE N+2: MCQ — Domain Question

**Gamma instruction: Question 24pt, options A-D clean list, no answer shown, interactive feel, blue accent**

## [Domain] Decision Point

**[Brief clinical vignette, 2-3 sentences]. [Key finding]. [Question stem: "What is the most appropriate next step?" or "What is the most likely diagnosis?"]**

- A. [Plausible but incorrect — tests common misconception]
- B. [Correct answer]
- C. [Reasonable but suboptimal — tests incomplete knowledge]
- D. [Classic distractor — tests whether student recognizes the pattern]

<!-- Speaker Notes:
Pause. This tests [specific shelf pattern]. The key discriminating
feature is [X]. (~100 words)
-->

---

### SLIDE N+3: MCQ_ANSWER — Domain Answer

**Gamma instruction: Dark bg, correct answer highlighted in accent, brief explanation with evidence**

## Answer: B — [Brief Rationale in One Sentence]

- **Why B:** [Keyword rationale, 3-7 words]
- **Why not A:** [Keyword explanation, 3-7 words]
- **Why not C:** [Keyword explanation, 3-7 words]
- **Why not D:** [Keyword explanation, 3-7 words]

> **Bottom Line:** [Max 12 words — the shelf testing pattern]

**Sources:** [N][M]

<!-- Speaker Notes:
Reveal and explain. Connect to the classification/table from earlier
in this section. Explain the specific shelf testing pattern.

> **Shelf Tip:** [How to recognize this pattern on exam day — "When you
> see [vital sign pattern / CT finding / mechanism], think [diagnosis].
> The shelf always pairs X with Y."]

(~200 words)
-->

---

### CLOSING SLIDES:

### SLIDE N: DATA_TABLE — Rapid-Fire Shelf Pearls

**Gamma instruction: Table dominates 70%, 2-column format, compact text, dark bg**

## [N] Shelf Pearls: One Fact, One Question Pattern

| Pearl | How It's Tested |
|-------|----------------|
| [Fact 1] | [Question stem pattern] |
| [Fact 2] | [Question stem pattern] |
| ... | ... |

---

### SLIDE N+1: TAKE_HOME

**Gamma instruction: Large numbered list 28pt, bold key phrase per item, clean dark bg, 6 items max**

## Take-Home Points

1. **[Bold key phrase]** — [3-5 word expansion]
2. **[Bold key phrase]** — [3-5 word expansion]
3. **[Bold key phrase]** — [3-5 word expansion]
4. **[Bold key phrase]** — [3-5 word expansion]
5. **[Bold key phrase]** — [3-5 word expansion]
6. **[Bold key phrase]** — [3-5 word expansion]

<!-- Speaker Notes:
Six actionable takeaways, one per domain. Each maps to a learning
objective. These are the patterns that will earn you points on exam day.
(~150 words)
-->

---

### SLIDE N+2: REFERENCES

**Gamma instruction: 2-column small text 12pt, no images, dense but clean, dark bg**

## References

1. [Author et al. Title. Journal Year;Vol:Pages. PMID: XXXXXXXX]
2. [Continue for all citations]

---

## Quality Checklist

- [ ] All body text is keyword phrases (3-7 words per bullet, max 50 words/slide)
- [ ] No slide has full sentences in body (only in speaker notes)
- [ ] Every content/data slide has Bottom Line blockquote
- [ ] Every content/data slide has Speaker Notes (150-250 words)
- [ ] Every content/data slide has KEY STAT
- [ ] 6 MCQ pairs included (one per major domain section)
- [ ] All slides have assertion-evidence titles (not topic labels)
- [ ] Sources block on every content/data slide
- [ ] Speaker notes include Shelf Tip callouts
- [ ] DATA_TABLE slides comprise 40-50% of total
- [ ] Marine theme specified in Gamma params
- [ ] Final MCQ is a multi-domain integration question
- [ ] Shelf Pearls rapid-fire table included near end
