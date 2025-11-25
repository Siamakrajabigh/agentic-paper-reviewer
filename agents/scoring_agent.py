from agents.base import AgentResult
from tools.llm import gemini_text
import json, re

DIMENSIONS = [
    "Originality",
    "Significance",
    "Soundness",
    "Clarity",
    "Reproducibility",
    "Contextualization",
    "Overall"
]

WEIGHTS = {
    "Originality": 0.17,
    "Significance": 0.17,
    "Soundness": 0.17,
    "Clarity": 0.14,
    "Reproducibility": 0.14,
    "Contextualization": 0.11,
    "Overall": 0.10
}

def scoring_agent(state) -> AgentResult:
    prompt = f"""
Score the paper on a 1-10 scale for each dimension:
{', '.join(DIMENSIONS[:-1])}

Paper title: {state['paper_title']}
Review draft:
{state['final_review']}

Return JSON exactly like:
{{
 "Originality": x,
 "Significance": x,
 "Soundness": x,
 "Clarity": x,
 "Reproducibility": x,
 "Contextualization": x,
 "Overall": x
}}
Only numbers 1-10.
"""
    raw = gemini_text(prompt, temperature=0.0)

    json_str = re.search(r"\{.*\}", raw, re.S)
    scores = json.loads(json_str.group(0)) if json_str else {}

    final = sum(scores.get(k, 5) * w for k, w in WEIGHTS.items())
    scores["FinalScore"] = round(final, 2)

    state["scores"] = scores
    return AgentResult(scores, {"step": "scoring", "final": scores["FinalScore"]})
