# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Eficiencia-Algoritmos** is a Python project for studying and implementing algorithms with a focus on algorithmic efficiency. The project uses Python 3.11 and is configured with a minimal initial setup.

## Development Environment

### Setup
- **Python version**: 3.11+ (specified in `.python-version`)
- **Package manager**: Use `pip` with pyproject.toml as the project specification
- **Virtual environment**: Create with `python -m venv venv` and activate with `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix)
- **Dependencies**: `pip install matplotlib numpy` (required for benchmark visualizations)

### Running the Project
- Main entry point: `main.py`
- Run with: `uv main.py`
- install with uv add

## Project Structure

- **algoritmos/**: Core algorithm implementations
  - `numeros.py`: Number-related algorithms (e.g., `es_par_impar`)
  - `estructuras.py`: Data structure implementations (stack, queue operations)
  
- **experimentos/**: Benchmarking and efficiency analysis scripts
  - `*_benchmark.py`: Scripts that measure algorithm performance
  - `img/`: Generated performance visualization graphs
  - Benchmarks measure time complexity across different input sizes using `matplotlib`

- **main.py**: Entry point for demonstrations

## Benchmarking and Experimentation

The project includes a framework for benchmarking algorithms to verify complexity claims:

### Running Benchmarks
```bash
python experimentos/es_par_impar_benchmark.py           # Measure time vs number value
python experimentos/es_par_impar_cantidad_benchmark.py  # Measure time vs quantity (O(n))
python experimentos/estructura_llenar_benchmark.py      # Compare stack vs queue fill times
python experimentos/estructura_vaciar_benchmark.py      # Compare stack vs queue empty times
```

### Benchmark Conventions
- Use linear axes for O(n) complexity visualization
- Use logarithmic axes to compress large value ranges
- Scatter plots show raw timing data without trend lines (let data speak for itself)
- All graphs save to `experimentos/img/` automatically
- Measure **total time** when benchmarking operations on N items (not per-item time)

## Algorithm Implementation Standards

When adding new algorithms or structures to `algoritmos/`:

1. **Complexity Analysis**: Include time and space complexity in docstrings (see `es_par_impar` for format)
2. **Type Hints**: Use Python type annotations for all function signatures
3. **Benchmarking**: Create corresponding benchmark scripts in `experimentos/` to verify O(n) claims with empirical data
4. **Naming**: Use Spanish names for functions (consistent with existing code)

## Creating New Benchmarks

When creating a new benchmark experiment:
1. Create a `*_benchmark.py` file in `experimentos/`
2. Use `time.perf_counter()` for high-resolution timing
3. Run operations multiple times (`repetitions` parameter) to average out system noise
4. Use `np.logspace()` to generate test points across a wide range
5. Visualize with `matplotlib` scatter plots (linear axes for clarity)
6. Save figures to `experimentos/img/` using absolute paths with `os.path.join()`
