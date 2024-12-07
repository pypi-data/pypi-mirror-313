"""
Speech recognition using Azure Speech.
"""

__all__ = ["AzureSpeech"]

import json
from typing import Any

import azure.cognitiveservices.speech as speechsdk
from scipy.io.wavfile import write

from verse.content.audio import Audio
from verse.core import Context, Operation, Provider, Response

from .._models import SpeechRecognitionResult
from .._operation import SpeechRecognitionOperation
from .._operation_parser import SpeechRecognitionOperationParser


class AzureSpeech(Provider):
    api_key: str
    service_region: str

    def __init__(
        self,
        api_key: str = "",
        service_region: str = "",
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

        self.speech_config = speechsdk.SpeechConfig(
            subscription=api_key, region=service_region
        )
        self.speech_config.output_format = speechsdk.OutputFormat.Detailed
        self.auto_detect_source_language_config = (
            speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
                languages=languages
            )
        )

    def run(
        self,
        operation: Operation | None = None,
        context: Context | None = None,
        **kwargs,
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
            return super().run(
                operation,
                context,
                **kwargs,
            )
        return Response(result=result)

    def _transcribe(self, audio: Audio):
        audio = audio.convert(
            type="bytes",
            format="wav",
            codec="pcm_s16le",
            rate=16000,
            channels=1,
        )
        audio_stream_callback = AudioInputStreamCallback(audio)

        stream = speechsdk.audio.PullAudioInputStream(
            pull_stream_callback=audio_stream_callback
        )
        audio_input = speechsdk.AudioConfig(stream=stream)
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=audio_input
        )
        result = speech_recognizer.recognize_once()
        json_obj = json.loads(result.json)

        return SpeechRecognitionResult(
            text=json_obj["DisplayText"], verbose=json_obj, language=None
        )

    def _detect_language(self, audio: Audio):
        audio = audio.convert(
            type="bytes",
            format="wav",
            codec="pcm_s16le",
            rate=16000,
            channels=1,
        )
        audio_stream_callback = AudioInputStreamCallback(audio)

        stream = speechsdk.audio.PullAudioInputStream(
            pull_stream_callback=audio_stream_callback
        )
        audio_input = speechsdk.AudioConfig(stream=stream)

        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config,
            auto_detect_source_language_config=self.auto_detect_source_language_config,
            audio_config=audio_input,
        )
        result = speech_recognizer.recognize_once()
        detected_language = result.properties[
            speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult
        ]
        json_obj = json.loads(result.json)
        return detected_language

    def _extract_and_resample_audio(self, stream, target_rate=16000):
        pass


class AudioInputStreamCallback(speechsdk.audio.PullAudioInputStreamCallback):
    def __init__(self, audio_data):
        super().__init__()
        self.audio_data = audio_data
        self.read_pos = 0  # Position in the audio data

    def read(self, buffer):
        # Read data into the buffer
        bytes_requested = len(buffer)
        bytes_available = len(self.audio_data) - self.read_pos
        bytes_to_copy = min(bytes_requested, bytes_available)

        if bytes_to_copy > 0:
            buffer[:bytes_to_copy] = self.audio_data[
                self.read_pos : self.read_pos + bytes_to_copy
            ]
            self.read_pos += bytes_to_copy
            return bytes_to_copy
        else:
            return 0  # No more data to read

    def close(self):
        pass
