# AGENTS.md

`zer0lint` diagnoses silent memory extraction failures and can generate a better extraction prompt when the baseline is bad.

## Use it for

- checking whether facts survive the extraction step
- verifying mem0 config behavior before tuning retrieval
- testing any memory service with HTTP add/search endpoints

## Do not use it for

- vector-store outages
- API credential failures
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

- `check` gives a clear HEALTHY, ACCEPTABLE, DEGRADED, or CRITICAL verdict
- `generate` only writes when the improved prompt actually performs better
- backups are created before config writes in mem0 mode

## Common failure cases

- users debug retrieval before confirming extraction health
- `--config` is mixed with `--add-url` or `--search-url`
- a team expects `memory.add(..., prompt=...)` to override extraction behavior in mem0
