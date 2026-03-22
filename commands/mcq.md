---
name: mcq
description: >
  MCQ generation command: creates high-yield multiple choice questions and
  clinical case vignettes on surgical topics using the mcq-case-pairs template.
  Optimized for board review, resident education, and conference Q&A sessions.
  Produces ABS/ABSITE-style questions with detailed explanations.
---

# /asf:mcq

Generate multiple choice questions and clinical case vignettes on a surgical topic.

## Usage

```
/asf:mcq {topic}
/asf:mcq {topic} --count {N}
/asf:mcq {topic} --style {board|vignette|rapid-fire}
/asf:mcq {topic} --difficulty {intern|resident|fellow|attending}
/asf:mcq {topic} --focus {diagnosis|management|anatomy|physiology|complications}
```

## What This Does

Generates MCQs using `templates/mcq-case-pairs.md` as the formatting standard. Produces:

1. **Clinical vignettes** — Realistic case stems with patient demographics, vitals, labs, imaging
2. **4-5 answer choices** — One clearly correct, one common distractor, others plausible but wrong
3. **Correct answer with explanation** — Why the right answer is right
4. **Distractor explanations** — Why each wrong answer is wrong (highest educational value)
5. **Teaching point** — The underlying principle the question tests
6. **PMID/reference** — Evidence base for the correct answer

## Question Styles

| Style      | Description                              | Use case                                  |
| ---------- | ---------------------------------------- | ----------------------------------------- |
| board      | Single best answer, ABS/ABSITE format    | Board prep, written exam                  |
| vignette   | Extended case with multiple questions    | Teaching conferences, case-based learning |
| rapid-fire | Short stems, 4 choices, minimal vignette | Quick knowledge check, warm-up            |

## Defaults

- Count: 5 questions per run
- Style: board (ABS-style single best answer)
- Difficulty: resident (PGY-3/PGY-4 level, appropriate for ABSITE)
- Domain: auto-detected from topic
- Answers: revealed after all questions (exam mode) unless --show-answers specified

## Examples

```
/asf:mcq DVT prophylaxis in trauma --count 5
/asf:mcq acute cholecystitis management --style vignette --difficulty fellow
/asf:mcq PADIS sedation --count 10 --focus management
/asf:mcq damage control surgery --style rapid-fire --count 15
/asf:mcq bowel obstruction --difficulty intern --focus diagnosis
```

## Output Structure

Questions follow `templates/mcq-case-pairs.md`:

```
## Question {N}: {Topic Area}
**Difficulty:** {level} | **Domain:** {knowledge area} | **Style:** {board/vignette/rapid-fire}

### Stem
A {age}-year-old {sex} presents with {chief complaint}. Relevant history:
{PMH, vitals, exam, labs, imaging as appropriate}.

Which of the following is the most appropriate {next step/diagnosis/management}?

A. {option}
B. {option}
C. {option}
D. {option}
E. {option} [if 5-choice]

---
**Correct Answer: {letter}**

**Explanation:**
{Why the correct answer is correct — mechanism, guideline, evidence}

**Why other answers are wrong:**
- A: {explanation}
- B: {explanation}
- C: {explanation}
- D: {explanation}

**Teaching Point:**
{The single most important principle this question tests}

**Reference:** {Author et al. Journal Year; PMID:XXXXXXXX}
```

## Board Exam Alignment

Questions are calibrated to:

- **ABSITE** (American Board of Surgery In-Training Examination): PGY-1 through PGY-5 content
- **ABS Qualifying Examination** (written boards): attending-level clinical decision-making
- **ABS Certifying Examination** (oral boards): case-based management, complications
- **FACS** (Fellow of ACS): advanced trauma and surgical critical care content

## Integration with Other Commands

MCQs are automatically embedded every 7-10 slides in `/asf:grand-rounds` presentations. Use `/asf:mcq` to:

- Generate standalone question sets for board review sessions
- Create quiz content for resident teaching conferences
- Build question banks for simulation or flipped-classroom formats

## Related Commands

- `/asf:chalk-talk {topic}` — Teaching session on the same topic
- `/asf:grand-rounds {topic}` — Full slide deck with embedded MCQs
- `/asf:journal-club {article}` — Article critique with comprehension questions
- `/asf:evidence-review {topic}` — GRADE-rated evidence base for question content
