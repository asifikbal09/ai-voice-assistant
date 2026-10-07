from abc import ABC, abstractmethod


class TTSProvider(ABC):

    @abstractmethod
    async def synthesize(self, text: str) -> bytes:
        """
        Convert text to speech and return audio bytes.
        """
        raise NotImplementedError