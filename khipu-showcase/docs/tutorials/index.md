# Tutorials Overview

This section contains step-by-step tutorials for common analysis workflows using the Khipu platform.

## Available Tutorials

### Beginner

| Notebook | Description | Time |
|----------|-------------|------|
| [Housing-Wage Divergence](../notebooks/01-metro-housing-wage-divergence.ipynb) | Analyze affordability gaps across metros | 15-20 min |

### Intermediate

| Notebook | Description | Time |
|----------|-------------|------|
| Gentrification Early Warning | Tract-level displacement modeling | 25-30 min |
| Environmental Justice Mapping | EPA EJScreen analysis | 20-25 min |

### Advanced

| Notebook | Description | Time |
|----------|-------------|------|
| Full Pipeline: Urban Resilience | Multi-source integration workflow | 45-60 min |

## Tutorial Structure

Each tutorial follows a consistent structure:

1. **Front Matter** - YAML metadata with title, authors, license, version
2. **Executive Summary** - Key findings and learning objectives
3. **Table of Contents** - Navigation links
4. **Setup and Imports** - Environment configuration
5. **Data Loading** - Loading and previewing data
6. **Analysis Sections** - Core analysis steps
7. **Visualization** - Charts and maps
8. **Key Insights** - Summary of findings
9. **Next Steps** - Links to related tutorials
10. **Data Provenance** - Full data documentation

## Running Tutorials

### Local

```bash
pip install khipu-demo
jupyter lab notebooks/
```

### Binder

Click the Binder badge on any notebook to launch it in the cloud.

### Docker

```bash
docker-compose -f docker/docker-compose.yml up jupyter
```

## Prerequisites

All tutorials assume:

- Python 3.9+
- Basic pandas/numpy knowledge
- Familiarity with Jupyter notebooks

Specific prerequisites are listed in each notebook's front matter.
