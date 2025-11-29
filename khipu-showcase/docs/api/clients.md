# Clients Module API

The `khipu_demo.clients` module provides mock API clients for generating synthetic data.

## Overview

All mock clients:

- Accept a `seed` parameter for reproducibility
- Return pandas DataFrames
- Mirror the schema of real production APIs
- Require no authentication

## get_demo_clients

Factory function to get all demo clients.

```python
from khipu_demo.clients import get_demo_clients

clients = get_demo_clients(seed=42)

# Available clients:
# - clients['labor']        -> BLSMockClient
# - clients['economic']     -> BEAMockClient
# - clients['census']       -> CensusMockClient
# - clients['environmental'] -> EPAMockClient
# - clients['health']       -> CDCMockClient
# - clients['housing']      -> ZillowMockClient
```

---

## BLSMockClient

Mock client for Bureau of Labor Statistics data.

```python
from khipu_demo.clients import BLSMockClient

client = BLSMockClient(seed=42)
```

### Methods

#### `get_unemployment_data()`

Get unemployment rates by state.

```python
df = client.get_unemployment_data()
```

**Columns:** state, unemployment_rate, labor_force, employed, unemployed

#### `get_wages_by_metro()`

Get median wages by metropolitan area.

```python
df = client.get_wages_by_metro()
```

**Columns:** metro, median_wage, mean_wage, employment

#### `get_employment_by_metro()`

Get employment statistics by metro.

```python
df = client.get_employment_by_metro()
```

---

## BEAMockClient

Mock client for Bureau of Economic Analysis data.

```python
from khipu_demo.clients import BEAMockClient

client = BEAMockClient(seed=42)
```

### Methods

#### `get_gdp_by_state()`

Get GDP by state.

```python
df = client.get_gdp_by_state()
```

**Columns:** state, gdp, gdp_per_capita, population

#### `get_gdp_by_metro()`

Get GDP by metropolitan area.

```python
df = client.get_gdp_by_metro()
```

**Columns:** metro, gdp, gdp_growth_rate

---

## CensusMockClient

Mock client for Census Bureau data.

```python
from khipu_demo.clients import CensusMockClient

client = CensusMockClient(seed=42)
```

### Methods

#### `get_population_data()`

Get population by state.

```python
df = client.get_population_data()
```

**Columns:** state, population, pop_density, median_age

#### `get_demographics()`

Get demographic breakdowns.

```python
df = client.get_demographics()
```

---

## EPAMockClient

Mock client for EPA environmental data.

```python
from khipu_demo.clients import EPAMockClient

client = EPAMockClient(seed=42)
```

### Methods

#### `get_ej_indices()`

Get Environmental Justice indices by tract.

```python
df = client.get_ej_indices()
```

**Columns:** tract_id, ej_index, pm25, ozone, lead_paint, proximity_to_rsei

#### `get_air_quality()`

Get air quality data.

```python
df = client.get_air_quality()
```

---

## CDCMockClient

Mock client for CDC health data.

```python
from khipu_demo.clients import CDCMockClient

client = CDCMockClient(seed=42)
```

### Methods

#### `get_health_outcomes()`

Get health outcomes by county.

```python
df = client.get_health_outcomes()
```

**Columns:** county, asthma_rate, diabetes_rate, obesity_rate, life_expectancy

---

## ZillowMockClient

Mock client for Zillow housing data.

```python
from khipu_demo.clients import ZillowMockClient

client = ZillowMockClient(seed=42)
```

### Methods

#### `get_zhvi_by_metro()`

Get Zillow Home Value Index by metro.

```python
df = client.get_zhvi_by_metro()
```

**Columns:** metro, zhvi, zhvi_change_yoy, for_sale_inventory

#### `get_housing_index()`

Get housing market indices.

```python
df = client.get_housing_index()
```

---

## Example Usage

```python
from khipu_demo.clients import get_demo_clients
import pandas as pd

# Get all clients with reproducible seed
clients = get_demo_clients(seed=42)

# Fetch data from multiple sources
unemployment = clients['labor'].get_unemployment_data()
gdp = clients['economic'].get_gdp_by_state()
housing = clients['housing'].get_zhvi_by_metro()

# Merge datasets
merged = pd.merge(
    unemployment,
    gdp,
    on='state',
    how='inner'
)

print(f"Combined dataset: {len(merged)} rows")
```
