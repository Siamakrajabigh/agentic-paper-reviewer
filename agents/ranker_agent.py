from agents.base import AgentResult

def ranker_agent(state, top_k=3) -> AgentResult:
    title = state["paper_title"].lower()
    candidates = state["candidates"]

    def score(c):
        t = c["title"].lower()
        return sum(1 for w in title.split() if w in t)

    ranked = sorted(candidates, key=score, reverse=True)[:top_k]
    state["top_related"] = ranked
    return AgentResult(
        output=ranked,
        logs={"step": "ranker", "top_k": [r["arxiv_id"] for r in ranked]}
    )
