<div align="center">
  <img src="../../../assets/images/KRLabs_WebLogo.png" alt="KR-Labs" width="200">
</div>

# D31: Civic Trust & Engagement

**Domain Category:** Minor Socioeconomic Domain  
**Tier:** 1, 2, 4  
**Geographic Levels:** State, County

---

## Overview

This domain measures civic trust, social cohesion, volunteerism, and local engagement using OECD frameworks, U.S. social capital research, and MIT civic data.

## Key Indicators

- **Trust Index** - Survey-based civic trust measure
- **Volunteer Rate** - Percentage of adults engaged in volunteer activities
- **Civic Participation Index** - Composite measure of local engagement

## Data Sources

### Primary Sources
1. **Social Capital Project (U.S.)**
   - URL: https://www.usc.edu/socialcapital/data
   - Geographic Level: State, County
   - Update Frequency: Biennial

2. **MIT Civic Data**
   - URL: https://civic.mit.edu/api
   - Geographic Level: State, County
   - Update Frequency: Annual

3. **OECD Trust in Government Surveys**
   - URL: https://stats.oecd.org
   - Geographic Level: National (benchmarking)
   - Update Frequency: Annual

### Modeling Notes
- State-level trust estimates from national surveys using MRP
- Volunteer rates from CPS Volunteer Supplement (September)
- Civic participation composite from voting, nonprofit engagement, community involvement

## Analysis Tiers

### Tier 1: Descriptive Analytics
- Trust index distributions
- Volunteer rate by demographics
- Regional civic engagement patterns

### Tier 2: Predictive Analytics
- Trust prediction from socioeconomic factors
- Bayesian hierarchical models for state-county effects
- Volunteer activity forecasting

### Tier 4: Unsupervised Learning
- Network analysis of civic connections
- Factor analysis for latent trust dimensions
- Clustering of high/low engagement regions

## Recommended Models

1. **Network Analysis** (networkx)
   - Use case: Social network structure & civic connections

2. **Factor Analysis** (sklearn)
   - Use case: Construct composite trust indices

3. **Bayesian Regression** (PyMC)
   - Use case: Hierarchical modeling of civic trust

## Visualizations

- **Choropleth Map:** Civic trust by county
- **Network Graph:** Civic engagement network
- **Scatter Plot:** Volunteer rate vs. civic participation
- **Bar Chart:** Trust levels by demographic group

## Example Use Cases

1. **Social Cohesion Assessment:** Measure community resilience through trust metrics
2. **Volunteer Program Evaluation:** Impact of volunteer initiatives on civic engagement
3. **Trust Trends:** Tracking changes in government trust over time
4. **Network Analysis:** Identify key nodes in civic engagement networks

## Getting Started

```python
from qrl_core.utils.plotly_visualization_engine import PlotlyVisualizationEngine
import pandas as pd
import networkx as nx

# Load civic data (example)
civic_data = pd.read_csv('path/to/civic_trust_data.csv')

# Build trust network
G = nx.from_pandas_edgelist(civic_data, 'source', 'target', 'strength')
centrality = nx.betweenness_centrality(G)

# Visualize
viz_engine = PlotlyVisualizationEngine()
charts = viz_engine.generate_tier_visualizations(
    data=civic_data,
    tier_type="tier_1",
    analysis_focus="civic_trust"
)
```

## References

- OECD. (2024). *Trust in Government Surveys*.
- Putnam, R. D. (2000). *Bowling Alone: The Collapse and Revival of American Community*.
- MIT Media Lab. (2024). *Civic Data Portal*.

---

**Status:** Production Ready  
**Last Updated:** October 15, 2025  
**Maintainer:** KR-Labs Analytics Team

---

## Trademark Notice

**KR-Labs™** is a trademark of Quipu Research Labs, LLC, a subsidiary of Sudiata Giddasira, Inc.

---

© 2025 KR-Labs. All rights reserved.
