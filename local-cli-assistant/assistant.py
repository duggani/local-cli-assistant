"""
Main terminal application for the local CLI assistant.
"""

from __future__ import annotations

import argparse

from config import DEFAULT_MODELS
from prompts import CHAT_SYSTEM_PROMPT, CODE_SYSTEM_PROMPT, TOOLS_SYSTEM_PROMPT
from ollama_client import chat


SYSTEM_PROMPTS = {
    "chat": CHAT_SYSTEM_PROMPT,
    "code": CODE_SYSTEM_PROMPT,
    "tools": TOOLS_SYSTEM_PROMPT,
}


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Local CLI Assistant")
    parser.add_argument(
        "--mode",
        choices=["chat", "code", "tools"],
        default="chat",
        help="Assistant operating mode",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Optional explicit model override",
    )
    return parser.parse_args()


def main() -> None:
    """
    Run the terminal chat loop.
    """
    args = parse_args()
    mode = args.mode
    model = args.model or DEFAULT_MODELS[mode]

    messages: list[dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPTS[mode]}
    ]

    print(f"Local CLI Assistant")
    print(f"Mode: {mode}")
    print(f"Model: {model}")
    print("Type 'exit' or 'quit' to leave.\n")

    while True:
        user_input = input("You> ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        try:
            response = chat(model=model, messages=messages)
            assistant_message = response["message"]["content"].strip()
        except Exception as exc:
            print(f"\nAssistant> Error: {exc}\n")
            messages.pop()
            continue

        print(f"\nAssistant> {assistant_message}\n")
        messages.append({"role": "assistant", "content": assistant_message})


if __name__ == "__main__":
    main()
