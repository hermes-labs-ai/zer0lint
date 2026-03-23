"""Environment scanner — inspects the system to understand what it needs to remember."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


def scan_environment(root: Path | None = None) -> dict:
    """
    Scan the user's environment to identify what kind of system this is.

    Looks at:
    - Git repos and their dominant file types
    - Recent shell history (what tools/commands they run)
    - Working directory structure (docs, code, data, etc.)
    - Current mem0 extraction prompt (what it's currently trying to do)

    Returns a dict of signals that describe the system's context.
    """
    root = root or Path.home()
    signals = {
        "file_types": [],
        "tools_detected": [],
        "repo_topics": [],
        "shell_patterns": [],
        "raw_summary": "",
    }

    # 1. Detect dominant file types in common project dirs
    project_dirs = [
        Path.home() / "Documents" / "projects",
        Path.home() / "projects",
        Path.home() / "code",
        Path.cwd(),
    ]
    ext_counts: dict[str, int] = {}
    for pdir in project_dirs:
        if pdir.exists():
            for p in pdir.rglob("*"):
                if p.is_file() and not any(
                    part.startswith(".") for part in p.parts[-3:]
                ):
                    ext = p.suffix.lower()
                    if ext:
                        ext_counts[ext] = ext_counts.get(ext, 0) + 1

    # Top 10 file extensions
    top_exts = sorted(ext_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    signals["file_types"] = [ext for ext, _ in top_exts]

    # 2. Detect tools from shell history
    history_files = [
        Path.home() / ".zsh_history",
        Path.home() / ".bash_history",
    ]
    tool_keywords = {
        "python": "Python/ML development",
        "pip": "Python packaging",
        "git": "Version control",
        "docker": "Containerization",
        "kubectl": "Kubernetes",
        "cargo": "Rust development",
        "npm": "Node.js development",
        "pytest": "Python testing",
        "curl": "API/HTTP work",
        "ollama": "Local LLM usage",
        "gh": "GitHub CLI",
        "psql": "PostgreSQL",
        "redis": "Redis",
        "aws": "AWS infrastructure",
    }
    found_tools = set()
    for hfile in history_files:
        if hfile.exists():
            try:
                text = hfile.read_text(errors="ignore")[-50000:]  # Last 50KB
                for tool, desc in tool_keywords.items():
                    if tool in text:
                        found_tools.add(desc)
            except Exception:
                pass
    signals["tools_detected"] = list(found_tools)

    # 3. Detect repo topics from git repos
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-50", "--all"],
            capture_output=True, text=True, timeout=5,
            cwd=str(Path.home() / "Documents" / "projects"),
        )
        if result.returncode == 0:
            commits = result.stdout.lower()
            topic_keywords = {
                "research": ["experiment", "hypothesis", "paper", "study", "dataset"],
                "infrastructure": ["deploy", "config", "server", "port", "migrate"],
                "ml": ["model", "training", "embedding", "llm", "inference"],
                "security": ["auth", "token", "inject", "audit", "policy"],
                "api": ["endpoint", "api", "rest", "graphql", "webhook"],
            }
            for topic, kws in topic_keywords.items():
                if any(kw in commits for kw in kws):
                    signals["repo_topics"].append(topic)
    except Exception:
        pass

    # 4. Check current mem0 extraction prompt
    mem0_config = Path.home() / ".mem0" / "config.json"
    current_prompt = None
    if mem0_config.exists():
        try:
            import json
            config = json.loads(mem0_config.read_text())
            current_prompt = config.get("custom_fact_extraction_prompt")
        except Exception:
            pass

    # 5. Build raw summary for LLM
    lines = []
    if signals["file_types"]:
        lines.append(f"Dominant file types: {', '.join(signals['file_types'][:5])}")
    if signals["tools_detected"]:
        lines.append(f"Tools used: {', '.join(signals['tools_detected'][:8])}")
    if signals["repo_topics"]:
        lines.append(f"Work topics: {', '.join(signals['repo_topics'])}")
    if current_prompt:
        lines.append(f"Current extraction prompt (first 200 chars): {current_prompt[:200]}")
    else:
        lines.append("Current extraction prompt: default (not customized)")

    signals["raw_summary"] = "\n".join(lines)
    signals["current_prompt"] = current_prompt

    return signals
