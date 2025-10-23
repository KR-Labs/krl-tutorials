![KR-Labs](../../../assets/images/KRLabs_WebLogo.png)

# D05: Housing

**Domain Category:** Major Socioeconomic Domain  
**Tier:** 1, 2, 6  
**Geographic Levels:** State, County, ZIP, Tract, Metro

---

## Overview

Housing market analysis including home values, rent, affordability, and market dynamics using Census ACS, Zillow, and HUD data. This domain tracks housing costs and accessibility across regions.

## Key Indicators

- **Median Home Value** (B25077_001E) - Median value for owner-occupied units
- **Occupancy Status** (B25003_001E) - Housing units by occupancy status
- **Rent Burden** (B25070_001E) - Gross rent as % of household income
- **Home Value Index** (ZHVI) - Zillow Home Value Index
- **Rent Index** (ZRI) - Zillow Rent Index
- **Fair Market Rent** (FMR) - HUD Fair Market Rents

## Data Sources

### Primary Sources

1. **Census ACS**
   - API Endpoint: https://api.census.gov/data/2023/acs/acs5
   - API Key Required: Yes (CENSUS_API_KEY)
   - Geographic Levels: State, County, ZIP, Tract
   - Update Frequency: Annual

2. **Zillow Open Data**
   - API Endpoint: https://www.zillow.com/research/data/
   - API Key Required: No
   - Geographic Levels: National, State, Metro, County, ZIP
   - Update Frequency: Monthly

3. **HUD Fair Market Rents**
   - API Endpoint: https://www.huduser.gov/portal/datasets/fmr.html
   - API Key Required: No
   - Geographic Levels: Metro, County
   - Update Frequency: Annual

## Analysis Tiers

### Tier 1: Descriptive Analytics
- Home value distributions
- Rent burden analysis
- Housing affordability metrics

### Tier 2: Predictive Analytics
- Home value prediction
- Market trend forecasting
- Affordability modeling

### Tier 6: Advanced Analytics
- Hedonic pricing models
- Spatial econometrics for housing
- Gentrification risk assessment

## Recommended Models

1. **Hedonic Regression** (statsmodels)
   - Use case: Home value prediction from characteristics

2. **OLS Regression** (statsmodels)
   - Use case: Price determinants, affordability

3. **Spatial Econometrics** (PySAL)
   - Use case: Neighborhood effects, location analysis

4. **Random Forest** (scikit-learn)
   - Use case: Price prediction, feature importance

5. **Gradient Boosting** (scikit-learn)
   - Use case: Market prediction, high accuracy

## Visualizations

- **Choropleth Map:** Median home value by county
- **Box Plot:** Home value distribution
- **Scatter Plot:** Home value vs. rent burden
- **Time Series:** Housing price trends

## Example Use Cases

1. **Market Analysis:** Track housing price trends and affordability
2. **Investment Research:** Identify high-growth housing markets
3. **Policy Analysis:** Evaluate rent control effectiveness
4. **Affordability Studies:** Measure housing cost burden by region

## Getting Started

```python
from qrl_core.api.census import CensusAPI
from qrl_core.utils.api_key_manager import load_api_key
import pandas as pd

census_key = load_api_key('CENSUS_API_KEY')
census_api = CensusAPI(api_key=census_key)

housing_data = census_api.get_data(
    dataset='acs/acs5',
    variables=['B25077_001E', 'B25003_001E', 'B25070_001E'],
    geography='county:*',
    year=2023
)

# Analyze affordability
housing_data['affordability_index'] = (
    housing_data['B25077_001E'] / housing_data['median_income']
)
```

## References

- Zillow Research. (2024). *Home Value Index Methodology*.
- HUD. (2024). *Fair Market Rent Documentation*.

---

**Status:** Production Ready  
**Notebook:** `D05_D05_housing.ipynb`  
**Last Updated:** October 15, 2025  
**Maintainer:** KR-Labs Analytics Team

---

## Trademark Notice

**KR-Labs™** is a trademark of Quipu Research Labs, LLC, a subsidiary of Sudiata Giddasira, Inc.

---

© 2025 KR-Labs. All rights reserved.
