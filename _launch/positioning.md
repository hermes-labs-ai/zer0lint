# Positioning - zer0lint

## Why now

Three forces converged in early 2026 that make zer0lint relevant today:

1. **mem0 adoption tipped.** mem0ai crossed 1M PyPI downloads and became the default memory layer for LangChain, LlamaIndex, and custom agent stacks. More devs are hitting memory bugs than ever - but the bugs are silent. No error, no warning. Just an agent that doesn't remember.

2. **Local model proliferation.** Ollama and similar tools moved smaller models (mistral:7b, qwen3.5:4b) into production agent pipelines. These models follow the default mem0 extraction prompt poorly - producing malformed JSON that gets silently dropped. The problem is model-dependent and has gotten worse as devs swap GPT-4 for local models in cost-cutting cycles.

3. **No tooling exists for this layer.** There is retrieval benchmarking (RAGAs, RAGAS), there is prompt testing (promptfoo, PromptLayer), but there is no tool that specifically measures extraction health - the step where raw text becomes structured facts in the store. zer0lint fills that gap.

The EU AI Act (August 2026 deadline) adds urgency for enterprises: AI systems must be auditable and traceable. A memory system that silently drops facts is neither.

## ICP

**The specific person:** A backend or ML engineer at a company with 5-50 engineers, building an AI assistant or agent that uses persistent memory. They've deployed mem0 or a similar system, the product is in beta or early production, and they've started getting user reports that "the AI forgot what I told it last week." They're looking at retrieval logs, seeing 90% hit rates, and can't figure out why the agent still gets things wrong.

They're willing to run one CLI command to diagnose. They are not willing to read a 40-page debugging guide. They use Ollama or OpenAI, they trust pip-installable tools, and they have seen at least one JSON parse error in their mem0 logs.

**Company types:** AI product studios, developer tools startups, enterprise teams building internal AI assistants, AI agent infrastructure companies.

**Willingness to try:** High. It's one command, read-only by default, no API keys required, installs in seconds.

## Competitor delta

| Competitor | What it does | Why zer0lint is different |
|---|---|---|
| Manual spot-check | Developer adds a fact, searches for it, checks the result | zer0lint runs 5 typed facts across 5 domains, scores them, and generates a validated fix. No manual work. |
| mem0 debug logs | Inspect JSON parse errors in the extraction logs | Logs show that extraction failed; they do not tell you by how much or how to fix it. zer0lint measures the failure rate and writes the fix. |
| Do nothing | Assume memory works until users complain | Silent failure is the default state. Retrieval benchmarks (90%+ hit@any) look healthy even when extraction is at 0%. zer0lint catches this case. |

No other tool specifically targets the mem0 `custom_fact_extraction_prompt` field. That's not a niche - it's the documented correct location for extraction customization that mem0 itself does not make easy to test.

## Adjacent interests

**If you use cogito-ergo:** zer0lint is the upstream prerequisite. cogito-ergo's 83%+ R@1 on LongMemEval depends on clean extraction. Running zer0lint before deploying cogito-ergo is the documented pipeline order.

**If you care about RAGAs / RAGAS benchmarks:** Those tools measure retrieval quality. zer0lint measures ingestion quality - the step before retrieval. A 90% retrieval score on bad data is still bad data. zer0lint is the missing first step in RAG evaluation pipelines.

**If you work on AI auditing (EU AI Act, ISO 42001):** Memory systems that silently drop facts are a traceability risk. zer0lint gives you a quantitative score for extraction health that can be included in audit trails and CI gates.
