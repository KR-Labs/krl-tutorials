# GitHub Actions Workflows - Tutorial Repository

## Overview

This repository uses GitHub Actions workflows specifically designed for educational Jupyter notebook repositories. These workflows focus on content quality, structure validation, and documentation standards rather than Python package development.

## Active Workflows

### 1. Notebook Validation (`notebook-validation.yml`)

**Purpose**: Ensures all Jupyter notebooks are structurally valid and maintain clean state for version control.

**Triggers**:
- Push to `main` branch (when notebooks change)
- Pull requests to `main` branch (when notebooks change)

**What it checks**:
- ✅ JSON structure validation (ensures notebooks are valid nbformat)
- ✅ Execution artifacts detection (warns about leftover outputs/execution counts)
- ✅ Notebook metadata verification (kernel info, language)
- ✅ Cell counts and structure

**Why it matters**: Prevents corrupted notebooks and reduces diff noise from execution outputs.

---

### 2. Markdown Quality (`markdown-quality.yml`)

**Purpose**: Maintains high-quality documentation with consistent formatting and valid links.

**Triggers**:
- Push to `main` branch (when .md files change)
- Pull requests to `main` branch (when .md files change)

**What it checks**:
- ✅ Markdown linting with `markdownlint-cli` (formatting consistency)
- ✅ Link validation with `markdown-link-check` (no broken links)
- ✅ Spell checking with `cspell` (professional documentation)

**Configuration files**:
- `.markdownlint.json` - Markdown style rules
- `.markdown-link-check.json` - Link checking settings
- `.cspell.json` - Custom dictionary (technical terms, product names)

**Why it matters**: Professional documentation builds trust and improves learning experience.

---

### 3. Tutorial Quality (`tutorial-quality.yml`)

**Purpose**: Validates educational content quality and repository structure.

**Triggers**:
- Push to `main` branch
- Pull requests to `main` branch

**What it checks**:
- ✅ Repository structure (required directories: `notebooks/`, `docs/`, `.github/`)
- ✅ Required files present (`README.md`, `LICENSE`, `CONTRIBUTING.md`)
- ✅ Notebook organization by tier (D1-D6 classification)
- ✅ Copyright headers in notebooks
- ✅ Learning objectives present (educational standards)
- ✅ References sections present (academic rigor)
- ✅ Code-to-text ratio analysis (ensures adequate explanations)

**Quality thresholds**:
- Markdown cells should be ≥30% of total cells (educational balance)
- Each notebook should have clear learning objectives
- Each notebook should include References section

**Why it matters**: Maintains educational standards and consistent learning experience across all tutorials.

---

## Removed Workflows (Saved as .disabled)

The following workflows were designed for Python package development and are **not appropriate** for tutorial repositories. They have been saved with `.disabled` extensions for potential use in private package repositories:

### `lint.yml.disabled`
- Python code linting (black, isort, flake8, mypy)
- Expected `src/` directory structure
- Appropriate for: `krl-core`, `krl-data-connectors`, `krl-models`, `krl-dashboard`

### `test.yml.disabled` & `tests.yml.disabled`
- Package unit testing with pytest
- Expected installable package structure
- Appropriate for: Private package repositories with test suites

### `build-and-sign.yml.disabled`
- Python package building and signing
- Package distribution workflow
- Appropriate for: Production package releases

### `security-checks.yml.disabled`
- Copyright header verification (requires `scripts/security/verify_copyright_headers.py`)
- Trademark verification (requires `scripts/security/check_trademarks.py`)
- Gitleaks secret scanning (requires `.gitleaks.toml`)
- License compliance scanning
- Appropriate for: Repositories with security verification scripts

**Location**: `/Users/bcdelo/KR-Labs/krl-tutorials/.github/workflows/*.disabled`

**To reuse in other repositories**:
```bash
# Copy to another repository
cp krl-tutorials/.github/workflows/lint.yml.disabled krl-core/.github/workflows/lint.yml
cp krl-tutorials/.github/workflows/test.yml.disabled krl-core/.github/workflows/test.yml
# etc.
```

---

## Workflow Status

**Current Status**: ✅ All 3 tutorial workflows passing

| Workflow | Status | Last Run |
|----------|--------|----------|
| Notebook Validation | ✓ Passed | ~1 minute ago |
| Markdown Quality | ✓ Passed | ~1 minute ago |
| Tutorial Quality | ✓ Passed | ~1 minute ago |

**Previous Status**: ❌ 89 failed runs (workflows designed for package repos)

---

## Configuration Files

### `.markdownlint.json`
- MD003: Use ATX-style headers (`#` syntax)
- MD007: Indent lists with 2 spaces
- MD013: Line length limit 120 characters
- MD024: Allow duplicate headers if not siblings
- MD025: Allow multiple level-1 headers (disabled)
- MD033: Allow inline HTML (disabled)
- MD034: Allow bare URLs (disabled)
- MD041: Don't require first line to be header (disabled)

### `.markdown-link-check.json`
- Ignore localhost URLs (development servers)
- Ignore krlabs.dev (may not be live yet)
- Retry on 429 (rate limiting) with 30s delay
- 20-second timeout per link
- GitHub-specific headers for API access

### `.cspell.json`
- Custom dictionary includes: KR-Labs, KRAnalytics, Quipu, Giddasira
- Python packages: pandas, numpy, scipy, sklearn, statsmodels, matplotlib, seaborn, plotly
- Data sources: FRED, BLS, OECD, Census Bureau
- File formats: jupyter, ipynb, nbformat, nbconvert
- Ignores: `node_modules/`, `htmlcov/`, `*.ipynb`, `.git/`, `__pycache__/`

---

## Running Workflows Locally

### Notebook Validation
```bash
# Validate notebook structure
python -c "
import nbformat
from pathlib import Path

for nb_path in Path('notebooks').rglob('*.ipynb'):
    with open(nb_path) as f:
        nb = nbformat.read(f, as_version=4)
    print(f'✅ {nb_path.name} - Valid')
"
```

### Markdown Linting
```bash
# Install markdownlint-cli
npm install -g markdownlint-cli

# Run linting
markdownlint '**/*.md' --ignore node_modules --config .markdownlint.json
```

### Link Checking
```bash
# Install markdown-link-check
npm install -g markdown-link-check

# Check links
markdown-link-check README.md --config .markdown-link-check.json
```

### Spell Checking
```bash
# Install cspell
npm install -g cspell

# Run spell checker
cspell "**/*.md" --config .cspell.json
```

---

## Best Practices

### Before Committing Notebooks
1. **Clear all outputs**: `Kernel > Restart & Clear Output` in Jupyter
2. **Validate structure**: Run notebook validation script locally
3. **Check metadata**: Ensure kernel info is correct

### Before Committing Documentation
1. **Run markdownlint**: Fix formatting issues
2. **Check links**: Verify no broken external links
3. **Spell check**: Add technical terms to `.cspell.json` if needed

### Pull Request Guidelines
1. All 3 workflows must pass before merging
2. Address any warnings in workflow output (continue-on-error items)
3. Maintain ≥30% markdown cells in notebooks (educational balance)
4. Include learning objectives and References in new tutorials

---

## Troubleshooting

### Notebook Validation Fails
- **Cause**: Corrupted notebook JSON
- **Fix**: Open notebook in Jupyter, verify it loads, re-save

### Markdown Quality Fails
- **Cause**: Broken links or formatting issues
- **Fix**: Run `markdownlint` locally, fix issues, update `.markdownlint.json` if rule is too strict

### Tutorial Quality Warns About Missing References
- **Cause**: Notebook lacks `## References` section
- **Fix**: Add References section with academic citations, data source URLs, documentation links

### Code-to-Text Ratio Warning
- **Cause**: Less than 30% markdown cells (too code-heavy)
- **Fix**: Add explanatory markdown cells between code blocks

---

## Future Enhancements

Potential workflow additions for consideration:

1. **Notebook Execution Testing**
   - Run notebooks in clean environment
   - Verify they execute without errors
   - Requires API key handling strategy

2. **Screenshot Validation**
   - Check for embedded images in notebooks
   - Verify image file paths are valid

3. **Learning Path Validation**
   - Verify prerequisite notebooks exist
   - Check tier progression makes sense

4. **Accessibility Checking**
   - Alt text for images
   - Color contrast in visualizations

5. **Performance Monitoring**
   - Track notebook execution time
   - Warn on computationally intensive cells

---

## Related Documentation

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [nbformat Documentation](https://nbformat.readthedocs.io/)
- [markdownlint Rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- [Jupyter Best Practices](https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Working%20With%20Markdown%20Cells.html)

---

**Last Updated**: October 23, 2025  
**Workflow Version**: 1.0.0  
**Repository**: [KR-Labs/krl-tutorials](https://github.com/KR-Labs/krl-tutorials)
