# Medical Grand Rounds Presentation Template - LONG FORMAT

<!-- 30-40 slides | 45-60 minute presentation -->

## Gamma Submission Parameters

```json
{
  "format": "presentation",
  "textMode": "preserve",
  "numCards": "<count --- separators + 1>",
  "cardOptions": { "dimensions": "16x9" },
  "imageOptions": {
    "source": "aiGenerated",
    "model": "imagen-4-pro",
    "style": "photorealistic medical photography, clinical emergency medicine"
  }
}
```

## How to Use This Template

**Purpose:** Comprehensive medical grand rounds presentation for 45-60 minute slots with deep evidence review.

**Differences from Medium Format:**

- 3x longer (35 vs 12 slides)
- Multiple MCQ/case scenarios interspersed throughout (not just at end)
- Detailed evidence review with multi-society guideline comparison
- GRADE evidence quality assessment
- Dedicated controversial topics section
- Emerging evidence/future directions section
- Progressive complexity building

**Instructions:**

1. Replace ALL `[PLACEHOLDER]` text with topic-specific content
2. Each slide has speaker notes — expand these for your actual talk
3. Learning Objective tags `[LO: 1,2]` track which objectives each slide addresses
4. Bottom Line boxes are mandatory — distill each slide to one key message
5. Use tables for data comparison (not prose lists)
6. MCQs should be answerable using only content presented up to that point
7. Keep one key message per slide (avoid text walls)
8. Progressive disclosure: simple → complex throughout presentation
9. `[LO: N]` tags are for authoring reference only — strip before Gamma submission (move to speaker notes or remove). The preprocessor does NOT auto-strip these.

**Common Topics This Works For:**

- Disease state deep dives (sepsis, HF, AKI, etc.)
- Guideline updates with evidence review
- Controversial management topics
- Emerging therapies with literature review

---

### SLIDE 1: TITLE

**Gamma instruction: Full-bleed hero image, centered white text overlay with presenter name**

## [TOPIC]: An Evidence-Based Approach

<!-- TITLE SLIDE -->

**Evan DeCan, MD**
[Department/Division]
[Institution]
[Date]

<!-- Speaker Notes:
- Introduce yourself and credentials
- Preview that this will be an evidence-heavy presentation
- Set tone: critical appraisal, not just guideline review
-->

---

### SLIDE 2: DISCLOSURES

**Gamma instruction: Clean minimal layout, solid dark blue background, no imagery, white text**

## Disclosures

**Financial Disclosures:**

- [List relevant financial relationships or state "None"]

**Non-Financial Disclosures:**

- [List guideline committees, society leadership, or state "None"]

**Off-Label Discussions:**

- This presentation includes discussion of [medication/device] for [indication], which is not FDA-approved for this use

> **Bottom Line:** Transparency in potential conflicts ensures objective evidence interpretation.

<!-- Speaker Notes:
- Required for CME accreditation
- Be specific about relationships that could influence content
- If discussing off-label use, state this explicitly upfront
-->

---

### SLIDE 3: LEARNING_OBJECTIVES

**Gamma instruction: Clean minimal layout, numbered list, dark background**

## Learning Objectives

By the end of this presentation, participants will be able to:

1. **[Objective 1 - Clinical Assessment]**: [Describe/Apply/Analyze] [specific skill related to diagnosis/assessment]

2. **[Objective 2 - Evidence Synthesis]**: [Compare/Evaluate] [specific guidelines or studies] for [clinical scenario]

3. **[Objective 3 - Management]**: [Implement/Justify] [therapeutic approach] based on current evidence

4. **[Objective 4 - Risk Stratification]**: [Calculate/Interpret] [specific tool/score] to guide [decision]

5. **[Objective 5 - Emerging Evidence]**: [Identify/Discuss] [recent trial/guideline] implications for practice

6. **[Objective 6 - Controversial Areas]**: [Analyze/Defend] management approach when evidence is conflicting

> **Bottom Line:** These objectives will be explicitly tagged throughout the presentation to track mastery.

<!-- Speaker Notes:
- Use Bloom's taxonomy action verbs (analyze, evaluate, create > remember, understand)
- Make objectives measurable and specific
- Reference objectives throughout: "This addresses LO #3..."
- MCQs should map to at least one objective
-->

---

### SLIDE 4: OPENING_CASE

**Gamma instruction: Split layout - clinical scene on left, patient details on right**

<!-- DENSITY: Body max 150w. Bullets max 8. Include only clinically relevant details. -->

## Case Presentation: [Patient Initials]

**Chief Complaint:** [Dramatic, relatable presenting symptom]

**History of Present Illness:**

- [Age]-year-old [gender] with [relevant PMH]
- Presented with [symptom timeline]
- [Key positive/negative history elements]

**Vital Signs:**

- BP [value], HR [value], RR [value], Temp [value], SpO2 [value]

**Key Physical Exam Findings:**

- [Relevant positive findings]
- [Relevant negative findings]

**Initial Labs/Imaging:**

- [Critical values with normal ranges for context]

> **Bottom Line:** This case illustrates [key clinical dilemma/teaching point] we'll explore throughout this presentation.

<!-- Speaker Notes:
- Start with a REAL case that hooks the audience
- Include details that will matter later (Chekhov's gun principle)
- End with a cliffhanger: "What would YOU do next?"
- Avoid giving away the diagnosis yet
- Make this relatable: "We've all seen this patient..."
-->

---

### SLIDE 5: EPIDEMIOLOGY

**Gamma instruction: Large bold statistics as focal points, subtle dark background**

<!-- DENSITY: Body max 60w. Table max 7r x 5c. Bullets max 3. Title = assertion with key statistic. Let the table speak — minimal prose around it. -->

## Why This Matters: The Burden of [CONDITION]

| Epidemiologic Measure  | Value               | Source |
| ---------------------- | ------------------- | ------ |
| **Incidence**          | [X per 100,000]     | [1]    |
| **Prevalence**         | [X% of population]  | [1]    |
| **Mortality Rate**     | [X% at Y timepoint] | [2]    |
| **Healthcare Costs**   | $[X billion/year]   | [3]    |
| **Years of Life Lost** | [X years]           | [2]    |

**High-Risk Populations:**

- [Population 1]: [Relative risk or incidence]
- [Population 2]: [Relative risk or incidence]
- [Population 3]: [Relative risk or incidence]

**Trends:**

- [Increasing/Decreasing/Stable] over past [timeframe]
- [Key driver of trend]

**Sources:** [1][2][3]

> **Bottom Line:** [CONDITION] affects [X patients annually] with [Y% mortality], making evidence-based management critical.

<!-- Speaker Notes:
- Use table format for scannable data (not paragraphs)
- Contextualize numbers: "That's equivalent to..."
- Highlight disparity if relevant (racial, geographic, etc.)
- Connect to audience: "In our ICU/clinic, that means..."
- Cite recent high-quality sources (ideally <3 years old)
-->

---

### SLIDE 6: PATHOPHYSIOLOGY_1

**Gamma instruction: Diagram connecting key concepts, educational illustration**

<!-- DENSITY: Body max 120w. Bullets max 6. Pick 2-3 most critical pathways. One key message per slide. -->

## [ASSERTION: State the key claim — must contain a verb. Example: "Mechanism X Drives Outcome Y via Pathway Z"]

<!-- MAX 5 BULLETS. Pick 2-3 most critical pathways. -->

- [Key mechanism → clinical consequence]
- [Key mechanism → clinical consequence]
- [Therapeutic target from mechanism]
<!-- STOP: More detail belongs in speaker notes, not on slide -->

**Sources:** [4][5]

> **Bottom Line:** [CONDITION] results from [key mechanism] leading to [clinical consequence] — this guides therapeutic targeting.

<!-- Speaker Notes:
- Connect pathophys to clinical practice (avoid pure biochemistry lecture)
- Use simple diagrams if possible (Gamma auto-generates)
- Explain WHY we care: "This is why we use drug X..."
- Avoid jargon; define technical terms
- Build foundation for treatment rationale later
-->

---

### SLIDE 7: PATHOPHYSIOLOGY_2

**Gamma instruction: Diagram connecting key concepts, educational illustration**

<!-- DENSITY: Body max 120w. Bullets max 6. Pick 2-3 most critical pathways. One key message per slide. -->

## [ASSERTION: State the key claim — must contain a verb. Example: "Secondary Pathway X Explains Clinical Heterogeneity"]

<!-- MAX 5 BULLETS. Focus on clinical relevance. -->

- [Key mechanism → clinical consequence]
- [Key mechanism → clinical consequence]
- [Individual variation factor → clinical implication]
- [Therapeutic implication from pathway]
<!-- STOP: More detail belongs in speaker notes, not on slide -->

**Sources:** [5][6]

> **Bottom Line:** [Second mechanism] explains [clinical heterogeneity/complications] and identifies [emerging therapeutic target].

<!-- Speaker Notes:
- Only include if genuinely important (don't pad for slide count)
- Link to case: "Remember our patient had..."
- Highlight knowledge gaps: "We still don't understand..."
- Transition to clinical assessment: "So how do we detect this early?"
-->

---

### SLIDE 8: PATHOPHYSIOLOGY_INTEGRATIVE

**Gamma instruction: Diagram connecting key concepts, educational illustration**

## Pathophysiology: Integrative Model

**Unified Framework:**

```
[Initiating Event]
        ↓
[Mechanism 1] ←→ [Mechanism 2]
        ↓             ↓
[Compensatory Response (helpful early, harmful late)]
        ↓
[Clinical Syndrome]
        ↓
[Complications if untreated]
```

**Key Therapeutic Windows:**

1. **Early ([timeframe])**: [Intervention type] can [prevent/reverse]
2. **Established ([timeframe])**: [Intervention type] can [mitigate/stabilize]
3. **Advanced ([timeframe])**: [Intervention type] limited to [palliate/support]

> **Bottom Line:** Understanding disease progression identifies optimal timing for specific interventions.

<!-- Speaker Notes:
- Synthesize prior pathophys slides into cohesive model
- Use flowchart/diagram format (not prose)
- Emphasize clinical actionability: "This is when we intervene..."
- Set up next section on clinical assessment
- Acknowledge complexity while maintaining clarity
-->

---

### SLIDE 9: CLINICAL_ASSESSMENT_DIAGNOSIS

**Gamma instruction: Full-width comparison table, data-first layout**

<!-- DENSITY: Body max 60w. Table max 7r x 5c. Bullets max 3. Let the table speak — minimal prose around it. -->

## Clinical Assessment: Recognition & Diagnosis

**Diagnostic Criteria ([Source - Year]):**

| Criterion Category      | Requirement               | Notes                              |
| ----------------------- | ------------------------- | ---------------------------------- |
| **Clinical Features**   | [Specific signs/symptoms] | [Sensitivity/specificity if known] |
| **Laboratory Findings** | [Biomarker thresholds]    | [Caveats/limitations]              |
| **Imaging/Testing**     | [Modality and findings]   | [When to order]                    |
| **Timing/Duration**     | [Temporal requirements]   | [Acute vs chronic]                 |

**Differential Diagnosis:**

- [Mimic 1]: Distinguished by [key differentiating feature]
- [Mimic 2]: Distinguished by [key differentiating feature]
- [Mimic 3]: Distinguished by [key differentiating feature]

**Diagnostic Pitfalls:**

- ⚠️ [Common mistake 1]
- ⚠️ [Common mistake 2]

**Sources:** [7][8]

> **Bottom Line:** Diagnosis requires [X + Y + Z]; beware [common mimic] which presents similarly but differs in [key feature].

<!-- Speaker Notes:
- Use validated/consensus diagnostic criteria (cite source)
- Tables for criteria (scannable, not prose)
- Highlight what NOT to do (pitfalls are high-yield)
- Real-world application: "I see this missed when..."
- Connect to case: "Our patient met criteria because..."
-->

---

### SLIDE 10: RISK_STRATIFICATION

**Gamma instruction: Full-width comparison table, data-first layout**

<!-- DENSITY: Body max 60w. Table max 7r x 5c. Bullets max 3. Let the table speak — minimal prose around it. -->

## Clinical Assessment: Severity & Risk Stratification

**[Validated Score/Tool Name] ([Acronym]):**

| Variable        | Points                   | Our Patient    |
| --------------- | ------------------------ | -------------- |
| [Variable 1]    | [Point value if present] | [✓ or ✗]       |
| [Variable 2]    | [Point value if present] | [✓ or ✗]       |
| [Variable 3]    | [Point value if present] | [✓ or ✗]       |
| [Variable 4]    | [Point value if present] | [✓ or ✗]       |
| **Total Score** | —                        | **[X points]** |

**Risk Stratification:**

- **Low Risk ([score range])**: [% event rate] → [Management approach]
- **Moderate Risk ([score range])**: [% event rate] → [Management approach]
- **High Risk ([score range])**: [% event rate] → [Management approach]

**Our Patient:** [X points] = [Risk category] → **[Recommended action]**

**Limitations:**

- [Validation population/exclusions]
- [Scenarios where tool underperforms]

**Sources:** [8][9]

> **Bottom Line:** The [SCORE] reliably predicts [outcome] and guides [decision point], but should not override clinical judgment.

<!-- Speaker Notes:
- Show HOW to calculate the score (walk through example)
- Apply to your opening case (concrete demonstration)
- Cite validation studies and c-statistics
- Discuss limitations honestly (external validity)
- Emphasize tool ASSISTS but doesn't replace gestalt
- Transition: "Now that we've risk-stratified, how do we treat?"
-->

---

### SLIDE 11: MCQ_1_QUESTION

**Gamma instruction: Quiz card layout, clean sans-serif, highlight correct answer in green**

<!-- DENSITY: Body max 120w. Options max 5 (A-E). MCQ must be on its own card. -->

## Knowledge Check: Case Scenario #1

**Clinical Vignette:**

A [age]-year-old [gender] presents with [key symptoms]. Exam shows [vital signs and physical findings]. Labs reveal [critical values].

**Question:** Based on the [SCORE/CRITERIA] discussed, what is the NEXT best step?

**A)** [Reasonable distractor]

**B)** [Correct answer based on prior slides]

**C)** [Tempting but incorrect choice]

**D)** [Overly aggressive/conservative option]

**E)** [Common mistake]

---

### SLIDE 12: MCQ_1_ANSWER

**Gamma instruction: Quiz card layout, clean sans-serif, highlight correct answer in green**

<!-- DENSITY: Body max 120w. Bullets max 4. Focus on reasoning, not repetition. -->

## Knowledge Check: Case Scenario #1 - Answer

**Correct Answer: B) [Correct answer]**

**Rationale:**

- The patient's [score/findings] places them in [risk category]
- Per [guideline/study], this indicates [recommended action]
- Option A is incorrect because [reason]
- Option C is tempting but wrong because [reason]
- Options D/E represent [over/under-treatment] given [evidence]

**Key Learning Points:**

- [Reinforced concept 1]
- [Reinforced concept 2]
- [Common pitfall to avoid]

> **Bottom Line:** [Risk stratification tool] successfully guides [clinical decision] when applied correctly.

<!-- Speaker Notes:
- PAUSE here for audience to think/discuss
- Ask for show of hands before revealing answer
- Explain not just why B is right, but why others are wrong
- Reference specific slides: "Remember slide 9 where we..."
- Use this to reinforce prior content before moving forward
- Check for questions before proceeding
-->

---

### SLIDE 13: GUIDELINE_COMPARISON

**Gamma instruction: Full-width comparison table, data-first layout**

<!-- DENSITY: Body max 30w. Table max 10r x 6c. Let the table speak. Minimal prose. -->

## Guideline Comparison: Society Recommendations

**Key Clinical Question:** [Specific PICO question]

| Society (Year)           | Recommendation                                    | Strength                  | Quality                      |
| ------------------------ | ------------------------------------------------- | ------------------------- | ---------------------------- |
| **[Society 1]** ([Year]) | [Specific recommendation with drug/dose/duration] | [Strong/Weak/Conditional] | [High/Moderate/Low/Very Low] |
| **[Society 2]** ([Year]) | [Specific recommendation]                         | [Strength]                | [Quality]                    |
| **[Society 3]** ([Year]) | [Specific recommendation]                         | [Strength]                | [Quality]                    |

**Areas of Consensus:**

- ✅ All societies agree on [shared recommendation]
- ✅ [Second point of agreement]

**Areas of Discordance:**

- ⚠️ [Society X] recommends [approach A], while [Society Y] recommends [approach B]
- **Reason:** [Different interpretation of same data / Different evidence base / Different patient populations]

**Sources:** [10][11][12]

> **Bottom Line:** Guidelines agree on [consensus area] but differ on [controversial area] due to [reason] — clinical judgment required.

<!-- Speaker Notes:
- Use table for side-by-side comparison (scannable)
- Cite specific guideline year (guidelines age fast)
- Explain GRADE strength (strong/weak) vs quality (high/low)
- Don't just present discordance — explain WHY societies disagree
- Acknowledge if one guideline is more recent/evidence-based
- Help audience choose when guidelines conflict
-->

---

### SLIDE 14: GUIDELINE_EVOLUTION

**Gamma instruction: Full-width comparison table, data-first layout**

<!-- DENSITY: Body max 30w. Table max 10r x 6c. Let the table speak. Minimal prose. -->

## Guideline Comparison: Evolution Over Time

**[Specific Recommendation Topic]** — How guidance has changed:

| Year         | Guideline | Recommendation            | What Changed             |
| ------------ | --------- | ------------------------- | ------------------------ |
| **[Year 1]** | [Society] | [Old recommendation]      | Baseline                 |
| **[Year 2]** | [Society] | [Modified recommendation] | [Trial X published]      |
| **[Year 3]** | [Society] | [Current recommendation]  | [Trial Y contradicted X] |

**Key Trials Driving Change:**

- **[Trial 1 Name, Year]**: [Finding that prompted change]
- **[Trial 2 Name, Year]**: [Finding that prompted change]
- **[Trial 3 Name, Year]**: [Finding that prompted change]

**Current Controversy:**

- [Pending trial name] (expected [year]) may further revise recommendations
- [Unresolved question]

**Sources:** [10][11][13]

> **Bottom Line:** Recommendations have shifted from [old approach] to [new approach] based on [key trials], but [area] remains debated.

<!-- Speaker Notes:
- Show evolution to highlight that "standard of care" changes
- Explain what evidence triggered each shift
- Acknowledge if current practice lags behind latest guidelines
- Prepare audience for future changes: "Watch for Trial X..."
- Humility: "What we recommend today may change tomorrow"
- Transition to deep dive on the key trials
-->

---

### SLIDE 15: GUIDELINE_SPECIAL_POPULATIONS

**Gamma instruction: Full-width comparison table, data-first layout**

<!-- DENSITY: Body max 30w. Table max 10r x 6c. Let the table speak. Minimal prose. -->

## Guideline Comparison: Special Populations

**How recommendations differ for specific patient groups:**

| Population                                  | Modification from General Recommendation      | Evidence Quality | Rationale                            |
| ------------------------------------------- | --------------------------------------------- | ---------------- | ------------------------------------ |
| **[Population 1 - e.g., Renal Impairment]** | [Dose adjustment / Alternative agent / Avoid] | [Quality]        | [Pharmacokinetic/safety concern]     |
| **[Population 2 - e.g., Pregnancy]**        | [Modified approach]                           | [Quality]        | [Limited safety data / Risk-benefit] |
| **[Population 3 - e.g., Elderly]**          | [Modified approach]                           | [Quality]        | [Increased adverse events / Frailty] |
| **[Population 4 - e.g., Pediatric]**        | [Modified approach]                           | [Quality]        | [Extrapolated from adult data]       |

**Evidence Gaps:**

- Most trials excluded [population], so recommendations are [expert opinion/extrapolated]
- [Specific study] is the ONLY trial in [population]

**Sources:** [10][11][14]

> **Bottom Line:** General guidelines require modification for [populations], but evidence quality is often [lower] — individualize based on risk-benefit.

<!-- Speaker Notes:
- Highlight evidence gaps (many populations understudied)
- Explain rationale for modifications (not arbitrary)
- Acknowledge when extrapolating from other populations
- Real-world challenges: "These patients weren't in the trials..."
- Medico-legal awareness: "Document shared decision-making"
- Transition to primary literature review of key trials
-->

---

### SLIDE 16: GUIDELINE_SUMMARY

**Gamma instruction: Multi-column tiered layout with procedural imagery**

## Guideline Comparison: Summary & Practical Approach

**Our Institutional Approach:**

```
Patient with [CONDITION] diagnosis
         ↓
Risk Stratification using [TOOL]
         ↓
Low Risk → [Approach A per Society X]
         ↓
Moderate Risk → [Approach B per Society Y, with caveat]
         ↓
High Risk → [Approach C, integrating Society Y + Trial Z]
         ↓
Special Populations → [Modified approach per table on previous slide]
```

**Justification for Our Protocol:**

- We favor [Society X] recommendations because [reason - more recent, better aligned with our population, etc.]
- We incorporate [Trial Y] findings even though not yet in guidelines because [reason]
- We deviate from guidelines in [scenario] based on [local data/expertise]

> **Bottom Line:** We synthesize multi-society guidelines into a practical protocol tailored to our patient population.

<!-- Speaker Notes:
- Present YOUR institutional approach (not just literature review)
- Justify choices when guidelines conflict
- Acknowledge when you deviate from guidelines (and why)
- Reference local quality data if available
- Emphasize this is YOUR approach (audience may differ)
- Transition: "Now let's examine the trials behind these recommendations"
-->

---

### SLIDE 17: LANDMARK_TRIAL_1

**Gamma instruction: Full-width comparison table, data-first layout**

<!-- DENSITY: Body max 130w. ONE table only (PICO or results, not both). Bullets max 4. -->

## Primary Literature: Landmark Trial #1

**[TRIAL ACRONYM]: [Full Trial Name]**
[First Author et al., Journal Year;Volume:Pages]

| Element             | Details                                                                       |
| ------------------- | ----------------------------------------------------------------------------- |
| **Study Design**    | [RCT / Observational / Meta-analysis]                                         |
| **Population**      | N=[X], [Inclusion criteria], [Exclusion criteria]                             |
| **Intervention**    | [Experimental arm details - drug, dose, duration]                             |
| **Comparator**      | [Control arm details]                                                         |
| **Primary Outcome** | [Specific outcome measure]                                                    |
| **Results**         | [Intervention X%] vs [Control Y%], **[RR/HR/OR] = [value] ([CI]); p=[value]** |
| **NNT/NNH**         | [Number needed to treat/harm if applicable]                                   |

**Strengths:** ✅ [Key strength 1], ✅ [Key strength 2]
**Limitations:** ⚠️ [Key limitation 1], ⚠️ [Key limitation 2]

**Impact:** [How this changed practice / Sparked controversy because...]

> **Bottom Line:** [TRIAL] showed [intervention] [increased/decreased] [outcome] by [X%], but [limitation] limits generalizability to [population].

<!-- Speaker Notes:
- Don't just describe the trial — APPRAISE it critically
- Explain PICO framework (Population, Intervention, Comparator, Outcome)
- Translate relative risk to absolute risk (more clinically meaningful)
- Calculate NNT if not reported (1 / ARR)
- Acknowledge COI if relevant (industry-funded?)
- Discuss applicability: "Does this apply to OUR patients?"
- Visual: Show key figure from paper if possible
-->

---

### SLIDE 18: LANDMARK_TRIAL_2

**Gamma instruction: Full-width comparison table, data-first layout**

<!-- DENSITY: Body max 130w. ONE table only (PICO or results, not both). Bullets max 4. -->

## Primary Literature: Landmark Trial #2

**[TRIAL ACRONYM]: [Full Trial Name]**
[First Author et al., Journal Year;Volume:Pages]

| Element               | Details                                                                    |
| --------------------- | -------------------------------------------------------------------------- |
| **Study Design**      | [Design type]                                                              |
| **Population**        | N=[X], [Key inclusion/exclusion]                                           |
| **Intervention**      | [Experimental arm]                                                         |
| **Comparator**        | [Control arm]                                                              |
| **Primary Outcome**   | [Outcome measure]                                                          |
| **Results**           | [Intervention X%] vs [Control Y%], **[Effect estimate] ([CI]); p=[value]** |
| **Subgroup Findings** | [Key subgroup interaction if relevant]                                     |

**Strengths:** ✅ [Strength 1], ✅ [Strength 2]
**Limitations:** ⚠️ [Limitation 1], ⚠️ [Limitation 2]

**Comparison to Trial #1:**

- [TRIAL 1] studied [population/intervention difference]
- [TRIAL 2] found [similar/contradictory] results, possibly because [explanation]

> **Bottom Line:** [TRIAL 2] [confirmed/contradicted] [TRIAL 1] findings, showing [key takeaway] in [specific population].

<!-- Speaker Notes:
- Explicitly compare to previous trial (build narrative)
- Explain discordant results if applicable (don't just present)
- Highlight subgroup analyses carefully (hypothesis-generating only)
- Discuss whether results are practice-changing
- Address audience skepticism: "You might wonder why..."
- Connect to guidelines: "This is why Society X now recommends..."
-->

---

### SLIDE 19: LANDMARK_TRIAL_3

**Gamma instruction: Full-width comparison table, data-first layout**

<!-- DENSITY: Body max 130w. ONE table only (PICO or results, not both). Bullets max 4. -->

## Primary Literature: Landmark Trial #3

**[TRIAL ACRONYM]: [Full Trial Name]**
[First Author et al., Journal Year;Volume:Pages]

| Element             | Details                                              |
| ------------------- | ---------------------------------------------------- |
| **Study Design**    | [Design - note if pragmatic/real-world]              |
| **Population**      | N=[X], [Broader/more restrictive than prior trials?] |
| **Intervention**    | [Experimental arm]                                   |
| **Comparator**      | [Control arm]                                        |
| **Primary Outcome** | [Outcome - note if different from prior trials]      |
| **Results**         | [Effect estimate with CI and p-value]                |
| **Safety Outcomes** | [Key adverse events, discontinuation rates]          |

**Strengths:** ✅ [Strength 1], ✅ [Strength 2]
**Limitations:** ⚠️ [Limitation 1], ⚠️ [Limitation 2]

**Why This Trial Matters:**

- Addressed [gap left by prior trials]
- [Pragmatic design / Real-world population / Long-term follow-up]
- [Changed practice by showing X]

> **Bottom Line:** [TRIAL 3] provided [real-world/safety/long-term] data supporting [intervention], solidifying its role in [clinical scenario].

<!-- Speaker Notes:
- By trial 3, focus on what's DIFFERENT/novel (avoid repetition)
- Emphasize if this is more generalizable (pragmatic design)
- Discuss safety data (often underemphasized in trial reporting)
- Explain how this filled a gap in the evidence base
- Synthesize all 3 trials: "Taken together, these show..."
- Transition to GRADE assessment of overall evidence quality
-->

---

### SLIDE 20: GRADE_SUMMARY

**Gamma instruction: Full-width comparison table, data-first layout**

<!-- DENSITY: Body max 40w. Table max 8r x 5c. Bold stats as focal points. -->

## Evidence Quality Assessment: GRADE Summary

**Clinical Question:** [Specific PICO question being evaluated]

| Outcome                                | Studies                | Quality    | Consistency           | Directness        | Effect Size            | GRADE Rating      |
| -------------------------------------- | ---------------------- | ---------- | --------------------- | ----------------- | ---------------------- | ----------------- |
| **[Outcome 1 - e.g., Mortality]**      | [N trials, X patients] | [RCTs/Obs] | [Consistent/Variable] | [Direct/Indirect] | [Large/Moderate/Small] | ⊕⊕⊕⊕ **HIGH**     |
| **[Outcome 2 - e.g., Adverse Events]** | [N trials, X patients] | [RCTs/Obs] | [Consistent/Variable] | [Direct/Indirect] | [Large/Moderate/Small] | ⊕⊕⊕◯ **MODERATE** |
| **[Outcome 3 - e.g., QoL]**            | [N trials, X patients] | [RCTs/Obs] | [Consistent/Variable] | [Direct/Indirect] | [Large/Moderate/Small] | ⊕⊕◯◯ **LOW**      |

**GRADE Criteria:**

- **Quality:** RCT starts high (⊕⊕⊕⊕), observational starts low (⊕⊕◯◯)
- **Downgrade for:** Risk of bias, inconsistency, indirectness, imprecision, publication bias
- **Upgrade for:** Large effect, dose-response, confounders minimizing effect

**Overall Confidence:**

- [High/Moderate/Low/Very Low] confidence that [intervention] [does/does not] improve [outcome]

> **Bottom Line:** Evidence for [intervention] is [GRADE level], meaning further research is [unlikely/likely] to change our confidence.

<!-- Speaker Notes:
- GRADE is about confidence in estimates, not just study design
- Explain what each rating means for practice:
  - HIGH = strong recommendation
  - MODERATE = conditional recommendation
  - LOW = weak recommendation, patient preference-driven
- Don't just show the table — interpret it
- Acknowledge nuance: high quality for mortality, low for QoL
- This prepares audience for strength of guideline recommendations
-->

---

### SLIDE 21: MCQ_2_QUESTION

**Gamma instruction: Quiz card layout, clean sans-serif, highlight correct answer in green**

## Knowledge Check: Case Scenario #2

**Clinical Vignette:**

You are reviewing guidelines for [CONDITION] and find that [Society A] recommends [approach X] while [Society B] recommends [approach Y]. Three major RCTs ([TRIAL1], [TRIAL2], [TRIAL3]) show [summarize key findings]. Your patient is a [age]-year-old with [relevant characteristics].

**Question:** Which approach is BEST supported by the evidence for THIS patient?

**A)** [Approach X from Society A]

**B)** [Approach Y from Society B]

**C)** [Hybrid approach combining elements]

**D)** [Alternative not recommended by either society]

**E)** [Approach that ignores patient characteristics]

---

### SLIDE 22: MCQ_2_ANSWER

**Gamma instruction: Quiz card layout, clean sans-serif, highlight correct answer in green**

## Knowledge Check: Case Scenario #2 - Answer

**Correct Answer: [Letter]) [Correct approach]**

**Rationale:**

- [Society A/B] recommendations are based primarily on [TRIAL X]
- However, this patient has [characteristic] which was [excluded/underrepresented] in [TRIAL X]
- [TRIAL Y] specifically studied [this population] and found [result]
- The GRADE quality for [approach] is [HIGH/MODERATE/LOW] based on [reasoning]

**Why Other Options Are Incorrect:**

- Option [X] ignores [patient characteristic / trial limitation]
- Option [Y] is based on [outdated evidence / weaker study design]
- Option [Z] represents [over/under-treatment] given [evidence]

**Application to Practice:**

- When guidelines conflict, consider [trial populations vs. your patient]
- [GRADE quality] informs strength of recommendation
- [Patient preference/values] may tip the balance when evidence is moderate quality

> **Bottom Line:** Guideline recommendations must be individualized based on trial applicability and patient characteristics.

<!-- Speaker Notes:
- This tests synthesis across multiple slides (guidelines + trials)
- Emphasize critical appraisal, not memorization
- Reinforce that guidelines are guides, not mandates
- Show how to apply evidence to individual patient
- Acknowledge uncertainty and need for shared decision-making
- Transition to practical management section
-->

---

### SLIDE 23: MANAGEMENT_INITIAL

**Gamma instruction: Multi-column tiered layout with procedural imagery**

<!-- DENSITY: Body max 120w. Table max 8r x 5c. Bullets max 6. Focus on actionable steps. -->

## [ASSERTION: State the key management principle — must contain a verb. Example: "Early Intervention with X Reduces Mortality by Y%"]

**Immediate Interventions (First [timeframe]):**

| Action               | Rationale                                | Evidence Level                        |
| -------------------- | ---------------------------------------- | ------------------------------------- |
| **[Intervention 1]** | [Why this first - physiologic rationale] | [Strong/Moderate/Weak based on GRADE] |
| **[Intervention 2]** | [Rationale]                              | [Evidence level]                      |
| **[Intervention 3]** | [Rationale]                              | [Evidence level]                      |
| **[Monitoring]**     | [What to monitor and how often]          | [Evidence level]                      |

**Initial Medication Dosing:**

- **[Drug 1]**: [Dose, route, frequency]
  - Adjust for [renal/hepatic impairment]: [Specific adjustments]
  - Contraindications: [Absolute and relative]

- **[Drug 2]**: [Dose, route, frequency]
  - Monitoring: [Labs/clinical parameters and timing]
  - Drug interactions: [Key interactions to avoid]

**Avoid Common Errors:**

- ❌ [Common mistake 1 and why it's harmful]
- ❌ [Common mistake 2 and why it's harmful]

**Sources:** [10][11][15]

> **Bottom Line:** Initial management focuses on [primary goals] achieved through [key interventions], while avoiding [common pitfalls].

<!-- Speaker Notes:
- Organized by TIME (what happens first)
- Link interventions to pathophysiology discussed earlier
- Provide EXACT doses/routes (practical reference)
- Highlight errors of omission and commission
- Apply to case: "For our patient, we would..."
- Explain what happens if initial approach fails (segue to next slide)
-->

---

### SLIDE 24: MANAGEMENT_ONGOING

**Gamma instruction: Multi-column tiered layout with procedural imagery**

## Clinical Management: Ongoing Care & Titration

**Response Assessment ([Timeframe]):**

| Parameter               | Target                        | Reassessment Timing | Action if Not Met |
| ----------------------- | ----------------------------- | ------------------- | ----------------- |
| **[Clinical Marker 1]** | [Specific target value/state] | [Hours/days]        | [Escalation plan] |
| **[Clinical Marker 2]** | [Target]                      | [Timing]            | [Action]          |
| **[Lab/Biomarker]**     | [Target range]                | [Timing]            | [Action]          |

**Treatment Escalation Algorithm:**

```
Initial therapy at [timeframe]
         ↓
Reassess at [timeframe]
         ↓
   Response adequate?
    ↙           ↘
  YES            NO
   ↓              ↓
Continue    Escalate to:
& Monitor   1) [Option A], or
            2) [Option B if A contraindicated]
                  ↓
            Reassess at [timeframe]
                  ↓
            If still failing → [Consider consultation/ICU/alternative Dx]
```

**De-escalation/Duration:**

- [When to de-escalate therapy]
- [Total duration of treatment]
- [Long-term monitoring post-acute phase]

**Sources:** [15][16]

> **Bottom Line:** Titrate therapy based on [specific markers] at [defined intervals], escalating through [algorithmic approach] if targets not met.

<!-- Speaker Notes:
- Emphasize dynamic reassessment (not "set and forget")
- Provide specific timing (not vague "monitor closely")
- Algorithm gives structure when patient not improving
- Discuss when to call for help (humility)
- Address duration: "Don't stop too early or continue too long"
- Real-world: "We reassess on rounds at..."
-->

---

### SLIDE 25: MANAGEMENT_SPECIAL_POPULATIONS

**Gamma instruction: Multi-column tiered layout with procedural imagery**

## Clinical Management: Special Populations

**Population-Specific Modifications:**

| Population                                   | Key Considerations                          | Approach Modification                                |
| -------------------------------------------- | ------------------------------------------- | ---------------------------------------------------- |
| **Renal Impairment (CrCl <[X])**             | [Pharmacokinetic/safety concern]            | [Dose adjustment / Alternative agent / Avoid drug Y] |
| **Liver Dysfunction (Child-Pugh B/C)**       | [Concern]                                   | [Modification]                                       |
| **Pregnancy/Lactation**                      | [Teratogenicity / Excretion in milk]        | [Preferred agents / Absolute contraindications]      |
| **Elderly/Frailty**                          | [Increased sensitivity / Drug interactions] | [Start low, go slow / Deprescribing]                 |
| **[Disease-Specific - e.g., Heart Failure]** | [Concern]                                   | [Modification]                                       |

**Shared Decision-Making Considerations:**

- **Higher Risk Populations:** Discuss [increased risk of X] vs [potential benefit Y]
- **Limited Evidence:** Acknowledge when extrapolating from general population
- **Goals of Care:** Treatment may differ if focused on [longevity vs QoL vs symptom control]

**Sources:** [14][17]

> **Bottom Line:** General protocols require individualization for [populations], balancing [efficacy vs safety] with explicit patient involvement.

<!-- Speaker Notes:
- Overlap with guideline special pops slide, but now ACTIONABLE
- Provide specific dose adjustments (not just "use caution")
- Highlight underrepresented trial populations (evidence gap)
- Emphasize shared decision-making language:
  - "We don't have great data in your situation, but..."
  - "The risks and benefits in your case..."
- Document discussions (medico-legal)
-->

---

### SLIDE 26: COMPLICATIONS_TROUBLESHOOTING

**Gamma instruction: Full-width comparison table, data-first layout**

## Clinical Management: Complications & Troubleshooting

**Common Complications:**

| Complication         | Incidence | Risk Factors   | Prevention           | Management if Occurs |
| -------------------- | --------- | -------------- | -------------------- | -------------------- |
| **[Complication 1]** | [X%]      | [Risk factors] | [Preventive measure] | [Treatment approach] |
| **[Complication 2]** | [X%]      | [Risk factors] | [Prevention]         | [Management]         |
| **[Complication 3]** | [X%]      | [Risk factors] | [Prevention]         | [Management]         |

**When Therapy Fails:**

🔍 **Troubleshooting Checklist:**

- [ ] Is the diagnosis correct? (Reconsider [key mimics])
- [ ] Is the patient adherent? (Medication reconciliation)
- [ ] Are doses adequate? (Check [drug levels / Biomarker response])
- [ ] Are there drug interactions? (Review med list for [specific interactions])
- [ ] Is there a complication? (Screen for [complications above])
- [ ] Is there an alternative mechanism? ([Secondary diagnosis to consider])

**When to Consult:**

- [Specialist type] if [specific scenario]
- ICU if [specific deterioration criteria]
- [Other service] if [scenario]

**Sources:** [15][16][18]

> **Bottom Line:** Complications occur in [X%], are predicted by [risk factors], and require [specific management]; treatment failure demands systematic reassessment.

<!-- Speaker Notes:
- Anticipate complications before they happen
- Provide INCIDENCE data (sets expectations)
- Prevention is high-yield (not just treatment)
- Troubleshooting checklist prevents anchoring bias
- Know when you're in over your head (get help)
- Apply to case: "Our patient developed..."
-->

---

### SLIDE 27: CONTROVERSY_1

**Gamma instruction: Large bold statistics as focal points, subtle dark background**

<!-- DENSITY: Body max 120w. Bullets max 6. Structure: debate statement, position A, position B, institutional approach. -->

## [ASSERTION: Frame the controversy as a question. Example: "Should All Patients Receive Prophylaxis or Only High-Risk?"]

**The Debate:** [Clearly state the controversy - e.g., "Should all patients receive X, or only high-risk patients?"]

**Position A: [Conservative/Broad/etc. Approach]**

- **Proponents:** [Society X, Trial Y]
- **Arguments:**
  - [Argument 1 with supporting evidence]
  - [Argument 2]
- **Weaknesses:** [Limitations of this approach/evidence]

**Position B: [Alternative Approach]**

- **Proponents:** [Society Z, Trial W]
- **Arguments:**
  - [Argument 1 with supporting evidence]
  - [Argument 2]
- **Weaknesses:** [Limitations of this approach/evidence]

**Why No Consensus:**

- [Trials studied different populations]
- [Outcome measures differed]
- [Cost-effectiveness concerns]
- [Awaiting definitive trial: [TRIAL NAME, expected completion [YEAR]]]

**Our Institutional Approach:**

- We currently [follow Position A/B / Use hybrid] because [rationale]
- We may revise based on [upcoming evidence]

**Sources:** [10][11][19]

> **Bottom Line:** [Question] remains unresolved; we adopt [position] pending [future evidence], but acknowledge reasonable alternatives.

<!-- Speaker Notes:
- Don't present false certainty where controversy exists
- Steelman both positions (avoid bias)
- Explain WHY controversy persists (not just different opinions)
- Identify what evidence would resolve the debate
- Model intellectual humility
- Acknowledge if your practice differs from others
- Prepare for audience questions/disagreement
-->

---

### SLIDE 28: CONTROVERSY_2

**Gamma instruction: Large bold statistics as focal points, subtle dark background**

<!-- DENSITY: Body max 120w. Bullets max 6. Structure: debate statement, what we know, what we don't know, practice approach. -->

## [ASSERTION: Frame the controversy as a question. Example: "When to Initiate Therapy: Immediately or After Confirmed Diagnosis?"]

**The Debate:** [State second major controversy]

**What We Know:**

- [Established facts both sides agree on]
- [Areas where evidence is clear]

**What We Don't Know:**

- [Key evidence gap 1]
- [Key evidence gap 2]
- [Methodologic challenge preventing resolution]

**Current Practice Patterns:**

- [Geographic variation: "In Europe, [X%] do A, while in US, [Y%] do B"]
- [Specialty variation: "Surgeons favor A, internists favor B"]

**Emerging Data:**

- **[Recent Study/Trial]**: [Finding that tilts toward one position]
- **Limitations:** [Why this doesn't fully resolve debate]

**How to Approach in Practice:**

- [Risk-stratify: "For low-risk patients, [approach], for high-risk, [approach]"]
- [Shared decision-making: "Discuss [trade-off] with patient"]
- [Document rationale clearly in chart]

**Sources:** [19][20]

> **Bottom Line:** Lacking definitive evidence, we use [risk-stratified/patient-centered] approach to [question], anticipating [future trial] will provide clarity.

<!-- Speaker Notes:
- Second controversy should be distinct from first
- Acknowledge practice variation (not everyone agrees)
- Provide framework for decision-making despite uncertainty
- Emphasize documentation (defensive medicine reality)
- Connect to case: "In our patient, we chose A because..."
- Transition to MCQ testing ability to navigate uncertainty
-->

---

### SLIDE 29: MCQ_3_QUESTION

**Gamma instruction: Quiz card layout, clean sans-serif, highlight correct answer in green**

## Knowledge Check: Case Scenario #3

**Complex Clinical Scenario:**

[Age]-year-old with [multiple comorbidities] presents with [CONDITION]. Initial therapy with [standard treatment] was started, but at [timeframe] the patient has [specific sign of treatment failure]. Labs show [values]. Imaging reveals [finding]. The patient also develops [complication discussed earlier].

**Complicating Factor:** [Element from "Special Populations" or "Controversial Topics" sections]

**Question:** What is the MOST appropriate next step in management?

**A)** [Escalate to next-line therapy without addressing complication]

**B)** [Correct answer - addresses complication AND adjusts therapy appropriately]

**C)** [Reasonable but suboptimal choice]

**D)** [Overly aggressive intervention]

**E)** [Misses the complication/special population issue]

---

### SLIDE 30: MCQ_3_ANSWER

**Gamma instruction: Quiz card layout, clean sans-serif, highlight correct answer in green**

## Knowledge Check: Case Scenario #3 - Answer

**Correct Answer: B) [Correct answer]**

**Rationale:**

- The patient's [specific finding] indicates [complication X]
- Before escalating therapy, must address [complication] with [intervention]
- The patient's [special population characteristic] requires [modification] per slide [X]
- Regarding [controversial topic], we chose [approach] because [patient-specific factor]

**Step-by-Step Reasoning:**

1. **Recognize the complication:** [Finding A + B] = [Complication]
2. **Address the complication:** [Immediate intervention]
3. **Adjust primary therapy:** [Modification for special population]
4. **Escalate if needed:** [Next-line therapy, now safe to give]

**Why Other Options Are Incorrect:**

- Option A: Dangerous because [would worsen complication]
- Option C: Suboptimal because [misses special population adjustment]
- Option D: Too aggressive given [patient frailty / Unclear benefit]
- Option E: Fails to recognize [key complication/contraindication]

> **Bottom Line:** Complex patients require [systematic approach]: recognize complications, individualize for special populations, apply evidence judiciously.

<!-- Speaker Notes:
- This tests synthesis of multiple domains (not isolated knowledge)
- Walk through clinical reasoning process step-by-step
- Highlight how complications change management
- Emphasize systematic approach over pattern recognition
- Acknowledge this is challenging (validates difficulty)
- Real-world: "This is exactly what happened last week..."
- Transition to future directions
-->

---

### SLIDE 31: EMERGING_NOVEL_THERAPIES

**Gamma instruction: Full-width comparison table, data-first layout**

<!-- DENSITY: Body max 60w. Table max 8r x 6c. Focus on therapies likely to reach practice soon. -->

## [ASSERTION: State what's emerging and when. Example: "Three Novel Agents Enter Phase 3 Trials This Year"]

**Therapies in Late-Stage Development:**

| Agent/Approach         | Mechanism             | Development Stage | Key Trial    | Expected Results | Potential Impact                 |
| ---------------------- | --------------------- | ----------------- | ------------ | ---------------- | -------------------------------- |
| **[Drug A]**           | [Mechanism of action] | Phase [II/III]    | [TRIAL NAME] | [Year/Quarter]   | [How this could change practice] |
| **[Drug B]**           | [Mechanism]           | Phase [II/III]    | [TRIAL NAME] | [Year/Quarter]   | [Potential impact]               |
| **[Device/Procedure]** | [How it works]        | [Stage]           | [TRIAL NAME] | [Year/Quarter]   | [Impact]                         |

**Promising Early-Stage Research:**

- **[Biomarker/Precision Medicine Approach]**: [Brief description, current evidence level]
- **[Gene Therapy/Novel Target]**: [Description, timeline to clinical use]

**What to Watch:**

- [Conference presentation expected [Date]]
- [FDA decision expected [Date]]
- [Guideline update anticipated [Date]]

> **Bottom Line:** [Agent/approach] may become available within [timeframe], potentially offering [benefit] for [specific population].

<!-- Speaker Notes:
- Focus on therapies likely to reach practice (not bench research)
- Explain MECHANISM (connects to pathophys earlier)
- Realistic timelines (not hype)
- Identify which patients would benefit (not everyone)
- Caveat: "Phase 3 trials sometimes fail..."
- Encourage audience to follow [trial name]
- Show how to stay current (journal clubs, guidelines)
-->

---

### SLIDE 32: EMERGING_PRACTICE_CHANGING

**Gamma instruction: Large bold statistics as focal points, subtle dark background**

<!-- DENSITY: Body max 120w. Bullets max 6. Focus on trials with expected results within 1-2 years. -->

## [ASSERTION: State expected practice changes. Example: "Two Ongoing Trials May Revise Guidelines by 2027"]

**Ongoing Trials That May Change Practice:**

**[TRIAL ACRONYM 1]**: [Full Name]

- **Question:** [Specific PICO question being tested]
- **Why This Matters:** [Current practice is X, but if this trial is positive, we'd switch to Y]
- **Design:** [Pragmatic RCT / Registry / etc., N=[target enrollment]]
- **Timeline:** Results expected [Quarter/Year]
- **Predicted Impact:** [Guideline change / New indication / De-adoption of current practice]

**[TRIAL ACRONYM 2]**: [Full Name]

- **Question:** [PICO question]
- **Why This Matters:** [Gap this addresses]
- **Design:** [Design and size]
- **Timeline:** [Expected results]
- **Predicted Impact:** [Impact on practice]

**Paradigm Shifts on the Horizon:**

- [Emerging concept - e.g., "biomarker-guided therapy" or "de-escalation strategies"]
- [How this challenges current dogma]
- [What evidence is needed to validate]

> **Bottom Line:** Within [timeframe], expect potential practice changes in [area 1] and [area 2] based on [trial results].

<!-- Speaker Notes:
- Distinguish "emerging" (soon) from "future" (distant)
- Help audience prioritize what to follow
- Explain how to access trial results when published:
  - Subscribe to journal alerts
  - Follow trial Twitter/X accounts
  - Attend [conference] where results will be presented
- Intellectual honesty: "These may fail or show no difference"
- Prepare for paradigm shifts (avoid dogmatism)
-->

---

### SLIDE 33: CASE_RESOLUTION

**Gamma instruction: Split layout - clinical scene on left, patient details on right**

## Return to Our Patient: Case Resolution

**Recall:** [Age]-year-old with [presenting symptoms] and [initial findings]

**Clinical Course:**

- **Initial Management:** [What was done based on this presentation]
  - [Specific interventions matching slides 21-24]
  - [Risk stratification score result]

- **Response at [Timeframe]:** [Clinical trajectory]
  - [Markers of improvement or deterioration]
  - [Adjustments made per escalation algorithm]

- **Complications:** [If any occurred]
  - [How recognized and managed per slide 24]

- **Final Outcome:** [Resolution, discharge, recovery]
  - [Duration of treatment]
  - [Follow-up plan]

**What We Applied:**

- ✅ [Learning Objective 1]: [How we demonstrated this in the case]
- ✅ [Learning Objective 2]: [Application to case]
- ✅ [Learning Objective 3]: [Application to case]

> **Bottom Line:** This case illustrates [key principle], demonstrating how [evidence-based approach] leads to [successful outcome].

<!-- Speaker Notes:
- Full-circle moment (recall opening case)
- Show how each section of presentation applied to real patient
- Acknowledge if outcome was complicated (not all cases resolve perfectly)
- Reinforce learning objectives through case application
- Humanize the case: "The patient was able to..."
- Acknowledge team effort (nurses, consultants, etc.)
- Transition to final summary
-->

---

### SLIDE 34: TAKE_HOME_POINTS

**Gamma instruction: Large numbered list with bold key phrases**

## Take-Home Points

**5 Key Messages:**

1️⃣ **[Diagnosis/Recognition]**: [Concise statement about diagnosis - e.g., "Use [SCORE] to risk-stratify all patients with [CONDITION]"]

2️⃣ **[Evidence Synthesis]**: [Statement about evidence - e.g., "[TRIAL X] and [TRIAL Y] provide high-quality evidence that [intervention] reduces [outcome]"]

3️⃣ **[Management]**: [Practical management pearl - e.g., "Initiate [drug] at [dose] within [timeframe], escalate if [marker] not improving by [timeframe]"]

4️⃣ **[Special Considerations]**: [Population-specific or complication message - e.g., "Adjust dosing for renal impairment and monitor for [complication]"]

5️⃣ **[Emerging/Controversial]**: [Forward-looking statement - e.g., "Guidelines currently conflict on [issue]; pending [TRIAL] results, we recommend [approach]"]

**One-Sentence Summary:**
[CONDITION] is [characterized by X], diagnosed using [tool], managed with [evidence-based intervention], with [ongoing controversy] to be resolved by [future evidence].

> **Bottom Line:** These five points summarize [X] minutes of content — apply them tomorrow on rounds.

<!-- Speaker Notes:
- MAXIMUM 5 points (3-4 is better than 6-7)
- Make them ACTIONABLE (not vague "consider" statements)
- Each point should change practice or thinking
- One-sentence summary for "elevator pitch"
- Briefly recap: "We covered [X] learning objectives..."
- Thank audience before questions
- Anticipate likely questions and prepare responses
-->

---

### SLIDE 35: QA

**Gamma instruction: Professional closing slide with contact info**

## Questions?

**Contact Information:**
[Your Name], [Credentials]
[Email]
[Twitter/X handle if professional]

**Resources:**

- Slides will be available at: [Link/location]
- Key references compiled at: [Link if available]
- Institutional protocol available at: [Internal link if applicable]

**Further Learning:**

- [Guideline 1]: [URL]
- [Trial 1 full text]: [URL]
- [Review article]: [Citation]

---

### SLIDE 36: REFERENCES_1

**Gamma instruction: Small text, no images, clean numbered list**

## References (Part 1)

**Guidelines:**

1. [Society 1]. [Guideline title]. [Journal]. [Year];[Vol]:[Pages]. [DOI/URL]
2. [Society 2]. [Guideline title]. [Journal]. [Year];[Vol]:[Pages]. [DOI/URL]

**Landmark Trials:** 3. [Author et al.] [TRIAL ACRONYM]: [Full title]. [Journal]. [Year];[Vol]:[Pages]. PMID: [ID] 4. [Author et al.] [TRIAL ACRONYM]: [Full title]. [Journal]. [Year];[Vol]:[Pages]. PMID: [ID] 5. [Author et al.] [TRIAL ACRONYM]: [Full title]. [Journal]. [Year];[Vol]:[Pages]. PMID: [ID]

**Systematic Reviews/Meta-Analyses:** 6. [Author et al.] [Title]. [Journal]. [Year];[Vol]:[Pages]. PMID: [ID] 7. [Author et al.] [Title]. [Journal]. [Year];[Vol]:[Pages]. PMID: [ID]

**Epidemiology/Background:** 8. [Author et al.] [Title]. [Journal]. [Year];[Vol]:[Pages]. PMID: [ID] 9. [Author et al.] [Title]. [Journal]. [Year];[Vol]:[Pages]. PMID: [ID] 10. [Author et al.] [Title]. [Journal]. [Year];[Vol]:[Pages]. PMID: [ID]

<!-- Continue numbering... -->

---

### SLIDE 37: REFERENCES_2

**Gamma instruction: Small text, no images, clean numbered list**

## References (Part 2)

**Pathophysiology:** 11. [Author et al.] [Title]. [Journal]. [Year];[Vol]:[Pages]. PMID: [ID] 12. [Author et al.] [Title]. [Journal]. [Year];[Vol]:[Pages]. PMID: [ID]

**Special Populations:** 13. [Author et al.] [Title]. [Journal]. [Year];[Vol]:[Pages]. PMID: [ID] 14. [Author et al.] [Title]. [Journal]. [Year];[Vol]:[Pages]. PMID: [ID]

**Emerging Evidence:** 15. ClinicalTrials.gov. [TRIAL NAME]. [NCT Number]. [URL] 16. ClinicalTrials.gov. [TRIAL NAME]. [NCT Number]. [URL]

**Additional Resources:** 17. [Author et al.] [Title]. [Journal]. [Year];[Vol]:[Pages]. PMID: [ID] 18. [Author et al.] [Title]. [Journal]. [Year];[Vol]:[Pages]. PMID: [ID] 19. [Author et al.] [Title]. [Journal]. [Year];[Vol]:[Pages]. PMID: [ID] 20. [Author et al.] [Title]. [Journal]. [Year];[Vol]:[Pages]. PMID: [ID]

<!-- References should be comprehensive, recent (<5 years for most), and properly formatted -->

<!-- Speaker Notes:
- Make references available to audience (slide deck or handout)
- Include DOI/PMID for easy lookup
- Hyperlink URLs if presenting electronically
- Consider QR code linking to reference list
- Highlight "must-read" references for audience
-->
