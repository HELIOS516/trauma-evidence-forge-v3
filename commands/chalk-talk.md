---
name: chalk-talk
description: >
  Interactive chalk talk command: generates a structured, conversational teaching
  session on a surgical topic using the chalk-talk template. Optimized for
  resident education, bedside teaching, and informal conference sessions.
  Produces a narrative-driven, question-anchored teaching script — not slides.
---

# /asf:chalk-talk

Generate an interactive chalk talk teaching session on a surgical topic.

## Usage

```
/asf:chalk-talk {topic}
/asf:chalk-talk {topic} --audience {residents|students|attendings|nurses}
/asf:chalk-talk {topic} --duration {15|30|45|60}
/asf:chalk-talk {topic} --style {Socratic|didactic|case-based}
```

## What This Does

Produces a structured chalk talk using `templates/chalk-talk.md` as the formatting guide. A chalk talk is an informal teaching session — conversational, question-driven, drawn on a whiteboard or flip chart. This command generates:

1. **Opening hook** — A clinical case vignette or provocative question to engage learners
2. **Core concept map** — 3-5 key concepts with logical connections (what you would draw)
3. **Socratic question sequence** — Questions to ask the audience at each step, with expected answers
4. **Key teaching points** — The 3-5 facts you want every learner to leave knowing
5. **Drawing guide** — What to put on the board at each stage
6. **Clinical pearl** — One memorable fact that anchors the session
7. **Closing question** — Sends learners away with something to look up or think about

## Defaults

- Audience: senior residents (PGY-3 to PGY-5)
- Duration: 30 minutes
- Style: Socratic (question-driven)
- Domain: auto-detected from topic (trauma/EGS/SCC/global surgery)
- Evidence level: landmark trials cited, GRADE ratings included

## Examples

```
/asf:chalk-talk DVT prophylaxis in trauma
/asf:chalk-talk open abdomen management --audience residents --duration 45
/asf:chalk-talk PADIS sedation guidelines --style didactic --duration 20
/asf:chalk-talk Hinchey classification --audience students --duration 15
```

## Output Structure

The chalk talk output follows `templates/chalk-talk.md` and includes:

```
## Chalk Talk: {Topic}
**Audience:** {level} | **Duration:** {N} minutes | **Style:** {style}

### Opening Hook (2-3 min)
[Case vignette or provocative clinical question]

### Concept Map (draw as you teach)
[Text diagram of what to put on whiteboard]

### Teaching Sequence
#### Concept 1: {name}
- What to draw: [description]
- Ask audience: "[Question]"
- Expected answer: [answer]
- Teaching point: [fact]

[Repeat for each concept]

### Key Takeaways (last 2 min)
1. [Fact 1]
2. [Fact 2]
3. [Fact 3]

### Clinical Pearl
[Memorable one-liner]

### Closing Question
[Question to send them away with]

### References
[3-5 key papers with PMIDs]
```

## Related Commands

- `/asf:grand-rounds {topic}` — Full slide deck (Gamma pipeline)
- `/asf:journal-club {article}` — Structured article critique
- `/asf:mcq {topic}` — Multiple choice questions for the same topic
- `/asf:evidence-review {topic}` — Full GRADE-rated evidence synthesis
