import asyncio, time, json
from memory.session_store import SessionState

from agents.intake_agent import intake_agent
from agents.orchestrator import orchestrator_agent
from agents.query_agent import query_builder_agent
from agents.retriever_agent import retriever_agent
from agents.ranker_agent import ranker_agent
from agents.summarizer_agent import summarizer_agent
from agents.review_writer_agent import review_writer_agent
from agents.scoring_agent import scoring_agent

async def run_pipeline(pdf_path: str):
    t0 = time.time()
    state = SessionState()
    logs = []

    logs.append(intake_agent(pdf_path, state).logs)
    logs.append(orchestrator_agent(state).logs)
    logs.append(query_builder_agent(state).logs)
    logs.append(retriever_agent(state).logs)
    logs.append(ranker_agent(state).logs)

    original_title = state["paper_title"]

    tasks = [
        asyncio.to_thread(summarizer_agent, p, original_title)
        for p in state["top_related"]
    ]
    results = await asyncio.gather(*tasks)

    related_summaries = []
    for r in results:
        related_summaries.append(r.output)
        logs.append(r.logs)
    state["related_summaries"] = related_summaries

    logs.append(review_writer_agent(state).logs)
    logs.append(scoring_agent(state).logs)

    logs.append({"step": "total", "seconds": round(time.time() - t0, 2)})
    return state["final_review"], state["scores"], logs

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python app.py path/to/paper.pdf")
        raise SystemExit(1)

    pdf_path = sys.argv[1]
    review, scores, logs = asyncio.run(run_pipeline(pdf_path))
    print(review)
    print("\n\n## SCORES\n", json.dumps(scores, indent=2))
    print("\n--- LOGS ---")
    print(json.dumps(logs, indent=2))
