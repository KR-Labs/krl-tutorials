# D32: Freedom & Civil Liberties

**Domain Category:** Minor Socioeconomic Domain  
**Tier:** 2, 3, 6  
**Geographic Levels:** State

---

## Overview

This domain analyzes state-level civil liberties, political rights, and regulatory freedom using Freedom House methodology, OECD regulatory indicators, and Heritage Foundation indices.

## Key Indicators

- **Civil Liberties Score** - Aggregate civil liberties index (0-100)
- **Political Rights Score** - Democratic freedoms index (0-100)
- **Regulatory Burden** - Ease of doing business proxy

## Data Sources

### Primary Sources
1. **Freedom House U.S. States Proxy**
   - URL: https://freedomhouse.org/data
   - Geographic Level: State (modeled from national framework)
   - Update Frequency: Annual

2. **OECD Regulatory Indicators**
   - URL: https://stats.oecd.org
   - Geographic Level: State (proxy from regulatory databases)
   - Update Frequency: Biennial

3. **Heritage Foundation Economic Freedom Index**
   - URL: https://www.heritage.org/index/
   - Geographic Level: National (state proxy via state policies)
   - Update Frequency: Annual

### Modeling Notes
- State-level civil liberties synthesized from voting laws, protest frequency, legal frameworks
- Political rights include ballot access, campaign finance, legislative transparency
- Regulatory burden from small business regulations, occupational licensing, zoning

## Analysis Tiers

### Tier 2: Predictive Analytics
- Classify high/low freedom states
- Feature importance for civil liberties determinants
- Random Forest risk assessment

### Tier 3: Time Series Analytics
- Trend analysis of civil liberties over time
- Forecasting freedom indices
- Structural break detection

### Tier 6: Advanced Analytics
- Bayesian hierarchical models for state-level effects
- Causal inference for policy impacts on freedom
- Spatial regression for regional spillovers

## Recommended Models

1. **OLS Regression** (statsmodels)
   - Use case: Freedom determinants & policy effects

2. **Random Forest** (scikit-learn)
   - Use case: Classification of high/low freedom states

3. **Bayesian Hierarchical Model** (PyMC)
   - Use case: Multi-level effects & uncertainty quantification

## Visualizations

- **Choropleth Map:** Civil liberties by state
- **Scatter Plot:** Political rights vs. regulatory burden
- **Line Chart:** Civil liberties trends over time
- **Heatmap:** Freedom correlations with economic indicators

## Example Use Cases

1. **Policy Environment Assessment:** Evaluate state business climate through freedom indices
2. **Governance Comparison:** Benchmark state civil liberties against national averages
3. **Regulatory Impact Analysis:** Measure effect of new regulations on freedom scores
4. **Trend Monitoring:** Track civil liberties changes after policy reforms

## Getting Started

```python
from qrl_core.models import PredictiveModel
from qrl_core.utils.plotly_visualization_engine import PlotlyVisualizationEngine
import pandas as pd

# Load freedom data (example)
freedom_data = pd.read_csv('path/to/freedom_indices.csv')

# Predict civil liberties
model = PredictiveModel(type="regression")
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Visualize
viz_engine = PlotlyVisualizationEngine()
charts = viz_engine.generate_tier_visualizations(
    data=freedom_data,
    tier_type="tier_2",
    analysis_focus="freedom_civil"
)
```

## References

- Freedom House. (2024). *Freedom in the World 2024*.
- OECD. (2023). *Regulatory Policy Outlook*.
- Miller, T., Kim, A. B., & Roberts, J. M. (2024). *Index of Economic Freedom*.

---

**Status:** Production Ready  
**Last Updated:** October 15, 2025  
**Maintainer:** KR-Labs Analytics Team

---

## Trademark Notice

**KR-Labs™** is a trademark of Quipu Research Labs, LLC, a subsidiary of Sudiata Giddasira, Inc.

---

© 2025 KR-Labs. All rights reserved.
