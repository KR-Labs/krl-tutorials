# Demo Mode

The Khipu showcase notebooks operate in **Demo Mode** by default. This ensures that all notebooks are safe to run anywhere without requiring API credentials or accessing real data.

## How Demo Mode Works

When `DEMO_MODE=true` (the default), the package:

1. **Uses synthetic data** instead of calling real APIs
2. **Requires no credentials** - no API keys needed
3. **Produces reproducible results** via fixed random seeds
4. **Mirrors production schemas** - data structures match real APIs

## Setting Demo Mode

Demo mode is controlled by the `DEMO_MODE` environment variable:

```bash
# Enable demo mode (default)
export DEMO_MODE=true

# Disable demo mode (production)
export DEMO_MODE=false
```

Or in Python:

```python
import os
os.environ['DEMO_MODE'] = 'true'

from khipu_demo import DEMO_MODE
print(f"Demo mode: {DEMO_MODE}")  # True
```

## Demo Mode Detection

The package provides utilities for checking demo mode:

```python
from khipu_demo import is_demo_mode, DEMO_MODE

if is_demo_mode():
    print("Running with synthetic data")
else:
    print("Running with production data")
```

## Mock Clients

In demo mode, API calls are handled by mock clients that return synthetic data:

```python
from khipu_demo.clients import get_demo_clients

clients = get_demo_clients(seed=42)

# These return synthetic DataFrames
unemployment = clients['labor'].get_unemployment_data()
gdp = clients['economic'].get_gdp_by_state()
housing = clients['housing'].get_zhvi_by_metro()
```

## Production Mode

When demo mode is disabled, you should use the full `krl-data-connectors` package with authenticated clients:

```python
# Production code (not included in demo package)
from krl_data_connectors import BLSConnector, ZillowConnector

bls = BLSConnector(api_key=os.environ['BLS_API_KEY'])
zillow = ZillowConnector(api_key=os.environ['ZILLOW_API_KEY'])

# Fetch real data
unemployment = bls.get_unemployment_rate(geography='state')
housing = zillow.get_zhvi(geography='metro')
```

## Why Demo Mode?

Demo mode serves several important purposes:

| Purpose | Benefit |
|---------|---------|
| **Security** | No secrets or credentials in notebooks |
| **Reproducibility** | Fixed seeds ensure consistent results |
| **Portability** | Runs anywhere without API access |
| **Education** | Focus on analysis, not API management |
| **CI/CD** | Notebooks can be tested automatically |

## Data Quality

Synthetic data in demo mode is designed to:

- Match the schema of production APIs
- Exhibit realistic statistical properties
- Include edge cases for robust testing
- Support all analysis workflows

The data is **not** real and should not be used for actual policy decisions.
