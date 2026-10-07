from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import UploadFile

from app.core.config import settings
from app.modules.voice.providers.groq_whisper import GroqWhisperProvider
from app.modules.voice.normalizer.service import normalize_transcription
from app.modules.voice.providers.elevenlabs import ElevenLabsProvider
from app.modules.voice.providers.edge_tts import EdgeTTSProvider
from app.modules.assistant.service import chat



async def transcribe_audio(
    audio: UploadFile,
    language: str | None = None,
) -> str:

    if settings.stt_provider != "groq":
        raise ValueError(
            f"Unsupported STT provider: {settings.stt_provider}"
        )

    suffix = Path(audio.filename or ".webm").suffix

    with NamedTemporaryFile(
        delete=False,
        suffix=suffix,
    ) as temp_file:

        temp_path = temp_file.name

        while chunk := await audio.read(1024 * 1024):
            temp_file.write(chunk)

    try:
        provider = GroqWhisperProvider()

        raw_text = await provider.transcribe(
            audio_path=temp_path,
            language=language,
        )

        normalized_text = await normalize_transcription(raw_text)

        return normalized_text

    finally:
        Path(temp_path).unlink(missing_ok=True)


async def synthesize_speech(text: str) -> bytes:

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    if settings.tts_provider == "elevenlabs":
        provider = ElevenLabsProvider()

    elif settings.tts_provider == "edge":
        provider = EdgeTTSProvider()

    else:
        raise ValueError(
            f"Unsupported TTS provider: {settings.tts_provider}"
        )

    audio = await provider.synthesize(text)

    if not audio:
        raise ValueError(
            "TTS provider returned empty audio."
        )

    return audio


from sqlalchemy.ext.asyncio import AsyncSession


async def voice_chat(
    audio: UploadFile,
    db: AsyncSession,
    session_id: str,
    language: str | None = None,
) -> bytes:

    # 1. Speech → Text
    user_text = await transcribe_audio(
        audio=audio,
        language=language,
    )

    if not user_text:
        raise ValueError(
            "Could not understand the audio."
        )

    # 2. Text → AI response
    assistant_result = await chat(
        db=db,
        session_id=session_id,
        message=user_text,
    )

    # chat() returns a dictionary
    assistant_text = assistant_result["response"]

    if not assistant_text:
        raise ValueError(
            "Assistant returned an empty response."
        )

    # 3. AI response → Speech
    audio_response = await synthesize_speech(
        assistant_text
    )

    return audio_response