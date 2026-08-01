"""Tests for backend isolation in the zer0lint orchestration flows."""

from types import SimpleNamespace

from zer0lint import orchestrator


def _result(score: int, total: int = 1) -> dict:
    return {
        "score": score,
        "total": total,
        "details": [],
        "failures": [],
    }


def test_run_check_uses_http_adapters_isolated_user_id(monkeypatch):
    backend = SimpleNamespace(default_user_id="zer0lint_random-check")
    seen_user_ids = []

    monkeypatch.setattr(orchestrator, "_make_backend", lambda **kwargs: backend)
    monkeypatch.setattr(
        orchestrator,
        "generate_test_facts_for_categories",
        lambda categories, count: [object()],
    )

    def validate(memory, facts, prompt, *, user_id, wait_seconds):
        seen_user_ids.append(user_id)
        return _result(1)

    monkeypatch.setattr(orchestrator, "validate_extraction_prompt", validate)

    result = orchestrator.run_check(
        add_url="http://memory.test/add",
        search_url="http://memory.test/search",
        wait_seconds=0,
    )

    assert result["status"] == "HEALTHY"
    assert seen_user_ids == [backend.default_user_id]


def test_run_generate_uses_each_http_adapters_isolated_user_id(monkeypatch):
    backends = iter(
        [
            SimpleNamespace(default_user_id="zer0lint_random-baseline"),
            SimpleNamespace(default_user_id="zer0lint_random-improved"),
        ]
    )
    seen_user_ids = []

    monkeypatch.setattr(orchestrator, "_make_backend", lambda **kwargs: next(backends))
    monkeypatch.setattr(
        orchestrator,
        "generate_test_facts_for_categories",
        lambda categories, count: [object()],
    )

    def validate(memory, facts, prompt, *, user_id, wait_seconds):
        seen_user_ids.append(user_id)
        return _result(len(seen_user_ids) - 1)

    monkeypatch.setattr(orchestrator, "validate_extraction_prompt", validate)

    result = orchestrator.run_generate(
        add_url="http://memory.test/add",
        search_url="http://memory.test/search",
        n_facts=1,
        wait_seconds=0,
    )

    assert result["success"] is True
    assert seen_user_ids == [
        "zer0lint_random-baseline",
        "zer0lint_random-improved",
    ]


def test_run_generate_suffixes_explicit_http_user_id_by_phase(monkeypatch):
    backend = SimpleNamespace(default_user_id="portfolio-check")
    seen_user_ids = []

    monkeypatch.setattr(orchestrator, "_make_backend", lambda **kwargs: backend)
    monkeypatch.setattr(
        orchestrator,
        "generate_test_facts_for_categories",
        lambda categories, count: [object()],
    )

    def validate(memory, facts, prompt, *, user_id, wait_seconds):
        seen_user_ids.append(user_id)
        return _result(len(seen_user_ids) - 1)

    monkeypatch.setattr(orchestrator, "validate_extraction_prompt", validate)

    result = orchestrator.run_generate(
        add_url="http://memory.test/add",
        search_url="http://memory.test/search",
        http_user_id="portfolio-check",
        n_facts=1,
        wait_seconds=0,
    )

    assert result["success"] is True
    assert seen_user_ids == ["portfolio-check_baseline", "portfolio-check_improved"]


def test_http_adapter_exposes_generated_or_overridden_user_id(monkeypatch):
    from zer0lint.http_adapter import HttpMemoryAdapter

    generated = HttpMemoryAdapter("http://memory.test/add", "http://memory.test/search")
    overridden = HttpMemoryAdapter(
        "http://memory.test/add",
        "http://memory.test/search",
        user_id="portfolio-check",
    )

    assert generated.default_user_id.startswith("zer0lint_")
    assert overridden.default_user_id == "portfolio-check"
