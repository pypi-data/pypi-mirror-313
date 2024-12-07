"""
Default chat completion provider.
"""

__all__ = ["Default"]

from .openai import OpenAI


class Default(OpenAI):
    pass
