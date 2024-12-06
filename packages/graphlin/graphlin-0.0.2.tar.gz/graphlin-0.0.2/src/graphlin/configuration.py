import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    MULTIPLE_LABELS: bool = False

    model_config = {
        "env_file": os.environ.get("GRAPHLIN_CONFIG", ".env"),
    }


settings = Settings()
