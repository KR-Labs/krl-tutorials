
© 2025 KR-Labs. All rights reserved.  
KR-Labs™ is a trademark of Quipu Research Labs, LLC, a subsidiary of Sundiata Giddasira, Inc.

SPDX-License-Identifier: MIT AND CC-BY-SA-4.0

# KRL Tutorials

A structured, comprehensive guide to mastering the KRL Analytics Suite. These tutorials combine interactive Jupyter notebooks, step-by-step instructions, and practical exercises designed for both individual analysts and institutional teams.

---

## Table of Contents

1. [Overview](#overview)  
2. [Learning Paths](#learning-paths)  
   - Beginner Path  
   - Intermediate Path  
   - Advanced Path  
   - Expert Path  
3. [Tutorial Index](#tutorial-index)  
4. [Quick Start](#quick-start)  
   - Installation  
   - Running Tutorials  
   - Running Individual Tutorials  
5. [Tutorial Structure](#tutorial-structure)  
6. [Prerequisites](#prerequisites)  
7. [Data Requirements](#data-requirements)  
8. [Video Tutorials](#video-tutorials)  
9. [Contributing](#contributing)  
10. [Tutorial Dataset Repository](#tutorial-dataset-repository)  
11. [FAQ](#faq)  
12. [Support](#support)  
13. [License](#license)  
14. [Related Projects](#related-projects)  
15. [Acknowledgments](#acknowledgments)

---

## Overview

KRL Tutorials provide a hands-on, guided learning experience for the KRL Analytics Suite. Whether you are beginning your journey in data analytics or advancing toward production-grade systems, this repository offers a clear, structured roadmap.

All tutorials are delivered as interactive Jupyter notebooks with embedded explanations, code examples, and exercises for practical application.

---

## Learning Paths

### Beginner Path: Getting Started
1. **Introduction to KRL** – Explore the analytics suite and core concepts.  
2. **Setting Up Your Environment** – Installation and configuration guidance.  
3. **Your First Data Analysis** – Load and visualize data.  
4. **Working with Economic Data** – Access FRED and Census APIs.  

### Intermediate Path: Data Analysis
1. **Advanced Data Connectors** – Combine data from multiple sources.  
2. **Time Series Analysis** – Learn ARIMA, seasonal decomposition, and forecasting.  
3. **Data Visualization** – Create professional-grade charts and figures.  
4. **Working with Geographic Data** – Geospatial analysis and mapping techniques.  

### Advanced Path: Causal Inference
1. **Difference-in-Differences** – Evaluate policy impacts using DiD.  
2. **Synthetic Control Methods** – Build counterfactual scenarios.  
3. **Regression Discontinuity Design** – Leverage policy thresholds.  
4. **Propensity Score Matching** – Control for confounders in observational studies.  

### Expert Path: Production Systems
1. **Building Dashboards** – Develop interactive visualizations with Streamlit.  
2. **Model Deployment** – Move models from notebooks to production.  
3. **API Development** – Construct robust data APIs.  
4. **Performance Optimization** – Implement caching, parallelization, and scaling.

---

## Tutorial Index

### Getting Started
- `01_introduction.ipynb` – Welcome to KRL Analytics Suite  
- `02_installation.ipynb` – Setup and configuration guide  
- `03_first_analysis.ipynb` – First economic analysis  
- `04_understanding_data_sources.ipynb` – Overview of data connectors  

### Data Collection
- `01_fred_connector.ipynb` – Federal Reserve Economic Data API  
- `02_census_connector.ipynb` – U.S. Census Bureau API  
- `03_bls_connector.ipynb` – Bureau of Labor Statistics  
- `04_world_bank_connector.ipynb` – World Bank Development Indicators  
- `05_oecd_connector.ipynb` – OECD data sources  
- `06_multi_source_integration.ipynb` – Multi-source integration  

### Data Exploration
- `01_exploratory_data_analysis.ipynb` – Exploratory Data Analysis techniques  
- `02_time_series_visualization.ipynb` – Visualizing temporal data  
- `03_geographic_visualization.ipynb` – Maps and spatial analytics  
- `04_interactive_charts.ipynb` – Interactive visualizations using Plotly  

### Statistical Models
- `01_arima_forecasting.ipynb` – Time series forecasting  
- `02_var_models.ipynb` – Vector autoregression models  
- `03_granger_causality.ipynb` – Testing causal relationships  
- `04_seasonal_decomposition.ipynb` – Seasonal analysis  

### Causal Inference
- `01_difference_in_differences.ipynb` – DiD methodology  
- `02_synthetic_control.ipynb` – Synthetic control analysis  
- `03_regression_discontinuity.ipynb` – Regression discontinuity design  
- `04_propensity_score_matching.ipynb` – Propensity score methods  
- `05_instrumental_variables.ipynb` – Instrumental variable estimation  

### Machine Learning
- `01_supervised_learning.ipynb` – Regression and classification  
- `02_unsupervised_learning.ipynb` – Clustering and dimensionality reduction  
- `03_feature_engineering.ipynb` – Construct predictive features  
- `04_model_evaluation.ipynb` – Cross-validation and performance metrics  

### Network Analysis
- `01_economic_networks.ipynb` – Network fundamentals  
- `02_supply_chain_analysis.ipynb` – Supply chain networks  
- `03_regional_networks.ipynb` – Regional economic linkages  
- `04_centrality_measures.ipynb` – Network metrics and centrality  

### Geospatial Analysis
- `01_geographic_data.ipynb` – Shapefiles and GeoJSON data  
- `02_spatial_econometrics.ipynb` – Spatial regression models  
- `03_interactive_maps.ipynb` – Folium maps and visualization  
- `04_spatial_clustering.ipynb` – Geographic clustering techniques  

### Dashboard Development
- `01_streamlit_basics.ipynb` – First dashboard creation  
- `02_interactive_components.ipynb` – Widgets and form controls  
- `03_data_integration.ipynb` – Integrate multiple data sources  
- `04_deployment.ipynb` – Deploy dashboards to production  

### Production Systems
- `01_api_development.ipynb` – Build RESTful APIs  
- `02_caching_strategies.ipynb` – Performance optimization techniques  
- `03_docker_deployment.ipynb` – Containerization for deployment  
- `04_ci_cd_pipelines.ipynb` – Automated testing and deployment pipelines  

---

## Quick Start

### Installation

```bash
git clone https://github.com/KR-Labs/krl-tutorials.git
cd krl-tutorials

pip install -r requirements.txt
pip install jupyter jupyterlab
```

### Running Tutorials

```bash
jupyter lab
# or
jupyter notebook
```

Navigate to the `tutorials/` directory and open any `.ipynb` file.

### Running Individual Tutorials

```bash
jupyter nbconvert --to notebook --execute tutorials/01_getting_started/01_introduction.ipynb
```

---

## Tutorial Structure

Each tutorial is organized consistently for a seamless learning experience:

1. **Learning Objectives** – Core concepts and skills covered  
2. **Prerequisites** – Knowledge and setup requirements  
3. **Theory** – Conceptual background and context  
4. **Code Examples** – Step-by-step implementation  
5. **Exercises** – Practice problems with solutions  
6. **Further Reading** – References for deeper exploration  

---

## Prerequisites

### Python
- Basics: variables, functions, loops  
- Libraries: pandas, numpy  
- Jupyter notebook familiarity  

### Statistics
- Descriptive statistics: mean, median, standard deviation  
- Probability fundamentals  
- Hypothesis testing (advanced tutorials)  

### Economics (optional)
- Basic micro/macro concepts  
- Understanding of economic indicators: GDP, unemployment, inflation  

---

## Data Requirements

Many tutorials require API keys:

```bash
export FRED_API_KEY=your_fred_api_key
export CENSUS_API_KEY=your_census_api_key
export BLS_API_KEY=your_bls_api_key
export WORLD_BANK_API_KEY=your_world_bank_api_key
```

- FRED: https://fred.stlouisfed.org/docs/api/api_key.html  
- Census: https://api.census.gov/data/key_signup.html  
- BLS: https://www.bls.gov/developers/home.htm  
- World Bank: No API key required  

---

## Video Tutorials

- **Getting Started Series** – 30-minute walkthroughs  
- **Causal Inference Masterclass** – 2-hour deep dive  
- **Dashboard Development** – 45-minute production dashboard guide  
- **Weekly Office Hours** – Live Q&A sessions  

See [VIDEO_INDEX.md](VIDEO_INDEX.md) for the full list.

---

## Contributing

Contributions are welcome:

1. Report bugs or typos  
2. Suggest new tutorial topics  
3. Submit your own tutorials  
4. Improve existing examples  
5. Add exercises  

Refer to [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Tutorial Dataset Repository

Sample datasets are available in `datasets/`:

- `economic_indicators/` – FRED sample data  
- `census_demographics/` – Census sample data  
- `policy_evaluation/` – Synthetic causal datasets  
- `geographic/` – Shapefiles and GeoJSON  

All datasets include open licensing with proper attribution.

---

## FAQ

**Do I need to complete tutorials sequentially?**  
No. Each tutorial is self-contained, though following the learning paths is recommended.  

**Can tutorials be used for teaching?**  
Yes. All tutorials are CC-BY 4.0 licensed; attribution required.  

**Are exercise solutions provided?**  
Yes. Solutions are located in the `solutions/` subdirectories.

**How often are tutorials updated?**  
Quarterly, to reflect new features and best practices.

---

## Support

- Documentation: https://krlabs.dev  
- Issues: https://github.com/KR-Labs/krl-tutorials/issues  
- Discussions: https://github.com/orgs/KR-Labs/discussions  
- Email: info@krlabs.dev  

---

## License

This repository uses **dual licensing** to provide maximum flexibility:

### 📝 For Code (MIT License)
All Python code, scripts, and code examples are licensed under the [MIT License](LICENSE-CODE).

**You can:**
- ✓ Use in commercial projects
- ✓ Modify and distribute
- ✓ Include in proprietary software
- ✓ No need to open source your project

**You must:**
- Include copyright notice and license

### 📚 For Content (CC-BY-SA-4.0)
All documentation, tutorials, and educational materials are licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](LICENSE-CONTENT).

**You can:**
- ✓ Share and redistribute
- ✓ Adapt for your courses/training
- ✓ Use commercially

**You must:**
- Provide attribution to KR-Labs
- Indicate if changes were made
- Share derivative works under CC-BY-SA-4.0

### Quick Guide

**Copying code into your project?** → Use MIT License terms ([LICENSE-CODE](LICENSE-CODE))  
**Using tutorials in your course?** → Use CC-BY-SA-4.0 terms ([LICENSE-CONTENT](LICENSE-CONTENT))  
**Using both?** → Follow both licenses for respective parts

See [LICENSE](LICENSE) for complete details.

---

## Related Projects

- [krl-open-core](https://github.com/KR-Labs/krl-open-core) – Core utilities  
- [krl-data-connectors](https://github.com/KR-Labs/krl-data-connectors) – API connectors  
- [krl-model-zoo](https://github.com/KR-Labs/krl-model-zoo) – Statistical modeling  
- [krl-dashboard](https://github.com/KR-Labs/krl-dashboard) – Interactive dashboards  

---

## Acknowledgments

Development and curation by academic researchers, industry practitioners, open-source contributors, and interns. Special thanks to all who have improved the tutorials and examples.
