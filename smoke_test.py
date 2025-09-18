#!/usr/bin/env python3
"""
smoke_test.py
-------------
This script runs a few basic checks to make sure the chatbot works as expected.
It's not a full test suite—just a quick way to verify that imports and simple
intent matching behave correctly.
"""

from pathlib import Path
import sys

# Ensure src is importable without installing the package
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mini_ai.engine import build_from_yaml  # noqa: E402


def main():
    # Build the bot from the YAML intents file
    bot = build_from_yaml(str(ROOT / "data" / "intents.yml"))

    # A small set of inputs and the intent we expect them to match
    tests = {
        "hello": "greeting",
        "goodbye": "goodbye",
        "my name is Alice": "name_intro",
        "what's the weather": "weather",
        "what time is it?": "time",
        "asdfasdf": "fallback",
    }

    passed = 0
    for text, expected_intent in tests.items():
        intent, entities = bot.predict_intent(text)
        ok = intent == expected_intent
        print(f"Input: {text!r} -> intent: {intent!r}, entities: {entities} | {'OK' if ok else 'FAIL'}")
        if ok:
            passed += 1

    print(f"\nPassed {passed}/{len(tests)} basic checks.")


if __name__ == "__main__":
    main()
