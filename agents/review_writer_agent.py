# agents/review_writer_agent.py

from tools.llm import gemini_text, LLMQuotaError, LLMConfigError


def review_writer_agent(state):
    """
    Uses:
      - state["paper_title"]
      - optional: state["paper_abstract"] / state["paper_md"] / state["paper_markdown"]
      - state["related_summaries"] (list of strings)
    Produces:
      - state["final_review"]
      - returns an object with `.logs`
    """

    paper_title = state.get("paper_title", "Unknown Title")

    # Try to find the main paper text in a few common keys
    main_text = (
        state.get("paper_abstract")
        or state.get("paper_md")
        or state.get("paper_markdown")
        or ""
    )

    related_summaries = state.get("related_summaries", [])

    # Build a compact related work block: each summary as a bullet
    related_block = "\n\n".join(
        f"- {s}" for s in related_summaries if isinstance(s, str)
    )

    # Truncate to keep prompts reasonable
    main_text_trunc = main_text[:4000]
    related_trunc = related_block[:4000]

    prompt = f"""
You are an expert peer reviewer for scientific papers.

You will write a structured review for the following paper:

Title: "{paper_title}"

Main paper (partial):
\"\"\"{main_text_trunc}\"\"\"

Related work summaries (partial):
\"\"\"{related_trunc}\"\"\"

Your output must be in this structure:

1. Summary (3–5 sentences)
2. Strengths (bullet list)
3. Weaknesses / Limitations (bullet list)
4. Suggestions for Improvement (bullet list)
5. Overall Recommendation (one of: strong accept, accept, weak accept, borderline, weak reject, reject)

Be concise, technical, and objective. Do not invent wild claims that are not supported by the text.
"""

    error_info = None
    try:
        review = gemini_text(prompt, temperature=0.25)
    except LLMQuotaError as e:
        review = (
            "[Review generation skipped: Gemini quota / rate limit exceeded. "
            "Please try again later or with a different API key.]"
        )
        error_info = str(e)
    except LLMConfigError as e:
        review = (
            "[Review generation failed due to Gemini configuration error. "
            "Check GEMINI_API_KEY and GEMINI_MODEL.]"
        )
        error_info = str(e)

    # Store in state so the rest of the pipeline (e.g. scoring) can use it
    state["final_review"] = review

    class ReviewResult:
        def __init__(self, logs):
            self.logs = logs

    logs = {
        "agent": "review_writer_agent",
        "num_related": len(related_summaries),
        "had_error": error_info is not None,
        "error": error_info,
    }

    return ReviewResult(logs)