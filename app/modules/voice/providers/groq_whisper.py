from pathlib import Path

from groq import AsyncGroq

from app.core.config import settings


class GroqWhisperProvider:

    def __init__(self):
        if not settings.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        self.client = AsyncGroq(
            api_key=settings.groq_api_key
        )

    async def transcribe(
        self,
        audio_path: str,
        language: str | None = None,
    ) -> str:

        path = Path(audio_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        with path.open("rb") as audio_file:

            kwargs = {
                "file": (
                    path.name,
                    audio_file,
                ),
                "model": settings.stt_model,
                "response_format": "json",
            }

            if language:
                kwargs["language"] = language

            transcription = await self.client.audio.transcriptions.create(
                **kwargs
            )

        return transcription.text.strip()