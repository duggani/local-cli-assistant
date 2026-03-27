"""
Central project configuration.
"""

OLLAMA_BASE_URL = "http://localhost:11434"

DEFAULT_MODELS = {
    "chat": "llama3.1:latest",
    "code": "qwen2.5-coder:latest",
    "tools": "llama3.1:latest",
}

READ_FILE_CHAR_LIMIT = 12000
LIST_FILES_LIMIT = 200
GREP_MATCH_LIMIT = 100
