<!--
© 2025 KR-Labs. All rights reserved.  
KR-Labs™ is a trademark of Quipu Research Labs, LLC, a subsidiary of Sudiata Giddasira, Inc.

SPDX-License-Identifier: Apache-2.0
-->

<div align="center">
  <h1>🏛️ Khipu Socioeconomic Analysis Suite</h1>
  <h3>Public Tutorial Showcases</h3>
  
  <p>
    <a href="https://mybinder.org/v2/gh/KR-Labs/khipu-showcase/main?urlpath=lab">
      <img src="https://mybinder.org/badge_logo.svg" alt="Launch Binder">
    </a>
    <a href="https://github.com/KR-Labs/khipu-showcase/actions/workflows/ci.yml">
      <img src="https://github.com/KR-Labs/khipu-showcase/actions/workflows/ci.yml/badge.svg" alt="CI Status">
    </a>
    <a href="https://opensource.org/licenses/Apache-2.0">
      <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License">
    </a>
    <a href="https://github.com/KR-Labs/khipu-showcase/actions/workflows/secrets-scan.yml">
      <img src="https://img.shields.io/badge/secrets-scanned-green.svg" alt="Secrets Scanned">
    </a>
  </p>
  
  <p><strong>Interactive, reproducible socioeconomic analysis notebooks for journalists, policymakers, investors, and researchers.</strong></p>
</div>

---

## 🎯 What This Is

This repository contains **production-quality Jupyter notebooks** demonstrating the Khipu Socioeconomic Analysis Suite's capabilities. Each notebook answers a specific intelligence question using publicly available data and reproducible methods.

### Key Features

- **23 Canonical Notebooks** covering housing, labor markets, equity, climate, causal inference, and policy analysis
- **Fully Reproducible** — Run in Binder, Docker, or locally with one command
- **Public Data Only** — Uses Census, BLS, BEA, EPA, CDC, and synthetic data
- **No Secrets Exposed** — All API calls mocked; no credentials in code or outputs
- **Accessible** — ARIA-compatible, high-contrast visualizations, keyboard controls
- **Production-Quality** — CI-tested, linted, output-stable

---

## 🚀 Quick Start

### Option 1: Launch in Binder (Recommended)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KR-Labs/khipu-showcase/main?urlpath=lab)

Click the badge above to launch a live, interactive environment. No installation required.

### Option 2: Run Locally

```bash
# Clone the repository
git clone https://github.com/KR-Labs/khipu-showcase.git
cd khipu-showcase

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Set demo mode
export DEMO_MODE=true

# Launch Jupyter Lab
jupyter lab notebooks/
```

### Option 3: Docker

```bash
docker build -t khipu-showcase .
docker run -p 8888:8888 khipu-showcase
```

---

## 📚 Notebook Catalog

### Foundation Series (01-10)

Core socioeconomic analysis techniques and domain applications.

| # | Notebook | Intelligence Question | Tags |
|---|----------|----------------------|------|
| 01 | [Metro Housing vs Wages](notebooks/01-metro-housing-wage-divergence.ipynb) | Where are housing costs diverging from wage growth? | `Housing`, `Labor`, `Investor` |
| 02 | [Gentrification Early Warning](notebooks/02-gentrification-early-warning.ipynb) | Which neighborhoods show early gentrification indicators? | `Housing`, `Equity`, `Policymaker` |
| 03 | [Economic Mobility Deserts](notebooks/03-economic-mobility-deserts.ipynb) | Where are upward mobility opportunities limited? | `Equity`, `Policymaker`, `Nonprofit` |
| 04 | [Environmental Justice & Health](notebooks/04-environmental-justice-health.ipynb) | Where do health and environmental burdens overlap? | `Health`, `Equity`, `Policymaker` |
| 05 | [Climate Resilience Economics](notebooks/05-climate-resilience-economics.ipynb) | How do climate risks affect economic outcomes? | `Climate`, `Risk`, `Investor` |
| 06 | [Small Business Ecosystem](notebooks/06-small-business-ecosystem.ipynb) | Which ZIPs show unusual business formation patterns? | `Business`, `Investor`, `Journalist` |
| 07 | [Labor Market Intelligence](notebooks/07-labor-market-intelligence.ipynb) | Where do job requirements exceed local workforce skills? | `Labor`, `Education`, `Corporate` |
| 10 | [Urban Resilience Dashboard](notebooks/10-urban-resilience-dashboard.ipynb) | How resilient are urban areas to economic shocks? | `Urban`, `Risk`, `Policymaker` |

### Advanced Causal Methods (11-17)

Rigorous causal inference and policy evaluation techniques.

| # | Notebook | Intelligence Question | Tags |
|---|----------|----------------------|------|
| 11 | [Heterogeneous Treatment Effects](notebooks/11-heterogeneous-treatment-effects.ipynb) | How do policy effects vary across populations? | `Causal`, `Policy`, `Research` |
| 12 | [Spatial Policy Targeting](notebooks/12-spatial-policy-targeting.ipynb) | Where should interventions be geographically focused? | `Spatial`, `Policy`, `Policymaker` |
| 13 | [Regional Development Zones](notebooks/13-regional-development-zones.ipynb) | How effective are regional development programs? | `Regional`, `Development`, `Investor` |
| 14 | [Synthetic Control Policy Lab](notebooks/14-synthetic-control-policy-lab.ipynb) | What would have happened without the intervention? | `Causal`, `Counterfactual`, `Research` |
| 15 | [Regression Discontinuity Toolkit](notebooks/15-regression-discontinuity-toolkit.ipynb) | Can we identify causal effects at policy thresholds? | `Causal`, `RDD`, `Research` |
| 16 | [End-to-End Policy Pipeline](notebooks/16-end-to-end-policy-pipeline.ipynb) | How to build a complete policy analysis workflow? | `Pipeline`, `Policy`, `Policymaker` |
| 17 | [Spatial-Causal Fusion](notebooks/17-spatial-causal-fusion.ipynb) | How to combine spatial and causal methods? | `Spatial`, `Causal`, `Research` |

### Applied Policy Analysis (18-23)

Real-world policy evaluation and decision support.

| # | Notebook | Intelligence Question | Tags |
|---|----------|----------------------|------|
| 18 | [Multi-Source Data Warehouse](notebooks/18-multi-source-data-warehouse.ipynb) | How to integrate diverse data sources for analysis? | `Data`, `Integration`, `All` |
| 19 | [Advanced Time Series](notebooks/19-advanced-time-series.ipynb) | How to forecast and analyze temporal patterns? | `TimeSeries`, `Forecasting`, `Research` |
| 20 | [Opportunity Zone Evaluation](notebooks/20-opportunity-zone-evaluation.ipynb) | Are Opportunity Zones achieving their goals? | `Policy`, `Investment`, `Policymaker` |
| 21 | [Environmental Justice Scoring](notebooks/21-environmental-justice-scoring.ipynb) | How to quantify environmental justice outcomes? | `EJ`, `Equity`, `Policymaker` |
| 22 | [Workforce Development ROI](notebooks/22-workforce-development-roi.ipynb) | What is the return on workforce training investments? | `Workforce`, `ROI`, `Policy` |
| 23 | [Climate Adaptation Planning](notebooks/23-climate-adaptation-planning.ipynb) | How to prioritize climate adaptation investments? | `Climate`, `Adaptation`, `Policymaker` |

---

## 🔒 Privacy & Security Statement

**This repository contains NO:**
- API keys, credentials, or secrets
- Proprietary algorithms or model weights
- Personally identifiable information (PII)
- Private or confidential data

**All notebooks use:**
- Publicly available government data (Census, BLS, BEA, EPA, CDC)
- Synthetic data with documented generation methods
- Mocked API interfaces that return canned responses

**Security measures:**
- Pre-commit hooks scan for secrets (detect-secrets, git-secrets)
- CI blocks any commit containing potential credentials
- All outputs are reviewed before publication

---

## 📊 Data Sources & Licensing

| Source | License | Usage |
|--------|---------|-------|
| U.S. Census Bureau | Public Domain | Demographics, ACS, CBP |
| Bureau of Labor Statistics | Public Domain | Employment, wages, CPI |
| Bureau of Economic Analysis | Public Domain | GDP, regional accounts |
| Environmental Protection Agency | Public Domain | EJScreen, air quality |
| Centers for Disease Control | Public Domain | Health indicators |
| Synthetic Data | Apache 2.0 | Demo-specific generated data |

All data usage complies with respective agency terms. See [`data/README.md`](data/README.md) for full provenance documentation.

---

## 🏗️ Repository Structure

```
khipu-showcase/
├── notebooks/                 # 12+ canonical tutorial notebooks
│   ├── 01-metro-housing-wage-divergence.ipynb
│   ├── 02-early-gentrification-signals.ipynb
│   └── ...
├── templates/                 # Reusable notebook skeleton
│   └── notebook_template.ipynb
├── src/khipu_demo/           # Lightweight demo Python package
│   ├── __init__.py
│   ├── clients/              # Mock API clients
│   ├── data/                 # Data loaders and generators
│   ├── viz/                  # Visualization utilities
│   └── utils/                # Helpers and validation
├── data/
│   ├── public/               # Cached public datasets
│   ├── synthetic/            # Generated demo data
│   └── README.md             # Data provenance documentation
├── tests/                    # Unit and integration tests
├── docker/                   # Docker configuration
├── binder/                   # Binder configuration
├── .github/workflows/        # CI/CD pipelines
├── docs/                     # Additional documentation
├── DEPLOY.md                 # Deployment instructions
├── DOCUMENTATION.md          # Development guide
└── pyproject.toml           # Package configuration
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=khipu_demo --cov-report=html

# Run notebook integration tests
pytest tests/test_notebooks.py -v

# Check for secrets
pre-commit run detect-secrets --all-files
```

---

## 📖 How to Cite

If you use these notebooks in your work, please cite:

```bibtex
@software{khipu_showcase_2025,
  title = {Khipu Socioeconomic Analysis Suite: Public Tutorial Showcases},
  author = {{KR-Labs}},
  year = {2025},
  url = {https://github.com/KR-Labs/khipu-showcase},
  license = {Apache-2.0}
}
```

---

## 🤝 Contributing

We welcome contributions! Please see [DOCUMENTATION.md](DOCUMENTATION.md) for development patterns and contribution guidelines.

**Before contributing:**
1. Read the security guidelines
2. Ensure no secrets are included
3. Use only public or synthetic data
4. Follow the notebook template structure

---

## 📬 Support

- **Documentation:** [DOCUMENTATION.md](DOCUMENTATION.md)
- **Issues:** [GitHub Issues](https://github.com/KR-Labs/khipu-showcase/issues)
- **Discussions:** [GitHub Discussions](https://github.com/KR-Labs/khipu-showcase/discussions)

---

## 📄 License

Apache License 2.0 — See [LICENSE](LICENSE) for details.

---

**Built by [KR-Labs](https://krlabs.dev) | Open Models. Trusted Intelligence. Shared Progress.**

© 2025 KR-Labs. All rights reserved.
