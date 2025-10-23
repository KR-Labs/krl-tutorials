# Installation & Setup

Complete guide to setting up your environment for KRL Tutorials.

## Prerequisites

### Required Software
- **Python**: 3.9 or higher
- **Jupyter**: JupyterLab or Jupyter Notebook
- **Git**: For cloning the repository

### Recommended Tools
- **Anaconda/Miniconda**: For environment management
- **VS Code**: With Python and Jupyter extensions
- **GitHub Desktop**: For easier repository management

## Installation Methods

### Method 1: Quick Install (Recommended for Beginners)

```bash
# Clone the repository
git clone https://github.com/KR-Labs/krl-tutorials.git
cd krl-tutorials

# Install dependencies
pip install -r config/requirements_opensource.txt

# Launch Jupyter
jupyter notebook
```

### Method 2: Conda Environment (Recommended for Isolation)

```bash
# Clone the repository
git clone https://github.com/KR-Labs/krl-tutorials.git
cd krl-tutorials

# Create conda environment
conda env create -f config/environment.yml

# Activate environment
conda activate krl-tutorials

# Launch Jupyter
jupyter lab
```

### Method 3: Virtual Environment (venv)

```bash
# Clone the repository
git clone https://github.com/KR-Labs/krl-tutorials.git
cd krl-tutorials

# Create virtual environment
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
.\venv\Scripts\activate

# Install dependencies
pip install -r config/requirements_opensource.txt

# Launch Jupyter
jupyter notebook
```

## Dependency Overview

### Core Libraries
```
pandas >= 1.5.0
numpy >= 1.23.0
matplotlib >= 3.6.0
seaborn >= 0.12.0
```

### Statistical & ML
```
scikit-learn >= 1.2.0
statsmodels >= 0.14.0
scipy >= 1.10.0
```

### Visualization
```
plotly >= 5.13.0
altair >= 4.2.0
```

### Data Access
```
pandas-datareader >= 0.10.0
fredapi >= 0.5.0
census >= 0.8.0
```

## Verifying Installation

Run this verification script:

```python
import sys
import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns
import sklearn
import statsmodels
import plotly

print(f"Python: {sys.version}")
print(f"Pandas: {pd.__version__}")
print(f"NumPy: {np.__version__}")
print(f"Matplotlib: {matplotlib.__version__}")
print(f"Seaborn: {sns.__version__}")
print(f"Scikit-learn: {sklearn.__version__}")
print(f"Statsmodels: {statsmodels.__version__}")
print(f"Plotly: {plotly.__version__}")

print("\n✅ All core libraries installed successfully!")
```

## API Keys Setup

Some tutorials require API keys for data access.

### FRED API (Federal Reserve Economic Data)

1. Register at: https://fred.stlouisfed.org/docs/api/api_key.html
2. Add to `config/apikeys`:
```
FRED_API_KEY=your_key_here
```

### Census API

1. Register at: https://api.census.gov/data/key_signup.html
2. Add to `config/apikeys`:
```
CENSUS_API_KEY=your_key_here
```

### Loading API Keys in Notebooks

```python
import os
from pathlib import Path

# Load API keys
config_path = Path(__file__).parent.parent / 'config' / 'apikeys'
with open(config_path) as f:
    for line in f:
        if '=' in line and not line.startswith('#'):
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

# Use keys
import fredapi
fred = fredapi.Fred(api_key=os.environ['FRED_API_KEY'])
```

## Repository Structure

```
krl-tutorials/
├── notebooks/           # All 33 tutorial notebooks
│   ├── 01_economic/    # D01-D05
│   ├── 02_social/      # D06-D10
│   └── ...
├── config/             # Configuration files
│   ├── apikeys         # API credentials (create this)
│   ├── environment.yml # Conda environment
│   └── requirements*.txt
├── data/               # Data directory (auto-created)
│   ├── raw/           # Original data
│   ├── processed/     # Cleaned data
│   └── external/      # External sources
├── docs/              # Documentation
└── tests/             # Test suite
```

## Troubleshooting Installation

### Issue: Package conflicts

**Solution**: Use a fresh environment
```bash
conda create -n krl-tutorials-fresh python=3.11
conda activate krl-tutorials-fresh
pip install -r config/requirements_opensource.txt
```

### Issue: Jupyter kernel not found

**Solution**: Register the kernel
```bash
python -m ipykernel install --user --name krl-tutorials --display-name "KRL Tutorials"
```

### Issue: Import errors in notebooks

**Solution**: Ensure you're in the correct directory
```bash
cd krl-tutorials
jupyter notebook notebooks/
```

### Issue: SSL certificate errors

**Solution**: Update certificates
```bash
pip install --upgrade certifi
```

## Platform-Specific Notes

### macOS
- May need to install Xcode Command Line Tools:
  ```bash
  xcode-select --install
  ```

### Windows
- Use Anaconda Prompt or PowerShell (not CMD)
- Some visualizations may require additional setup

### Linux
- May need system packages:
  ```bash
  sudo apt-get install python3-dev build-essential
  ```

## Next Steps

Once installation is complete:

1. **[Run the Quick Start Guide](Quick-Start-Guide)** - Test your setup
2. **[Choose a Learning Path](Learning-Paths)** - Find your starting point
3. **[Browse the Tutorial Catalog](Tutorial-Catalog)** - Explore available tutorials

## Getting Help

- **Installation Issues**: [Open an issue](https://github.com/KR-Labs/krl-tutorials/issues/new?template=bug_report.yml)
- **Questions**: [Start a discussion](https://github.com/KR-Labs/krl-tutorials/discussions)
- **General Support**: See [SUPPORT.md](https://github.com/KR-Labs/krl-tutorials/blob/main/.github/SUPPORT.md)

---

**Last Updated**: October 2025
