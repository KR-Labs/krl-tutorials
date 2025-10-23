# D04: Health

**Domain Category:** Major Socioeconomic Domain  
**Tier:** 2, 6  
**Geographic Levels:** State, County, Tract

---

## Overview

Health outcomes, life expectancy, mortality rates, and healthcare access analysis using CDC, HRSA, and County Health Rankings data. This domain provides comprehensive health metrics for population health assessment.

## Key Indicators

- **Life Expectancy** (LE_AGE) - Life expectancy at birth by county
- **Mortality Rate** (MORT) - Age-adjusted mortality rate per 100,000
- **HPSA Score** (HPSA_SCORE) - Health Professional Shortage Area score
- **Health Outcomes Rank** (CHR_HEALTH_OUTCOMES) - Composite health ranking

## Data Sources

### Primary Sources

1. **CDC WONDER**
   - API Endpoint: https://wonder.cdc.gov/controller/datarequest/D76
   - API Key Required: No
   - Geographic Levels: State, County
   - Update Frequency: Annual

2. **Health Resources & Services Administration (HRSA)**
   - API Endpoint: https://data.hrsa.gov/api
   - API Key Required: No
   - Geographic Levels: County, Tract
   - Update Frequency: Quarterly

3. **County Health Rankings**
   - API Endpoint: https://www.countyhealthrankings.org/
   - API Key Required: No
   - Geographic Levels: County
   - Update Frequency: Annual

## Analysis Tiers

### Tier 2: Predictive Analytics
- Disease risk prediction
- Health outcome classification
- Healthcare access modeling

### Tier 6: Advanced Analytics
- Survival analysis (Cox PH models)
- Bayesian hierarchical health modeling
- Causal inference for health interventions

## Recommended Models

1. **Survival Analysis (Cox PH)** (lifelines)
   - Use case: Mortality prediction, hazard ratios

2. **Bayesian Hierarchical Model** (PyMC)
   - Use case: Multi-level health outcomes, uncertainty

3. **XGBoost** (xgboost)
   - Use case: Disease prediction, risk stratification

4. **Random Forest** (scikit-learn)
   - Use case: Health status classification, risk factors

## Visualizations

- **Choropleth Map:** Life expectancy by county
- **Line Chart:** Mortality trends over time
- **Scatter Plot:** Income vs. life expectancy
- **Kaplan-Meier Curve:** Survival analysis

## Example Use Cases

1. **Health Disparities:** Identify regions with poor health outcomes
2. **Resource Planning:** Target healthcare resources to shortage areas
3. **Policy Evaluation:** Assess public health intervention impacts
4. **Mortality Analysis:** Study determinants of life expectancy

## Getting Started

```python
from qrl_core.models import SurvivalModel
from lifelines import CoxPHFitter
import pandas as pd

# Load health data
health_data = pd.read_csv('path/to/health_data.csv')

# Cox Proportional Hazards model
cph = CoxPHFitter()
cph.fit(health_data, duration_col='time', event_col='death')
cph.print_summary()

# Predict survival
cph.predict_survival_function(X_new)
```

## References

- CDC. (2024). *WONDER - Wide-ranging ONline Data for Epidemiologic Research*.
- HRSA. (2024). *Health Professional Shortage Areas*.
- County Health Rankings. (2024). *Annual Rankings Report*.

---

**Status:** Production Ready  
**Notebook:** `D04_D04_health.ipynb`  
**Last Updated:** October 15, 2025  
**Maintainer:** KR-Labs Analytics Team

---

## Trademark Notice

**KR-Labs™** is a trademark of Quipu Research Labs, LLC, a subsidiary of Sudiata Giddasira, Inc.

---

© 2025 KR-Labs. All rights reserved.
