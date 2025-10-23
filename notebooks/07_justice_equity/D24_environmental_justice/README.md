<div align="center">
  <img src="../../../assets/images/KRLabs_WebLogo.png" alt="KR-Labs" width="200">
</div>

# D24: Environmental Justice

**Domain Category:** Minor Socioeconomic Domain  
**Tier:** 2, 6  
**Geographic Levels:** County, Tract, Block Group

---

## Overview

Pollution exposure disparity, environmental racism, green space access using EPA EJScreen data. Includes Bayesian spatial modeling.

## Key Indicators

- **Air Quality Index** - EPA Air Quality Index
- **Toxic Releases** - Proximity to toxic release facilities (km)
- **EJ Index** - Composite EJ burden and demographics (percentile)
- **Total Population** (B01001_001E) - For exposure normalization

## Data Sources

1. **EPA EJScreen** - https://www.epa.gov/ejscreen
2. **Census ACS** - https://api.census.gov/data/2023/acs/acs5

## Recommended Models

1. **Bayesian Spatial Model** (PyMC) - Spatial environmental justice
2. **OLS Regression** - Environmental burden determinants
3. **Random Forest** - Environmental risk classification

## Visualizations

- Choropleth: Environmental justice index by tract
- Heatmap: Toxic release proximity
- Scatter: Pollution exposure by demographics

## Example Use Cases

- Environmental justice assessment
- Pollution exposure mapping
- Health disparities analysis
- Policy impact evaluation

---

**Status:** Production Ready  
**Notebook:** `D24_D24_environmental_justice.ipynb`  
**Last Updated:** October 15, 2025

---

## Trademark Notice

**KR-Labs™** is a trademark of Quipu Research Labs, LLC, a subsidiary of Sudiata Giddasira, Inc.

---

© 2025 KR-Labs. All rights reserved.
