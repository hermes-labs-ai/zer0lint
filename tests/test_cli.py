from typer.testing import CliRunner

from zer0lint import cli


def test_generate_prints_cleanup_when_baseline_is_already_healthy(monkeypatch):
    monkeypatch.setattr(cli, "_load_config", lambda _path: ({}, "config.json"))
    monkeypatch.setattr(cli, "detect_extraction_model", lambda _config: "test-model")
    monkeypatch.setattr(cli, "configured_extraction_prompt", lambda _config: None)
    monkeypatch.setattr(
        cli,
        "run_generate",
        lambda **_kwargs: {
            "success": True,
            "verdict": "already_healthy",
            "cleanup": {
                "baseline": {
                    "mode": "delete",
                    "deleted": 4,
                    "attempted": 5,
                    "failed": 1,
                }
            },
        },
    )

    result = CliRunner().invoke(cli.app, ["generate", "--config", "config.json"])

    assert result.exit_code == 0
    assert "Cleanup (baseline): 4/5 test memories deleted (1 failed)" in result.stdout
    assert "already at 100%" in result.stdout


def test_generate_rejects_http_before_writing(monkeypatch):
    def unexpected_generate(**kwargs):
        raise AssertionError("generate must not run in HTTP mode")

    monkeypatch.setattr(cli, "run_generate", unexpected_generate)
    result = CliRunner().invoke(
        cli.app,
        ["generate", "--add-url", "http://localhost/add", "--search-url", "http://localhost/search"],
    )
    assert result.exit_code == 2
    assert "cannot test a changed extraction prompt" in result.output


def test_check_reports_http_transport_failure_as_inconclusive(monkeypatch):
    monkeypatch.setattr(
        cli,
        "run_check",
        lambda **kwargs: {
            "score": 0,
            "total": 1,
            "pct": 0,
            "status": "INCONCLUSIVE",
            "details": [],
            "failures": ["search(API endpoint): timeout"],
            "cleanup": {"mode": "isolated_no_delete", "user_id": "zer0lint_test"},
        },
    )
    result = CliRunner().invoke(
        cli.app,
        ["check", "--add-url", "http://localhost/add", "--search-url", "http://localhost/search"],
    )
    assert result.exit_code == 1
    assert "INCONCLUSIVE" in result.output
    assert "search(API endpoint): timeout" in result.output
