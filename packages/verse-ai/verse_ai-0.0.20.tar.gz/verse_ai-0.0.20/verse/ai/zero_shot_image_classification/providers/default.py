"""
Default zero shot image classification provider.
"""

__all__ = ["Default"]

from .clip import Clip


class Default(Clip):
    pass
