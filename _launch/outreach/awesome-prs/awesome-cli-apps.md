# PR draft: agarrharr/awesome-cli-apps

**Target repo:** https://github.com/agarrharr/awesome-cli-apps
**Last updated:** 2026-04-13 (active)
**Category to add under:** Development > Testing

---

**PR Title:** Add zer0lint - AI memory extraction diagnostics

**PR Body:**

## zer0lint

Adding `zer0lint` - a CLI tool for diagnosing silent extraction failures in AI agent memory systems (mem0 and compatible).

**Why it fits:**
- Pure CLI tool (`pip install zer0lint`, then `zer0lint check` / `zer0lint generate`)
- Solves a specific developer pain point: AI memory pipelines that return success codes but silently drop facts
- Read-only by default (`zer0lint check` makes no changes)
- No API keys or accounts required for basic use

**Entry to add:**

Under "AI / Machine Learning" or "Development / Testing":

```markdown
- [zer0lint](https://github.com/hermes-labs-ai/zer0lint) - Diagnoses silent mem0 extraction failures. Injects synthetic facts, measures round-trip recall, and generates a validated extraction prompt if needed.
```

**Links:**
- Repo: https://github.com/hermes-labs-ai/zer0lint
- PyPI: https://pypi.org/project/zer0lint/
- License: Apache 2.0

---

**Roli's notes before submitting:**
1. Find the correct section header in the current README (may be "AI / Machine Learning", "Developer Tools", or "Miscellaneous")
2. Check if there is a section for diagnostic/testing tools - that's the most accurate fit
3. The PR should only change one line in the README
