# AI Agent

A command-line AI assistant powered by Google's Gemini API. Send natural language prompts directly from your terminal and get intelligent responses back instantly.

---

## What It Does

This is a CLI tool that accepts a coding task and autonomously works through it using a set of predefined functions:

- Scan the files in a directory
- Read a file's contents
- Write or overwrite a file's contents
- Execute the Python interpreter on a file

The agent repeats these actions in a loop until the task is complete. For example:
```sh
uv run main.py "fix my calculator app, it's not starting correctly"

# Calling function: get_files_info
# Calling function: get_file_content
# Calling function: write_file
# Calling function: run_python_file
# Calling function: write_file
# Calling function: run_python_file
# Final response:
# The calculator app is now working correctly.
```

---

## Project Structure
```
ai_agent/
├── calculator/
│   ├── main.py
│   ├── pkg/
│   │   ├── calculator.py
│   │   └── render.py
│   └── tests.py
├── functions/
│   ├── __init__.py
│   ├── get_files_info.py
│   ├── get_file_content.py
│   └── write_file.py
├── config.py
├── main.py
└── .env
```

---

## Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager
- A valid [Gemini API key](https://aistudio.google.com/app/apikey)

---

## Setup

1. Clone the repository:
```sh
   git clone https://github.com/Adrianbrou/ai_agent.git
   cd ai_agent
```

2. Install dependencies:
```sh
   uv sync
```

3. Create a `.env` file in the project root:
```sh
   GEMINI_API_KEY=your_api_key_here
```

---

## Usage

**Basic prompt:**
```sh
uv run main.py "your task here"
```

**Verbose mode:**
```sh
uv run main.py "your task here" --verbose
```

---

## Phases

### Phase 1 — CLI AI Assistant
Single-turn CLI that sends a prompt to Gemini and prints the response. Supports verbose token usage output.

### Phase 2 — Tool-Calling Agent
Extends the agent with function calling so the model can interact with the local filesystem within a sandboxed working directory.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | Yes | Your Google Gemini API key |

---

## License

MIT