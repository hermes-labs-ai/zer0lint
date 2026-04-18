# Paper Decision - zer0lint

## Novelty signals found

**Empirical results (README, llms.txt, cogito memory):**

1. "mistral:7b with default mem0 config: 0/5 (0%) on 5 typed technical facts" (2026-03-22)
2. "Same model with zer0lint extraction prompt: 5/5 (100%)" - +100 percentage points
3. "qwen3.5:4b: 80% default, 100% with zer0lint prompt" (+20pp)
4. "Scale test, 10 facts, 5 domains: 7/10 default vs 9/10 zer0lint" (+20pp at scale)
5. From cogito memory: "zer0lint ran against cogito_main corpus got 0/5 (CRITICAL) and fixed it to 5/5 (+100pp)" - this is a PRODUCTION deployment result, not a curated demo

**Structural insight (README, agents.md):**

The `custom_fact_extraction_prompt` field behavior in mem0 v1.x: passing prompt via `memory.add(..., prompt=X)` has zero effect on extraction. This is undocumented and non-obvious. The fix requires config-level injection. zer0lint is the only tool that validates this field works before writing to it.

**Code-level evidence:**

- `zer0lint/tester.py`: 5 typed synthetic fact categories (exact phrase, paraphrase, negation, multi-fact, entity reference) - a typed test protocol, not random sampling
- `zer0lint/orchestrator.py`: 3-phase validate-before-apply protocol (baseline, retest, conditional apply)
- `zer0lint/http_adapter.py`: universal HTTP mode - the diagnostic is backend-agnostic

## Prior art

The closest published work would be:

1. mem0 documentation (docs.mem0.ai) - does not describe extraction health testing or the `add(..., prompt=X)` no-op behavior
2. RAGAs / RAGAS (paper: "RAGAS: Automated Evaluation of Retrieval Augmented Generation", Es et al., 2023) - measures retrieval, not extraction
3. Benchmarks for LLM-based information extraction (various EMNLP/ACL papers) - general IE, not specific to agent memory pipelines with the mem0 silent-failure pattern

No directly competing published work was found on diagnosing the extraction layer in mem0-style memory systems.

## Recommendation

**`blog-only`**

## Confidence

0.70

What would raise confidence to `publish-workshop`: a systematic study across 5+ models with n>=50 test cases per model, measuring the relationship between model size/family and extraction failure rate. The current dataset (2 models, 5-10 facts) is too small for a credible paper. The finding is real and replicable, but the sample size doesn't meet conference bar.

## Reasoning

- The 0->100pp finding is genuine and empirical. It happened on production data (cogito_main corpus, 2026-03-22) not a curated benchmark.
- The `add(..., prompt=X)` no-op behavior is a real undocumented bug/limitation worth publishing.
- BUT: 2 models and one corpus is not enough data for a publishable result. A reviewer would ask "does this hold across model families, sizes, providers?"
- The structural insight (config vs call-level extraction) is more suitable for a technical blog post where the audience is practitioners, not for a workshop paper where the audience is researchers.
- A blog post with zer0lint as the artifact is the correct vehicle. If Roli runs a systematic multi-model study for v0.3 (5+ models, multiple domains, n=50+), that data could support a short paper at MemSys, ACL Workshop on Agent Memory, or similar.
