---
name: zer0lint
description: Use when an agent's memory system (mem0 config, or any HTTP memory API with add/search endpoints) reports successful ingestion but the agent keeps forgetting facts — zer0lint injects known facts, measures round-trip recall through the LLM extraction step, and generates a stronger extraction prompt validated on your own model. Deterministic diagnostic, no MCP.
license: Apache-2.0
compatibility: Requires Python 3.9+; installs via pip. mem0 config mode needs `pip install "zer0lint[mem0]"`; HTTP mode needs no extra dependencies but requires an existing add/search memory endpoint.
---

# zer0lint

zer0lint is a memory-extraction health diagnostic for mem0 configs and HTTP
memory endpoints. It flags the silent failure mode where ingestion reports
success but facts never survive the LLM extraction step, then generates a
stronger extraction prompt validated on your own model before writing it to
config.

## Use it for

- Diagnosing whether a mem0-backed or custom HTTP memory system's extraction
  step is actually preserving injected facts (`zer0lint check`)
- Generating and validating a replacement extraction prompt, only writing it
  back if it measurably improves the score (`zer0lint generate`)
- Checking any custom memory API that exposes add/search over HTTP, not just
  mem0 (`--add-url` / `--search-url`)
- Ruling out extraction as the cause before spending time tuning retrieval
  ranking or ingestion

## Do not use it for

- Vector-store outages, API connectivity failures, or other non-extraction
  memory bugs
- Proving one prompt fix generalizes beyond the synthetic technical/research
  facts it injects — always re-check the score on your own domain
- Debugging retrieval ranking or recall@k — zer0lint checks the extraction
  step only

## Quickstart

```bash
pip install "zer0lint[mem0]"
zer0lint check --config ~/.mem0/config.json
```

If the score is below 80%:

```bash
zer0lint generate --config ~/.mem0/config.json --dry-run
zer0lint generate --config ~/.mem0/config.json
```

HTTP mode against any memory server (no mem0 dependency):

```bash
pip install zer0lint
zer0lint check --add-url http://localhost:19420/add --search-url http://localhost:19420/recall_b
```

## Output shape

- `zer0lint check`: prints a score out of 5 injected facts, a percentage, and
  a status — `HEALTHY` (≥80%), `ACCEPTABLE` (60–79%), `DEGRADED` (40–59%), or
  `CRITICAL` (<40%) — plus which facts were dropped
- `zer0lint generate`: three phases (baseline, re-test, apply) and only
  writes the new prompt to config if the re-tested score improves
- Cleanup receipts: `{"mode": "delete", "user_id": ..., "attempted": N,
  "deleted": N, "failed": N, "errors": [...]}`

## Common gotchas

- Per-call prompts passed to `memory.add(..., prompt=...)` have no effect in
  Mem0 — extraction instructions must live in config, which is exactly what
  `zer0lint generate` writes.
- `zer0lint generate` always backs up the original config with an ISO
  timestamp before writing.
- HTTP mode does not delete its test facts (no documented delete endpoint);
  isolation relies on a per-run random `user_id`, and the receipt reports
  `"mode": "isolated_no_delete"` to make that explicit.
- This is a plain CLI/HTTP diagnostic, not an MCP server.

## More

Full docs and CLI reference:
https://github.com/hermes-labs-ai/zer0lint
