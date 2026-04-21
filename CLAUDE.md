# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Eficiencia-Algoritmos** is a Python project for studying and implementing algorithms with a focus on algorithmic efficiency. The project uses Python 3.11 and is configured with a minimal initial setup.

## Development Environment

### Setup
- **Python version**: 3.11+ (specified in `.python-version`)
- **Package manager**: Use `pip` with pyproject.toml as the project specification
- **Virtual environment**: Create with `python -m venv venv` and activate with `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix)

### Running the Project
- Main entry point: `main.py`
- Run with: `uv run main.py`

## Expected Architecture

This project is set up for implementing and analyzing algorithms. Expected structure:
- **main.py**: Entry point, should coordinate algorithm demonstrations or benchmarks
- Algorithm implementations: Likely to be organized by category (sorting, searching, dynamic programming, etc.) or by efficiency analysis
- Code should emphasize clarity and measurable performance characteristics

## Code Quality and Testing

The `.gitignore` indicates support for:
- **pytest**: For unit testing (`pytest` or specific tests with `pytest tests/test_*.py`)
- **coverage**: For test coverage reports
- **ruff**: For linting and code formatting (recommended for Python 3.11 codebases)
- **mypy**: For static type checking

While not yet configured, these tools are recommended as the project grows to ensure algorithm implementations are correct and performant.

## Key Considerations

- **Algorithm documentation**: Include time and space complexity analysis in docstrings
- **Performance testing**: When analyzing efficiency, include benchmarking code to verify algorithmic complexity claims
- **Type hints**: Use Python type annotations to make algorithm signatures clear
