<div align="center">
  <img src="../../../assets/images/KRLabs_WebLogo.png" alt="KR-Labs" width="200">
</div>

# D02: Employment & Labor Markets

**Domain Category:** Major Socioeconomic Domain  
**Tier:** 2, 3, 5  
**Geographic Levels:** National, State, County, MSA

---

## Overview

Comprehensive labor market analysis including unemployment rates, employment by occupation, workforce dynamics, and commuting patterns. This domain integrates data from BLS and Census LEHD to provide detailed employment insights.

## Key Indicators

- **Unemployment Rate** (LNS14000000) - Seasonally adjusted unemployment rate
- **Labor Force Participation** (LNU04000000) - Labor force participation rate
- **Employment by Occupation** (OEUXXX) - Employment and wage estimates by occupation
- **Worker Counts** (WAC_S000) - Total jobs by workplace area
- **Origin-Destination Flows** (OD) - Commuting patterns between areas

## Data Sources

### Primary Sources

1. **Bureau of Labor Statistics (BLS) - LAUS**
   - API Endpoint: https://api.bls.gov/publicAPI/v2/timeseries/data/
   - API Key Required: Yes (BLS_API_KEY)
   - Geographic Levels: National, State, County, MSA
   - Update Frequency: Monthly

2. **BLS Occupational Employment Statistics (OES)**
   - API Endpoint: https://api.bls.gov/publicAPI/v2/timeseries/data/
   - API Key Required: Yes (BLS_API_KEY)
   - Geographic Levels: National, State, MSA
   - Update Frequency: Annual

3. **Census LEHD (Longitudinal Employer-Household Dynamics)**
   - API Endpoint: https://lehd.ces.census.gov/data/
   - API Key Required: No
   - Geographic Levels: State, County, Tract
   - Update Frequency: Quarterly

## Analysis Tiers

### Tier 2: Predictive Analytics
- Unemployment determinant modeling
- Wage prediction by occupation and region
- Employment classification models

### Tier 3: Time Series Analytics
- Unemployment forecasting with ARIMA/Prophet
- Seasonal labor market patterns
- Trend decomposition and analysis

### Tier 5: Ensemble Methods
- Advanced employment forecasting with ensemble models
- High-accuracy wage prediction
- Bayesian Structural Time Series (BSTS) for policy impact

## Recommended Models

1. **OLS Regression** (statsmodels)
   - Use case: Unemployment determinants, wage analysis

2. **GMM (Generalized Method of Moments)** (linearmodels)
   - Use case: Panel labor data, endogeneity correction

3. **ARIMA** (statsmodels)
   - Use case: Unemployment forecasting, seasonal adjustment

4. **Prophet** (prophet)
   - Use case: Labor market forecasting with trend/seasonality

5. **Random Forest** (scikit-learn)
   - Use case: Employment classification, occupation prediction

6. **Gradient Boosting** (scikit-learn)
   - Use case: Wage prediction, feature importance

7. **Network Analysis** (networkx)
   - Use case: Commuting patterns, job flow networks

8. **BSTS** (tensorflow-probability)
   - Use case: Employment forecasting with structural breaks

## Visualizations

- **Line Chart:** Unemployment rate trends over time
- **Choropleth Map:** Unemployment by county/state
- **Scatter Plot:** Employment vs. wages by industry
- **Network Graph:** Commuting flow patterns
- **Heatmap:** Employment density by occupation/region

## Example Use Cases

1. **Labor Market Analysis:** Track unemployment trends and identify at-risk regions
2. **Workforce Planning:** Forecast labor demand by industry and occupation
3. **Commuting Studies:** Analyze job-to-residence flow patterns
4. **Wage Analysis:** Compare compensation across occupations and geographies
5. **Policy Evaluation:** Assess impact of workforce development programs

## Getting Started

```python
from qrl_core.api.bls import BLSAPI
from qrl_core.models import TimeSeriesModel
from qrl_core.utils.api_key_manager import load_api_key
import pandas as pd

# Load API key
bls_key = load_api_key('BLS_API_KEY')
bls_api = BLSAPI(api_key=bls_key)

# Fetch unemployment data
unemployment_data = bls_api.get_series(
    series_ids=['LNS14000000'],
    start_year=2020,
    end_year=2024
)

# Forecast unemployment
model = TimeSeriesModel(method="prophet")
forecast = model.forecast(unemployment_data, periods=12)

# Visualize results
forecast.plot()
```

## References

- Bureau of Labor Statistics. (2024). *Local Area Unemployment Statistics*.
- Census Bureau. (2024). *LEHD Origin-Destination Employment Statistics*.
- Abraham, K. G., & Katz, L. F. (1986). "Cyclical Unemployment: Sectoral Shifts or Aggregate Disturbances?" *Journal of Political Economy*.

---

**Status:** Production Ready  
**Notebook:** `D02_D02_employment_and_labor.ipynb`  
**Last Updated:** October 15, 2025  
**Maintainer:** KR-Labs Analytics Team

---

## Trademark Notice

**KR-Labs™** is a trademark of Quipu Research Labs, LLC, a subsidiary of Sudiata Giddasira, Inc.

---

© 2025 KR-Labs. All rights reserved.
