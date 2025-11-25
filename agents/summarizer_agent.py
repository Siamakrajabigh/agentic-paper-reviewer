# agents/summarizer_agent.py

from typing import Any
import json

from tools.llm import gemini_text, LLMQuotaError, LLMConfigError


def _paper_to_text(paper_md: Any) -> str:
    """
    Convert whatever `paper_md` is (string, dict, etc.) into a text blob.
    This avoids type errors like 'unhashable type: slice'.
    """
    # If it's already a string, good
    if isinstance(paper_md, str):
        return paper_md

    # If it's a dict, try common text fields
    if isinstance(paper_md, dict):
        for key in ["content", "text", "markdown", "body", "abstract"]:
            if key in paper_md and isinstance(paper_md[key], str):
                return paper_md[key]

        # Otherwise, join all string values
        texts = [v for v in paper_md.values() if isinstance(v, str)]
        if texts:
            return "\n\n".join(texts)

        # Fallback: JSON dump
        return json.dumps(paper_md, ensure_ascii=False)

    # Last resort: string conversion
    return str(paper_md)


def summarizer_agent(paper_md: Any, original_title: str):
    """
    Summarizer agent that:
    - Safely converts input to text (even if it's a dict).
    - Truncates context to avoid hitting Gemini's large-input quota.
    - Handles quota/config errors gracefully instead of crashing.
    """

    raw_text = _paper_to_text(paper_md)

    # ↓ LIMIT INPUT to ~4000 chars (safe for flash-lite)
    max_chars = 4000
    truncated = raw_text[:max_chars]

    prompt = f"""
You are helping write a peer review for a scientific paper titled:
"{original_title}"

Your task:
- Summarize the related paper below.
- Max 5 bullet points.
- Focus on contributions, method, results, relevance.
- Be concise (150 words max).
- Avoid hype; be technical and objective.

Related paper content:
\"\"\"{truncated}\"\"\"
"""

    error_info = None
    try:
        summary = gemini_text(prompt, temperature=0.2)
    except LLMQuotaError as e:
        # If Gemini quota is exhausted, don't crash the whole pipeline
        summary = "[Summarizer skipped: Gemini quota / rate limit exceeded.]"
        error_info = str(e)
    except LLMConfigError as e:
        # If the model/key config is bad, still return something
        summary = "[Summarizer failed due to Gemini configuration error.]"
        error_info = str(e)

    class SummaryResult:
        def __init__(self, output, error=None):
            self.output = output
            self.logs = {
                "agent": "summarizer_agent",
                "chars_used": len(truncated),
                "summary_length": len(output),
                "had_error": error is not None,
                "error": error,
            }

    return SummaryResult(summary, error_info)