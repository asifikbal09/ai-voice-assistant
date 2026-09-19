from pathlib import Path

from groq import AsyncGroq

from app.core.config import settings


SUPPORTED_LANGUAGES = {"bn", "en"}


class GroqWhisperProvider:
    """
    Groq Whisper Speech-to-Text provider.

    Supports:
    - Bangla: bn
    - English: en
    - Auto-detection: language=None
    """

    def __init__(self):
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY is not configured.")

        self.client = AsyncGroq(
            api_key=settings.groq_api_key
        )

    async def transcribe(
        self,
        audio_path: str,
        language: str | None = None,
    ) -> str:
        """
        Convert an audio file into text.

        Args:
            audio_path: Path to the audio file.
            language:
                - "bn" for Bangla
                - "en" for English
                - None for automatic language detection

        Returns:
            Transcribed text.
        """

        # ---------------------------------------------------------
        # 1. Validate audio file
        # ---------------------------------------------------------
        path = Path(audio_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Audio file not found: {audio_path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Audio path is not a file: {audio_path}"
            )

        # ---------------------------------------------------------
        # 2. Validate language
        # ---------------------------------------------------------
        if language:
            language = language.strip().lower()

            if language not in SUPPORTED_LANGUAGES:
                raise ValueError(
                    f"Unsupported language: {language}. "
                    f"Supported languages: {', '.join(sorted(SUPPORTED_LANGUAGES))}"
                )

        # ---------------------------------------------------------
        # 3. Prepare Whisper request
        # ---------------------------------------------------------
        kwargs = {
            "file": (
                path.name,
                path.open("rb"),
            ),
            "model": settings.stt_model,
            "response_format": "json",
        }

        # Only send language when explicitly provided.
        #
        # language=None means Whisper can automatically detect
        # the language.
        if language:
            kwargs["language"] = language

        # ---------------------------------------------------------
        # 4. Send audio to Groq Whisper
        # ---------------------------------------------------------
        try:
            transcription = await self.client.audio.transcriptions.create(
                **kwargs
            )

        finally:
            # Always close the opened audio file.
            kwargs["file"][1].close()

        # ---------------------------------------------------------
        # 5. Extract transcription
        # ---------------------------------------------------------
        text = transcription.text.strip()

        if not text:
            raise ValueError(
                "Whisper returned an empty transcription."
            )

        return text