from __future__ import annotations

"""
engine.py
-----------
This file contains the tiny "brain" of our mini AI chatbot. It:
- Defines what an "Intent" is (a label with patterns and responses)
- Loads intents from a YAML file
- Uses simple regular expressions (regex) to decide which intent matches a message
- Tries to extract a user's name from sentences like "I'm Alice"
- Picks a response and fills in placeholders like {name}

The goal is to keep this easy to read for beginners.
"""

import re
import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


# An Intent groups together:
# - a unique name (like "greeting")
# - patterns: list of regex patterns that should match user messages
# - responses: possible replies the bot can use for that intent
@dataclass
class Intent:
    name: str
    patterns: List[str]
    responses: List[str]


class MiniAI:
    """A tiny rule-based intent matcher with lightweight entity extraction.

    How it works (in short):
    1) Compile all regex patterns so they're fast to use
    2) When a message comes in:
       - Try to extract simple "entities" (like a name)
       - Find the first intent whose pattern matches the text
       - If nothing matches, use the "fallback" intent
       - Choose a response and fill in any placeholders
    """

    def __init__(self, intents: Dict[str, Intent], default_response: str = "I'm not sure I understand.") -> None:
        self.intents = intents
        self.default_response = default_response
        # Compile each regex once (case-insensitive) for better performance
        self._compiled: Dict[str, List[re.Pattern]] = {
            name: [re.compile(p, re.IGNORECASE) for p in intent.patterns]
            for name, intent in intents.items()
        }

    @staticmethod
    def _extract_name(text: str) -> Optional[str]:
        """Try to find a name in the user's message.

        Examples this can catch:
        - "I'm Alice"
        - "I am Bob"
        - "My name is Carol"

        NOTE: This is intentionally simple to keep it beginner-friendly.
        """
        name_patterns = [
            r"\b(?:i am|i'm|im)\s+([A-Z][a-z]+)\b",
            r"\bmy\s+name\s+is\s+([A-Z][a-z]+)\b",
        ]
        for pat in name_patterns:
            m = re.search(pat, text, flags=re.IGNORECASE)
            if m:
                # Normalize the name to Capitalized form (e.g., "alice" -> "Alice")
                return m.group(1).strip().capitalize()
        return None

    def predict_intent(self, text: str) -> Tuple[str, Dict[str, str]]:
        """Return the best-matching intent name and any extracted entities.

        For simplicity, we return the first intent whose regex matches the text.
        """
        text = text.strip()
        entities: Dict[str, str] = {}

        # Extract entities regardless of which intent we end up with
        name = self._extract_name(text)
        if name:
            entities["name"] = name

        # Find the first intent whose pattern matches the text
        best_intent: Optional[str] = None
        for name_i, patterns in self._compiled.items():
            if any(p.search(text) for p in patterns):
                best_intent = name_i
                break

        if best_intent is None:
            # Fall back to a special intent if nothing else matched
            best_intent = "fallback"

        return best_intent, entities

    def respond(self, text: str) -> str:
        """Generate a response string for the given user message."""
        intent_name, entities = self.predict_intent(text)
        return self.render_response(intent_name, entities)

    def _apply_dynamic(self, intent_name: str, entities: Dict[str, str]) -> Dict[str, str]:
        """Inject dynamic values for certain intents (e.g., current time)."""
        if intent_name == "time":
            from datetime import datetime
            out = dict(entities)
            out["time"] = datetime.now().strftime("%I:%M %p").lstrip("0")
            return out
        return entities

    def render_response(self, intent_name: str, entities: Dict[str, str]) -> str:
        """Render a response for a known intent using provided entities.

        This is useful when callers want to merge additional context (e.g.,
        session memory) into the entities before rendering.
        """
        intent = self.intents.get(intent_name)
        if not intent:
            return self.default_response

        # Choose one of the possible responses at random (for variety)
        template = random.choice(intent.responses) if intent.responses else self.default_response

        # Fill placeholders like {name}. If a placeholder is missing, use "" instead of raising an error.
        class _SafeDict(dict):
            def __missing__(self, key):  # type: ignore[override]
                return ""

        # Inject dynamic fields as needed (e.g., time)
        enriched = self._apply_dynamic(intent_name, entities)
        return template.format_map(_SafeDict(enriched))


def build_from_yaml(path: str) -> MiniAI:
    """Create a MiniAI instance by reading intents from a YAML file."""
    import yaml  # Local import so this file has minimal top-level dependencies

    # Load YAML into a Python dictionary
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    # Convert the raw data into Intent objects
    intents_map: Dict[str, Intent] = {}
    for item in raw.get("intents", []):
        name = item.get("name")
        patterns = item.get("patterns", [])
        responses = item.get("responses", [])
        if not name:
            # Skip entries without a name
            continue
        intents_map[name] = Intent(name=name, patterns=patterns, responses=responses)

    default_resp = raw.get("default_response", "I'm not sure I understand.")
    return MiniAI(intents=intents_map, default_response=default_resp)
