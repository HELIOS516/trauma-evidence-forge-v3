# Slide Design Principles — Medical Presentation Design Reference

> Evidence-based design principles for medical education presentations. Focused on clinical case presentations, grand rounds, journal clubs, and evidence-based lectures.

---

## Optimal Medical Slide Design

### One Message Per Slide

- Each slide communicates exactly ONE key concept, finding, or recommendation
- If a slide has two distinct points, split it into two slides
- The audience should grasp the take-home message in under 5 seconds
- Test: cover the body text — can someone understand the slide from the title alone?

### Text Density Rules

- **Maximum 20 projected words per minute** of presentation time (NIH guideline)
- **≤7 lines of text** per slide (excluding tables and data elements)
- **≤7 words per bullet** — use keywords and phrases, not sentences
- Detailed narrative belongs in speaker notes, not on the slide
- Exception: dosing tables, algorithms, and data-dense reference slides (see Clinical Adaptations)

### High Contrast and Readability

- **Dark backgrounds with light text** reduce screen glare and keep the presenter as the visual focal point
- Minimum **18pt font** for all primary text; **24pt+ recommended** for projected slides
- **Maximum 4 colors** per slide — excessive color reduces readability
- Test color combinations for colorblind accessibility (avoid red-green encoding alone)
- Sans-serif fonts (Arial, Calibri, Helvetica) for body text; consistent font throughout

### Visual-First Approach

- Prefer **figures, images, and data visualizations** over text whenever possible
- One powerful image > three mediocre ones
- Full-bleed images with minimal text overlay for emotional/clinical impact moments
- Every image must serve the learning objective — decorative images add cognitive noise
- Prefer reproduced figures from source articles (with attribution) over AI-generated images

### Slide Pacing

- Target approximately **1 slide per minute** of presentation time
- Insert interactive checkpoints (MCQs, case questions) every **7-10 minutes** to reset attention
- A 30-minute talk = ~25-30 slides (including title, disclosures, LOs, MCQs, references)

---

## CRAP Design Principles

### Contrast

- Use size, color, and font weight to create clear visual hierarchy
- The most important element should be the most visually prominent
- Headlines vs body text: minimum **1.5x size difference**
- Use one accent color for key findings — highlight the p-value, the NNT, the confidence interval
- Never let two elements be "almost the same" — make differences obvious
- **Medical application:** Use color contrast to draw attention to statistically significant results, contraindications, or critical dosing information

### Repetition

- Consistent visual patterns build trust and reduce cognitive load
- Same color = same category across ALL slides in the presentation
- Same layout structure for similar content types (all trial slides look alike, all case slides look alike)
- Repeating elements: header style, citation format, color coding, Bottom Line box formatting
- Consistency signals professionalism and reliability in clinical settings
- **Medical application:** Evidence level color coding (e.g., green = Level 1A, yellow = Level 2, red = expert opinion) should be consistent throughout

### Alignment

- Everything on the slide should connect to something else visually
- Left-align body text (never center long passages)
- Align charts and tables to a consistent grid
- Invisible lines of alignment create order from chaos
- Misaligned elements feel "off" even when viewers can't articulate why
- **Medical application:** Align comparison tables so columns line up exactly; align forest plot elements to the line of no effect

### Proximity

- Related items grouped together, unrelated items separated
- Citations near the claims they support
- Legend near the chart it describes
- Group related bullet points; use spacing to separate topic clusters
- Proximity implies relationship — be intentional
- **Medical application:** Place the "Bottom Line" callout directly adjacent to the supporting data, not at the bottom as an afterthought

---

## Cognitive Load Theory (Sweller, Paivio)

### Three Types of Cognitive Load

**Intrinsic Load** — The inherent complexity of the content itself

- Pharmacokinetics of enoxaparin is inherently complex
- Cannot be reduced, but can be managed through sequencing
- Build from simple to complex; scaffold understanding

**Extraneous Load** — Cognitive burden from poor design

- Cluttered slides, inconsistent formatting, buried key points
- This is the load you CAN and MUST eliminate
- Every design decision should minimize extraneous load
- **Common offenders:** decorative backgrounds, logos on every slide, animation effects, dense prose paragraphs

**Germane Load** — Effort directed toward understanding

- This is the good kind — the thinking that leads to learning
- Encourage through questions, comparisons, clinical applications
- Case-based slides generate germane load

### Dual Coding Theory (Paivio)

- Information encoded both verbally AND visually is retained better
- Pair text with relevant visuals for key concepts
- A dosing table + a visual timeline > either alone
- Do NOT use visuals that merely decorate — they must encode information
- **Medical application:** Pair a Kaplan-Meier curve with a text summary of the HR/CI; pair an anatomical diagram with the clinical finding

### Chunking Rules

- **7 ± 2 rule:** Maximum 7 items per cognitive chunk
- Group related items into meaningful clusters
- Use headers and spacing to delineate chunks on each slide
- A 15-item list should become 3-4 grouped categories
- **Medical application:** Group dosing recommendations by indication rather than listing all doses in one block

### The 7x7 Rule for Slides

- Maximum 7 bullet points per slide
- Maximum 7 words per bullet point
- If you exceed this, split the slide or simplify the language
- Exception: data tables, dosing protocols, and clinical algorithms (see Clinical Adaptations below)

---

## Medical Education Specific (Bloom, ADDIE)

### Learning Objectives Drive Content

- Every slide should map to a stated learning objective
- Objectives use Bloom's taxonomy verbs: identify, compare, apply, evaluate
- If a slide doesn't serve an objective, question its inclusion
- State objectives early; reference them in the summary
- **LO tagging:** During authoring, tag slides with `LO1:`, `LO2:` etc. (stripped by preprocessor before Gamma submission)

### Case-Based vs Didactic

- Case-based learning produces better retention than pure didactic
- Open with a clinical scenario that creates a knowledge gap
- Return to the case throughout to apply new evidence
- Close the case with the evidence-based decision
- **Structure:** Case → Evidence → Application → Next Decision Point → More Evidence → Resolution

### Assertion-Evidence Slide Format

- **Title = Claim** (an assertion, not a topic label)
  - Bad: "DVT Prophylaxis Timing"
  - Good: "Early Prophylaxis (<48h) Reduces VTE by 40%"
- **Body = Supporting evidence** for the title's claim
  - Data, figures, study results that prove the assertion
  - The audience should be able to understand the key point from the title alone
- **Research basis:** Assertion-evidence format improves audience recall of key messages vs. topic-label format (Garner & Alley, 2013; Alley et al., 2006)

### Active Learning Checkpoints

- Insert interactive elements every 7-10 minutes
- Polling questions, case-based MCQs, think-pair-share prompts
- These reset attention and consolidate learning
- Even rhetorical questions ("What would you do here?") help
- **Placement:** After every 8-12 content slides, insert an MCQ or case question

### Spaced Repetition

- Revisit key concepts across multiple slides, not just once
- Summary slides that reference earlier evidence
- The "key takeaways" slide should echo the learning objectives
- Repetition across contexts (didactic, case, summary) deepens encoding

---

## Clinical Presentation Adaptations

### When Data Density is Acceptable

Unlike general presentations, medical slides may require high information density for:

- **Dosing tables:** Exact doses, routes, frequencies, contraindications
- **Comparison matrices:** Drug A vs Drug B vs Drug C across multiple parameters
- **Clinical algorithms:** Decision trees with multiple branch points
- **Guideline summaries:** Multi-society recommendation comparisons
- **Trial result tables:** PICO breakdown, primary/secondary outcomes, NNT/NNH

The 7x7 rule relaxes for these content types. Readability trumps minimalism for reference-quality slides.

### Annotation is Mandatory

- Every data table or figure needs annotation
- Use arrows pointing to key findings
- Highlight the row/column that matters most
- Add a **"Bottom Line"** or **"THE POINT"** callout box
- Never present raw data without interpretation
- **Rule:** Every slide with data MUST have a `> **Bottom Line:** ...` blockquote

### Structured Case Presentation Layout

Medical case presentations should follow a consistent structure:

- **Case slide:** Split layout — clinical scene/image on left, patient details on right
- **Include:** Age, sex, mechanism/chief complaint, vitals, key initial findings
- **Avoid:** Narrative paragraphs — use structured fields (Age/Sex, CC, HPI key points, PMH, Meds)
- **Return to case:** Each time the case advances, reference new data/decision points
- **Resolution:** Final slide ties the case to the evidence-based recommendation

### Clinical Images and Figures

- Prefer figures and images from source articles over AI-generated images
- Reproduce key figures with proper attribution
- If using AI images, ensure medical accuracy (anatomy, equipment, settings)
- Label all clinical images with relevant findings
- **Attribution format:** "Adapted from [Author], [Journal], [Year]" below the figure

### The "So What?" Rule

- Every data slide MUST have a "So What?" or "Bottom Line" element
- After presenting the evidence, state what it means for practice
- This can be a callout box, a bold footer line, or a highlighted conclusion
- The audience should never have to guess the clinical implication
- **Format:** `> **Bottom Line:** [1-2 sentence clinical implication]`

### Data Visualization for Clinical Data

- **Forest plots** for meta-analyses (horizontal, with pooled estimate highlighted)
- **Kaplan-Meier curves** for survival/event-free data
- **Bar charts** for categorical comparisons
- **Avoid pie charts** (poor for comparing similar proportions)
- Always include confidence intervals visually
- Annotate statistical significance directly on the visualization
- **Color coding:** Use consistent colors for intervention vs control throughout all figures

### Slide Type Templates

| Slide Type           | Layout                                    | Key Elements                                      |
| -------------------- | ----------------------------------------- | ------------------------------------------------- |
| Title                | Full-bleed hero image, white text overlay | Topic, presenter name, date, institution          |
| Disclosures          | Clean minimal, solid dark background      | Financial disclosures, no imagery                 |
| Learning Objectives  | Numbered list, solid background           | 3-5 Bloom's taxonomy verb objectives              |
| Case                 | Split layout — image left, details right  | Age/sex, CC, key findings, vitals                 |
| Content/Evidence     | Assertion title + supporting body         | Data, citations, Bottom Line box                  |
| Data/Table           | Table-dominant, minimal prose             | Annotated table, highlighted key row, Bottom Line |
| Trial Results        | PICO summary + outcomes table             | Key outcome highlighted, NNT/NNH, Bottom Line     |
| Guideline Comparison | Full-width comparison table               | Multi-society recommendations side by side        |
| MCQ/Knowledge Check  | Question + A-D options, clean layout      | Reveal answer with evidence rationale             |
| Take-Home            | Large numbered list, bold key phrases     | 3-5 actionable clinical recommendations           |
| Q&A                  | Professional closing                      | Summary metrics, presenter contact                |
| References           | Small text, no images, clean list         | Vancouver format, PMIDs at end of each line       |
