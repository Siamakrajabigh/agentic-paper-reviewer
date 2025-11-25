import os
import google.generativeai as genai
from tenacity import retry, wait_random_exponential, stop_after_attempt

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-1.5-pro")

@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(4))
def gemini_text(prompt: str, temperature: float = 0.2) -> str:
    """
    Simple Gemini text helper.
    Requires GEMINI_API_KEY env var.
    """
    model = genai.GenerativeModel(MODEL_NAME)
    resp = model.generate_content(
        prompt,
        generation_config={"temperature": temperature}
    )
    return resp.text.strip()
