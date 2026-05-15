# Week 1 Assignment: LLM-Powered Task Router

## Goal

Build a small CLI app that takes a natural-language user request, asks a real LLM to classify the request into a structured route, and then executes the corresponding branch.

This assignment is not about writing a local keyword classifier. The router must use an actual LLM call for route decisions.

## Learning Objectives

By the end of this assignment, you should be able to:

- Load environment variables from `.env`.
- Configure a real LLM provider through the project client code.
- Use structured output to turn an LLM response into a validated Pydantic model.
- Route user requests into task categories such as `chat`, `summarize`, `translate`, and `tool_call`.
- Connect an LLM routing decision to a small CLI workflow.
- Register and call a local Python tool from a router decision.

## Recommended workflow

Work from **your own copy** of this repository so you can push commits, experiment freely, and keep API keys out of any public history.

1. On GitHub, **fork** the course repository to your account.
2. **Clone your fork** locally (not the instructor copy, unless you only need read-only reference).
3. Add a local `.env` from `.env.example` and **never commit** `.env` or real API keys.
4. Optional: add the original course repo as `upstream` if you want to **pull updates** from the instructor later:

```bash
git remote add upstream <course-repo-git-url>
git fetch upstream
```

After that, follow **Setup** below on your machine.

## Starter Code Map

This repo gives you a working foundation, but it intentionally does not implement the core router for you.

- `src/config.py`: loads settings from `.env`.
- `src/llm_client.py`: provides a basic provider abstraction and `chat(...)` helper.
- `src/schemas.py`: defines `TaskType`, `RouteDecision`, and `ToolCall`.
- `src/prompts.py`: provides the starter router prompt.
- `src/router.py`: contains `parse_route_decision(...)` and the `route_task(...)` TODO.
- `src/main.py`: contains the CLI loop and route-handling skeleton.
- `src/tools.py`: contains example local tools, `TOOLS`, and `call_tool(...)`.
- `tests/`: verifies starter infrastructure and gives you a place to add assignment tests.

Your main job is to replace the `route_task(...)` TODO with a real LLM structured-output implementation and then complete the CLI route branches.

## Setup

Install dependencies:

```bash
uv sync --extra dev
```

Create your local `.env` file:

```bash
cp .env.example .env
```

For this assignment, configure a real OpenAI provider:

```bash
LLM_PROVIDER=openai
LLM_MODEL=gpt-5.4-mini
OPENAI_API_KEY=your_api_key_here
```

Never commit `.env`.

Check your environment:

```bash
uv run python check_env.py
```

Run the test suite:

```bash
uv run --extra dev pytest
```

The starter tests should pass before you begin. They do not prove the assignment is complete. You will need to add or update tests for your LLM router behavior.

## Required Tasks

### 1. Implement a Real LLM Router

Modify `src/router.py` so that `route_task` uses a real LLM structured-output call to classify the user request.

The function must:

- Call the OpenAI Responses API through `client.responses.create(...)` or the project LLM client wrapper if you extend it cleanly.
- Request JSON schema structured output.
- Validate the LLM output as a `RouteDecision` Pydantic model.
- Support at least these route types: `chat`, `summarize`, `translate`, and `tool_call`.
- Include a confidence score and a short reason in the returned `RouteDecision`.

The main application behavior must not use keyword rules or a mock router for route decisions.

### 2. Update the CLI

Modify `src/main.py` so the CLI:

- Accepts user input in a loop.
- Calls `route_task` for each user request.
- Prints the route, confidence, and reason.
- Handles each route with an appropriate branch.

At minimum:

- `chat` should produce a normal assistant response.
- `summarize` should summarize text or ask the user for text to summarize.
- `translate` should translate text or ask for the missing target language/text.
- `tool_call` should call a local Python tool.

### 3. Add or Extend a Local Tool

Modify `src/tools.py` so the app has at least one local tool the router can choose.

Examples:

- `get_word_count(text: str) -> int`
- `uppercase(text: str) -> str`
- `reverse_text(text: str) -> str`

Register the tool in `TOOLS`, and make sure it can be called through `call_tool`.

### 4. Use Structured Data

Use the existing models in `src/schemas.py`, or extend them if needed.

The route decision should remain structured and validated. Do not pass raw JSON strings around the app after validation.

### 5. Add Tests

Automated tests should not depend on paid API calls.

Add tests that cover:

- `RouteDecision` validation.
- Router parsing/validation using a fake or monkeypatched LLM response.
- CLI branch behavior where practical.
- Local tool registration and execution.

It is okay for tests to mock the LLM response. The production `route_task` implementation itself must still be designed to call a real LLM.

When you implement `route_task(...)`, update `tests/test_router.py` so it verifies the real router code path with a fake LLM response instead of calling the live API.

## Expected CLI Behavior

When running:

```bash
uv run python -m src.main
```

The app should behave like this:

```text
LLM Task Router CLI
Type 'exit' to quit.

You: summarize this paragraph about agent memory
Route: summarize (0.92)
Reason: User asks for a summary.
Bot: Please paste the paragraph you want summarized.

You: translate "good morning" into Chinese
Route: translate (0.96)
Reason: User requests translation.
Bot: 早上好

You: count words in "structured output is useful"
Route: tool_call (0.88)
Reason: User asks for a word count, which can be handled by a local tool.
Tool: get_word_count
Result: 4

You: what is a Python decorator?
Route: chat (0.81)
Reason: User asks a general explanation question.
Bot: A Python decorator is ...
```

The exact wording can differ, but the route decision must come from the LLM.

## Manual Real API Check

Because automated tests should avoid real paid API calls, run a manual check with OpenAI enabled:

```bash
LLM_PROVIDER=openai uv run python -m src.main
```

Try at least four prompts:

- A general chat question.
- A summarize request.
- A translate request.
- A tool request.

Keep the prompts, routes, and outputs as your own debugging notes so you can compare behavior as you improve the router.

## Stretch Goals

- Add more route types, such as `write_code`, `data_analysis`, or `unknown`.
- Let the router return a specific tool name and arguments for `tool_call`.
- Use OpenAI function calling for tool execution.
- Add a confidence threshold and fallback behavior.
- Add support for another real provider.
- Improve CLI UX with clearer prompts and error handling.

## Self-Check

Before you consider the assignment complete, make sure:

- `uv run python check_env.py` passes.
- `uv run --extra dev pytest` passes.
- `route_task` uses a real LLM structured-output call in production code.
- The CLI shows route, confidence, and reason.
- At least one local tool can be executed through the CLI.
- You tested the app manually with `LLM_PROVIDER=openai`.
- `.env` stays local and is not shared.

