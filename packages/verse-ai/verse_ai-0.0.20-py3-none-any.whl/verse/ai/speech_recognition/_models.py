from verse.core import DataModel
from typing import Any

class SpeechRecognitionResult(DataModel):
    """Speech recognition result."""

    text: str | None
    language: str | None
    verbose: Any | None
    """Transcribed text."""
