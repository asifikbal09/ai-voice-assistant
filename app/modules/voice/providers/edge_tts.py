from pathlib import Path
from tempfile import NamedTemporaryFile

import edge_tts

from app.core.config import settings
from app.modules.voice.providers.base import TTSProvider


class EdgeTTSProvider(TTSProvider):

    def __init__(self):
        if not settings.edge_tts_voice:
            raise ValueError(
                "EDGE_TTS_VOICE is not configured."
            )

        self.voice = settings.edge_tts_voice

    async def synthesize(self, text: str) -> bytes:

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        with NamedTemporaryFile(
            delete=False,
            suffix=".mp3",
        ) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            communicate = edge_tts.Communicate(
                text=text.strip(),
                voice=self.voice,
            )

            await communicate.save(str(temp_path))

            audio = temp_path.read_bytes()

            if not audio:
                raise ValueError(
                    "Edge TTS returned empty audio."
                )

            return audio

        finally:
            temp_path.unlink(missing_ok=True)