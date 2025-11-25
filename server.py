import tempfile, os
from fastapi import FastAPI, UploadFile, File
from app import run_pipeline

app = FastAPI(title="Agentic Paper Reviewer")

@app.post("/review")
async def review_paper(pdf: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await pdf.read())
        path = tmp.name

    review, scores, logs = await run_pipeline(path)
    try:
        os.remove(path)
    except OSError:
        pass
    return {"review": review, "scores": scores, "logs": logs}

@app.get("/health")
def health():
    return {"ok": True}
