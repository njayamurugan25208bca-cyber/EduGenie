from functools import lru_cache

from google import genai

from config import settings


@lru_cache(maxsize=1)
def get_client():

    if not settings.gemini_api_key:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Please create a .env file and add your Gemini API key."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_text(
    prompt: str,
    temperature: float = 0.3
) -> str:

    client = get_client()

    response = client.models.generate_content(

        model=settings.gemini_model,

        contents=prompt,

        config={
            "temperature": temperature
        }
    )

    text = getattr(
        response,
        "text",
        None
    )

    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()