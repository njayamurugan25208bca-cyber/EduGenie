from typing import List

from pydantic import BaseModel, Field, field_validator


# -----------------------------
# Q&A Request
# -----------------------------

class QARequest(BaseModel):

    question: str = Field(
        min_length=2,
        max_length=10000
    )


# -----------------------------
# Explanation Request
# -----------------------------

class ExplainRequest(BaseModel):

    topic: str = Field(
        min_length=2,
        max_length=5000
    )

    level: str = Field(
        default="beginner",
        min_length=2,
        max_length=30
    )


# -----------------------------
# Summary Request
# -----------------------------

class SummaryRequest(BaseModel):

    text: str = Field(
        min_length=20,
        max_length=30000
    )


# -----------------------------
# Quiz Request
# -----------------------------

class QuizRequest(BaseModel):

    text: str = Field(
        min_length=10,
        max_length=30000
    )

    count: int = Field(
        default=3,
        ge=1,
        le=10
    )


# -----------------------------
# Learning Path
# -----------------------------

class LearningPathRequest(BaseModel):

    topic: str = Field(
        min_length=2,
        max_length=5000
    )

    level: str = Field(
        default="beginner",
        min_length=2,
        max_length=30
    )


# -----------------------------
# Quiz Question
# -----------------------------

class QuizQuestion(BaseModel):

    question: str

    options: List[str] = Field(
        min_length=4,
        max_length=4
    )

    correct_answer: str

    explanation: str = ""

    @field_validator("correct_answer")
    @classmethod
    def validate_correct_answer(
        cls,
        value,
        info
    ):

        options = info.data.get(
            "options",
            []
        )

        if options and value not in options:

            raise ValueError(
                "correct_answer must match one option"
            )

        return value


# -----------------------------
# Quiz Response
# -----------------------------

class QuizResponse(BaseModel):

    questions: List[QuizQuestion]


# -----------------------------
# Health
# -----------------------------

class HealthResponse(BaseModel):

    status: str

    service: str