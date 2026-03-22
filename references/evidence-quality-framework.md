# Evidence Quality Framework — Grading, Classification, and Assessment

## GRADE Rating System (Grading of Recommendations, Assessment, Development and Evaluations)

The GRADE system is the international standard for rating certainty of evidence and strength of recommendations.

### Certainty of Evidence

| Rating       | Meaning                                                                                                        | Implication                                 |
| ------------ | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| **High**     | Further research is very unlikely to change confidence in the estimate of effect                               | Strong basis for clinical recommendations   |
| **Moderate** | Further research is likely to have an important impact on confidence and may change the estimate               | Recommendations with caveats                |
| **Low**      | Further research is very likely to have an important impact on confidence and is likely to change the estimate | Weak recommendations; more research needed  |
| **Very Low** | Any estimate of effect is very uncertain                                                                       | Insufficient for definitive recommendations |

### Factors That Lower GRADE Rating

- Risk of bias (poor study design, lack of blinding)
- Inconsistency (heterogeneous results across studies)
- Indirectness (population, intervention, or outcome differs from question)
- Imprecision (wide confidence intervals, small sample size)
- Publication bias (funnel plot asymmetry, missing studies)

### Factors That Raise GRADE Rating

- Large magnitude of effect (RR >2 or <0.5 with no plausible confounders)
- Dose-response gradient
- All plausible confounders would reduce the demonstrated effect

---

## Evidence Tier Classification

### Tier 1: Experimental Evidence

| Tier   | Study Type                     | Description                                                                                   |
| ------ | ------------------------------ | --------------------------------------------------------------------------------------------- |
| **1A** | Systematic review of RCTs      | Meta-analysis pooling multiple RCTs with homogeneous results                                  |
| **1B** | Individual RCT (well-designed) | Single randomized controlled trial with adequate power, allocation concealment, and follow-up |

### Tier 2: Quasi-Experimental Evidence

| Tier   | Study Type                                | Description                                                            |
| ------ | ----------------------------------------- | ---------------------------------------------------------------------- |
| **2A** | Systematic review of cohort studies       | Meta-analysis of observational longitudinal studies                    |
| **2B** | Individual cohort study / low-quality RCT | Prospective or retrospective cohort; RCTs with significant limitations |

### Tier 3: Observational Evidence

| Tier  | Study Type           | Description                                                         |
| ----- | -------------------- | ------------------------------------------------------------------- |
| **3** | Case-control studies | Retrospective comparison of cases with outcomes vs controls without |

### Tier 4: Expert Evidence

| Tier  | Study Type                                  | Description                                                |
| ----- | ------------------------------------------- | ---------------------------------------------------------- |
| **4** | Case series / case reports / expert opinion | Descriptive studies without controls; consensus statements |

---

## Oxford Centre for Evidence-Based Medicine (CEBM) Levels

| Level  | Therapy / Prevention                       | Prognosis                                                     | Diagnosis                                                             | Economic Analysis                                              |
| ------ | ------------------------------------------ | ------------------------------------------------------------- | --------------------------------------------------------------------- | -------------------------------------------------------------- |
| **1a** | SR of RCTs                                 | SR of inception cohort studies                                | SR of Level 1 diagnostic studies                                      | SR of Level 1 economic studies                                 |
| **1b** | Individual RCT (narrow CI)                 | Individual inception cohort (>80% follow-up)                  | Validating cohort with good reference standard                        | Analysis based on clinically sensible costs; systematic review |
| **1c** | All or none                                | All or none case-series                                       | Absolute SpPins and SnNouts                                           |                                                                |
| **2a** | SR of cohort studies                       | SR of retrospective cohort / untreated control groups in RCTs | SR of Level >2 diagnostic studies                                     | SR of Level >2 economic studies                                |
| **2b** | Individual cohort / low-quality RCT        | Retrospective cohort or follow-up of untreated controls       | Exploratory cohort with good reference standard                       | Analysis based on clinically sensible costs; limited data      |
| **2c** | Outcomes research; ecological studies      | Outcomes research                                             |                                                                       | Audit or outcomes research                                     |
| **3a** | SR of case-control studies                 |                                                               | SR of 3b and better studies                                           | SR of 3b and better studies                                    |
| **3b** | Individual case-control study              |                                                               | Non-consecutive study without consistently applied reference standard | Analysis without clinically sensible costs                     |
| **4**  | Case-series (and poor cohort/case-control) | Case-series or superseded reference standard                  | Case-control, poor or non-independent reference standard              | Analysis with no sensitivity analysis                          |
| **5**  | Expert opinion without critical appraisal  | Expert opinion without critical appraisal                     | Expert opinion without critical appraisal                             | Expert opinion without critical appraisal                      |

---

## Required Statistical Metrics

### Effect Size Measures

| Metric                            | When to Use                               | Interpretation                                        |
| --------------------------------- | ----------------------------------------- | ----------------------------------------------------- |
| **Odds Ratio (OR)**               | Case-control studies, logistic regression | OR >1 = increased odds; OR <1 = decreased odds        |
| **Relative Risk (RR)**            | Cohort studies, RCTs                      | RR >1 = increased risk; RR <1 = decreased risk        |
| **Hazard Ratio (HR)**             | Time-to-event / survival analysis         | HR >1 = higher hazard rate; HR <1 = lower hazard rate |
| **Absolute Risk Reduction (ARR)** | RCTs, treatment comparisons               | Control event rate minus treatment event rate         |
| **Number Needed to Treat (NNT)**  | Clinical decision-making                  | 1/ARR; how many patients treated for one to benefit   |

### Mandatory Reporting

For ALL effect sizes presented in slides:

- **95% Confidence Interval (CI):** Must accompany every OR, RR, HR, and ARR
- **NNT:** Calculate and present where applicable (treatment comparisons)
- **p-values:** Report but NOT as sole evidence of significance
- **Absolute numbers:** Include raw event rates, not just relative measures
  - "30% relative reduction" means nothing without baseline rate
  - "Reduced from 10% to 7% (ARR 3%, NNT 33)" is informative

### Presentation Format

```
VTE rate: 5.3% vs 8.1% (OR 0.63, 95% CI 0.45-0.88, p=0.007)
ARR: 2.8%, NNT: 36
```

### Statistical Significance vs Clinical Significance

- A p-value < 0.05 does not necessarily mean clinically meaningful
- Always assess: Is the effect size large enough to change practice?
- Wide CI crossing 1.0 (for OR/RR/HR) = not statistically significant
- Narrow CI entirely below 1.0 (for protective effects) = robust finding
- Consider: sample size, event rates, and clinical context

---

## Multi-Society Guideline Comparison Framework

### Standard Comparison Table Format

| Guideline | Organization                              | Recommendation            | Evidence Level | Year   | Key Difference |
| --------- | ----------------------------------------- | ------------------------- | -------------- | ------ | -------------- |
| ATLS      | American College of Surgeons              | [Specific recommendation] | [Level]        | [Year] | [vs others]    |
| EAST      | Eastern Association for Surgery of Trauma | [Specific recommendation] | [Level]        | [Year] | [vs others]    |
| WEST      | Western Trauma Association                | [Specific recommendation] | [Level]        | [Year] | [vs others]    |
| ACCP      | American College of Chest Physicians      | [Specific recommendation] | [Level]        | [Year] | [vs others]    |
| SCCM      | Society of Critical Care Medicine         | [Specific recommendation] | [Level]        | [Year] | [vs others]    |
| ACS-TQIP  | ACS Trauma Quality Improvement            | [Specific recommendation] | [Level]        | [Year] | [vs others]    |

### Key Elements to Compare Across Guidelines

- **Agent recommended:** Which pharmacologic agent(s)?
- **Timing of initiation:** Early (<24h), standard (<48h), delayed (>48h)?
- **Contraindications:** What specific injuries/conditions preclude prophylaxis?
- **Mechanical prophylaxis:** Role of SCDs, IPC devices?
- **Duration:** How long to continue prophylaxis?
- **Monitoring:** What labs or imaging for surveillance?
- **Special populations:** TBI, spinal cord injury, solid organ injury?

### Discordance Documentation

When guidelines disagree, document:

1. The specific point of disagreement
2. The evidence each guideline cites for its position
3. The evidence level/GRADE for each recommendation
4. Whether the disagreement is clinically meaningful
5. Which recommendation is most recent / based on most current evidence

---

## Bias Assessment

### Selection Bias Checklist

- [ ] Was randomization adequate (computer-generated, concealed allocation)?
- [ ] Were groups comparable at baseline?
- [ ] Was there differential loss to follow-up (>20% or imbalanced)?
- [ ] Was intention-to-treat analysis performed?
- [ ] Were exclusion criteria applied equally to both groups?

### Information Bias Checklist

- [ ] Were outcome assessors blinded to group assignment?
- [ ] Were participants blinded (if feasible)?
- [ ] Were outcomes measured objectively or subjectively?
- [ ] Was surveillance for outcomes equal in both groups (detection bias)?
- [ ] Were data collection methods standardized?

### Confounding Assessment

- [ ] Were known confounders identified and controlled for?
- [ ] Was multivariable analysis performed?
- [ ] Were subgroup analyses pre-specified (not post-hoc)?
- [ ] Is there residual confounding that could explain the results?
- [ ] Were sensitivity analyses performed?

### Reporting Standards Compliance

| Standard    | Study Type                                                    | Key Requirements                                                     |
| ----------- | ------------------------------------------------------------- | -------------------------------------------------------------------- |
| **CONSORT** | Randomized controlled trials                                  | Flow diagram, ITT analysis, allocation concealment, blinding         |
| **STROBE**  | Observational studies (cohort, case-control, cross-sectional) | Study design, setting, participants, variables, bias assessment      |
| **PRISMA**  | Systematic reviews and meta-analyses                          | Search strategy, selection criteria, quality assessment, forest plot |
| **MOOSE**   | Meta-analyses of observational studies                        | Search strategy, study characteristics, quantitative synthesis       |
| **STARD**   | Diagnostic accuracy studies                                   | Index test, reference standard, 2x2 table, sensitivity/specificity   |
| **CARE**    | Case reports                                                  | Timeline, diagnostic assessment, therapeutic interventions, outcomes |

### Quick Bias Risk Rating

| Risk Level   | Criteria                                                               | Slide Annotation                                          |
| ------------ | ---------------------------------------------------------------------- | --------------------------------------------------------- |
| **Low**      | Adequate randomization, blinding, >90% follow-up, ITT analysis         | No annotation needed                                      |
| **Moderate** | Minor limitations in one domain (e.g., single-blind, 80-90% follow-up) | Note limitation in Sources                                |
| **High**     | Major limitations in 2+ domains or fundamental design flaw             | Flag prominently: "Caution: High risk of bias"            |
| **Critical** | Study conclusions unreliable due to bias                               | Do not cite as primary evidence; mention only for context |
