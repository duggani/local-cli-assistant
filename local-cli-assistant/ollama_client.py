"""
Minimal Ollama chat client.
"""

from __future__ import annotations

from typing import Any
import requests

from config import OLLAMA_BASE_URL


def chat(model: str, messages: list[dict[str, str]]) -> dict[str, Any]:
    """
    Send a chat request to the local Ollama server and return the JSON response.
    """
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
    }

    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()
    return response.json()
