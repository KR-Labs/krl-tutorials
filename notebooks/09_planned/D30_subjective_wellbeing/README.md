# D30: Subjective Well-Being

**Domain Category:** Minor Socioeconomic Domain  
**Tier:** 1, 2, 4  
**Geographic Levels:** State, County

---

## Overview

This domain analyzes happiness, life satisfaction, and emotional well-being using data from the World Happiness Report methodology, CDC BRFSS surveys, and OECD well-being frameworks.

## Key Indicators

- **Life Satisfaction** - Self-reported life evaluation (0-10 scale)
- **Emotional Health** - Days of poor mental health in past 30 days
- **Happiness Score** - Composite well-being measure

## Data Sources

### Primary Sources
1. **CDC BRFSS Well-Being Module**
   - URL: https://www.cdc.gov/brfss/data_documentation/index.htm
   - Geographic Level: State, County
   - Update Frequency: Annual

2. **World Happiness Report (U.S. Proxy)**
   - URL: https://worldhappiness.report/
   - Geographic Level: State (modeled)
   - Update Frequency: Annual

### Modeling Notes
- U.S. subnational estimates derived using Bayesian MRP on BRFSS microdata
- State-level aggregations from county survey responses
- Small-area estimation for tract-level inference

## Analysis Tiers

### Tier 1: Descriptive Analytics
- Distribution of life satisfaction scores
- Emotional health summary statistics
- Regional well-being comparisons

### Tier 2: Predictive Analytics
- Well-being prediction from socioeconomic factors
- Random Forest classification of high/low satisfaction areas
- Income and health correlates

### Tier 4: Unsupervised Learning
- Factor analysis for latent well-being dimensions
- Clustering of geographic regions by well-being profiles
- Dimension reduction (PCA)

## Recommended Models

1. **OLS Regression** (statsmodels)
   - Use case: Identify well-being determinants

2. **Random Forest** (scikit-learn)
   - Use case: Non-linear well-being prediction

3. **Factor Analysis** (sklearn)
   - Use case: Construct composite well-being indices

## Visualizations

- **Choropleth Map:** Life satisfaction by county
- **Box Plot:** Emotional health distribution
- **Scatter Plot:** Life satisfaction vs. happiness score
- **Heatmap:** Well-being correlations with income, health, education

## Example Use Cases

1. **Policy Evaluation:** Measure impact of mental health programs on life satisfaction
2. **Quality of Life Indices:** Build composite well-being scores for city rankings
3. **Correlation Analysis:** Relationship between income inequality and happiness
4. **Trend Analysis:** Track well-being changes over time by state

## Getting Started

```python
from qrl_core.api.census import CensusAPI
from qrl_core.utils.plotly_visualization_engine import PlotlyVisualizationEngine
import pandas as pd

# Load BRFSS data (example)
# Note: Requires custom data loader for BRFSS
brfss_data = pd.read_csv('path/to/brfss_wellbeing.csv')

# Analyze life satisfaction
viz_engine = PlotlyVisualizationEngine()
charts = viz_engine.generate_tier_visualizations(
    data=brfss_data,
    tier_type="tier_1",
    analysis_focus="subjective_wellbeing"
)

for chart in charts:
    chart.show()
```

## References

- Helliwell, J. F., Layard, R., & Sachs, J. D. (2024). *World Happiness Report 2024*.
- CDC. (2024). *Behavioral Risk Factor Surveillance System*.
- OECD. (2020). *How's Life? 2020: Measuring Well-Being*.

---

**Status:** Production Ready  
**Last Updated:** October 15, 2025  
**Maintainer:** KR-Labs Analytics Team

---

## Trademark Notice

**KR-Labs™** is a trademark of Quipu Research Labs, LLC, a subsidiary of Sudiata Giddasira, Inc.

---

© 2025 KR-Labs. All rights reserved.
