"""
Default image embedding provider.
"""

__all__ = ["Default"]

from .clip import Clip


class Default(Clip):
    pass
