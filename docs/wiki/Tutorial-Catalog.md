# Tutorial Catalog

Complete catalog of all 33 KRL Analytics Tutorials organized by domain and tier.

## Quick Reference

| Domain | Code | Title | Tiers | Data Sources | Difficulty |
|--------|------|-------|-------|--------------|------------|
| Economic | D01 | Income & Wealth Inequality | 1-4 | Census ACS, FRED | ⭐ Beginner |
| Economic | D02 | Health Economics & Insurance | 1-4 | CDC BRFSS, CMS | ⭐⭐ Intermediate |
| Economic | D03 | Housing Affordability | 1-3 | Census ACS, Zillow | ⭐ Beginner |
| Economic | D04 | Education Economics | 1-4 | NCES, Census | ⭐⭐ Intermediate |
| Economic | D05 | Labor Force & Employment | 1-4 | BLS, FRED | ⭐⭐ Intermediate |
| Social | D06 | Crime Statistics & Safety | 1-4 | FBI UCR, BJS | ⭐⭐ Intermediate |
| Social | D07 | Environmental Quality | 1-4 | EPA, NOAA | ⭐⭐⭐ Advanced |
| Social | D08 | Population & Demographics | 1-3 | Census, UN | ⭐ Beginner |
| Social | D09 | Migration & Immigration | 1-4 | Census, DHS | ⭐⭐ Intermediate |
| Social | D10 | Intergenerational Mobility | 1-4 | Opportunity Insights | ⭐⭐⭐ Advanced |
| Advanced | D30 | Subjective Well-Being | 1-4 | OECD, World Bank | ⭐⭐ Intermediate |
| Advanced | D31 | Civic Trust | 1-4 | Gallup, Pew | ⭐⭐ Intermediate |
| Advanced | D32 | Freedom & Civil Liberties | 1-4 | Freedom House | ⭐⭐ Intermediate |
| Advanced | D33 | Gender Equality | 1-4 | WEF, ILO | ⭐⭐ Intermediate |

*Note: 19 additional domains (D11-D29) are in development*

## By Domain Category

### 📊 Economic Analytics (D01-D05)

#### D01: Income & Wealth Inequality
**Path**: `notebooks/01_economic/D01_income_wealth/`

**What You'll Learn:**
- Measure income inequality (Gini coefficient, percentile ratios)
- Analyze wealth concentration
- Trend analysis of inequality over time
- Regional inequality comparisons

**Tiers Covered:**
- **Tier 1**: Descriptive statistics, income distributions
- **Tier 2**: Income forecasting, trend predictions
- **Tier 3**: Policy impact evaluation (tax changes)
- **Tier 4**: Clustering by income patterns

**Data Sources:**
- Census American Community Survey
- FRED income series
- Synthetic income distributions

**Key Techniques:**
- Lorenz curves
- Gini coefficient calculation
- OLS regression
- Time series analysis

**Difficulty**: ⭐ Beginner-friendly

---

#### D02: Health Economics & Insurance Coverage
**Path**: `notebooks/01_economic/D02_health_economics/`

**What You'll Learn:**
- Health insurance coverage analysis
- Healthcare cost trends
- Access to care metrics
- Health outcome disparities

**Tiers Covered:**
- **Tier 1**: Coverage rates, cost distributions
- **Tier 2**: Cost forecasting, demand modeling
- **Tier 3**: Insurance policy impacts
- **Tier 4**: Patient segmentation

**Data Sources:**
- CDC BRFSS (Behavioral Risk Factor Surveillance)
- CMS (Centers for Medicare & Medicaid)
- NHIS (National Health Interview Survey)

**Key Techniques:**
- Survival analysis
- Cost-effectiveness analysis
- Difference-in-differences
- Logistic regression

**Difficulty**: ⭐⭐ Intermediate

---

#### D03: Housing Affordability & Market Dynamics
**Path**: `notebooks/01_economic/D03_housing_market/`

**What You'll Learn:**
- Housing affordability metrics
- Price-to-income ratios
- Market trend analysis
- Regional market comparisons

**Tiers Covered:**
- **Tier 1**: Price distributions, affordability metrics
- **Tier 2**: Price forecasting
- **Tier 3**: Policy impact on affordability

**Data Sources:**
- Census ACS (housing values, rents)
- Zillow (market data)
- FRED (mortgage rates, construction)

**Key Techniques:**
- Time series forecasting
- Hedonic pricing models
- Spatial analysis
- Panel data methods

**Difficulty**: ⭐ Beginner-friendly

---

#### D04: Education Economics & Human Capital
**Path**: `notebooks/01_economic/D04_education_economics/`

**What You'll Learn:**
- Educational attainment analysis
- Returns to education
- School quality metrics
- Education-income relationships

**Tiers Covered:**
- **Tier 1**: Enrollment, completion rates
- **Tier 2**: Earning potential predictions
- **Tier 3**: Education policy impacts
- **Tier 4**: School clustering and segmentation

**Data Sources:**
- NCES (National Center for Education Statistics)
- Census ACS
- Department of Education

**Key Techniques:**
- Mincer equations (wage returns)
- Instrumental variables
- Difference-in-differences
- Regression discontinuity

**Difficulty**: ⭐⭐ Intermediate

---

#### D05: Labor Force & Employment Dynamics
**Path**: `notebooks/01_economic/D05_labor_employment/`

**What You'll Learn:**
- Unemployment rate analysis
- Labor force participation
- Job creation/destruction
- Wage dynamics

**Tiers Covered:**
- **Tier 1**: Employment rates, participation
- **Tier 2**: Unemployment forecasting
- **Tier 3**: Policy impact on employment
- **Tier 4**: Industry clustering

**Data Sources:**
- BLS (Bureau of Labor Statistics)
- FRED
- JOLTS (Job Openings and Labor Turnover Survey)

**Key Techniques:**
- ARIMA forecasting
- Seasonal adjustment
- Event studies
- Synthetic control methods

**Difficulty**: ⭐⭐ Intermediate

---

### 🏛️ Social & Policy Analytics (D06-D10)

#### D06: Crime Statistics & Public Safety
**Path**: `notebooks/02_social/D06_crime_statistics/`

**What You'll Learn:**
- Crime rate analysis
- Spatial crime patterns
- Deterrence effects
- Police effectiveness

**Tiers Covered:**
- **Tier 1**: Crime rates, trends
- **Tier 2**: Crime forecasting
- **Tier 3**: Intervention impacts
- **Tier 4**: Crime hotspot detection

**Data Sources:**
- FBI UCR (Uniform Crime Reporting)
- NIBRS (National Incident-Based Reporting)
- BJS (Bureau of Justice Statistics)

**Key Techniques:**
- Poisson regression
- Spatial autocorrelation
- Difference-in-differences
- Network analysis

**Difficulty**: ⭐⭐ Intermediate

---

#### D07: Environmental Quality & Climate Data
**Path**: `notebooks/02_social/D07_environmental_quality/`

**What You'll Learn:**
- Air quality metrics
- Climate trends
- Environmental justice
- Pollution-health relationships

**Tiers Covered:**
- **Tier 1**: Pollution levels, trends
- **Tier 2**: Quality forecasting
- **Tier 3**: Policy impact evaluation
- **Tier 4**: Geographic clustering

**Data Sources:**
- EPA (Environmental Protection Agency)
- NOAA (Climate data)
- CDC (Environmental health)

**Key Techniques:**
- Time series decomposition
- Spatial regression
- Regression discontinuity
- GIS analysis

**Difficulty**: ⭐⭐⭐ Advanced

---

#### D08: Population & Demographic Trends
**Path**: `notebooks/02_social/D08_demographics/`

**What You'll Learn:**
- Population growth analysis
- Age structure transitions
- Demographic forecasting
- Migration patterns

**Tiers Covered:**
- **Tier 1**: Population pyramids, growth rates
- **Tier 2**: Population forecasting
- **Tier 3**: Demographic dividend analysis

**Data Sources:**
- Census Bureau
- UN Population Division
- CDC (births, deaths)

**Key Techniques:**
- Cohort-component projections
- Life tables
- Fertility/mortality analysis
- Leslie matrices

**Difficulty**: ⭐ Beginner-friendly

---

#### D09: Migration & Immigration Patterns
**Path**: `notebooks/02_social/D09_migration/`

**What You'll Learn:**
- Internal migration flows
- Immigration trends
- Push-pull factors
- Economic integration

**Tiers Covered:**
- **Tier 1**: Migration rates, patterns
- **Tier 2**: Flow predictions
- **Tier 3**: Policy impact on migration
- **Tier 4**: Network analysis of flows

**Data Sources:**
- Census ACS (migration data)
- DHS (Department of Homeland Security)
- IRS (tax migration data)

**Key Techniques:**
- Gravity models
- Network analysis
- Survival analysis
- Spatial econometrics

**Difficulty**: ⭐⭐ Intermediate

---

#### D10: Intergenerational Mobility
**Path**: `notebooks/02_social/D10_mobility/`

**What You'll Learn:**
- Income mobility metrics
- Opportunity gaps
- Geographic variation
- Policy effects on mobility

**Tiers Covered:**
- **Tier 1**: Mobility statistics
- **Tier 2**: Mobility predictions
- **Tier 3**: Causal analysis of policies
- **Tier 4**: Community clustering

**Data Sources:**
- Opportunity Insights
- PSID (Panel Study of Income Dynamics)
- Census data

**Key Techniques:**
- Transition matrices
- Rank-rank regressions
- Instrumental variables
- Causal forests

**Difficulty**: ⭐⭐⭐ Advanced

---

### 🌟 Advanced Topics (D11-D33)

#### D30: Subjective Well-Being
**Path**: `notebooks/09_planned/D30_subjective_wellbeing/`

**What You'll Learn:**
- Life satisfaction measurement
- Happiness economics
- Emotional well-being
- Quality of life indices

**Tiers Covered:**
- **Tier 1**: Well-being distributions
- **Tier 2**: Satisfaction predictions
- **Tier 4**: Factor analysis, clustering

**Data Sources:**
- OECD Better Life Index
- World Happiness Report
- CDC BRFSS

**Key Techniques:**
- Factor analysis
- K-means clustering
- Random Forest
- Survey analysis

**Difficulty**: ⭐⭐ Intermediate

---

#### D31: Civic Trust (Planned)
**Path**: `notebooks/09_planned/D31_civic_trust/`

**What You'll Learn:**
- Trust in institutions
- Civic engagement
- Volunteer participation
- Social capital

**Data Sources:**
- Gallup polls
- Pew Research
- General Social Survey

**Status**: 🚧 Template ready, needs customization

---

#### D32: Freedom & Civil Liberties (Planned)
**Path**: `notebooks/09_planned/D32_freedom_civil/`

**What You'll Learn:**
- Freedom House indices
- Civil liberties trends
- Democratic backsliding
- Rights protection

**Data Sources:**
- Freedom House
- V-Dem Institute
- Polity Project

**Status**: 🚧 Template ready, needs customization

---

#### D33: Gender Equality (Planned)
**Path**: `notebooks/09_planned/D33_gender_equality/`

**What You'll Learn:**
- Gender pay gaps
- Labor force participation
- Educational attainment
- Political representation

**Data Sources:**
- WEF Gender Gap Report
- ILO (International Labour Organization)
- World Bank

**Status**: 🚧 Template ready, needs customization

---

## By Analytical Tier

### Tier 1 (Descriptive): All Tutorials
Every tutorial includes Tier 1 content - start anywhere!

### Tier 2 (Predictive): Best Tutorials
- D01: Income forecasting
- D03: Housing price prediction
- D05: Unemployment forecasting
- D07: Air quality prediction

### Tier 3 (Causal): Policy Analysis
- D01: Tax policy impacts
- D02: Insurance mandate effects
- D05: Employment program evaluation
- D06: Crime intervention impacts
- D10: Education policy and mobility

### Tier 4 (Unsupervised): Pattern Discovery
- D01: Income group clustering
- D04: School quality segmentation
- D06: Crime hotspots
- D30: Well-being factor analysis

### Tier 5 (Advanced ML): Coming Soon
Future expansions will include deep learning applications.

### Tier 6 (Network/Spatial): Specialized
- D06: Crime spatial analysis
- D07: Environmental spatial patterns
- D09: Migration network flows

## By Difficulty Level

### ⭐ Beginner-Friendly
Start here if you're new to analytics:
- D01: Income & Wealth
- D03: Housing Affordability
- D08: Demographics

### ⭐⭐ Intermediate
Comfortable with Python and basic statistics:
- D02: Health Economics
- D04: Education Economics
- D05: Labor Force
- D06: Crime Statistics
- D09: Migration
- D30: Subjective Well-Being

### ⭐⭐⭐ Advanced
For experienced analysts and researchers:
- D07: Environmental Quality
- D10: Intergenerational Mobility

## By Data Source

### Census ACS
D01, D03, D04, D08, D09

### FRED
D01, D03, D05

### CDC
D02, D30

### BLS
D05

### Specialized Agencies
- D06: FBI, BJS
- D07: EPA, NOAA
- D10: Opportunity Insights
- D30: OECD, World Bank

## Learning Pathways

### Path 1: Economic Policy Analyst
1. D01 (Income)
2. D05 (Employment)
3. D03 (Housing)
4. D04 (Education)
5. D10 (Mobility)

### Path 2: Public Health Analyst
1. D02 (Health Economics)
2. D07 (Environmental Quality)
3. D08 (Demographics)
4. D30 (Well-Being)

### Path 3: Social Scientist
1. D08 (Demographics)
2. D09 (Migration)
3. D10 (Mobility)
4. D06 (Crime)
5. D30 (Well-Being)

### Path 4: Data Science Generalist
Pick 1 from each category:
- Economic: D01 or D05
- Social: D06 or D09
- Advanced: D30

## Coming Soon (D11-D29)

Future tutorials in development across:
- Financial markets
- Technology & innovation
- Urban development
- Energy economics
- Healthcare delivery
- And more!

## How to Navigate

1. **Browse by interest**: Pick a domain you care about
2. **Follow a path**: Use the learning pathways
3. **Progress by tier**: Master Tier 1 everywhere, then move to Tier 2
4. **Filter by data**: Explore tutorials using familiar data sources

## Next Steps

- **[Quick Start Guide](Quick-Start-Guide)** - Run your first tutorial
- **[Learning Paths](Learning-Paths)** - Structured curricula
- **[Data Sources](Data-Sources)** - Understand the data
- **[Analytical Tiers](Analytical-Tiers-Guide)** - Master the framework

---

**Last Updated**: October 2025 | **Tutorials**: 33 (14 complete, 19 planned)
