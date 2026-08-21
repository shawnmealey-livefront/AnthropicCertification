# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A Python package implementing document-related tools (conversion, processing) exposed through an MCP (Model Context Protocol) server for integration with AI assistants. Built with `mcp[cli]` (FastMCP) and `markitdown` for document-to-markdown conversion.

## Setup and commands

```bash
# Create a virtual env and activate it
uv venv
source .venv/bin/activate

# Install the package in development mode
uv pip install -e .

# Start the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test file / test
uv run pytest tests/test_document.py
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_pdf
```

**Python version gotcha:** `uv venv` with no arguments picks the newest installed CPython. `onnxruntime` (a transitive dependency of `markitdown`/`magika`, pinned to `1.21.1` in `uv.lock`) does not publish wheels for Python 3.14, so a venv created against 3.14 will fail during `uv run pytest` with a resolution error. If that happens, recreate the venv against an already-installed 3.13 interpreter: `rm -rf .venv && uv venv --python 3.13`, then reinstall with `uv pip install -e .`.

## Architecture

- `main.py` — creates the `FastMCP("docs")` server instance and registers tool functions with `mcp.tool()(fn)`. This is the wiring point: a function existing in `tools/` does **not** make it available to the server — it must be explicitly registered here.
- `tools/` — plain Python functions implementing the actual tool logic, decoupled from MCP registration. Each function is written to be self-documenting for an LLM caller, since the MCP client only sees the function signature + docstring, not the implementation (see "Defining MCP tools" below).
  - `tools/math.py` — `add`, currently the only tool registered in `main.py`.
  - `tools/document.py` — `binary_document_to_markdown(binary_data, file_type)`, converts binary document bytes (e.g. docx, pdf) to markdown text via `markitdown`. Has test coverage in `tests/test_document.py` but is **not yet registered** with `mcp.tool()` in `main.py` — wire it up there when making it available to the server.
- `tests/` — pytest tests import directly from `tools.*` (not through the MCP layer), and use binary fixtures in `tests/fixtures/` (`mcp_docs.docx`, `mcp_docs.pdf`) for document conversion tests.

## Defining MCP tools

Tools are plain Python functions, registered with the MCP server via:

```python
mcp.tool()(my_function)
```

Because the MCP client sees only the function's signature and docstring (never its implementation), both must fully specify how an LLM should call the tool.

**Docstrings** should:

- Begin with a one-line summary
- Provide a detailed explanation of functionality
- Explain when to use (and not use) the tool
- Include usage examples with expected input/output

**Parameters** should use `Field` from `pydantic` for descriptions:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does")
) -> ReturnType:
    """Comprehensive docstring here"""
    # Implementation
```

`tools/math.py::add` is the reference example already in the codebase for this pattern (one-line summary, fuller explanation, "When to use" section, and doctest-style examples with expected output).

## Code style

- Always apply appropriate type annotations to function arguments (and return types), as already done throughout `tools/*.py`.
