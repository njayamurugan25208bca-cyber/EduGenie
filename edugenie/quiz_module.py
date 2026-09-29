import json
import re

from pydantic import ValidationError

from config import settings
from gemini_client import get_client

from schemas import (
    QuizResponse
)


def clean_json_block(
    text: str
) -> str:

    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


def generate_quiz(
    text: str,
    count: int = 3
) -> QuizResponse:

    client = get_client()

    schema = {

        "type": "object",

        "properties": {

            "questions": {

                "type": "array",

                "minItems": count,

                "maxItems": count,

                "items": {

                    "type": "object",

                    "properties": {

                        "question": {
                            "type": "string"
                        },

                        "options": {

                            "type": "array",

                            "minItems": 4,

                            "maxItems": 4,

                            "items": {
                                "type": "string"
                            }
                        },

                        "correct_answer": {
                            "type": "string"
                        },

                        "explanation": {
                            "type": "string"
                        }
                    },

                    "required": [
                        "question",
                        "options",
                        "correct_answer",
                        "explanation"
                    ]
                }
            }
        },

        "required": [
            "questions"
        ]
    }

    prompt = f"""
Create exactly {count}
multiple-choice questions
from this passage.

PASSAGE:

{text}

Rules:

- Four options per question.
- Only one correct answer.
- correct_answer must exactly match
  one of the four options.
- Distractors should be plausible.
- Questions must be based only
  on the supplied passage.
- Provide a short explanation.
"""

    response = client.models.generate_content(

        model=settings.gemini_model,

        contents=prompt,

        config={

            "temperature": 0.25,

            "response_mime_type":
                "application/json",

            "response_schema":
                schema
        }
    )

    raw = getattr(
        response,
        "text",
        None
    )

    if not raw:

        raise RuntimeError(
            "Gemini returned no quiz data."
        )

    try:

        data = json.loads(
            clean_json_block(raw)
        )

        quiz = QuizResponse.model_validate(
            data
        )

        if len(quiz.questions) != count:

            raise ValueError(
                "Unexpected number of questions."
            )

        return quiz

    except (
        json.JSONDecodeError,
        ValidationError,
        ValueError
    ) as exc:

        raise RuntimeError(
            f"Quiz validation failed: {exc}"
        ) from exc