# Verification Commands

## Test Suite

```bash
# Run full test suite
python3 -m pytest ~/claude-skills/skills/trauma-evidence-forge-v3/evals/ -v

# Run specific test files
python3 -m pytest ~/claude-skills/skills/trauma-evidence-forge-v3/evals/test_format_citations.py -v
python3 -m pytest ~/claude-skills/skills/trauma-evidence-forge-v3/evals/test_preprocess.py -v
python3 -m pytest ~/claude-skills/skills/trauma-evidence-forge-v3/evals/test_card_utils.py -v
python3 -m pytest ~/claude-skills/skills/trauma-evidence-forge-v3/evals/test_audit.py -v
python3 -m pytest ~/claude-skills/skills/trauma-evidence-forge-v3/evals/test_validate_new.py -v
```

## Script Dry-Runs

```bash
# Format citations (dry-run, no file modification)
python3 ~/claude-skills/skills/trauma-evidence-forge-v3/scripts/format_citations.py --dry-run ~/claude-skills/skills/trauma-evidence-forge-v3/projects/*/presentation.md

# Preprocess for Gamma (dry-run, no file modification)
python3 ~/claude-skills/skills/trauma-evidence-forge-v3/scripts/preprocess_for_gamma.py --dry-run ~/claude-skills/skills/trauma-evidence-forge-v3/projects/*/presentation.md
```

## Design Audit

```bash
# Run design audit on a presentation
python3 ~/claude-skills/skills/trauma-evidence-forge-v3/scripts/audit_slide_design.py \
  ~/claude-skills/skills/trauma-evidence-forge-v3/projects/*/presentation-long-gamma.md

# JSON output for programmatic analysis
python3 ~/claude-skills/skills/trauma-evidence-forge-v3/scripts/audit_slide_design.py \
  ~/claude-skills/skills/trauma-evidence-forge-v3/projects/*/presentation-long-gamma.md --json
```

## Citation Verification

```bash
# Verify all PMIDs/DOIs in presentation files
python3 ~/claude-skills/skills/trauma-evidence-forge-v3/scripts/verify_citations.py ~/claude-skills/skills/trauma-evidence-forge-v3/projects/*/presentation.md
```

## Structure Check

```bash
# Verify skill directory structure is complete
ls -la ~/claude-skills/skills/trauma-evidence-forge-v3/references/ \
       ~/claude-skills/skills/trauma-evidence-forge-v3/templates/ \
       ~/claude-skills/skills/trauma-evidence-forge-v3/scripts/ \
       ~/claude-skills/skills/trauma-evidence-forge-v3/evals/ \
       ~/claude-skills/skills/trauma-evidence-forge-v3/commands/ \
       ~/claude-skills/skills/trauma-evidence-forge-v3/agents/ \
       ~/claude-skills/skills/trauma-evidence-forge-v3/projects/
```

## Quick Smoke Test

```bash
# Verify scripts are importable
python3 -c "import sys; sys.path.insert(0, '$HOME/claude-skills/skills/trauma-evidence-forge-v3/scripts'); import format_citations; print('format_citations OK')"
python3 -c "import sys; sys.path.insert(0, '$HOME/claude-skills/skills/trauma-evidence-forge-v3/scripts'); import preprocess_for_gamma; print('preprocess_for_gamma OK')"
python3 -c "import sys; sys.path.insert(0, '$HOME/claude-skills/skills/trauma-evidence-forge-v3/scripts'); import card_utils; print('card_utils OK')"
python3 -c "import sys; sys.path.insert(0, '$HOME/claude-skills/skills/trauma-evidence-forge-v3/scripts'); import audit_slide_design; print('audit_slide_design OK')"
```
