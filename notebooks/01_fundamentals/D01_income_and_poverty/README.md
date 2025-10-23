# D01: Income & Poverty

**Domain Category:** Major Socioeconomic Domain  
**Tier:** 1, 2, 3  
**Geographic Levels:** State, County, ZIP, Tract

---

## Overview

Analysis of household income, poverty rates, and income inequality using Census ACS and Federal Reserve Economic Data (FRED). This domain provides comprehensive metrics for understanding economic well-being and disparities across geographic regions.

## Key Indicators

- **Median Household Income** (B19013_001E) - Median household income in the past 12 months
- **Poverty Count** (B17001_002E) - Population for whom poverty status is determined
- **Gini Index** (B19083_001E) - Measure of income inequality (0-1 scale)
- **Personal Income** (MEPAINUSA672N) - Real median personal income in the United States
- **National Gini** (SIPOVGINIUSA) - Gini index for the United States

## Data Sources

### Primary Sources

1. **U.S. Census Bureau - American Community Survey (ACS)**
   - API Endpoint: https://api.census.gov/data/2023/acs/acs5
   - API Key Required: Yes (CENSUS_API_KEY)
   - Geographic Levels: State, County, ZIP, Tract
   - Update Frequency: Annual (5-year estimates)

2. **Federal Reserve Economic Data (FRED)**
   - API Endpoint: https://api.stlouisfed.org/fred/series/observations
   - API Key Required: Yes (FRED_API_KEY)
   - Geographic Levels: National, State
   - Update Frequency: Annual/Quarterly (varies by series)

## Analysis Tiers

### Tier 1: Descriptive Analytics
- Distribution of household income across geographies
- Poverty rate calculations and trends
- Income inequality measures (Gini coefficient, Lorenz curves)
- Regional income comparisons

### Tier 2: Predictive Analytics
- Income prediction models using demographic and economic factors
- Poverty correlate analysis
- Machine learning for income forecasting

### Tier 3: Time Series Analytics
- Income trend analysis over time
- Poverty rate forecasting
- Structural break detection in income patterns

## Recommended Models

1. **OLS Regression** (statsmodels)
   - Use case: Linear income determinants, poverty correlates

2. **Bayesian Hierarchical Model** (PyMC)
   - Use case: Multi-level income analysis across geographies

3. **Quantile Regression** (statsmodels)
   - Use case: Income inequality analysis across distribution

4. **Gradient Boosting** (scikit-learn)
   - Use case: Non-linear income prediction, high accuracy

5. **Random Forest** (scikit-learn)
   - Use case: Poverty classification, variable importance

6. **Dynamic Factor Models (DFM)** (statsmodels)
   - Use case: High-dimensional income analysis, nowcasting

## Visualizations

- **Choropleth Map:** Median household income by county
- **Box Plot:** Income distribution by county/state
- **Violin Plot:** Income distribution with probability density
- **Scatter Plot:** Income vs. poverty with trendlines
- **Lorenz Curve:** Income inequality visualization

## Example Use Cases

1. **Regional Economic Analysis:** Compare income levels across metro areas
2. **Poverty Assessment:** Identify high-poverty communities for targeted interventions
3. **Inequality Studies:** Measure and track income inequality over time
4. **Policy Impact:** Evaluate effects of minimum wage changes on income distribution
5. **Grant Applications:** Demonstrate community economic needs

## Getting Started

```python
from qrl_core.api.census import CensusAPI
from qrl_core.api.fred import FREDAPI
from qrl_core.utils.api_key_manager import load_api_key
from qrl_core.utils.plotly_visualization_engine import PlotlyVisualizationEngine
import pandas as pd

# Load API keys
census_key = load_api_key('CENSUS_API_KEY')
fred_key = load_api_key('FRED_API_KEY')

# Initialize APIs
census_api = CensusAPI(api_key=census_key)
fred_api = FREDAPI(api_key=fred_key)

# Fetch median household income for all states
income_data = census_api.get_data(
    dataset='acs/acs5',
    variables=['B19013_001E', 'B17001_002E', 'B19083_001E'],
    geography='state:*',
    year=2023
)

# Create visualizations
viz_engine = PlotlyVisualizationEngine()
charts = viz_engine.generate_tier_visualizations(
    data=income_data,
    tier_type="tier_1",
    analysis_focus="income_poverty"
)

for chart in charts:
    chart.show()
```

## References

- U.S. Census Bureau. (2024). *American Community Survey (ACS)*.
- Federal Reserve Bank of St. Louis. (2024). *FRED Economic Data*.
- Piketty, T., & Saez, E. (2003). "Income Inequality in the United States, 1913-1998." *Quarterly Journal of Economics*.
- Chetty, R., et al. (2014). "Where is the Land of Opportunity?" *The Quarterly Journal of Economics*.

---

**Status:** Production Ready  
**Notebook:** `D01_D01_income_and_poverty.ipynb`  
**Last Updated:** October 15, 2025  
**Maintainer:** KR-Labs Analytics Team

---

## Trademark Notice

**KR-Labs™** is a trademark of Quipu Research Labs, LLC, a subsidiary of Sudiata Giddasira, Inc.

---

© 2025 KR-Labs. All rights reserved.
