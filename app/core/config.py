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
    stt_model: str = "whisper-large-v3-turbo"

    tts_provider: str = "edge"
    tts_api_key: str = "sk_48123093c6f03df79e92f2b82de83138251f9a0fbb6cf800"
    tts_voice_id: str = "3XjJ1C8taYP9CHnHKmK5"
    edge_tts_voice: str = "bn-BD-NabanitaNeural"

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