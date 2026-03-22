# Citation Standards — Verification, Formatting, and Quality Control

## Why Rigorous Citation Verification Matters

AI language models frequently hallucinate PMIDs, fabricate author names, and invent journal articles. In academic medical presentations, a single fabricated reference destroys credibility. Every citation must be independently verified before inclusion.

### The Reference [16] Incident

During the DVT Prophylaxis project, PMID 38243640 was cited for a trauma DVT meta-analysis (attributed to "Jiang H, et al. Int J Surg. 2025"). Verification revealed:

- **PMID 38243640** actually belonged to Hermann et al., "Brain coupling in cardiac arrest," Ann Clin Transl Neurol 2024 — a completely unrelated cardiac arrest paper
- The cited author existed in the field but had not published the claimed paper
- The journal, year, and topic were all plausible — making the fabrication hard to detect without PMID lookup

**Resolution:** Replaced with verified Kerwin AJ, et al., "The CLOTT Study," Ann Surg. 2025;282(3):382-388. PMID: 40492307.

**Lesson:** Every PMID must be checked. Plausibility is not verification.

---

## Rigid Verification Protocol

### Step 1: PMID Verification via PubMed Web Search

For every PMID in the presentation:

```
web_search("PMID {number}")
```

Check ALL of the following match:

- Author name(s)
- Article title
- Journal name
- Publication year
- Volume/issue/pages

A match on author alone is NOT sufficient. Title and journal must also match.

### Step 2: DOI Verification via doi.org Resolution

For every DOI in the presentation:

```
web_search("doi.org/{DOI}")
```

Verify the resolved page matches the claimed paper. DOIs should resolve to the publisher's page for the exact article.

### Step 3: Hyperlink Validation

All URLs included in citations or references must be confirmed working:

- PubMed links: `https://pubmed.ncbi.nlm.nih.gov/{PMID}/`
- DOI links: `https://doi.org/{DOI}`
- Guideline URLs: verify they resolve to the correct document

### Step 4: Classification and Action

| Result                              | Action                                            |
| ----------------------------------- | ------------------------------------------------- |
| PMID matches perfectly (all fields) | Keep as-is                                        |
| PMID exists, wrong paper            | Flag "[PMID UNVERIFIED]", search for correct PMID |
| PMID doesn't exist                  | Flag: likely fabricated reference                 |
| Paper found, different PMID         | Replace with correct PMID                         |
| Paper not found anywhere            | Flag: entire citation may be fabricated           |

### Step 5: Documentation

Log all verification results for audit trail:

```
[16] Jiang H, et al. Int J Surg. 2025
  PMID 38243640 -> WRONG (Hermann et al., cardiac arrest paper)
  Searched: "Jiang early late VTE prophylaxis trauma meta-analysis"
  Result: No matching publication found
  Status: FABRICATED - replaced with Kerwin CLOTT Study PMID 40492307
```

---

## Known Hallucination Patterns

### Pattern 1: Fabricated PMIDs (Most Common)

The PMID is a real number that exists in PubMed but belongs to a completely different paper. The AI generates a plausible-looking number.

**Detection:** Always look up the PMID directly. Never trust that a number "looks right."

### Pattern 2: PMID Exists but Wrong Paper

The PMID is valid and even in a related field, but it's a different study by different authors. Often the journal or topic area is close enough to seem correct.

**Detection:** Verify author AND title AND journal, not just one field.

### Pattern 3: Author Matches but Different Paper

A real researcher in the field is cited, but the specific paper doesn't exist or has a different PMID. The AI knows the author publishes in the area and invents a plausible citation.

**Detection:** Search for the specific paper by title, not just by author name.

### Pattern 4: Truncated or Altered Journal Names

The journal name is slightly wrong — abbreviated differently, missing a word, or using an older name. This makes web searches fail to find the mismatch.

**Detection:** Compare the exact journal name from the PMID lookup against the citation.

### Pattern 5: Future-Dated Publications

Citations from the current or next year with suspiciously perfect results that align exactly with the presentation's argument. These are especially hard to disprove.

**Detection:** Be extra skeptical of papers dated within the past 12 months. Verify with multiple search strategies.

---

## Standardized Citation Format

### Authoring Format (Before Pipeline Processing)

When writing slides, use numbered `[N]` references:

- In body text: `...mortality rate of 15%[1] compared to...`
- Per-slide sources: `**Sources:** [1][2][3]`
- References section: numbered list with `[N]` at end of each entry

The pipeline (`format_citations.py`) will:

1. Pass 1: Remove `[N]` from headings
2. Pass 2: Expand `**Sources:** [1][2]` to full citation lines
3. Pass 3: Convert body `[N]` to `<sup>[N]</sup>`

**DO NOT use parenthetical format** like `(Author et al., Year; PMID: XXXXX)` -- the pipeline cannot process this format.

### Reference List Format

**CRITICAL:** `[N]` must be at the **END** of each reference line. The `format_citations.py` script's `build_ref_lookup()` uses a regex that matches trailing `[N]` to build the citation lookup table. Putting `[N]` at the start breaks the pipeline.

```
Author(s). Title. Journal. Year;Vol(Issue):Pages. PMID: XXXXX [N]
```

### Examples

```
O'Toole RV, et al. Aspirin or LMWH for thromboprophylaxis after fracture (PREVENT CLOT). N Engl J Med. 2023;388:203-213. PMID: 36652353 [6]
Wu X, et al. Early VTE prophylaxis in severe TBI. J Trauma Acute Care Surg. 2023;95:94-104. PMID: 36626625 [9]
Kerwin AJ, et al. The CLOTT Study. Ann Surg. 2025;282(3):382-388. PMID: 40492307 [16]
```

### Legacy Migration

For presentations authored with parenthetical citations `(Author, Year; PMID: XXXXXXXX)`, use the one-time migration tool before running the pipeline:

```bash
python3 scripts/convert_inline_citations.py projects/<topic>/presentation-long.md
```

### Rules

- Use "et al." after the first author for 3+ authors
- Include up to 3 authors before "et al." for landmark studies
- Abbreviate journal names per NLM conventions
- Always include PMID when available
- Include DOI as secondary identifier when PMID is not available
- Volume and issue in format: `Year;Vol(Issue):Pages`
- Page ranges use en-dash in print, hyphen in digital

---

## Three-Pass Formatting Pipeline

### Pass 1: Clean Slide Titles

Remove bracket reference numbers from headings. Titles must be clean for readability.

**Regex:** Remove `\[\d+\]` from lines starting with `#`

```python
if line.startswith('#') and not line.startswith('# References'):
    line = re.sub(r'\[(\d+)\]', '', line).strip()
```

### Pass 2: Expand Sources Lines

Replace compact source references with full citations.

**Find:** `**Sources:** [1][2][3]`
**Replace with:**

```
**Sources:**
- [1] Full Author, et al. Full Title. Journal. Year;Vol:Pages. PMID: XXXXXXXX
- [2] Full Author, et al. Full Title. Journal. Year;Vol:Pages. PMID: XXXXXXXX
```

Requires building a reference lookup dict from the References section first.

### Pass 3: Superscript In-Text Citations

Convert bracket citations to superscript format for presentation rendering.

**Regex:** `\[(\d+)\]` becomes `<sup>[\1]</sup>`

**Exclude these line types:**

```python
if line.startswith('#'):              continue  # headings (cleaned in Pass 1)
if '**Sources:**' in line:            continue  # source headers
if line.startswith('- ['):            continue  # expanded source items
# In References section:              skip entirely
```

---

## End-of-Presentation Verification Checklist

### Before Submission

- [ ] Every PMID verified via direct PubMed lookup
- [ ] Every DOI resolves to the correct paper
- [ ] All URLs confirmed working
- [ ] No "[PMID UNVERIFIED]" flags remaining
- [ ] No fabricated references remaining
- [ ] Author names match PubMed records exactly
- [ ] Journal abbreviations follow NLM conventions
- [ ] Publication years verified against PubMed
- [ ] Volume/issue/page numbers verified against PubMed
- [ ] References section numbered sequentially without gaps

### Formatting Checks

- [ ] Slide titles contain NO bracket numbers
- [ ] All in-text citations use `<sup>[N]</sup>` superscript
- [ ] Sources blocks expanded with full citations on every slide
- [ ] References slide has complete bibliography
- [ ] Citation numbers are consistent (same number = same paper throughout)

### Content Integrity

- [ ] Statistical claims match the cited source (check OR, RR, CI, p-values)
- [ ] Dosing information matches source guidelines
- [ ] Study population/setting matches how the study is described
- [ ] No cherry-picked results that misrepresent the source study
- [ ] Guideline recommendations accurately reflect the cited guideline version
