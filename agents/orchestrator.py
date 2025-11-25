from tools.llm import gemini_text
from agents.base import AgentResult

def orchestrator_agent(state) -> AgentResult:
    title = state.get("paper_title", "Unknown")
    plan_prompt = f"""
You are the Orchestrator for an agentic paper reviewer.
Paper title: {title}

Create a short plan:
1) what to extract from the paper
2) what search queries to generate
3) how many related papers to select
4) what the final review sections are
Return bullet points only.
"""
    plan = gemini_text(plan_prompt, temperature=0.1)
    state["plan"] = plan
    return AgentResult(plan, {"step": "orchestrator", "plan_preview": plan[:500]})
