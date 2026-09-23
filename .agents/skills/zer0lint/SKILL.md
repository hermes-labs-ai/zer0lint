---
name: zer0lint
description: Use when an agent's memory backend reports successful ingestion but specific facts are missing on search. zer0lint checks add/search fact survival for compatible mem0 or HTTP backends; with a local mem0 config it can compare and apply a replacement extraction prompt. HTTP mode cannot isolate extraction or test a prompt change.
license: Apache-2.0
compatibility: Requires Python 3.9+; installs via pip. mem0 config mode needs `pip install "zer0lint[mem0]"`; HTTP mode needs no extra dependencies but requires an existing add/search memory endpoint.
---

# zer0lint

zer0lint checks whether synthetic facts survive an add/search round trip.
For local mem0 configs, it can compare the current extraction prompt with a
technical-fact prompt and update the config when the comparison improves.

## Use it for

- Checking whether injected facts survive a compatible backend's add/search
  round trip (`zer0lint check`)
- Comparing a replacement extraction prompt and applying it when the score
  improves in local mem0 config mode (`zer0lint generate`)
- Checking HTTP services that implement the documented JSON request contract
  (`--add-url` / `--search-url`)

## Do not use it for

- Pinpointing which stage lost a fact, especially in HTTP mode
- API connectivity failures or vector-store outages
- Proving one prompt fix generalizes beyond the synthetic technical/research
  facts it injects — always re-check the score on your own domain
- Proving production retrieval ranking or recall@k from a synthetic check

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

HTTP mode against a server that implements the documented add/search JSON contract:

```bash
pip install zer0lint
zer0lint check --add-url http://localhost:19420/add --search-url http://localhost:19420/recall_b
```

## Output shape

- `zer0lint check`: prints a score out of 5 injected facts, a percentage, and
  a status — `HEALTHY` (≥80%), `ACCEPTABLE` (60–79%), `DEGRADED` (40–59%), or
  `CRITICAL` (<40%) — plus which facts were dropped. Add/search errors return
  `INCONCLUSIVE` and a nonzero exit code.
- `zer0lint generate`: in mem0 config mode, compares prompts and only writes
  the new prompt if both phases are error-free and the re-tested score improves enough
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
- HTTP mode cannot validate a changed extraction prompt, so `generate` rejects
  HTTP flags before contacting the backend.
- This is a plain CLI/HTTP diagnostic, not an MCP server.

## More

Full docs and CLI reference:
https://github.com/hermes-labs-ai/zer0lint
