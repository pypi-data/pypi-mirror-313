"""
Default image captioning provider.
"""

__all__ = ["Default"]

from .blip import Blip


class Default(Blip):
    pass
