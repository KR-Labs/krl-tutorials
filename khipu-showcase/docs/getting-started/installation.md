# Installation

This guide covers how to install the `khipu-demo` package for running the showcase notebooks.

## Requirements

- Python 3.9 or higher
- pip (Python package manager)

## Installation Methods

### Using pip (Recommended)

```bash
pip install khipu-demo
```

### Development Installation

For contributing or modifying the package:

```bash
git clone https://github.com/KR-Labs/khipu-showcase.git
cd khipu-showcase
pip install -e ".[dev]"
```

### With Optional Dependencies

Install with geospatial tools:

```bash
pip install "khipu-demo[geospatial]"
```

Install with machine learning tools:

```bash
pip install "khipu-demo[ml]"
```

Install everything:

```bash
pip install "khipu-demo[all]"
```

## Verify Installation

```python
from khipu_demo import DEMO_MODE, __version__

print(f"khipu-demo version: {__version__}")
print(f"Demo mode: {DEMO_MODE}")
```

## Running Notebooks

After installation, start Jupyter:

```bash
jupyter lab
```

Then navigate to the `notebooks/` directory and open any notebook.

## Docker Installation

If you prefer using Docker:

```bash
# Clone the repository
git clone https://github.com/KR-Labs/khipu-showcase.git
cd khipu-showcase

# Start JupyterLab with Docker Compose
docker-compose -f docker/docker-compose.yml up jupyter
```

Access JupyterLab at: http://localhost:8888

## Troubleshooting

### ImportError for khipu_demo

Ensure you're using Python 3.9+:

```bash
python --version
```

### Missing visualization libraries

Install visualization dependencies:

```bash
pip install plotly matplotlib
```

### Notebook kernel not found

Install the IPython kernel:

```bash
pip install ipykernel
python -m ipykernel install --user --name khipu-demo
```
