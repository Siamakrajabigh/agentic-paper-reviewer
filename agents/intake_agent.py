from agents.base import AgentResult
from tools.pdf_to_md import pdf_to_markdown_tool

def intake_agent(pdf_path: str, state) -> AgentResult:
    md = pdf_to_markdown_tool(pdf_path)

    # naive title extraction: first non-empty line
    title = next((line for line in md.splitlines() if line.strip()), "Unknown Title")

    state["paper_md"] = md
    state["paper_title"] = title

    return AgentResult(
        output={"title": title, "md_preview": md[:2000]},
        logs={"step": "intake", "title": title, "chars": len(md)}
    )
