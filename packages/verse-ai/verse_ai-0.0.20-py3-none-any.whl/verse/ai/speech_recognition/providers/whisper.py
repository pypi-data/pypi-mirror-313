"""
Speech recognition using Whisper.
"""

__all__ = ["Whisper"]

from typing import Any

import av
import numpy as np
import whisper
from whisper import Whisper as OpenAIWhisper

from verse.content.audio import Audio
from verse.core import Context, Operation, Provider, Response

from .._operation import SpeechRecognitionOperation
from .._operation_parser import SpeechRecognitionOperationParser

from .._models import SpeechRecognitionResult


class Whisper(Provider):
    model: str
    device: str | None

    _model: OpenAIWhisper

    def __init__(
        self,
        model: str = "tiny",
        device: str | None = None,
        **kwargs,
    ):
        """Intialize.

        Args:
            model:
                Whisper model name.
            device:
                Pytorch device name.
        """
        self.model = model
        self.device = device
        self._model = None

    def init(self, context: Context | None = None) -> None:
        if self._model:
            return
        self._model = whisper.load_model(name=self.model, device=self.device)

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
        waudio = self._extract_and_resample_audio(audio.convert(type="stream"))
        waudio = whisper.pad_or_trim(waudio)
        result = whisper.transcribe(self._model, waudio)
        result = SpeechRecognitionResult(text=result["text"], 
                                        language=result["language"],
                                        verbose=result)
        return result

    def _detect_language(self, audio: Audio):
        whisper_audio = self._extract_and_resample_audio(audio.convert(type="stream"))
        whisper_audio = whisper.pad_or_trim(whisper_audio)
        mel = whisper.log_mel_spectrogram(whisper_audio).to(self._model.device)
        _, probs = self._model.detect_language(mel)
        return max(probs, key=probs.get)

    def _extract_and_resample_audio(self, stream, target_rate=16000):
        container = av.open(stream)
        stream = container.streams.audio[0]

        resampler = av.audio.resampler.AudioResampler(
            format="s16", layout="mono", rate=target_rate
        )

        samples = []

        for frame in container.decode(stream):
            resampled_frames = resampler.resample(frame)
            for resampled_frame in resampled_frames:
                samples.append(resampled_frame.to_ndarray())

        audio_data = np.concatenate(samples, axis=1)
        if audio_data.ndim > 1:
            audio_data = audio_data.mean(axis=0)

        audio_data = audio_data / np.max(np.abs(audio_data))
        if audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32)

        return audio_data
