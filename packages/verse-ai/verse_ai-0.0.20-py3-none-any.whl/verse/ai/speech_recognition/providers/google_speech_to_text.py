"""
Speech Recognition using Google Speech-to-Text.
"""

__all__ = ["GoogleSpeechToText"]
import json
from typing import Any
from verse.core import Provider
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account

from verse.content.audio import Audio
from verse.core import Context, Operation, Provider, Response

from .._operation import SpeechRecognitionOperation
from .._operation_parser import SpeechRecognitionOperationParser
from .._models import SpeechRecognitionResult

class GoogleSpeechToText(Provider):
    def __init__(
        self,
        api_key_path: str = "",
        languages: list[str] = ["en-US", "en-GB", "es-ES", "fr-FR"],
        **kwargs,
    ):
        """Intialize.

        Args:
            api_key:
                Azure speech api key.
            service_region:
                Azure speech service region.
        """
        credentials = service_account.Credentials.from_service_account_file(api_key_path)
        self.client = speech.SpeechClient(credentials=credentials)
        self.languages = languages
        self.config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
            sample_rate_hertz=16000,
            language_code="en-US",  # Fallback language
            alternative_language_codes=languages,  # Possible languages
        )
    
    def run(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
    ) -> Any:
        self.init(context=context)
        op_parser = SpeechRecognitionOperationParser(operation)
        result: Any = None
        # TRANSCRIBE
        if op_parser.op_equals(SpeechRecognitionOperation.TRANSCRIBE):
            result = self._transcribe(audio=op_parser.get_audio())
        # DETECT_LANGUAGE
        elif op_parser.op_equals(SpeechRecognitionOperation.DETECT_LANGUAGE):
            result = self._detect_language(audio=op_parser.get_audio())
        else:
            return super().run(operation)
        return Response(result=result)

    def _transcribe(self, audio: Audio):
        audio = audio.convert(type="bytes", format="wav", codec="pcm_s16le", rate=16000, channels=1)
        audio = speech.RecognitionAudio(content=audio)
        
        response = self.client.recognize(config=self.config, audio=audio)
        
        return SpeechRecognitionResult(
            text=response.results[0].alternatives[0].transcript,
            verbose=response,
            language=response.results[0].language_code,
        )

    def _detect_language(self, audio: Audio):
        
        return self._transcribe(audio).language