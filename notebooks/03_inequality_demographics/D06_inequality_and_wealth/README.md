<div align="center">
  <img src="../../../assets/images/KRLabs_WebLogo.png" alt="KR-Labs" width="200">
</div>

# D06: Inequality & Wealth

**Domain Category:** Major Socioeconomic Domain  
**Tier:** 1, 2, 4  
**Geographic Levels:** National, State, County, ZIP

---

## Overview

Analysis of income inequality, wealth distribution, and economic stratification using Census data and Federal Reserve's Survey of Consumer Finances. Includes advanced inequality metrics and fairness-aware machine learning.

## Key Indicators

- **Gini Index** (B19083_001E) - Income inequality coefficient (0-1)
- **Income Distribution** (B19001_001E) - Household income distribution
- **Net Wealth** (NetWealth) - Household net worth by demographic
- **Wealth Percentiles** (WealthPercentiles) - Wealth distribution by percentile

## Data Sources

### Primary Sources

1. **Census ACS**
   - API Endpoint: https://api.census.gov/data/2023/acs/acs5
   - API Key Required: Yes (CENSUS_API_KEY)
   - Geographic Levels: State, County, ZIP
   - Update Frequency: Annual

2. **Survey of Consumer Finances (SCF)**
   - API Endpoint: https://www.federalreserve.gov/econres/scfindex.htm
   - API Key Required: No
   - Geographic Levels: National, State
   - Update Frequency: Triennial

## Analysis Tiers

### Tier 1: Descriptive Analytics
- Inequality measures (Gini, Theil, Atkinson indices)
- Wealth distribution analysis
- Lorenz curves

### Tier 2: Predictive Analytics
- Inequality prediction models
- Wealth accumulation forecasting

### Tier 4: Unsupervised Learning
- Wealth segmentation
- Inequality clustering
- Fairness-aware ML with bias detection

## Recommended Models

1. **Theil Index** (pandas)
   - Use case: Inequality decomposition

2. **Atkinson Index** (numpy)
   - Use case: Welfare-based inequality

3. **Bayesian Hierarchical Model** (PyMC)
   - Use case: Multi-level wealth modeling

4. **Quantile Regression** (statsmodels)
   - Use case: Distributional effects

5. **Gradient Boosting** (scikit-learn)
   - Use case: Inequality forecasting

6. **Fairness-Aware ML** (fairlearn)
   - Use case: Algorithmic fairness, bias detection

## Visualizations

- **Choropleth Map:** Gini coefficient by county
- **Box Plot:** Income distribution
- **Lorenz Curve:** Cumulative income vs. population
- **Scatter Plot:** Income vs. wealth

## Example Use Cases

1. **Inequality Research:** Measure and decompose income inequality
2. **Wealth Studies:** Analyze wealth gaps across demographics
3. **Policy Evaluation:** Assess redistributive policy impacts
4. **Fairness Analysis:** Detect bias in economic algorithms

## Getting Started

```python
from qrl_core.api.census import CensusAPI
from qrl_core.utils.api_key_manager import load_api_key
import numpy as np

census_key = load_api_key('CENSUS_API_KEY')
census_api = CensusAPI(api_key=census_key)

inequality_data = census_api.get_data(
    dataset='acs/acs5',
    variables=['B19083_001E', 'B19001_001E'],
    geography='state:*',
    year=2023
)

# Calculate Theil index
def theil_index(incomes):
    mean_income = np.mean(incomes)
    return np.mean(incomes / mean_income * np.log(incomes / mean_income))
```

## References

- Piketty, T. (2014). *Capital in the Twenty-First Century*.
- Atkinson, A. B. (2015). *Inequality: What Can Be Done?*

---

**Status:** Production Ready  
**Notebook:** `D06_D06_inequality_and_wealth.ipynb`  
**Last Updated:** October 15, 2025  
**Maintainer:** KR-Labs Analytics Team

---

## Trademark Notice

**KR-Labs™** is a trademark of Quipu Research Labs, LLC, a subsidiary of Sudiata Giddasira, Inc.

---

© 2025 KR-Labs. All rights reserved.
