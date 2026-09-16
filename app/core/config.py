from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Premium Voice Assistant"
    app_env: str = "development"

    api_prefix: str = "/api/v1"

    groq_api_key: str = ""
    groq_model: str = ""

    database_url: str = ""

    redis_url: str = ""

    qdrant_url: str = "localhost:6333"
    qdrant_api_key: str = ""
    qdrant_collection: str = "premium_design_knowledge"

    embedding_provider: str = ""
    embedding_model: str = ""

    stt_provider: str = "groq"

    tts_provider: str = ""
    tts_api_key: str = ""

    laravel_api_url: str = ""
    laravel_api_token: str = ""

    frontend_url: str = "http://localhost:5173"

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()