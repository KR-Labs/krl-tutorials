# Contributing Guidelines

Thank you for your interest in contributing to Khipu Showcase!

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please read and follow our Code of Conduct.

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Use the bug report template
3. Include reproduction steps
4. Attach relevant notebook output

### Suggesting Features

1. Open a feature request issue
2. Describe the use case
3. Explain the expected behavior

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `pytest tests/`
5. Run linting: `ruff check src/`
6. Commit with clear messages
7. Push and open a PR

## Development Setup

```bash
# Clone the repo
git clone https://github.com/KR-Labs/khipu-showcase.git
cd khipu-showcase

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run linting
ruff check src/ tests/
black --check src/ tests/
```

## Notebook Guidelines

When creating or modifying notebooks:

### Required Elements

1. **Front Matter** - YAML metadata block with:
   - title
   - authors
   - license (CC-BY-4.0)
   - version
   - date
   - tags
   - prerequisites

2. **Executive Summary** - Brief overview with:
   - Key findings (3-5 bullets)
   - Learning objectives
   - Estimated time
   - Difficulty level

3. **Table of Contents** - Navigation links

4. **Data Provenance** - Always include:
   - Source
   - License
   - Transformation steps
   - Dataset hash

### Security Requirements

- **No API keys or credentials** in notebooks
- **No real PII** - use synthetic data only
- **DEMO_MODE=true** must be the default
- All data must be reproducible

### Accessibility

- Use colorblind-safe palettes
- Include alt text for visualizations
- Ensure WCAG AA contrast ratios
- Provide text alternatives for charts

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings (Google style)
- Maximum line length: 100 characters

## Testing

- Unit tests in `tests/`
- Notebook tests with nbval
- Minimum coverage: 70%

```bash
# Run all tests
pytest tests/ -v --cov=khipu_demo

# Run notebook tests
pytest notebooks/ --nbval --nbval-lax
```

## Documentation

- Update docs for new features
- Use MkDocs with Material theme
- Preview locally: `mkdocs serve`

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create a GitHub release
4. CI will publish to PyPI
