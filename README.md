# AI Coding Agent

A production-grade, autonomous coding agent built from scratch in Python — no LangChain, no frameworks. Just the Gemini API, clean architecture, and raw engineering.

> Give it a task. Watch it think. It reads your code, finds the bug, writes the fix, runs the tests, and reports back.

---

## Demo

```bash
$ uv run main.py "Fix the bug: 3 + 7 * 2 shouldn't be 20"

 - Calling function: get_files_info
 - Calling function: get_file_content
 - Calling function: get_file_content
 - Calling function: write_file
 - Calling function: run_python_file

The bug has been fixed. The + operator had an incorrect precedence of 3,
which caused it to evaluate before *. I restored it to 1 and confirmed
that 3 + 7 * 2 now correctly returns 17.
```

---

## How It Works

The agent runs an **agentic loop** — it calls the LLM, executes whatever tools it requests, feeds the results back, and repeats until it has a final answer for you.

```
User Prompt
     │
     ▼
┌─────────────────────────────────────────┐
│              Agentic Loop               │
│                                         │
│  ┌─────────┐     ┌──────────────────┐   │
│  │  Gemini │────▶│  Function Call?  │   │
│  │   LLM   │     └────────┬─────────┘   │
│  └────▲────┘              │ Yes         │
│       │            ┌──────▼──────┐      │
│       │            │  Execute    │      │
│       └────────────│  Function   │      │
│      Feed result   └─────────────┘      │
│                                         │
│         No function call → DONE         │
└─────────────────────────────────────────┘
     │
     ▼
Final Response
```

The LLM never directly touches your filesystem — it *requests* function calls, and the Python runtime executes them within a sandboxed working directory.

---

## Features

| Capability | Details |
|---|---|
|  **File navigation** | List directories with size and type metadata |
|  **File reading** | Read file contents with configurable character cap |
|  **File writing** | Write or overwrite files, auto-creating parent dirs |
|  **Code execution** | Run Python files with args, capture stdout/stderr |
|  **Path sandboxing** | All file ops are jailed to the working directory |
|  **Agentic loop** | Up to 20 iterations with full conversation history |
|  **Verbose mode** | Token usage, function calls, and raw results |

---

## Architecture

```
ai_agent/
├── main.py                  # CLI entry point + agentic loop
├── prompts/
│   └── prompts.py           # System prompt for the LLM
├── call_function/
│   └── call_function.py     # Function router + tool registry
├── functions/
│   ├── get_files_info.py    # List directory contents
│   ├── get_file_content.py  # Read file contents
│   ├── write_file.py        # Write file contents
│   └── run_python_file.py   # Execute Python files
├── config.py                # Shared constants (MAX_CHARS, etc.)
└── calculator/              # Sample codebase for the agent to work on
    ├── main.py
    ├── tests.py
    └── pkg/
        ├── calculator.py
        └── render.py
```

**Key design decisions:**
- Each function is sandboxed — `working_directory` is always injected server-side, never exposed to the LLM
- Functions always return strings — clean, consistent interface between the runtime and the LLM
- The tool registry is a simple dict — easy to extend with new functions
- Conversation history grows each loop iteration — the model always has full context

---

## Tech Stack

- **Python 3.11**
- **Google Gemini API** (`gemini-2.5-flash`) via `google-genai`
- **uv** — fast Python package manager
- **python-dotenv** — environment variable management
- **subprocess** — sandboxed Python execution

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/Adrianbrou/AI-AGENT.git
cd AI-AGENT
```

**2. Install dependencies**
```bash
uv sync
```

**3. Add your Gemini API key**
```bash
# Create a .env file in the project root
echo "GEMINI_API_KEY=your_key_here" > .env
```
Get a free key at [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## Usage

**Run a task:**
```bash
uv run main.py "explain how the calculator renders results"
```

**Verbose mode (shows token usage + function results):**
```bash
uv run main.py "fix the bug in calculator.py" --verbose
```

**Example tasks to try:**
```bash
uv run main.py "what files are in the calculator project?"
uv run main.py "read main.py and explain what it does"
uv run main.py "run the calculator tests and tell me if they pass"
uv run main.py "refactor render.py to use f-strings instead of .format()"
```

---

## Security Notes

This is a **learning project** — not production-ready for general use.

- The agent is sandboxed to `./calculator` by default
- It can execute arbitrary Python within that directory
- Do not point it at sensitive codebases
- Do not share your `.env` file or API key

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` |  Yes | Your Google Gemini API key |

---

## What I Learned

Building this without a framework forced me to understand what agents actually are under the hood:

- LLMs don't "call" functions — they *describe* function calls, and you execute them
- The agentic loop is just a while loop with a conversation history list
- Sandboxing is your responsibility — the model will happily path-traverse if you let it
- System prompt engineering is real work — the agent's behavior changes dramatically based on how you instruct it

---

## Roadmap

- [ ] Structured logging (replace print statements with `logging` module)
- [ ] Support multiple LLM providers (OpenAI, Claude)
- [ ] Recursive directory search tool
- [ ] `search_in_files` grep-like tool
- [ ] Web search tool integration

---

## License

MIT — built as part of the [Boot.dev](https://boot.dev) backend curriculum.

---

*Built by [Adrian Brou](https://github.com/Adrianbrou) — Software Engineering graduate pursuing backend + DevOps roles.*

## Certificate

Completed as part of the [Boot.dev](https://boot.dev) Backend Developer curriculum.  
[View Certificate](https://www.boot.dev/certificates/40f82cd7-c8d5-4977-b6d7-fe706157e9f1)