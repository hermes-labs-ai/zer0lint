# PR draft: vinta/awesome-python

**Target repo:** https://github.com/vinta/awesome-python
**Last updated:** 2026-04-17 (actively maintained)
**Category to add under:** Testing

---

**PR Title:** Add zer0lint to Testing section - AI memory extraction diagnostics

**PR Body:**

## zer0lint

Adding `zer0lint` to the Testing section.

**What it is:**
zer0lint is a Python CLI tool for measuring and fixing AI memory extraction health. It injects synthetic facts into a mem0 (or HTTP-compatible) memory system, measures round-trip recall, and generates a validated extraction prompt if the score is below threshold. Primarily used to diagnose silent extraction failures where `add()` returns success but facts are not recoverable.

**Why it fits "Testing":**
- Automated measurement of extraction pipeline correctness
- Provides a numeric health score (HEALTHY/ACCEPTABLE/DEGRADED/CRITICAL)
- Can be run in CI as a health check (non-zero exit on CRITICAL/DEGRADED)
- Zero side effects in check mode (no data modification)

**Entry to add:**

```markdown
- [zer0lint](https://github.com/roli-lpci/zer0lint) - AI memory extraction diagnostics. Tests whether facts added to a mem0 (or any HTTP memory endpoint) survive the LLM extraction step and are retrievable.
```

**Links:**
- Repo: https://github.com/roli-lpci/zer0lint
- PyPI: https://pypi.org/project/zer0lint/
- License: Apache 2.0

---

**Roli's notes before submitting:**
1. Check the current Testing section in vinta/awesome-python - zer0lint may fit better under "AI" if that section is more active
2. vinta/awesome-python has strict quality standards - confirm the repo has: passing tests, PyPI package, active maintenance
3. The PR description should note the CI health-check use case (exit codes on failure) since that makes the "Testing" category fit natural
