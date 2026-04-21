# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Eficiencia-Algoritmos** is a Python laboratory for empirically verifying theoretical Big O complexity. It implements algorithms across complexity classes (O(1), O(n), O(n log n), O(n²)), runs benchmarks against them, and generates scatter plots from real measured data. The project uses Python 3.11+ and `uv` exclusively as the package manager.

## Development Environment

### Setup
- **Python version**: 3.11+ (specified in `.python-version`)
- **Package manager**: `uv` (exclusive — do not use pip directly)
- **Virtual environment**: Managed automatically by `uv`
- **Dependencies**: `uv add matplotlib numpy` (required for benchmark visualizations)
- **Sync all dependencies**: `uv sync`

### Running the Project
- Main entry point: `main.py`
- Run with: `uv run main.py`

## Project Structure

- **algoritmos/**: Core algorithm implementations
  - `numeros.py`: `es_par_impar` — O(1) time, O(1) space
  - `estructuras.py`: stack and queue fill/drain — O(n)
  - `ordenamiento.py`: `bubble_sort` O(n²), `merge_sort` O(n log n)
  - `pares.py`: `contar_inversiones`, `encontrar_pares_suma` — O(n²)
  - `geometria.py`: circle collision detection — O(n²)

- **experimentos/**: 9 numbered benchmark scripts (01–09)
  - `img/`: Generated scatter plot images

- **colisiones_pygame.py**: Interactive real-time O(n²) collision demo (Pygame)
- **main.py**: Basic entry point

## Benchmarking and Experimentation

The project includes a framework for benchmarking algorithms to verify complexity claims:

### Running Benchmarks
```bash
uv run experimentos/01_es_par_impar_benchmark.py           # O(1): measure time vs number value
uv run experimentos/02_es_par_impar_cantidad_benchmark.py  # O(n): measure time vs quantity
uv run experimentos/03_estructura_llenar_benchmark.py      # O(n): stack vs queue fill times
uv run experimentos/04_estructura_vaciar_benchmark.py      # O(n): stack vs queue empty times
uv run experimentos/05_bubble_sort_benchmark.py            # O(n²): bubble sort performance
uv run experimentos/06_bubble_vs_merge_benchmark.py        # O(n²) vs O(n log n) comparison
uv run experimentos/07_contador_inversiones_benchmark.py   # O(n²): inversion counting
uv run experimentos/08_colisiones_benchmark.py             # O(n²): circle collision detection
uv run experimentos/09_dog_image_benchmark.py              # External latency (API calls)
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
