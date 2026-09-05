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
