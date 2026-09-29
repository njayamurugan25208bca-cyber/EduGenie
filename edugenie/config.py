import os

from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:

    app_name: str = os.getenv(
        "APP_NAME",
        "EduGenie"
    )

    gemini_api_key: str = os.getenv(
        "GEMINI_API_KEY",
        ""
    )

    gemini_model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    )

    local_explainer_enabled: bool = (
        os.getenv(
            "ENABLE_LOCAL_EXPLAINER",
            "false"
        ).lower() == "true"
    )

    local_explainer_model: str = os.getenv(
        "LOCAL_EXPLAINER_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M"
    )


settings = Settings()