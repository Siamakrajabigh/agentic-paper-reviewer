# tools/llm.py

import os
import google.generativeai as genai
from google.api_core import exceptions
from tenacity import retry, stop_after_attempt, wait_exponential


# Configure Gemini client from environment
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables.")

genai.configure(api_key=API_KEY)

# Use model from env, default to free-tier-friendly one
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
model = genai.GenerativeModel(MODEL_NAME)


class LLMQuotaError(RuntimeError):
    """Raised when Gemini quota / rate limits are hit."""
    pass


class LLMConfigError(RuntimeError):
    """Raised when the API key or model configuration is invalid."""
    pass


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=4))
def gemini_text(prompt: str, temperature: float = 0.2) -> str:
    """
    Simple helper around Gemini text generation.
    Raises LLMQuotaError when quota is exceeded so callers can handle it.
    """
    try:
        resp = model.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": 512,
            },
        )
        return resp.text.strip()
    except exceptions.ResourceExhausted as e:
        # 429 quota / rate limit
        raise LLMQuotaError(
            f"Gemini quota / rate limit exceeded: {e.message}"
        ) from e
    except exceptions.InvalidArgument as e:
        # bad API key or invalid model, bad request, etc.
        raise LLMConfigError(
            f"Gemini configuration or request invalid: {e.message}"
        ) from e