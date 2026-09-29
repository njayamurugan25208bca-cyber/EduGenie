from gemini_client import generate_text


def summarize_text(
    text: str
) -> str:

    prompt = f"""
You are EduGenie.

Summarize the following educational passage.

PASSAGE:

{text}

Return:

1. Short summary
2. Important points
3. Important terms

Requirements:

- Preserve the original meaning.
- Use simple language.
- Remove unnecessary repetition.
- Do not add unsupported information.
"""

    return generate_text(
        prompt,
        temperature=0.2
    )