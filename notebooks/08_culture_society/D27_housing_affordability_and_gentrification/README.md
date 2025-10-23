<div align="center">
  <img src="../../../assets/images/KRLabs_WebLogo.png" alt="KR-Labs" width="200">
</div>

# D27: Housing Affordability & Gentrification

**Domain Category:** Minor Socioeconomic Domain  
**Tier:** 2, 6  
**Geographic Levels:** State, County, ZIP, Tract, Metro

---

## Overview

Rent burden, eviction rates, displacement risk, gentrification using Census ACS, Zillow, and Eviction Lab data. Includes Bayesian hierarchical modeling.

## Key Indicators

- **Rent Burden** (B25070_001E) - Gross rent as % of household income
- **Tenure** (B25003_001E) - Owner vs. renter occupied units
- **Zillow Rent Index** (ZRI) - Median market rent
- **Zillow Home Value Index** (ZHVI) - Typical home value
- **Eviction Rate** - Evictions per 100 renter households

## Data Sources

1. **Census ACS** - https://api.census.gov/data/2023/acs/acs5
2. **Zillow Open Data** - https://www.zillow.com/research/data/
3. **Eviction Lab** - https://evictionlab.org/get-the-data/

## Recommended Models

1. **OLS Regression** - Affordability determinants
2. **Panel Regression** - Gentrification dynamics
3. **Bayesian Hierarchical Model** (PyMC) - Multi-level housing analysis

## Visualizations

- Choropleth: Rent burden by tract
- Box: Rent distribution
- Scatter: Rent vs. eviction rate

## Example Use Cases

- Housing affordability assessment
- Gentrification risk analysis
- Eviction prevention planning
- Displacement impact studies

---

**Status:** Production Ready  
**Notebook:** `D27_D27_housing_affordability_and_gentrification.ipynb`  
**Last Updated:** October 15, 2025

---

## Trademark Notice

**KR-Labs™** is a trademark of Quipu Research Labs, LLC, a subsidiary of Sudiata Giddasira, Inc.

---

© 2025 KR-Labs. All rights reserved.
