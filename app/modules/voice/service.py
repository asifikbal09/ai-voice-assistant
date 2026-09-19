from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import UploadFile

from app.core.config import settings
from app.modules.voice.providers.groq_whisper import (
    GroqWhisperProvider,
)


async def transcribe_audio(
    audio: UploadFile,
    language: str | None = None,
) -> str:

    if settings.stt_provider != "groq":
        raise ValueError(
            f"Unsupported STT provider: {settings.stt_provider}"
        )

    suffix = Path(
        audio.filename or ".webm"
    ).suffix

    with NamedTemporaryFile(
        delete=False,
        suffix=suffix,
    ) as temp_file:

        temp_path = temp_file.name

        while chunk := await audio.read(1024 * 1024):

            temp_file.write(chunk)

    try:

        provider = GroqWhisperProvider()

        text = await provider.transcribe(
            audio_path=temp_path,
            language=language,
        )

        return text

    finally:

        Path(temp_path).unlink(
            missing_ok=True
        )