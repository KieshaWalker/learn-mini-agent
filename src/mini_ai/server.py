"""
server.py
---------
Minimal FastAPI server that exposes:
- POST /chat  -> accepts JSON {"message": "..."} and returns {"reply": "..."}
- GET  /      -> serves a simple React page from ../web/index.html

This keeps everything very small and easy to understand for beginners.
"""
from __future__ import annotations

from pathlib import Path
import os
import uuid
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .engine import build_from_yaml


ROOT = Path(__file__).resolve().parent.parent.parent

# Read configuration from environment variables (with sensible defaults)
INTENTS_PATH = Path(os.getenv("INTENTS_PATH", str(ROOT / "data" / "intents.yml")))
WEB_INDEX = ROOT / "web" / "index.html"

app = FastAPI(title="Mini AI API")

# Allow the demo page to call the API from a browser
allow_origins_env = os.getenv("CORS_ALLOW_ORIGINS", "*")
allow_origins = [o.strip() for o in allow_origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


# Build bot once on startup
bot = build_from_yaml(str(INTENTS_PATH))

# Very small in-memory session store: { session_id: {"name": "Alice"} }
SESSIONS: dict[str, dict[str, str]] = {}
SESSION_COOKIE = os.getenv("SESSION_COOKIE", "mini_ai_sid")


@app.get("/")
def serve_index():
    if not WEB_INDEX.exists():
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(str(WEB_INDEX))


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest, request: Request, response: Response):
    if not req.message.strip():
        return ChatResponse(reply="Please type something.")

    # Get or create a session id from cookies
    sid = request.cookies.get(SESSION_COOKIE)
    if not sid:
        sid = uuid.uuid4().hex
        response.set_cookie(key=SESSION_COOKIE, value=sid, httponly=True, samesite="lax")
    memory = SESSIONS.setdefault(sid, {})

    # Predict intent and entities from the message
    intent_name, entities = bot.predict_intent(req.message)

    # Learn name if provided
    if "name" in entities:
        memory["name"] = entities["name"]

    # Merge memory into entities for rendering (memory should not be overwritten by empty values)
    merged = {**memory, **entities}

    # Render final response using merged entities
    reply = bot.render_response(intent_name, merged)
    return ChatResponse(reply=reply)
