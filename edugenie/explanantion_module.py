from config import settings

from gemini_client import generate_text


def gemini_explanation(
    topic: str,
    level: str
) -> str:

    prompt = f"""
You are EduGenie.

Explain this topic to a {level} learner.

Topic:
{topic}

Use this structure:

1. Simple definition
2. Easy explanation
3. Example or analogy
4. Important points
5. Short recap

Rules:

- Use simple language.
- Avoid unnecessary technical terms.
- Define technical terms when needed.
- Keep the explanation concise.
"""

    return generate_text(
        prompt,
        temperature=0.3
    )


local_pipeline = None


def local_explanation(
    topic: str,
    level: str
) -> str:

    global local_pipeline

    if local_pipeline is None:

        from transformers import pipeline

        local_pipeline = pipeline(
            "text2text-generation",
            model=settings.local_explainer_model
        )

    prompt = f"""
Explain {topic}
to a {level} learner
using simple language.

Include:

- definition
- example
- key points
"""

    result = local_pipeline(
        prompt,
        max_new_tokens=220,
        do_sample=False
    )

    return result[0][
        "generated_text"
    ].strip()


def explain_concept(
    topic: str,
    level: str = "beginner"
) -> str:

    if settings.local_explainer_enabled:

        try:

            return local_explanation(
                topic,
                level
            )

        except Exception:

            # Fallback to Gemini
            pass

    return gemini_explanation(
        topic,
        level
    )