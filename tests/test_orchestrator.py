"""Tests for backend isolation in the zer0lint orchestration flows."""

import sys
from types import SimpleNamespace

import pytest

from zer0lint import orchestrator


def _result(score: int, total: int = 1) -> dict:
    return {
        "score": score,
        "total": total,
        "details": [],
        "failures": [],
    }


def test_make_memory_uses_current_mem0_custom_instructions(monkeypatch):
    """Catch injecting the removed custom_fact_extraction_prompt into current Mem0."""
    seen = {}

    class FakeMemory:
        @classmethod
        def from_config(cls, config):
            seen.update(config)
            return cls()

    monkeypatch.setitem(sys.modules, "mem0", SimpleNamespace(Memory=FakeMemory))
    monkeypatch.setattr(
        orchestrator,
        "resolve_extraction_prompt_field",
        lambda: "custom_instructions",
    )

    orchestrator._make_memory(
        {"custom_fact_extraction_prompt": "stale"},
        custom_prompt="current prompt",
    )

    assert seen["custom_instructions"] == "current prompt"
    assert "custom_fact_extraction_prompt" not in seen


def test_make_memory_preserves_configured_prompt_for_baseline(monkeypatch):
    """Baseline checks must measure the user's current extraction configuration."""
    seen = {}

    class FakeMemory:
        @classmethod
        def from_config(cls, config):
            seen.update(config)
            return cls()

    monkeypatch.setitem(sys.modules, "mem0", SimpleNamespace(Memory=FakeMemory))

    orchestrator._make_memory({"custom_instructions": "configured baseline"})

    assert seen["custom_instructions"] == "configured baseline"


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


def test_mem0_checks_use_distinct_user_ids(monkeypatch):
    monkeypatch.setattr(orchestrator, "_make_backend", lambda **kwargs: SimpleNamespace())
    monkeypatch.setattr(
        orchestrator, "generate_test_facts_for_categories", lambda categories, count: [object()]
    )
    seen = []

    def validate(memory, facts, prompt, *, user_id, wait_seconds):
        seen.append(user_id)
        return _result(1)

    monkeypatch.setattr(orchestrator, "validate_extraction_prompt", validate)
    monkeypatch.setattr(orchestrator, "cleanup_test_memories", lambda *args, **kwargs: {})

    orchestrator.run_check(base_config={"llm": {}}, n_facts=1, wait_seconds=0)
    orchestrator.run_check(base_config={"llm": {}}, n_facts=1, wait_seconds=0)

    assert len(set(seen)) == 2
    assert all(uid.startswith("zer0lint_") and uid.endswith("_check") for uid in seen)


def test_mem0_generate_phases_share_run_id_but_have_distinct_user_ids(monkeypatch):
    monkeypatch.setattr(orchestrator, "_make_memory", lambda *args, **kwargs: SimpleNamespace())
    monkeypatch.setattr(
        orchestrator, "generate_test_facts_for_categories", lambda categories, count: [object()]
    )
    seen = []

    def validate(memory, facts, prompt, *, user_id, wait_seconds):
        seen.append(user_id)
        return _result(0)

    monkeypatch.setattr(orchestrator, "validate_extraction_prompt", validate)
    monkeypatch.setattr(orchestrator, "cleanup_test_memories", lambda *args, **kwargs: {})
    orchestrator.run_generate(base_config={"llm": {}}, n_facts=1, wait_seconds=0)

    assert len(seen) == 2
    assert seen[0].removesuffix("_baseline") == seen[1].removesuffix("_improved")
    assert seen[0] != seen[1]


def test_run_generate_rejects_http_before_writing(monkeypatch):
    def unexpected_backend(**kwargs):
        raise AssertionError("HTTP backend must not be contacted")

    monkeypatch.setattr(orchestrator, "_make_backend", unexpected_backend)
    with pytest.raises(ValueError, match="cannot test a changed extraction prompt"):
        orchestrator.run_generate(
            add_url="http://memory.test/add",
            search_url="http://memory.test/search",
        )


def test_run_check_reports_measurement_error_as_inconclusive(monkeypatch):
    monkeypatch.setattr(orchestrator, "_make_backend", lambda **kwargs: SimpleNamespace())
    monkeypatch.setattr(
        orchestrator, "generate_test_facts_for_categories", lambda categories, count: [object()]
    )
    monkeypatch.setattr(
        orchestrator, "validate_extraction_prompt",
        lambda *args, **kwargs: {**_result(0), "failures": ["search(API endpoint): timeout"]},
    )
    result = orchestrator.run_check(
        add_url="http://memory.test/add", search_url="http://memory.test/search", wait_seconds=0
    )
    assert result["status"] == "INCONCLUSIVE"


def test_run_generate_does_not_apply_after_measurement_error(monkeypatch):
    monkeypatch.setattr(orchestrator, "_make_memory", lambda *args, **kwargs: SimpleNamespace())
    monkeypatch.setattr(
        orchestrator, "generate_test_facts_for_categories", lambda categories, count: [object()]
    )
    scores = iter([_result(0), {**_result(1), "failures": ["search(API endpoint): timeout"]}])
    monkeypatch.setattr(orchestrator, "validate_extraction_prompt", lambda *args, **kwargs: next(scores))
    monkeypatch.setattr(orchestrator, "cleanup_test_memories", lambda *args, **kwargs: {})
    monkeypatch.setattr(
        orchestrator, "apply_prompt", lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("must not apply")
        )
    )

    result = orchestrator.run_generate(base_config={"llm": {}}, config_path="config.json", n_facts=1)
    assert result["success"] is False
    assert result["verdict"] == "measurement_error"
    assert result["applied"] is False


def test_run_generate_does_not_apply_after_failed_baseline_even_if_retest_is_clean(monkeypatch):
    monkeypatch.setattr(orchestrator, "_make_memory", lambda *args, **kwargs: SimpleNamespace())
    monkeypatch.setattr(
        orchestrator, "generate_test_facts_for_categories", lambda categories, count: [object()]
    )
    scores = iter([{**_result(0), "failures": ["search: timeout"]}, _result(1)])
    monkeypatch.setattr(orchestrator, "validate_extraction_prompt", lambda *args, **kwargs: next(scores))
    monkeypatch.setattr(orchestrator, "cleanup_test_memories", lambda *args, **kwargs: {})
    applied = []

    def apply(config_path, prompt, backup):
        applied.append((config_path, prompt, backup))
        raise AssertionError("must not apply")

    monkeypatch.setattr(orchestrator, "apply_prompt", apply)

    result = orchestrator.run_generate(base_config={"llm": {}}, config_path="config.json", n_facts=1)
    assert result["success"] is False
    assert result["verdict"] == "measurement_error"
    assert result["applied"] is False
    assert result["initial_score"] == 0
    assert result["improved_score"] == 1
    assert result["baseline_failures"] == ["search: timeout"]
    assert not applied


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
