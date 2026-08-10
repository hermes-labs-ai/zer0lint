"""Apply generated extraction prompts to mem0 config."""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

CURRENT_EXTRACTION_PROMPT_FIELD = "custom_instructions"
LEGACY_EXTRACTION_PROMPT_FIELD = "custom_fact_extraction_prompt"


def resolve_extraction_prompt_field(memory_config_cls: type | None = None) -> str:
    """Return the extraction-instruction field supported by installed Mem0."""
    if memory_config_cls is None:
        try:
            from mem0.configs.base import MemoryConfig
        except ImportError:
            return CURRENT_EXTRACTION_PROMPT_FIELD
        memory_config_cls = MemoryConfig

    fields = getattr(memory_config_cls, "model_fields", None)
    if fields is None:
        fields = getattr(memory_config_cls, "__fields__", {})

    if CURRENT_EXTRACTION_PROMPT_FIELD in fields:
        return CURRENT_EXTRACTION_PROMPT_FIELD
    if LEGACY_EXTRACTION_PROMPT_FIELD in fields:
        return LEGACY_EXTRACTION_PROMPT_FIELD
    return CURRENT_EXTRACTION_PROMPT_FIELD


def configured_extraction_prompt(config: dict) -> object | None:
    """Read either current or legacy extraction instructions from a config."""
    if CURRENT_EXTRACTION_PROMPT_FIELD in config:
        return config[CURRENT_EXTRACTION_PROMPT_FIELD]
    return config.get(LEGACY_EXTRACTION_PROMPT_FIELD)


def backup_config(config_path: str | Path) -> str:
    """
    Backup the current config before modifying.

    Args:
        config_path: Path to mem0 config file

    Returns:
        Path to backup file
    """
    config_path = Path(config_path)
    backup_path = config_path.parent / f"{config_path.stem}.backup.{datetime.now().isoformat()}"
    shutil.copy2(config_path, backup_path)
    return str(backup_path)


def apply_prompt(
    config_path: str | Path, new_prompt: str, backup: bool = True
) -> dict:
    """
    Apply a new extraction prompt to mem0 config file.

    Args:
        config_path: Path to mem0 config.json
        new_prompt: The new extraction prompt to set
        backup: Whether to backup the original config (default True)

    Returns:
        Dict with keys: success (bool), backup_path (str), config_path (str), changes (dict)
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")

    # Read current config
    with open(config_path) as f:
        config = json.load(f)

    # Backup
    backup_path = None
    if backup:
        backup_path = backup_config(config_path)

    # Select the field supported by the installed Mem0 schema and migrate away
    # from the other spelling so strict config validation sees only one key.
    field = resolve_extraction_prompt_field()
    other_field = (
        LEGACY_EXTRACTION_PROMPT_FIELD
        if field == CURRENT_EXTRACTION_PROMPT_FIELD
        else CURRENT_EXTRACTION_PROMPT_FIELD
    )
    old_prompt = configured_extraction_prompt(config) or "(none)"

    # Apply new prompt
    config.pop(other_field, None)
    config[field] = new_prompt

    # Write back
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    return {
        "success": True,
        "config_path": str(config_path),
        "backup_path": backup_path,
        "changes": {
            "field": field,
            "old_length": len(old_prompt),
            "new_length": len(new_prompt),
        },
    }


def detect_extraction_model(config: dict) -> str:
    """
    Detect which LLM is configured for extraction in mem0 config.

    Args:
        config: Parsed mem0 config dict

    Returns:
        String describing the extraction model (e.g., "mistral:7b", "gpt-4o", "unknown")
    """
    # Most configs have an llm.config.model field
    llm_config = config.get("llm", {})
    if isinstance(llm_config, dict):
        if "config" in llm_config:
            model = llm_config["config"].get("model")
            if model:
                return model
        if "model" in llm_config:
            return llm_config["model"]

    return "unknown"


def detect_vector_store(config: dict) -> str:
    """
    Detect which vector store is configured in mem0.

    Args:
        config: Parsed mem0 config dict

    Returns:
        String describing the vector store (e.g., "chroma", "qdrant", "unknown")
    """
    vs_config = config.get("vector_store", {})
    if isinstance(vs_config, dict):
        provider = vs_config.get("provider")
        if provider:
            return provider
    return "unknown"
