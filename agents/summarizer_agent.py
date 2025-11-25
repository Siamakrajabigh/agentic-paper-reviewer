from agents.base import AgentResult
from tools.llm import gemini_text

def summarizer_agent(related_paper, original_title) -> AgentResult:
    prompt = f"""
Summarize this related paper for a review context.

Original paper: "{original_title}"
Related paper title: "{related_paper['title']}"
Abstract:
{related_paper['summary']}

Focus on:
- main contribution
- method/architecture
- key results
- relation to the original paper (supporting, competing, complementary)

Return 5-8 bullet points.
"""
    summary = gemini_text(prompt, temperature=0.2)

    out = {
        "arxiv_id": related_paper["arxiv_id"],
        "title": related_paper["title"],
        "summary": summary
    }
    return AgentResult(out, {"step": "summarizer", "arxiv_id": out["arxiv_id"]})
