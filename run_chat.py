#!/usr/bin/env python3
"""
run_chat.py
-----------
This small script makes it easy to run the chatbot without installing the
package. It adds the local "src/" folder to Python's import path so
`from mini_ai import ...` works while developing.
"""

from pathlib import Path
import sys

# Ensure src/ is on the import path (so we can import mini_ai while developing)
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from mini_ai.cli import main  # noqa: E402 (import after sys.path manipulation)

if __name__ == "__main__":
    main()
