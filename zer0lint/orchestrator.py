"""Main orchestrator for zer0lint generate flow."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from zer0lint.analyzer import analyze_with_llm, fallback_prompt_from_patterns
from zer0lint.fixer import apply_prompt
from zer0lint.scanner import scan_environment
from zer0lint.tester import generate_test_facts_for_categories, validate_extraction_prompt


def run_generate(
    memory: object,
    config_path: Optional[str | Path] = None,
    verbose: bool = False,
) -> dict:
    """
    Full zer0lint generate flow:
      scan environment → diagnose current extraction → generate prompt → test → apply.

    Steps:
    1. Scan environment (repos, shell history, file types, current prompt)
    2. Check current extraction: inject 5 test facts, score them
    3. If score < 4: generate new prompt from environment signals
    4. Test the generated prompt
    5. Apply if score >= 4/5

    Args:
        memory: mem0.Memory instance (initialized with user's config)
        config_path: Path to mem0 config.json (for applying the fix)
        verbose: Print detailed output

    Returns dict with: success, initial_score, final_score, generated_prompt, applied, backup_path
    """

    result = {
        "success": False,
        "initial_score": None,
        "final_score": None,
        "generated_prompt": None,
        "applied": False,
        "backup_path": None,
        "iteration_log": [],
    }

    try:
        # Step 1: Scan environment
        if verbose:
            print("[1/4] Scanning environment...")
        env = scan_environment()
        if verbose:
            print(f"  File types: {env['file_types'][:5]}")
            print(f"  Tools: {env['tools_detected'][:5]}")
            print(f"  Topics: {env['repo_topics']}")
            prompt_status = "custom" if env.get("current_prompt") else "default (not customized)"
            print(f"  Current extraction prompt: {prompt_status}")
        result["iteration_log"].append(f"Environment scanned: {env['raw_summary'][:100]}")

        # Step 2: Diagnose current extraction with a quick 5-fact check
        if verbose:
            print("\n[2/4] Diagnosing current extraction quality...")

        # Use environment signals to pick relevant test categories
        detected_categories = env.get("repo_topics", [])
        if not detected_categories:
            # Fallback: infer from file types
            file_types = env.get("file_types", [])
            if any(ext in file_types for ext in [".py", ".js", ".ts", ".go", ".rs"]):
                detected_categories = ["technical"]
            else:
                detected_categories = ["technical"]  # safe default

        test_facts = generate_test_facts_for_categories(detected_categories, count=5)
        initial_result = validate_extraction_prompt(memory, test_facts, prompt="current")
        initial_score = initial_result["score"]
        result["initial_score"] = initial_score

        if verbose:
            print(f"  Current extraction score: {initial_score}/5")
            for i, fact in enumerate(test_facts):
                status = "✅" if initial_result["results"][i] else "❌"
                print(f"    {status} {fact.label}")

        result["iteration_log"].append(
            f"Baseline extraction: {initial_score}/5 with categories {detected_categories}"
        )

        # Step 3: If already good (>= 4), report and skip generation
        if initial_score >= 4:
            if verbose:
                print(f"\n✓ Current extraction is healthy ({initial_score}/5). No changes needed.")
            result["success"] = True
            result["final_score"] = initial_score
            result["iteration_log"].append("Extraction already healthy — no prompt change needed")
            return result

        # Step 4: Generate new prompt from environment signals
        if verbose:
            print(f"\n[3/4] Extraction score is {initial_score}/5 — generating optimized prompt...")

        try:
            generated_prompt = analyze_with_llm(memory.config.llm, env["raw_summary"])
            if verbose:
                print("  ✓ Generated prompt via LLM analysis of environment")
            result["iteration_log"].append("Generated prompt from environment via LLM")
        except Exception as e:
            if verbose:
                print(f"  ⚠ LLM failed ({e}), using pattern-based fallback")
            # Infer patterns from environment signals
            patterns = {}
            if "Python/ML development" in env.get("tools_detected", []) or \
               ".py" in env.get("file_types", []):
                patterns["technical"] = ["port", "version", "model", "config", "api"]
            if "research" in detected_categories:
                patterns["research"] = ["hypothesis", "experiment", "dataset", "finding"]
            generated_prompt = fallback_prompt_from_patterns(patterns)
            result["iteration_log"].append("Generated prompt via pattern fallback (LLM unavailable)")

        # Step 5: Test the generated prompt
        if verbose:
            print("\n[4/4] Testing generated prompt...")
        final_result = validate_extraction_prompt(memory, test_facts, prompt=generated_prompt)
        final_score = final_result["score"]
        result["final_score"] = final_score
        result["generated_prompt"] = generated_prompt

        if verbose:
            print(f"  Generated prompt score: {final_score}/5")
            for i, fact in enumerate(test_facts):
                status = "✅" if final_result["results"][i] else "❌"
                print(f"    {status} {fact.label}")

        result["iteration_log"].append(f"Generated prompt scored: {final_score}/5")

        # Step 6: Apply if score improved and >= 4
        if config_path and final_score >= 4:
            apply_result = apply_prompt(config_path, generated_prompt, backup=True)
            result["applied"] = apply_result["success"]
            result["backup_path"] = apply_result["backup_path"]
            result["iteration_log"].append("Prompt applied to config")
            if verbose:
                print(f"\n✓ Prompt applied ({initial_score}/5 → {final_score}/5)")
                if apply_result["backup_path"]:
                    print(f"  Backup: {apply_result['backup_path']}")
        elif config_path and final_score < 4:
            if verbose:
                print(f"\n⚠ Generated prompt scored {final_score}/5 — not applying (threshold: 4/5)")
            result["iteration_log"].append(
                f"Prompt NOT applied — score {final_score}/5 below threshold"
            )

        result["success"] = True

    except Exception as e:
        result["iteration_log"].append(f"ERROR: {e}")
        if verbose:
            print(f"\n✗ Generation failed: {e}")

    return result
