from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import (
    ExplainRequest,
    QARequest,
    QuizRequest,
    SummaryRequest,
    LearningPathRequest,
    QuizResponse,
    HealthResponse,
)

from explanation_module import explain_concept
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# -----------------------------
# Home Page
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health", response_model=HealthResponse)
async def health():

    return HealthResponse(
        status="ok",
        service="EduGenie"
    )


# -----------------------------
# Q&A
# -----------------------------

@app.post("/qa")
async def qa(payload: QARequest):

    try:

        answer = answer_question(
            payload.question
        )

        return {
            "answer": answer
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# -----------------------------
# Explanation
# -----------------------------

@app.post("/explain")
async def explain(payload: ExplainRequest):

    try:

        explanation = explain_concept(
            payload.topic,
            payload.level
        )

        return {
            "explanation": explanation
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# -----------------------------
# Quiz
# -----------------------------

@app.post("/quiz", response_model=QuizResponse)
async def quiz(payload: QuizRequest):

    try:

        return generate_quiz(
            payload.text,
            payload.count
        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# -----------------------------
# Summary
# -----------------------------

@app.post("/summarize")
async def summarize(payload: SummaryRequest):

    try:

        summary = summarize_text(
            payload.text
        )

        return {
            "summary": summary
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )


# -----------------------------
# Learning Path
# -----------------------------

@app.post("/learn/recommendations")
async def learning_path(
    payload: LearningPathRequest
):

    try:

        result = get_learning_recommendations(
            payload.topic,
            payload.level
        )

        return {
            "learning_path": result
        }

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )