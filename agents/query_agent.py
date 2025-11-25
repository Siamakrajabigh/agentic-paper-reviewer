from agents.base import AgentResult
import re

def query_builder_agent(state) -> AgentResult:
    md = state["paper_md"]
    title = state["paper_title"]

    # crude keyword extraction from first ~2k chars
    keywords = re.findall(r"\b[A-Za-z][A-Za-z\-]{4,}\b", md[:2000])
    keywords = list(dict.fromkeys([k.lower() for k in keywords]))[:8]

    queries = [
        title,
        " ".join(keywords[:4]) if keywords else title,
        f"{keywords[0]} benchmark baseline" if keywords else title,
        f"{title} arxiv",
    ]
    state["queries"] = queries
    return AgentResult(
        output=queries,
        logs={"step": "query_builder", "queries": queries}
    )
