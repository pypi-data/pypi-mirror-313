# Rustils

[![Tests](https://github.com/tsonglew/rustils/actions/workflows/test.yml/badge.svg)](https://github.com/tsonglew/rustils/actions/workflows/test.yml)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/tsonglew/rustils)](https://github.com/tsonglew/rustils/releases)
[![Publish to PyPI](https://github.com/tsonglew/rustils/actions/workflows/publish.yml/badge.svg)](https://github.com/tsonglew/rustils/actions/workflows/publish.yml)

A collection of utility functions implemented in Rust with Python bindings, focusing on performance and reliability.

## Features

### String to Boolean Conversion

- `str_to_bool(s: str) -> bool`: Convert string to boolean (Rust implementation)
- `py_str_to_bool(s: str) -> bool`: Convert string to boolean (Python reference implementation)

Supported values:

- True: "true", "1", "yes", "y", "on" (case-insensitive)
- False: "false", "0", "no", "n", "off" (case-insensitive)

### 3D Point Distance Calculation

- `point3d_distance(p1: Tuple[float, float, float], p2: Tuple[float, float, float]) -> float`: Calculate Euclidean distance between two 3D points (Rust implementation)
- `py_point3d_distance(p1: Tuple[float, float, float], p2: Tuple[float, float, float]) -> float`: Calculate Euclidean distance between two 3D points (Python reference implementation)

Example:

```python
from rustils import point3d_distance

# Calculate distance between two 3D points
distance = point3d_distance((0, 0, 0), (1, 1, 1))  # Returns sqrt(3)
```

## Installation

### Requirements

- Python >= 3.9
- Rust toolchain (for development)
- Poetry (for dependency management)

### Installing from Source

```bash
# Clone the repository
git clone https://github.com/tsonglew/rustils.git
cd rustils

# Install with poetry
poetry install
```

## Usage

### Python Interface

```python
from rustils import str_to_bool, py_str_to_bool

# Using Rust implementation
result = str_to_bool("yes")  # Returns True
result = str_to_bool("0")    # Returns False

# Using Python implementation
result = py_str_to_bool("true")  # Returns True
result = py_str_to_bool("n")     # Returns False

# Invalid inputs raise ValueError
try:
    str_to_bool("invalid")
except ValueError as e:
    print(e)  # Cannot convert 'invalid' to bool
```

## Performance Comparison

Benchmark results comparing Rust and Python implementations:

### Single Value Operation

```
Name (time in ns)                Min      Max     Mean    StdDev   Median   OPS (Kops/s)
----------------------------------------------------------------------------------------
test_benchmark_single_python    123.75   11,469   138.41   77.46   135.00   7,224.79
test_benchmark_single_rust      500.00  631,292   635.66  2,730.91  625.00   1,573.17
```

### Multiple Values Operation

```
Name (time in ns)            Min       Max      Mean     StdDev    Median   OPS (Kops/s)
----------------------------------------------------------------------------------------
test_benchmark_python       1,597.00  334,764  1,732.36  1,699.67  1,653.00    577.25
test_benchmark_rust         6,541.00  107,125  7,141.03  1,862.39  6,959.00    140.04
```

Note: For this simple operation, the Python implementation shows better performance due to the overhead of crossing the Python/Rust boundary. For more complex operations or larger datasets, the Rust implementation would likely show better performance.

## Development

### Common Commands

The project includes a Makefile for common development tasks:

```bash
# Install dependencies
make install

# Run tests
make test

# Run benchmarks
make benchmark

# Format code
make format

# Run linting
make lint

# Build package
make build

# Publish to PyPI
make publish

# Show all available commands
make help
```

### Setting up Development Environment

```bash
# Install development dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run only benchmark tests
poetry run pytest tests/test_benchmark.py -v --benchmark-only
```

### Project Structure

```
rustils/
├── Cargo.toml          # Rust package configuration
├── pyproject.toml      # Python package configuration
├── rustils/
│   ├── __init__.py    # Python package initialization
│   └── py_utils.py    # Python implementation
├── src/
│   └── lib.rs         # Rust implementation
└── tests/
    ├── test_basic.py     # Basic functionality tests
    └── test_benchmark.py # Performance benchmark tests
```

## License

MIT License - see the [LICENSE](LICENSE) file for details
