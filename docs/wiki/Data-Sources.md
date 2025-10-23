# Data Sources

Comprehensive guide to data sources used in KRL Tutorials.

## Overview

KRL Tutorials use a combination of:
- **Synthetic data** (generated for learning, no API keys needed)
- **Real public data** (from government agencies and institutions)
- **API access** (requires free registration)

## Primary Data Sources

### 1. U.S. Census Bureau

#### What It Provides
- **American Community Survey (ACS)**: Demographics, income, housing, education
- **Population Estimates**: Annual population by state, county, metro area
- **Economic Indicators**: Business patterns, international trade
- **Decennial Census**: Comprehensive population counts

#### API Access
```python
from census import Census
import os

c = Census(os.environ['CENSUS_API_KEY'])

# Example: Get median income by state
data = c.acs5.state(
    ('NAME', 'B19013_001E'),  # Median household income
    year=2021
)
```

#### Registration
- **URL**: https://api.census.gov/data/key_signup.html
- **Cost**: Free
- **Rate Limits**: 500 requests per IP per day

#### Tutorials Using Census Data
- D01: Income & Wealth Inequality
- D03: Housing Affordability
- D04: Education Economics
- D08: Population & Demographics

#### Key Variables
```python
# Common ACS variables
'B19013_001E'  # Median household income
'B25077_001E'  # Median home value
'B15003_022E'  # Bachelor's degree attainment
'B23025_005E'  # Unemployment
'C17002_001E'  # Poverty status
```

### 2. Federal Reserve Economic Data (FRED)

#### What It Provides
- **Economic indicators**: GDP, inflation, interest rates
- **Labor statistics**: Unemployment, wages, participation rates
- **Financial markets**: Stock indices, bond yields
- **Regional data**: State and metro-level economics

#### API Access
```python
from fredapi import Fred
import os

fred = Fred(api_key=os.environ['FRED_API_KEY'])

# Example: Get unemployment rate
unemployment = fred.get_series('UNRATE')

# Example: Get GDP growth
gdp = fred.get_series('GDP', observation_start='2010-01-01')
```

#### Registration
- **URL**: https://fred.stlouisfed.org/docs/api/api_key.html
- **Cost**: Free
- **Rate Limits**: No strict limits (be reasonable)

#### Tutorials Using FRED Data
- D01: Income & Wealth Inequality
- D05: Labor Force & Employment
- D09: Migration & Immigration
- D10: Intergenerational Mobility

#### Popular Series
```python
# Commonly used FRED series
'UNRATE'        # Unemployment rate
'GDP'           # Gross Domestic Product
'CPIAUCSL'      # Consumer Price Index
'FEDFUNDS'      # Federal Funds Rate
'DGS10'         # 10-Year Treasury Rate
'MORTGAGE30US'  # 30-Year Mortgage Rate
```

### 3. Centers for Disease Control (CDC)

#### What It Provides
- **BRFSS**: Behavioral Risk Factor Surveillance System (health behaviors)
- **WONDER**: Mortality, births, disease surveillance
- **NHANES**: National Health and Nutrition Examination Survey
- **Vaccination data**: COVID-19 and routine immunizations

#### API Access
```python
import requests

# CDC WONDER API example
url = "https://wonder.cdc.gov/controller/datarequest/D176"
params = {
    'request_xml': """
    <request-parameters>
        <parameter>
            <name>B_1</name>
            <value>D176.V1</value>
        </parameter>
    </request-parameters>
    """
}

response = requests.post(url, data=params)
```

#### Registration
- **URL**: Most CDC data is open (no key required)
- **Cost**: Free
- **Rate Limits**: Varies by dataset

#### Tutorials Using CDC Data
- D02: Health Economics & Insurance
- D04: Education Economics (nutrition/health)
- D30: Subjective Well-Being

### 4. Bureau of Labor Statistics (BLS)

#### What It Provides
- **Employment**: Job openings, hires, separations (JOLTS)
- **Wages**: Occupational employment statistics
- **Productivity**: Labor productivity and costs
- **Prices**: CPI, PPI (also in FRED)

#### API Access
```python
import requests
import os

# BLS API v2
headers = {'Content-type': 'application/json'}
data = {
    'seriesid': ['LNS14000000'],  # Unemployment rate
    'startyear': '2020',
    'endyear': '2025',
    'registrationkey': os.environ['BLS_API_KEY']
}

response = requests.post(
    'https://api.bls.gov/publicAPI/v2/timeseries/data/',
    json=data,
    headers=headers
)
```

#### Registration
- **URL**: https://www.bls.gov/developers/home.htm
- **Cost**: Free
- **Rate Limits**: 500 queries/day (with key), 25 without

#### Tutorials Using BLS Data
- D05: Labor Force & Employment
- D10: Intergenerational Mobility

### 5. OECD Data

#### What It Provides
- **International comparisons**: Cross-country economic and social indicators
- **Well-being metrics**: Life satisfaction, work-life balance
- **Education**: PISA scores, attainment levels
- **Health**: Expenditure, outcomes, access

#### API Access
```python
import pandas as pd

# OECD API (no key required)
url = "https://stats.oecd.org/restsdmx/sdmx.ashx/GetData/QNA/USA.B1_GE.CUR+VOBARSA.Q/all"
df = pd.read_xml(url)
```

#### Registration
- **URL**: No registration required for most data
- **Cost**: Free
- **Rate Limits**: None specified

#### Tutorials Using OECD Data
- D30: Subjective Well-Being
- D32: Freedom & Civil Liberties
- D33: Gender Equality

### 6. World Bank

#### What It Provides
- **Development indicators**: Global poverty, education, health
- **Economic data**: GDP, trade, debt for all countries
- **Climate**: Emissions, energy, environmental indicators

#### API Access
```python
import wbdata
import datetime

# World Bank API
date_range = (datetime.datetime(2015, 1, 1), datetime.datetime(2025, 1, 1))

# Get GDP per capita for USA
gdp_data = wbdata.get_dataframe(
    {"NY.GDP.PCAP.CD": "GDP per capita"},
    country='USA',
    data_date=date_range
)
```

#### Registration
- **URL**: No registration required
- **Cost**: Free
- **Rate Limits**: None

#### Tutorials Using World Bank Data
- D30: Subjective Well-Being
- D33: Gender Equality

## Synthetic Data Generation

Many tutorials include synthetic data generation for offline learning.

### Why Synthetic Data?

✅ **Advantages:**
- No API keys required
- Works offline
- Reproducible
- Customizable for teaching
- No rate limits

⚠️ **Limitations:**
- Not real-world patterns
- Simplified relationships
- Educational purposes only

### Example: Synthetic Income Data

```python
import numpy as np
import pandas as pd

np.random.seed(42)

# Generate synthetic income distribution
n = 10000
years = range(2015, 2025)

data = []
for year in years:
    # Log-normal income distribution
    incomes = np.random.lognormal(
        mean=10.5 + 0.02 * (year - 2015),
        sigma=0.7,
        size=n
    )
    
    df_year = pd.DataFrame({
        'year': year,
        'income': incomes,
        'state': np.random.choice(['CA', 'TX', 'NY', 'FL'], n)
    })
    data.append(df_year)

df = pd.concat(data, ignore_index=True)
```

## Data Quality Considerations

### Census Data
- **Updates**: ACS 5-year estimates lag 1-2 years
- **Margins of Error**: All estimates include MOEs
- **Coverage**: Not all geographies for all variables

### FRED Data
- **Revisions**: Many series are revised retroactively
- **Seasonality**: Choose seasonally adjusted series when appropriate
- **Frequency**: Check if daily, weekly, monthly, quarterly, annual

### CDC Data
- **Suppression**: Small cell sizes suppressed for privacy
- **Sampling**: BRFSS uses complex survey design (need weights)
- **Timeliness**: Can lag 1-2 years

## Setting Up API Keys

### Step 1: Create `config/apikeys` File

```bash
cd krl-tutorials
touch config/apikeys
```

### Step 2: Add Your Keys

Edit `config/apikeys`:
```
CENSUS_API_KEY=your_census_key_here
FRED_API_KEY=your_fred_key_here
BLS_API_KEY=your_bls_key_here
```

### Step 3: Load in Notebooks

```python
import os
from pathlib import Path

# Load API keys
config_path = Path('../../config/apikeys')
if config_path.exists():
    with open(config_path) as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
```

## Data Storage Best Practices

### Directory Structure
```
data/
├── raw/              # Original downloaded data
│   ├── census/
│   ├── fred/
│   └── cdc/
├── interim/          # Partially processed
│   └── cleaned/
└── processed/        # Final analysis-ready
    └── merged/
```

### Caching Data

```python
import os
import pandas as pd
from pathlib import Path

def get_cached_data(cache_path, fetch_function, *args, **kwargs):
    """Fetch data with caching."""
    if os.path.exists(cache_path):
        print(f"Loading from cache: {cache_path}")
        return pd.read_csv(cache_path)
    else:
        print(f"Fetching fresh data...")
        data = fetch_function(*args, **kwargs)
        data.to_csv(cache_path, index=False)
        return data

# Usage
df = get_cached_data(
    'data/raw/census/median_income_2021.csv',
    fetch_census_data,
    year=2021,
    variables=['B19013_001E']
)
```

## Rate Limiting Best Practices

```python
import time
from functools import wraps

def rate_limit(calls=1, period=1):
    """Decorator to rate limit API calls."""
    def decorator(func):
        last_called = [0.0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = period - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

@rate_limit(calls=1, period=1)  # 1 call per second
def fetch_data(series_id):
    return fred.get_series(series_id)
```

## Additional Data Sources

### Environmental Data
- **EPA**: Air quality, water quality, toxics
- **NOAA**: Climate, weather, oceanographic

### Crime & Justice
- **FBI UCR**: Uniform Crime Reporting
- **BJS**: Bureau of Justice Statistics

### International
- **UN Data**: Global development indicators
- **IMF**: International financial statistics

### Academic
- **IPUMS**: Integrated census microdata
- **NBER**: Economic research datasets

## Troubleshooting

### "API key invalid"
- Check key is correctly entered in `config/apikeys`
- Verify key is active (may need to re-register)
- Check API-specific requirements

### "Rate limit exceeded"
- Add delays between requests
- Use caching to avoid repeat calls
- Upgrade to higher tier (if available)

### "Data not available for period"
- Check data availability documentation
- Try different date ranges
- Verify geographic coverage

## Next Steps

- **[Quick Start Guide](Quick-Start-Guide)** - Apply these data sources
- **[Code Examples](Code-Examples)** - Data fetching patterns
- **[Tutorial Catalog](Tutorial-Catalog)** - See which tutorials use which sources

---

**Last Updated**: October 2025
