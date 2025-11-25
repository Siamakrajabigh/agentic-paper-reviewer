# Agentic Paper Reviewer (Capstone)

A multi-agent system that:
1. Ingests a paper PDF
2. Extracts text + title
3. Generates search queries
4. Retrieves related work from arXiv
5. Summarizes top related papers in parallel
6. Writes a structured peer review grounded in related work
7. Scores the paper on 7 dimensions

## Setup

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Set Gemini env vars:

```bash
export GEMINI_API_KEY="YOUR_KEY"
export GEMINI_MODEL="gemini-1.5-pro"
```

## Run (CLI)

```bash
python app.py path/to/paper.pdf
```

## Run (API)

```bash
uvicorn server:app --reload
```

Open:
`http://127.0.0.1:8000/docs`

## Deploy to Cloud Run (ADK)

```bash
adk deploy cloud_run \
  --project YOUR_GCP_PROJECT_ID \
  --region us-central1 \
  --service-name agentic-paper-reviewer \
  --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY,GEMINI_MODEL=$GEMINI_MODEL
```

## Notes
- Do not commit API keys.
- Prefer text-based PDFs (arXiv PDFs work well).
