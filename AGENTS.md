# AGENTS.md

`zer0lint` checks whether facts survive a memory backend's add/search round trip. For a local mem0 config, it can compare and apply a better extraction prompt.

## Use it for

- checking whether facts survive Mem0 or compatible HTTP add/search endpoints
- comparing a replacement prompt for a local mem0 config
- verifying fact survival before tuning the memory pipeline

## Do not use it for

- diagnosing which HTTP pipeline stage lost a fact
- vector-store outages or API credential failures
- proving a generated prompt will generalize to every model or domain

## Minimal commands

```bash
pip install -e ".[dev]"
zer0lint check --config ~/.mem0/config.json
zer0lint generate --config ~/.mem0/config.json --dry-run
pytest -q
```

## Output shape

- `check` prints a score, percentage, status, and per-fact details
- `generate` prints before/after scores, delta in percentage points, and whether a prompt was applied or saved

## Success means

- `check` gives a HEALTHY, ACCEPTABLE, DEGRADED, CRITICAL, or INCONCLUSIVE verdict
- `generate` only writes a mem0 config when both phases are error-free and the re-test improves enough
- backups are created before config writes in mem0 mode

## Common failure cases

- users tune prompts or retrieval without checking fact survival
- `--config` is mixed with `--add-url` or `--search-url`
- a team expects `memory.add(..., prompt=...)` to override extraction behavior in mem0

Current Mem0 stores extraction guidance in `custom_instructions`. Older supported
schemas used `custom_fact_extraction_prompt`; zer0lint detects the installed schema
and writes only the field it accepts.

`check` and `generate` clean up the test facts they write after each phase (mem0
mode deletes them; HTTP mode isolates by user_id only) and return the outcome as
a machine-readable `cleanup` receipt (`attempted`/`deleted`/`failed`/`errors`) —
see README "Side Effects & Recovery" for the full contract.

HTTP `generate` is unsupported: add/search endpoints cannot test a changed
extraction prompt. Use `check` for HTTP fact survival and investigate extraction
versus search in the backend.
