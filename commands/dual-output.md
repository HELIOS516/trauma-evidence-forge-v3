# /asf:dual-output

Same evidence base producing BOTH a presentation AND a manuscript.

## Usage

```
/asf:dual-output {topic} [--journal JTACS] [--presentation long|medium]
```

## Workflow

1. Run evidence synthesis as shared source of truth
2. Fork to presentation: author slides, run 5-script pipeline
3. Fork to manuscript: author IMRAD paper, run checklist validation
4. Both outputs reference the same verified PMIDs

## Claude Code Optimization

Use Agent Teams for maximum parallelism. See CLAUDE.md "Team: Dual Output" composition.
