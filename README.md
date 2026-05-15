# repo-01-llm-task-router

Lesson repo for building a minimal LLM task router. Lesson 1 focuses on `.env` loading, provider abstraction, and a multi-turn CLI chatbot. Lesson 2 introduces Pydantic schemas, prompt templates, function calling tools, and task routing.

## Structure

```text
repo-01-llm-task-router/
  src/
    config.py
    llm_client.py
    main.py
    schemas.py
    prompts.py
    tools.py
    router.py
  tests/
    test_llm_client.py
    test_router.py
  assignments/
    week-1-llm-task-router.md
  notebooks/
    01_llm_basics.ipynb
    02_structured_output_and_tools.ipynb
```

## Setup

This repo uses `uv` to manage the Python environment and dependencies.

```bash
uv sync --extra dev
```

This reads `pyproject.toml` and `uv.lock`, then creates a local virtual environment:

```text
.venv/
```

You usually do not need to activate `.venv` manually. Use `uv run` to execute commands inside the repo environment.

Optional manual activation:

```bash
source .venv/bin/activate
```

Create your local environment file:

```bash
cp .env.example .env
```

Then edit `.env` and fill in at least one real API key:

```bash
OPENAI_API_KEY=...
# or
ANTHROPIC_API_KEY=...
```

For offline tests and non-router exercises, you can use:

```bash
LLM_PROVIDER=mock
```

For the Week 1 assignment and real OpenAI calls, use:

```bash
LLM_PROVIDER=openai
LLM_MODEL=gpt-5.4-mini
```

Never commit `.env`.

## Check Environment

Before class, run:

```bash
uv run python check_env.py
```

This checks Python version, `uv`, virtual environment status, and whether at least one API key is available from `.env`.

## Run Tests

```bash
uv run --extra dev pytest
```

## Run the CLI Chatbot

```bash
uv run python -m src.main
```

Type `exit` or `quit` to stop.

## Week 1 Assignment

Build a real LLM-powered task router CLI. The core requirement is that `route_task` must use a real LLM structured-output call to classify user requests. It should not rely on local keyword rules or a mock router for the main app behavior.

The repo starts with working infrastructure and clear TODOs:

- `src/config.py` and `src/llm_client.py` provide environment loading and basic LLM chat calls.
- `src/schemas.py` defines the structured route schema.
- `src/router.py` contains the `route_task` function students must implement with a real LLM call.
- `src/main.py` contains the CLI route-handling skeleton.
- `src/tools.py` contains example local tools and a tool registry.

Read the full assignment here:

[Week 1 Assignment: LLM-Powered Task Router](assignments/week-1-llm-task-router.md)

## Notebooks

Register the repo `.venv` as a Jupyter kernel:

```bash
uv run --extra dev python -m ipykernel install --user \
  --name repo-01-llm-task-router \
  --display-name "Python (.venv: repo-01-llm-task-router)"
```

Start Jupyter with the repo environment:

```bash
uv run --extra dev jupyter notebook
```

If you prefer JupyterLab:

```bash
uv run --extra dev jupyter lab
```

Then open:

```text
notebooks/01_llm_basics.ipynb
notebooks/02_structured_output_and_tools.ipynb
```

In the notebook UI, choose this kernel:

```text
Python (.venv: repo-01-llm-task-router)
```

If `from dotenv import load_dotenv` fails, the notebook is using the wrong kernel. Switch to the kernel above and restart the notebook kernel.

The first notebook walks through direct API calls, chat completion parameters, multi-turn message history, and the bridge from notebook code to `src/llm_client.py`.

## Troubleshooting

If OpenAI raises this error:

```text
UnsupportedProtocol: Request URL is missing an 'http://' or 'https://' protocol.
```

check `.env` for this line:

```bash
OPENAI_BASE_URL=
```

For normal OpenAI usage, delete that line or comment it out. If you are using an OpenAI-compatible provider, set a full URL including `https://`.

## Notes for Students

- First debug step: verify the API key is loaded from `.env`.
- `messages` is the model input. If history is missing, the model has no memory.
- `finish_reason` and `usage` are required debugging signals.
- Tests should not call real paid APIs; use mocks or monkeypatching in tests only.
