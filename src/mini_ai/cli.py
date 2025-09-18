from __future__ import annotations

"""
cli.py
------
This file provides a simple command-line interface (CLI) for chatting with the bot.
It loads the intents file, creates the bot, and then starts a loop where you can
type messages and see the bot's replies.
"""

import argparse
from pathlib import Path

from .engine import build_from_yaml


def main():
    # Set up a command-line argument parser. This lets users pass in a custom
    # path to the intents YAML file if they want.
    parser = argparse.ArgumentParser(description="Mini AI Chatbot")
    parser.add_argument(
        "--intents",
        type=str,
        # Default to the repository's data/intents.yml
        default=str(Path(__file__).resolve().parent.parent.parent / "data" / "intents.yml"),
        help="Path to intents YAML file",
    )
    args = parser.parse_args()

    # Build the bot by reading and parsing the YAML file
    bot = build_from_yaml(args.intents)

    print("Mini AI ready. Type 'exit' to quit.")
    # Simple REPL (Read-Eval-Print Loop): read input, get a response, print it
    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            # Handle Ctrl+D (EOF) or Ctrl+C (KeyboardInterrupt) gracefully
            print("\nBye!")
            break
        if user.lower() in {"exit", "quit"}:
            print("Bye!")
            break
        reply = bot.respond(user)
        print(f"Bot: {reply}")


if __name__ == "__main__":
    main()
