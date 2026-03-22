# Gamma API Guide (Medical Adapter)

This file is a medical-domain adapter on top of shared Gamma contracts.

## Source of Truth

Do not treat this file as a standalone Gamma contract reference.
Use core contracts first:

- `../gamma-presentation-core/references/gamma-canonical-spec.md`
- `../gamma-presentation-core/references/gamma-mcp-tool-contracts.md`
- `../gamma-presentation-core/references/gamma-api-endpoint-contracts.md`
- `../gamma-presentation-core/references/gamma-local-vs-official-delta.md`

## Adapter Scope

Medical adapter owns:

- presenter defaults
- medical image style defaults
- citation/table preservation requirements
- per-slide pedagogy and layout instructions

Core owns:

- API/MCP parameter validity
- accepted enums and limits
- drift detection rules

## Current MCP Tool Set

- `GAMMA_GENERATE_GAMMA`
- `GAMMA_CREATE_FROM_TEMPLATE`
- `GAMMA_GET_GAMMA_FILE_URLS`
- `GAMMA_LIST_THEMES`
- `GAMMA_LIST_FOLDERS`

## Medical Defaults (Profile)

Stored in:

- `config/gamma-medical-profile.json`

Defaults:

- `format: presentation`
- `textMode: preserve`
- `cardSplit: auto`
- `cardOptions.dimensions: 16x9`
- `imageOptions.source: aiGenerated`
- `imageOptions.model: imagen-4-pro`
- `imageOptions.style: photorealistic medical photography...`
- `textOptions.amount: detailed`
- `textOptions.language: en`

## Card Splitting Strategy

`cardSplit` is available in MCP for generate workflows.

Recommended:

- Use `cardSplit: auto` + explicit `numCards` for deterministic card count.
- Use `cardSplit: inputTextBreaks` when authored `---` boundaries must be respected.

## Additional Instructions

- Hard cap: 2000 characters.
- Use compressed per-slide directive blocks in API mode.
- Keep richer design instructions in web guide fallback output.

## Mode-Dependent Text Options

- `tone` and `audience` are generate-mode controls.
- In preserve mode, omit tone/audience to reduce noise and confusion.

## Medical Safety Constraints

Always include these behaviors in instructions/content:

- Preserve all tables exactly.
- Preserve superscript citation formatting (`<sup>[N]</sup>`).
- Preserve Sources blocks on content slides.
- Keep clinical phrasing appropriate for physician audience.

## Build + Validate Workflow

1. Build payload via adapter script (uses core builder internally):

```bash
python3 scripts/generate_gamma_params.py projects/<topic>/presentation-long-gamma.md
```

2. Validate payload directly with core validator when needed:

```bash
python3 ../gamma-presentation-core/scripts/validate_gamma_payload.py \
  --payload projects/<topic>/presentation-long-gamma-api.json \
  --scan-markdown references/gamma-api-guide.md \
  --scan-markdown SKILL.md
```

3. If drift findings exist, fix adapter docs before submission.

## Pipeline Output Files

- `*-gamma.md` — cleaned submission markdown
- `*-gamma-instructions.json` — extracted per-slide instructions
- `*-gamma-notes.md` — extracted speaker notes
- `*-gamma-api.json` — MCP/API payload (core-valid)
- `*-gamma-web.md` — web fallback instructions

## Notes

- `generate_gamma_params.py` now uses `gamma-presentation-core/scripts/build_gamma_payload.py`.
- Payload validity is checked through `gamma-presentation-core/scripts/validate_gamma_payload.py` before writing output.
- This adapter should not reintroduce deprecated claims (for example: “cardSplit unavailable”).
