from typing import Any

from verse.content.audio import Audio, AudioParam
from verse.core import Component, Response

from ._models import SpeechRecognitionResult
from ._operation import SpeechRecognitionOperation


class SpeechRecognition(Component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def transcribe(
        self,
        audio: str | bytes | Audio | AudioParam | dict,
        **kwargs: Any,
    ) -> Response[SpeechRecognitionResult]:
        """Transcribe audio and convert to text.

        Args:
            audio: Audio to transcibe.

        Returns:
            Transciption result.
        """
        return self._run_internal(
            SpeechRecognitionOperation.TRANSCRIBE, locals()
        )

    def detect_language(
        self,
        audio: str | bytes | Audio | AudioParam | dict,
        **kwargs: Any,
    ) -> Response[SpeechRecognitionResult]:
        """Detect langauge in audio.

        Args:
            audio: Audio to recognize.

        Returns:
            Detection result.
        """
        return self._run_internal(
            SpeechRecognitionOperation.DETECT_LANGUAGE, locals()
        )

    async def atranscribe(
        self,
        audio: str | bytes | Audio | AudioParam | dict,
        **kwargs: Any,
    ) -> Response[SpeechRecognitionResult]:
        """Transcribe audio and convert to text.

        Args:
            audio: Audio to transcibe.

        Returns:
            Transciption result.
        """
        return await self._arun_internal(
            SpeechRecognitionOperation.TRANSCRIBE, locals()
        )

    async def adetect_language(
        self,
        audio: str | bytes | Audio | AudioParam | dict,
        **kwargs: Any,
    ) -> Response[SpeechRecognitionResult]:
        """Detect langauge in audio.

        Args:
            audio: Audio to recognize.

        Returns:
            Detection result.
        """
        return await self._arun_internal(
            SpeechRecognitionOperation.DETECT_LANGUAGE, locals()
        )
