# Script Equivalents: Manual Checklists for Tier 1 Users

These checklists replicate the logic of the key Python scripts in `scripts/` for users on claude.ai or Claude Desktop who do not have Bash access. Work through each checklist manually against your manuscript text.

---

## 1. Manuscript Validation (validate_manuscript.py)

16 checks total: 10 hard gates (any failure = FAIL) and 6 soft gates (warnings only).

### Hard Gates (all must pass)

**Check 1 -- IMRAD Sections Present**
Verify the manuscript has ALL six section headings (any heading level):

- [ ] Abstract
- [ ] Introduction
- [ ] Methods
- [ ] Results
- [ ] Discussion
- [ ] References

If any are missing, the manuscript fails.

**Check 2 -- Body Citations Exist**

- [ ] At least one `[N]` numbered citation appears in the body text (before the References section)

**Check 3 -- Citation Coverage Complete**

- [ ] Every `[N]` citation number used in the body text has a matching entry in the References section
- List all citation numbers from the body. List all reference numbers from the References section. Every body citation must appear in the references. (Orphan references -- in References but not cited -- are acceptable.)

**Check 4 -- PMID or DOI Present**

- [ ] At least one PMID (format: `PMID: 1234567` or `PMID:12345678`, 7-8 digits) or DOI (format: `10.XXXX/...`) appears anywhere in the manuscript

**Check 5 -- No Fabricated PMIDs**
Flag any PMID that matches these suspicious patterns:

- [ ] Not `00000000`
- [ ] Not `12345678`
- [ ] Not all identical digits (e.g., `11111111`, `99999999`)

If any suspicious PMIDs are found, the manuscript fails.

**Check 6 -- Abstract Present**

- [ ] A heading matching "Abstract" exists (redundant with Check 1 but scored independently)

**Check 7 -- Results Has Statistics**
Look at the Results section only. At least one of these must appear:

- [ ] A percentage sign (`%`)
- [ ] A p-value (`p=` or `p<`)
- [ ] A confidence interval (`CI`)
- [ ] An odds ratio (`OR `)

**Check 8 -- Methods Non-Empty**

- [ ] The Methods section contains substantive content (more than just a heading -- roughly 50+ characters of actual text)

**Check 9 -- Discussion Non-Empty**

- [ ] The Discussion section contains substantive content (more than just a heading -- roughly 50+ characters of actual text)

**Check 10 -- References >= 5**

- [ ] At least 5 numbered reference entries exist in the References section (counted by `[N]` bracket format or `N.` numbered list format)

### Soft Gates (warnings, do not cause failure)

**Check 11 -- Word Count <= 5,000**

- [ ] Total word count (excluding markdown syntax like `#`, `*`, `_`, links) is at most 5,000 words

**Check 12 -- Study Type Detected**
Scan the manuscript for these keyword patterns to identify the study type:

| Study Type          | Keywords to Look For                                         | Reporting Checklist |
| ------------------- | ------------------------------------------------------------ | ------------------- |
| RCT                 | "randomized", "randomly assigned", "random allocation"       | CONSORT             |
| Systematic Review   | "systematic review", "meta-analysis", "PRISMA"               | PRISMA              |
| Cohort              | "cohort study", "prospective cohort", "retrospective cohort" | STROBE              |
| Case-Control        | "case-control", "case control", "matched controls"           | STROBE              |
| Cross-Sectional     | "cross-sectional", "cross sectional", "prevalence study"     | STROBE              |
| Case Report         | "case report", "single patient", "we present a case"         | CARE                |
| Quality Improvement | "quality improvement", "PDSA", "plan-do-study-act"           | SQUIRE              |

- [ ] At least one study type is identifiable (check in the order listed above; first match wins)

**Check 13 -- >= 50% of Statistical Claims Have Confidence Intervals**

- Find every line that contains a percentage (`N%`)
- For each, check whether the same line also contains `95% CI` or `confidence interval`
- [ ] At least half of those lines include a CI

**Check 14 -- >= 80% of References Have PMID or DOI**

- Count total numbered references in the References section
- Count total PMIDs (`PMID: NNNNNNN`) plus DOIs (`10.XXXX/...`) in the manuscript
- [ ] The identifier count is at least 80% of the reference count

**Check 15 -- GRADE Ratings Valid**
Find all GRADE ratings in the text (pattern: `GRADE:` or `GRADE ` followed by a value). Each must be one of:

- Numeric scale: `1A`, `1B`, `1C`, `2A`, `2B`, `2C`, `3`, `4`
- Descriptive scale: `High`, `Moderate`, `Low`, `Very Low`
- [ ] All GRADE ratings use valid values from the lists above

### Scoring

- **PASS**: All 10 hard gates pass (soft gate warnings are informational)
- **FAIL**: Any hard gate fails

---

## 2. AI Pattern Detection (detect_ai_patterns.py)

Scores text on a 0-100 scale across 8 categories. Higher = more likely AI-generated.

### Category 1: Hedging Phrases (0-15 points)

Count occurrences of these exact phrases (case-insensitive):

- "it is important to note that"
- "it should be noted that"
- "it is worth mentioning that"
- "it is interesting to observe that"
- "it is essential to understand that"
- "one must consider that"
- "it cannot be overstated that"
- "it bears mentioning that"

Calculate: (count / total words) x 1000 = rate per 1,000 words

| Rate per 1,000 words | Points |
| -------------------- | ------ |
| <= 3                 | 0      |
| 3.1 - 6              | 5      |
| 6.1 - 9              | 10     |
| > 9                  | 15     |

### Category 2: Transition Words at Sentence Start (0-15 points)

Count sentences that START with any of these words followed by a comma:

- Furthermore, / Moreover, / Additionally, / In addition,
- Similarly, / Consequently, / Nevertheless, / Nonetheless,
- Accordingly, / Conversely,

Calculate: (count / total sentences) x 100 = percentage

| Percentage | Points |
| ---------- | ------ |
| <= 2%      | 0      |
| 2.1 - 5%   | 5      |
| 5.1 - 8%   | 10     |
| > 8%       | 15     |

### Category 3: Sentence Length Uniformity (0-15 points)

Count the number of words in each sentence. Calculate:

- Mean sentence length
- Standard deviation of sentence lengths
- Coefficient of variation (CV) = standard deviation / mean

(Skip if fewer than 5 sentences.)

| CV          | Points                           |
| ----------- | -------------------------------- |
| > 0.45      | 0 (good variation -- human-like) |
| 0.36 - 0.45 | 5                                |
| 0.26 - 0.35 | 10                               |
| <= 0.25     | 15 (very uniform -- AI-like)     |

### Category 4: Over-Qualification Phrases (0-10 points)

Count occurrences of these phrases (case-insensitive):

- "comprehensive analysis" / "robust study" / "thorough investigation"
- "rigorous examination" / "extensive research" / "groundbreaking study"
- "novel approach" / "significant finding" / "important contribution"
- "valuable insights"

Calculate: (count / total words) x 1000 = rate per 1,000 words

| Rate per 1,000 words | Points |
| -------------------- | ------ |
| <= 1                 | 0      |
| 1.1 - 3              | 3      |
| 3.1 - 5              | 7      |
| > 5                  | 10     |

### Category 5: Missing Surgical Jargon (0-10 points)

Check how many of these abbreviations appear at least once (as whole words):

**Trauma/Critical Care**: ISS, GCS, FAST, REBOA, MTP, DCR, DCS, MAP, CVP, ECMO
**Blood Products**: PRBC, FFP, PLT, TXA, ASA
**Clinical**: ICU, OR, ED, SBP, UOP
**Global Surgery**: ACS, TBI, ARDS, DVT, VTE, PE, INR, POMR, NSOAP, LCoGS

| Abbreviations found | Points                        |
| ------------------- | ----------------------------- |
| >= 15               | 0 (rich jargon -- human-like) |
| 10 - 14             | 3                             |
| 5 - 9               | 7                             |
| < 5                 | 10 (sparse jargon -- AI-like) |

### Category 6: Repetitive Paragraph Structure (0-10 points)

For each of the first 10 paragraphs (with 3+ sentences):

- Count words in each sentence
- Calculate the average difference in length between consecutive sentences
- If the average difference is less than 5 words, the paragraph is "template-like"

Calculate: template paragraphs / analyzed paragraphs = ratio

| Ratio      | Points |
| ---------- | ------ |
| <= 0.2     | 0      |
| 0.21 - 0.4 | 5      |
| > 0.4      | 10     |

### Category 7: Passive Voice (0-10 points)

Count sentences containing passive constructions:

- "was/were/is/are/been/being" + word ending in "-ed"
- "was/were/is/are/been/being" + word ending in "-en"
- "was/were/is/are/been/being" + found/shown/seen/given/made/done/taken

Calculate: (passive sentences / total sentences) x 100 = percentage

| Percentage | Points |
| ---------- | ------ |
| <= 50%     | 0      |
| 51 - 60%   | 5      |
| > 60%      | 10     |

### Category 8: Enumeration Patterns (0-15 points)

Count these patterns:

- "First(ly),... Second(ly),..." sequences spanning sentences
- "First, ... second, ... third, ..." within a passage
- "There are several/three/four/five key/main/important factors/reasons/aspects/points"
- "The following points/factors/aspects are..."
- 3+ sentences starting with "First,", "Second,", "Third,", "Fourth,", "Finally,", or "Lastly,"

| Pattern count | Points |
| ------------- | ------ |
| 0             | 0      |
| 1             | 5      |
| 2             | 10     |
| 3+            | 15     |

### Overall Score Interpretation

| Total Score (0-100) | Interpretation                           |
| ------------------- | ---------------------------------------- |
| 0 - 20              | Likely human-authored                    |
| 21 - 30             | Likely human, minor AI elements possible |
| 31 - 45             | Uncertain, may be AI-assisted            |
| 46 - 60             | Likely AI-generated                      |
| 61 - 100            | Definitively AI-generated                |

---

## 3. Reference Formatting (format_references.py)

### Step 1: Locate the References Section

Find the heading "References" (any heading level: `#`, `##`, or `###`). Everything after that heading is the references section.

### Step 2: Extract Reference Entries

Each reference should be in one of these formats:

- Bracket format: `[1] Author. Title. Journal. Year;...`
- Numbered list: `1. Author. Title. Journal. Year;...`

### Step 3: Check Sequential Numbering

- [ ] References are numbered sequentially starting from 1
- [ ] No gaps or out-of-order numbers (e.g., [1], [2], [4] is wrong -- [3] is missing)

### Step 4: Check Identifiers

For each reference:

- [ ] Has a PMID (`PMID:` followed by digits) OR a DOI (`DOI:` or `doi.org/10.XXXX/...`)
- Flag any reference missing both PMID and DOI

### Step 5: Check Vancouver/AMA Format

Each reference should match the general pattern:

- Author(s). Title. Journal abbreviation. Year;Volume(Issue):Pages.
- Specifically: look for a period, then words, then another period, then a 4-digit year
- [ ] Each reference contains at least: `. SomeText. YYYY` (period, space, text, period, space, year)

### Step 6: Check for Duplicates

- Extract all PMIDs from references
- [ ] No two references share the same PMID

---

## 4. Research Utilities Reference (research_utils.py)

These are the format definitions and detection rules used by the other scripts.

### PMID Format

- Pattern: `PMID:` or `PMID ` followed by 7-8 digits
- Example: `PMID: 12345678` or `PMID:1234567`

### DOI Format

- Pattern: `DOI:` or `doi.org/` followed by `10.` then 4+ digits, then `/`, then the rest of the identifier
- Example: `DOI: 10.1016/j.lancet.2015.02.024`

### Body Citations

- Pattern: `[N]` where N is a number, found in text BEFORE the References section
- Extract all unique numbers; these are the citations that need matching references

### Reference Numbers

- Found in the References section only
- Either `[N]` bracket format or `N.` at the start of a line followed by text

### Citation Coverage Check

1. Collect all `[N]` numbers from body text (before References heading)
2. Collect all reference numbers from the References section
3. **Coverage is complete** if every body citation number exists in the reference numbers
4. **Missing references** = body citations not found in reference entries
5. **Orphan references** = reference entries not cited in the body (acceptable)

### Word Count

- Strip markdown syntax: `#`, `*`, `_`, backticks, brackets, parentheses, `>`, `|`
- Strip HTML tags
- Strip horizontal rules (`---`)
- Count remaining whitespace-separated tokens

### Study Type Detection (checked in this order -- first match wins)

1. **RCT**: "randomized", "randomly assigned", "random allocation"
2. **Systematic Review**: "systematic review", "meta-analysis", "PRISMA"
3. **Cohort**: "cohort study", "prospective cohort", "retrospective cohort"
4. **Case-Control**: "case-control", "case control", "matched controls"
5. **Cross-Sectional**: "cross-sectional", "cross sectional", "prevalence study"
6. **Case Report**: "case report", "single patient", "we present a case"
7. **Quality Improvement**: "quality improvement", "PDSA", "plan-do-study-act"

### Study Type to Reporting Checklist Mapping

| Study Type          | Checklist |
| ------------------- | --------- |
| RCT                 | CONSORT   |
| Systematic Review   | PRISMA    |
| Cohort              | STROBE    |
| Case-Control        | STROBE    |
| Cross-Sectional     | STROBE    |
| Case Report         | CARE      |
| Quality Improvement | SQUIRE    |

### GRADE Rating Validation

Valid values (case-sensitive for descriptive scale):

- **Numeric**: `1A`, `1B`, `1C`, `2A`, `2B`, `2C`, `3`, `4`
- **Descriptive**: `High`, `Moderate`, `Low`, `Very Low`

Pattern in text: `GRADE:` or `GRADE ` followed by one of the values above.

### Statistical Claims Detection

- Find every line containing a percentage (`N%`)
- For each line, check:
  - **Has CI**: line contains `95% CI` or `confidence interval` (case-insensitive)
  - **Has p-value**: line contains `p=`, `p<`, or `p>` followed by a digit
  - **Has citation**: line contains `[N]` bracket reference

### IMRAD Section Detection

Look for headings at any level (`#`, `##`, `###`) matching these names (case-insensitive):

- Abstract, Introduction, Methods, Results, Discussion, References
- A manuscript is **structurally complete** when all six are present
