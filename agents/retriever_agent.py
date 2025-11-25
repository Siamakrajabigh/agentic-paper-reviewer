from agents.base import AgentResult
from tools.arxiv_search import arxiv_search_tool

def retriever_agent(state, max_per_query=5) -> AgentResult:
    all_hits = []
    for q in state["queries"]:
        hits = arxiv_search_tool(q, max_results=max_per_query)
        all_hits.extend(hits)

    # de-dup by arxiv_id
    seen = {}
    for h in all_hits:
        seen[h["arxiv_id"]] = h

    candidates = list(seen.values())
    state["candidates"] = candidates
    return AgentResult(
        output=candidates[:10],
        logs={"step": "retriever", "num_candidates": len(candidates)}
    )
