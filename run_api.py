#!/usr/bin/env python3
"""
run_api.py
----------
Convenience script to run the FastAPI server with Uvicorn.
Visit http://localhost:8000 to open the React page.
"""
from pathlib import Path
import os
import sys

# Ensure src/ is on the path for local imports
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import uvicorn  # noqa: E402


def main():
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", "8000"))
    log_level = os.getenv("LOG_LEVEL", "info")
    access_log_env = os.getenv("ACCESS_LOG", "true").lower()
    access_log = access_log_env in {"1", "true", "yes", "on"}
    uvicorn.run(
        "mini_ai.server:app",
        host=host,
        port=port,
        reload=False,
        log_level=log_level,
        access_log=access_log,
    )


if __name__ == "__main__":
    main()
