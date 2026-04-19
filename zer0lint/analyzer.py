"""Generate extraction prompt from environment signals."""

from __future__ import annotations


def analyze_with_llm(llm: object, environment_summary: str) -> str:
    """
    Use LLM to generate a domain-specific extraction prompt from environment signals.

    Args:
        llm: mem0's configured LLM instance (any provider)
        environment_summary: Text describing the system environment (from scanner)

    Returns:
        A domain-specific extraction prompt tailored to the environment
    """

    analysis_prompt = f"""You are an expert at designing memory extraction prompts for AI agents.

Here is a description of the system environment you're designing a prompt for:

---
{environment_summary}
---

Based on this environment, write a mem0 custom_fact_extraction_prompt that will capture
the most important facts this system needs to remember.

The prompt should:
1. Identify 5-8 specific categories of facts this system deals with
2. Be specific to the actual work (not generic)
3. Include 2-3 concrete examples (Input → Output in JSON)
4. End with: Return facts as JSON with key "facts" and a list of strings. Extract generously.

Return ONLY the prompt text. No explanation, no markdown, no preamble. Start writing now:"""

    try:
        response = llm.chat_completion(
            messages=[{"role": "user", "content": analysis_prompt}],
            temperature=0.3,
        )
        if isinstance(response, dict):
            prompt_text = response.get("message", response.get("content", ""))
        else:
            prompt_text = str(response)
        return prompt_text.strip()
    except Exception as e:
        raise RuntimeError(f"LLM analysis failed: {e}")


def fallback_prompt_from_patterns(patterns: dict[str, list[str]]) -> str:
    """
    Generate a basic extraction prompt from detected patterns when LLM is unavailable.
    """
    if not patterns:
        return (
            "Extract all factual information from the conversation. "
            "Return as JSON with key 'facts' and a list of strings. Extract generously."
        )

    categories_text = "\n".join(
        f"{i+1}. {cat.capitalize()}: {', '.join(words)}"
        for i, (cat, words) in enumerate(patterns.items())
    )

    return f"""You are a memory organizer for a system that works with {', '.join(patterns.keys())} data.

Extract ALL significant facts from the conversation. Focus on:
{categories_text}

Return facts as JSON with key "facts" and a list of strings. Extract generously."""
