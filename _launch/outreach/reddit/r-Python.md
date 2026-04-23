# r/Python draft

**Subreddit:** r/Python
**Flair:** Showcase

---

**Title:** zer0lint - diagnose silent mem0 extraction failures (0% to 100% in one command)

---

**Body:**

I built a small CLI tool to diagnose a specific, silent failure mode in mem0-based agent memory: `add()` returns success, `search()` returns results, but your extraction LLM is quietly producing malformed JSON and dropping facts.

Discovery: tested mistral:7b with default mem0 config on 5 technical facts. Score: 0/5 (0%). Same model with a config-level extraction prompt: 5/5 (100%). No other changes.

The trap most devs hit: in mem0 v1.x, passing `memory.add(text, prompt="custom")` has zero effect on extraction. The extraction prompt must live in `custom_fact_extraction_prompt` in the config JSON. zer0lint writes the fix to the right field (with a backup).

**Install:**
```bash
pip install zer0lint
zer0lint check --config ~/.mem0/config.json
zer0lint generate --config ~/.mem0/config.json  # if score < 80%
```

Also works over HTTP with any memory system:
```bash
zer0lint check --add-url http://localhost:19420/add --search-url http://localhost:19420/recall_b
```

GitHub: https://github.com/hermes-labs-ai/zer0lint | Apache 2.0

Happy to answer questions about how the extraction prompt works or why `add(..., prompt=X)` is a no-op.
