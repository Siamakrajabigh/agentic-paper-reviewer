from agents.base import AgentResult
from tools.llm import gemini_text
from tools.context import compact_context

def review_writer_agent(state) -> AgentResult:
    title = state["paper_title"]
    paper_md = compact_context(state["paper_md"])
    related = state["related_summaries"]

    related_block = "\n\n".join(
        [f"Title: {r['title']}\nSummary:\n{r['summary']}" for r in related]
    )

    prompt = f"""
You are an expert conference reviewer.

Paper title: {title}

Paper content (compacted):
{paper_md}

Top related papers:
{related_block}

Write a structured review with:
1) Summary (1 paragraph)
2) Strengths (bullets)
3) Weaknesses (bullets)
4) Novelty & related work positioning
5) Methodology soundness
6) Reproducibility & clarity
7) Suggestions to improve

Be specific, cite related papers by title when used.
No hallucinations. If unsure, say so.
"""
    review = gemini_text(prompt, temperature=0.2)
    state["final_review"] = review
    return AgentResult(review, {"step": "review_writer"})
