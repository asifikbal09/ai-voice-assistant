from elevenlabs.client import AsyncElevenLabs

from app.core.config import settings
from app.modules.voice.providers.base import TTSProvider


class ElevenLabsProvider(TTSProvider):

    def __init__(self):
        if not settings.tts_api_key:
            raise ValueError("TTS_API_KEY is not configured.")

        if not settings.tts_voice_id:
            raise ValueError("TTS_VOICE_ID is not configured.")

        self.client = AsyncElevenLabs(
            api_key=settings.tts_api_key
        )

    async def synthesize(self, text: str) -> bytes:

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        audio_stream = self.client.text_to_speech.convert(
            voice_id=settings.tts_voice_id,
            text=text.strip(),
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )

        chunks = []

        async for chunk in audio_stream:
            chunks.append(chunk)

        return b"".join(chunks)