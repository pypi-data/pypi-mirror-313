"""
Default speech recognition provider.
"""

__all__ = ["Default"]

from .whisper import Whisper


class Default(Whisper):
    pass
