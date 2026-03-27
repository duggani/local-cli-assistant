# Local CLI Assistant

A lightweight, local-first terminal assistant powered by Ollama.

This project is designed to bring AI-assisted workflows directly into the command line, enabling practical, secure, and reproducible interactions with local files, code, and development environments.

---

## Overview

The Local CLI Assistant provides a structured, extensible interface for interacting with a locally hosted large language model (LLM). It is intentionally designed to be:

- **Local-first** — all model inference runs on your machine
- **Safe by default** — no automatic file modification or command execution
- **Developer-focused** — built for terminal workflows, code assistance, and debugging
- **Modular and extensible** — designed to evolve into a tool-aware assistant

---

## Core Features (v1)

### Chat Mode
General-purpose terminal assistant for:
- Technical questions
- Workflow planning
- Debugging support
- Command suggestions

### Code Mode
Targeted support for:
- Python development
- Shell scripting
- Refactoring and scaffolding
- Code explanation and debugging

### Terminal UX Enhancements
- Animated “thinking” spinner during model response

---

## Architecture

```text
local-cli-assistant/
├── assistant.py        # Main CLI entry point
├── ollama_client.py    # Handles API calls to Ollama
├── prompts.py          # System prompts per mode
├── config.py           # Central configuration
├── spinner.py          # Terminal animation during inference
├── tools.py            # Safe helper tools (v1: defined, v2: wired)
├── requirements.txt
└── README.md

## Roadmap

### Phase 1 (Current)
- Chat mode
- Code mode
- Local model integration via `/api/chat`
- Terminal spinner for response feedback

### Phase 2 (Next)
- Manual tool commands (e.g., `/files`, `/read`, `/grep`, `/git-status`)
- Safe local file and repo inspection

### Phase 3
- Model-assisted tool usage (tool calling)
- Context-aware reasoning using local data

### Phase 4
- Controlled file editing and patch suggestions
- Session memory and persistence
- Repo-aware startup summaries

---

## Design Principles

- **Explicit over implicit** — no hidden actions  
- **Read-only by default** — prevents accidental changes  
- **Composable architecture** — each module has a clear responsibility  
- **CLI-native UX** — built for real terminal usage, not demos  

---

## Why This Project Exists

This project explores how local LLMs can be integrated into everyday development workflows without relying on external APIs.

It serves as both:
- a practical productivity tool  
- a foundation for building more advanced AI-assisted systems  

---

## Future Extensions

- Tool calling via Ollama  
- Git-aware commit message generation  
- Local document summarization  
- Project-level context injection  
- Integration with Makefiles and data pipelines  

---

## License

TBD

---

## Author

Ian Duggan  
Healthcare Operations Specialist | Graduate Student (MSCS)  
Focus: AI, Data Systems, and Operational Efficiency