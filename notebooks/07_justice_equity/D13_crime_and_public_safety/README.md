<div align="center">
  <img src="../../../assets/images/KRLabs_WebLogo.png" alt="KR-Labs" width="200">
</div>

# D13: Crime & Public Safety

**Domain Category:** Major Socioeconomic Domain  
**Tier:** 2, 6  
**Geographic Levels:** National, State, County

---

## Overview

Crime rates, public safety, and law enforcement analysis using FBI Uniform Crime Reports and Bureau of Justice Statistics data. Includes spatial crime analysis and hotspot detection.

## Key Indicators

- **Violent Crime Rate** - Violent crimes per 100,000
- **Property Crime Rate** - Property crimes per 100,000
- **Arrest Counts** - By offense type
- **Clearance Rate** - % of crimes cleared by arrest

## Data Sources

1. **FBI UCR** - https://crime-data-explorer.fr.cloud.gov/api
2. **Bureau of Justice Statistics** - https://www.bjs.gov/developer/

## Recommended Models

1. **OLS Regression** - Crime determinants
2. **Spatial Regression** (PySAL) - Spatial crime patterns
3. **Poisson Regression** - Count model for incidents
4. **Random Forest** - Crime risk prediction
5. **Hotspot Analysis** (PySAL) - Getis-Ord Gi* statistic

## Visualizations

- Choropleth: Violent crime rate by county
- Line: Crime trends over time
- Scatter: Violent vs. property crime
- Heatmap: Crime hotspot map

## Example Use Cases

- Crime pattern analysis
- Public safety resource allocation
- Policy evaluation
- Predictive policing

---

**Status:** Production Ready  
**Notebook:** `D13_D13_crime_and_public_safety.ipynb`  
**Last Updated:** October 15, 2025

---

## Trademark Notice

**KR-Labs™** is a trademark of Quipu Research Labs, LLC, a subsidiary of Sudiata Giddasira, Inc.

---

© 2025 KR-Labs. All rights reserved.
