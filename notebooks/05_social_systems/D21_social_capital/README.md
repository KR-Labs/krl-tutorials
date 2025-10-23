# D21: Social Capital

**Domain Category:** Minor Socioeconomic Domain  
**Tier:** 4, 5  
**Geographic Levels:** State, County

---

## Overview

Civic participation, volunteerism, and social network strength using Census ACS and MIT Civic Data. Includes graph neural networks for social network analysis.

## Key Indicators

- **Gini Index** (B19083_001E) - Income inequality as social capital proxy
- **Civic Engagement Index** - Composite civic participation measure

## Data Sources

1. **Census ACS** - https://api.census.gov/data/2023/acs/acs5
2. **MIT Civic Data** - https://civic.mit.edu/api

## Recommended Models

1. **Network Analysis** (networkx) - Social network structure
2. **Factor Analysis** - Latent social capital dimensions
3. **Bayesian Regression** (PyMC) - Hierarchical modeling
4. **GNN (Graph Neural Networks)** (torch-geometric) - Deep learning on graphs

## Visualizations

- Network: Social capital network
- Choropleth: Civic engagement by county
- Scatter: Inequality vs. civic engagement

## Example Use Cases

- Social cohesion measurement
- Community resilience assessment
- Network analysis of social connections
- Policy impact on social capital

---

**Status:** Production Ready  
**Notebook:** `D21_D21_social_capital.ipynb`  
**Last Updated:** October 15, 2025

---

## Trademark Notice

**KR-Labs™** is a trademark of Quipu Research Labs, LLC, a subsidiary of Sudiata Giddasira, Inc.

---

© 2025 KR-Labs. All rights reserved.
