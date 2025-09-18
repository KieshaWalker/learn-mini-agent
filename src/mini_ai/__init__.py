"""mini_ai package

This package contains:
- engine: the core logic for matching intents and generating responses
- cli: a command-line interface for chatting with the bot

`__all__` below lists what gets imported when using `from mini_ai import *`.
"""
# Import submodules so they are available as mini_ai.engine / mini_ai.cli
from . import engine, cli  # noqa: F401

__all__ = ["engine", "cli"]
