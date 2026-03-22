# PubMed Connector Setup

> How to enable PubMed integration for citation verification, abstract retrieval, and literature search.

---

## Why PubMed Integration Matters

Without PubMed, Claude relies on its training data for citations. This means it can:

- Fabricate plausible-looking PMIDs that do not exist
- Misattribute findings to the wrong paper
- Miss recent publications after its knowledge cutoff

With PubMed connected, Claude can:

- **Verify citations are real** -- look up any PMID and confirm it exists with correct title, authors, and journal
- **Retrieve abstracts** -- pull the actual abstract text for evidence grading
- **Search for literature** -- find relevant papers by topic, author, or keyword
- **Convert between identifiers** -- translate between PMID, PMCID, and DOI
- **Find related articles** -- discover papers that cite or are cited by a given reference
- **Access PMC full text** -- retrieve full-text articles from PubMed Central when available

---

## Platform 1: claude.ai / Claude Desktop App

### Setup

1. Open **claude.ai** in your browser (or the **Claude Desktop** app)
2. Click the **gear icon** (bottom-left) to open Settings
3. Select **Connectors** from the sidebar
4. Find **PubMed** in the connector list
5. Click **Connect**

That is it. No API key, no account, no configuration needed. PubMed is a free public resource from the National Library of Medicine.

### Using It

Once connected, Claude automatically searches PubMed when you ask about citations or literature. You do not need special syntax. Examples:

- "Verify PMID 25924834"
- "Search PubMed for global surgery capacity assessment Zambia"
- "Find the abstract for DOI 10.1016/S0140-6736(15)60160-X"
- "What papers has Meara JG published on global surgery?"

---

## Platform 2: Claude Code (CLI)

### Option A: Life Sciences Plugin (Recommended)

If the Anthropic life-sciences plugin is available in the marketplace:

```bash
# Install the life-sciences plugin bundle
/plugin marketplace add anthropics/life-sciences

# Enable the PubMed module
/plugin install pubmed@life-sciences
```

### Option B: Manual MCP Configuration

Add the PubMed MCP server to your Claude Code settings. Edit `~/.claude/settings.json` and add under `mcpServers`:

```json
{
  "mcpServers": {
    "pubmed": {
      "command": "npx",
      "args": ["-y", "@anthropic/pubmed-mcp-server"],
      "env": {}
    }
  }
}
```

Then restart Claude Code for the server to load.

### Option C: NCBI E-utilities Direct (Advanced)

If you need custom PubMed access (e.g., higher rate limits), register for an NCBI API key at https://www.ncbi.nlm.nih.gov/account/settings/ and configure:

```json
{
  "mcpServers": {
    "pubmed": {
      "command": "npx",
      "args": ["-y", "@anthropic/pubmed-mcp-server"],
      "env": {
        "NCBI_API_KEY": "your-key-here"
      }
    }
  }
}
```

An API key raises the rate limit from 3 requests/second to 10 requests/second. This is only needed for bulk operations (systematic reviews with hundreds of citations).

---

## What PubMed Integration Enables

| Capability            | Without PubMed                            | With PubMed                                    |
| --------------------- | ----------------------------------------- | ---------------------------------------------- |
| Citation verification | Pattern-only (catches obvious fakes)      | Real lookup (confirms title, authors, journal) |
| Abstract retrieval    | Not available                             | Full abstract text for evidence grading        |
| Literature search     | Relies on training data (may be outdated) | Live search of 36M+ articles                   |
| Identifier conversion | Not available                             | PMID, PMCID, DOI interconversion               |
| Related articles      | Not available                             | Citation network discovery                     |
| PMC full text         | Not available                             | Full-text retrieval when available             |

### Impact on Each Module

- **Manuscript Forge**: Validates every `[N]` citation in your draft against real PubMed records. Catches fabricated PMIDs before submission.
- **Peer Review Engine**: Checks whether cited evidence actually supports the claims made. Identifies missing key references by searching related literature.
- **Global Surgery Analysis**: Finds current country-specific surgical capacity data and recent framework publications.
- **Text Naturalizer**: No direct PubMed dependency (text pattern analysis only).

---

## Verification Test

After setup, run this test to confirm PubMed is working:

> "Verify PMID 25924834"

**Expected result**: Claude should return details for:

- **Title**: An estimation of the global volume of surgery: a modelling strategy based on available data (or the Lancet Commission "Global Surgery 2030" paper)
- **Authors**: Meara JG, Leather AJM, Hagander L, et al.
- **Journal**: The Lancet, 2015
- **DOI**: 10.1016/S0140-6736(15)60160-X

If Claude returns these details (or close to them), PubMed is connected and working.

**If verification fails**:

- claude.ai: Check Settings > Connectors and confirm PubMed shows as "Connected"
- Claude Code: Run `/mcp` to list active MCP servers and confirm `pubmed` appears
- Try restarting the application and testing again

---

## Troubleshooting

**"PubMed connector not showing in Settings"**
The connector list depends on your Claude plan and region. If PubMed is not listed, you can still ask Claude to verify citations using its training data -- just be aware that verification will be less reliable.

**"Claude is not searching PubMed even though it is connected"**
Be explicit in your request: "Search PubMed for..." or "Look up this PMID on PubMed:". Sometimes Claude will answer from memory instead of searching unless you specifically ask it to use PubMed.

**"Rate limit errors in Claude Code"**
If you are running bulk citation verification (50+ PMIDs), you may hit the default 3 requests/second limit. Register for a free NCBI API key (Option C above) to increase the limit to 10/second.

**"MCP server failed to start in Claude Code"**
Check that Node.js is installed (`node --version`). The MCP server requires Node 18+. If using npx, ensure npm is configured and can download packages.
