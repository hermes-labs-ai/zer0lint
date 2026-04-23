# X / Twitter Thread

---

**Tweet 1 (hook):**
We ran zer0lint against a real mem0 production corpus (mistral:7b, default config).

Extraction score: 0/5 (0%).

After one config change: 5/5 (100%).

The failure was completely silent. Thread on how this works.

---

**Tweet 2:**
The failure mode: mem0's extraction LLM produces malformed JSON on smaller models.

```
Unterminated string starting at: line 1 column 10
Expecting ',' delimiter: line 1 column 13
```

add() returns success. search() returns results. Your agent just... forgets. No error.

---

**Tweet 3:**
The common fix attempt doesn't work:

```python
memory.add("fact", prompt="Extract technical facts")
```

In mem0 v1.x, the `prompt` parameter to add() has no effect on extraction. Zero. No error either.

The fix must go in config: `custom_fact_extraction_prompt`.

---

**Tweet 4:**
zer0lint automates three things:

1. Measure: inject 5 typed facts, score round-trip recall
2. Generate: test a domain-aware extraction prompt  
3. Apply: write it to config only if score improves

```bash
pip install zer0lint
zer0lint check --config ~/.mem0/config.json
zer0lint generate --config ~/.mem0/config.json
```

---

**Tweet 5:**
Numbers from 2026-03-22, five technical facts:

mistral:7b | default: 0% | zer0lint: 100% (+100pp)
qwen3.5:4b | default: 80% | zer0lint: 100% (+20pp)

Improvement is larger on models that struggle with structured JSON output.

---

**Tweet 6:**
Also works via HTTP - no mem0 dependency:

```bash
zer0lint check \
  --add-url http://localhost:19420/add \
  --search-url http://localhost:19420/recall_b
```

Works with cogito-ergo, Zep, LangMem, or any custom HTTP memory API.

---

**Tweet 7:**
Open source, Apache 2.0, part of the Hermes Labs agent tooling suite.

If you run agent memory on local models - check your extraction score first. Retrieval benchmarks look healthy even when extraction is at 0%.

github.com/hermes-labs-ai/zer0lint
pypi.org/project/zer0lint/
