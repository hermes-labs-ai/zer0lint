# r/LocalLLaMA draft

**Subreddit:** r/LocalLLaMA
**Flair:** Tool

---

**Title:** zer0lint - if your local model + mem0 setup has bad memory, this might be why

---

**Body:**

Found a nasty silent failure: when using local models (mistral:7b, qwen3.5:4b) with mem0, the default extraction prompt produces malformed JSON that gets silently dropped.

```
Error in new_retrieved_facts: Unterminated string starting at: line 1 column 10 (char 9)
```

`add()` still returns success. `search()` still returns results. Your agent just... forgets.

Tested on real data:
- mistral:7b + default mem0 config: 0/5 (0%) recall on technical facts
- mistral:7b + zer0lint extraction prompt: 5/5 (100%)
- qwen3.5:4b + default: 80%, with zer0lint: 100%

The fix is a `custom_fact_extraction_prompt` field in the mem0 config JSON. The tool generates a validated one and writes it to the right location (not via `add(text, prompt=X)` which is a no-op in mem0 v1.x).

```bash
pip install zer0lint
zer0lint check --config ~/.mem0/config.json   # measure
zer0lint generate --config ~/.mem0/config.json # fix
```

Also works via HTTP with cogito-ergo, Zep, or any custom memory endpoint.

GitHub: https://github.com/hermes-labs-ai/zer0lint

If you're running local models with mem0 - what's your extraction score? Would be curious to see results across different Ollama models.
