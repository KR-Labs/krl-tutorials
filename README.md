---
© 2025 KR-Labs. All rights reserved.  
KR-Labs™ is a trademark of Quipu Research Labs, LLC, a subsidiary of Sudiata Giddasira, Inc.

SPDX-License-Identifier: CC-BY-4.0
---

# KRL Tutorials

Comprehensive tutorials and learning resources for the KRL Analytics Suite, featuring interactive Jupyter notebooks, video guides, and hands-on examples.

## Overview

This repository provides educational content for learning the KRL Analytics Suite, from beginner-friendly introductions to advanced analytical techniques. All tutorials are provided as interactive Jupyter notebooks with detailed explanations, code examples, and exercises.

## Learning Paths

### 🌱 Beginner Path (Getting Started)
1. **Introduction to KRL** - Overview of the analytics suite and core concepts
2. **Setting Up Your Environment** - Installation and configuration
3. **Your First Data Analysis** - Basic data loading and visualization
4. **Working with Economic Data** - FRED and Census API basics

### 📊 Intermediate Path (Data Analysis)
1. **Advanced Data Connectors** - Multi-source data integration
2. **Time Series Analysis** - ARIMA, seasonal decomposition, forecasting
3. **Data Visualization** - Creating publication-quality charts
4. **Working with Geographic Data** - Geospatial analysis and mapping

### 🎓 Advanced Path (Causal Inference)
1. **Difference-in-Differences** - Policy evaluation with DiD
2. **Synthetic Control Methods** - Creating counterfactual scenarios
3. **Regression Discontinuity Design** - Exploiting policy thresholds
4. **Propensity Score Matching** - Controlling for confounders

### 🚀 Expert Path (Production Systems)
1. **Building Dashboards** - Interactive analytics with Streamlit
2. **Model Deployment** - Deploying models to production
3. **API Development** - Building data APIs
4. **Performance Optimization** - Caching, parallelization, and scaling

## Tutorial Index

### Getting Started (tutorials/01_getting_started/)
- `01_introduction.ipynb` - Welcome to KRL Analytics Suite
- `02_installation.ipynb` - Setup and configuration guide
- `03_first_analysis.ipynb` - Your first economic analysis
- `04_understanding_data_sources.ipynb` - Data connectors overview

### Data Collection (tutorials/02_data_collection/)
- `01_fred_connector.ipynb` - Federal Reserve Economic Data API
- `02_census_connector.ipynb` - U.S. Census Bureau data
- `03_bls_connector.ipynb` - Bureau of Labor Statistics
- `04_world_bank_connector.ipynb` - World Bank Development Indicators
- `05_oecd_connector.ipynb` - OECD data
- `06_multi_source_integration.ipynb` - Combining multiple data sources

### Data Exploration (tutorials/03_data_exploration/)
- `01_exploratory_data_analysis.ipynb` - EDA techniques
- `02_time_series_visualization.ipynb` - Visualizing temporal data
- `03_geographic_visualization.ipynb` - Maps and spatial analysis
- `04_interactive_charts.ipynb` - Plotly and interactive visualizations

### Statistical Models (tutorials/04_statistical_models/)
- `01_arima_forecasting.ipynb` - Time series forecasting
- `02_var_models.ipynb` - Vector autoregression
- `03_granger_causality.ipynb` - Testing causal relationships
- `04_seasonal_decomposition.ipynb` - Seasonal analysis

### Causal Inference (tutorials/05_causal_inference/)
- `01_difference_in_differences.ipynb` - DiD methodology
- `02_synthetic_control.ipynb` - Synthetic control methods
- `03_regression_discontinuity.ipynb` - RDD design
- `04_propensity_score_matching.ipynb` - PSM techniques
- `05_instrumental_variables.ipynb` - IV estimation

### Machine Learning (tutorials/06_machine_learning/)
- `01_supervised_learning.ipynb` - Regression and classification
- `02_unsupervised_learning.ipynb` - Clustering and dimensionality reduction
- `03_feature_engineering.ipynb` - Creating predictive features
- `04_model_evaluation.ipynb` - Cross-validation and metrics

### Network Analysis (tutorials/07_network_analysis/)
- `01_economic_networks.ipynb` - Network fundamentals
- `02_supply_chain_analysis.ipynb` - Supply chain networks
- `03_regional_networks.ipynb` - Regional economic linkages
- `04_centrality_measures.ipynb` - Network metrics

### Geospatial Analysis (tutorials/08_geospatial/)
- `01_geographic_data.ipynb` - Working with shapefiles and GeoJSON
- `02_spatial_econometrics.ipynb` - Spatial regression models
- `03_interactive_maps.ipynb` - Folium and mapping
- `04_spatial_clustering.ipynb` - Geographic clustering

### Dashboard Development (tutorials/09_dashboards/)
- `01_streamlit_basics.ipynb` - Building your first dashboard
- `02_interactive_components.ipynb` - Widgets and forms
- `03_data_integration.ipynb` - Connecting data sources
- `04_deployment.ipynb` - Deploying to production

### Production Systems (tutorials/10_production/)
- `01_api_development.ipynb` - Building REST APIs
- `02_caching_strategies.ipynb` - Performance optimization
- `03_docker_deployment.ipynb` - Containerization
- `04_ci_cd_pipelines.ipynb` - Automated testing and deployment

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/KR-Labs/krl-tutorials.git
cd krl-tutorials

# Install dependencies
pip install -r requirements.txt

# Install Jupyter
pip install jupyter jupyterlab
```

### Running Tutorials

```bash
# Launch Jupyter Lab
jupyter lab

# Or Jupyter Notebook
jupyter notebook

# Navigate to tutorials/ directory and open any .ipynb file
```

### Running Individual Tutorials

```bash
# Run a specific tutorial
jupyter nbconvert --to notebook --execute tutorials/01_getting_started/01_introduction.ipynb
```

## Tutorial Structure

Each tutorial follows a consistent structure:

1. **Learning Objectives** - What you'll learn
2. **Prerequisites** - Required knowledge and setup
3. **Theory** - Conceptual background
4. **Code Examples** - Hands-on implementation
5. **Exercises** - Practice problems with solutions
6. **Further Reading** - Additional resources

## Prerequisites

### Python Knowledge
- Basic Python programming (variables, functions, loops)
- Familiarity with pandas and numpy
- Understanding of Jupyter notebooks

### Statistical Knowledge
- Descriptive statistics (mean, median, standard deviation)
- Basic probability concepts
- Hypothesis testing (for advanced tutorials)

### Economic Knowledge (Helpful but not required)
- Basic microeconomics and macroeconomics concepts
- Understanding of economic indicators (GDP, unemployment, inflation)

## Data Requirements

Many tutorials require API keys for data sources:

```bash
# Set environment variables
export FRED_API_KEY=your_fred_api_key
export CENSUS_API_KEY=your_census_api_key
export BLS_API_KEY=your_bls_api_key
export WORLD_BANK_API_KEY=your_world_bank_api_key
```

Get free API keys:
- **FRED**: https://fred.stlouisfed.org/docs/api/api_key.html
- **Census**: https://api.census.gov/data/key_signup.html
- **BLS**: https://www.bls.gov/developers/home.htm
- **World Bank**: No API key required

## Video Tutorials

Video walkthroughs are available for select tutorials:

- **Getting Started Series** (30 min) - YouTube playlist
- **Causal Inference Masterclass** (2 hours) - In-depth DiD and Synthetic Control
- **Dashboard Development** (45 min) - Building production dashboards
- **Weekly Office Hours** - Live Q&A sessions

See [VIDEO_INDEX.md](VIDEO_INDEX.md) for the complete list.

## Contributing

We welcome contributions! Ways to contribute:

1. **Report Issues** - Found a bug or typo? Open an issue
2. **Suggest Tutorials** - Request topics you'd like to learn
3. **Submit Tutorials** - Share your own tutorials
4. **Improve Examples** - Enhance existing code examples
5. **Add Exercises** - Create practice problems

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Tutorial Dataset Repository

Sample datasets are provided in the `datasets/` directory:

- `economic_indicators/` - Sample FRED data
- `census_demographics/` - Sample Census data
- `policy_evaluation/` - Synthetic datasets for causal inference
- `geographic/` - Shapefiles and GeoJSON

All datasets are provided under open licenses with proper attribution.

## FAQ

### Q: Do I need to complete tutorials in order?
A: We recommend following the learning paths, but each tutorial is self-contained.

### Q: Can I use tutorials for teaching?
A: Yes! Tutorials are CC-BY 4.0 licensed. Please provide attribution.

### Q: Are solutions provided for exercises?
A: Yes, solutions are in the `solutions/` subdirectory of each tutorial.

### Q: How often are tutorials updated?
A: We update tutorials quarterly to reflect new features and best practices.

## Support

- **Documentation**: https://docs.krlanalytics.org
- **Issues**: https://github.com/KR-Labs/krl-tutorials/issues
- **Discussions**: https://github.com/orgs/KR-Labs/discussions
- **Email**: tutorials@krlabs.org

## License

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

You are free to share and adapt the material with proper attribution.

## Related Projects

- [krl-open-core](https://github.com/KR-Labs/krl-open-core) - Core utilities
- [krl-data-connectors](https://github.com/KR-Labs/krl-data-connectors) - Data connectors
- [krl-model-zoo](https://github.com/KR-Labs/krl-model-zoo) - Statistical models
- [krl-dashboard](https://github.com/KR-Labs/krl-dashboard) - Interactive dashboards

## Acknowledgments

These tutorials were developed with contributions from:
- Academic researchers
- Industry practitioners
- Open-source community members
- Student interns and fellows

Special thanks to all contributors who have improved these learning resources.
