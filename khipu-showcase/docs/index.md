# Khipu Showcase

Welcome to the **Khipu Socioeconomic Analysis Suite** public showcase!

This repository contains interactive Jupyter notebooks demonstrating the capabilities of the Khipu platform for analyzing housing affordability, environmental justice, labor markets, and public health outcomes.

## 🚀 Quick Links

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Getting Started**

    ---

    Install the package and run your first notebook in 5 minutes.

    [:octicons-arrow-right-24: Installation Guide](getting-started/installation.md)

-   :material-book-open-variant:{ .lg .middle } **Tutorials**

    ---

    Step-by-step guides for common analysis workflows.

    [:octicons-arrow-right-24: View Tutorials](tutorials/index.md)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Detailed documentation for the `khipu_demo` package.

    [:octicons-arrow-right-24: API Docs](api/data.md)

-   :material-github:{ .lg .middle } **Source Code**

    ---

    View and contribute to the project on GitHub.

    [:octicons-arrow-right-24: GitHub Repository](https://github.com/KR-Labs/khipu-showcase)

</div>

## 📊 Featured Notebooks

| Notebook | Description | Topics |
|----------|-------------|--------|
| [Housing-Wage Divergence](notebooks/01-metro-housing-wage-divergence.ipynb) | Analyze the growing gap between home values and wages | Housing, Labor, Affordability |
| Gentrification Early Warning | Tract-level displacement risk modeling | Urban, Equity, Prediction |
| Environmental Justice Mapping | EPA EJScreen environmental burden analysis | Environment, Health, Equity |

## 🔒 Security First

All notebooks in this showcase:

- ✅ Use **synthetic data** that mirrors real API schemas
- ✅ Contain **no API keys, secrets, or credentials**
- ✅ Run in **DEMO_MODE** by default
- ✅ Include **full data provenance** documentation

## 🌐 Launch Options

### Binder (Zero Installation)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/KR-Labs/khipu-showcase/main)

### Local Installation

```bash
pip install khipu-demo
jupyter lab
```

### Docker

```bash
docker-compose -f docker/docker-compose.yml up jupyter
```

## 📝 License

- **Code**: Apache 2.0
- **Documentation & Notebooks**: CC-BY-4.0
- **Data**: Synthetic (no restrictions)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](contributing/guidelines.md) for details.

---

*Built with ❤️ by [KR-Labs](https://github.com/KR-Labs)*
