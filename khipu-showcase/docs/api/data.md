# Data Module API

The `khipu_demo.data` module provides utilities for loading and generating synthetic datasets.

## DataProvenance

Track data provenance for reproducibility and auditing.

```python
from khipu_demo.data import DataProvenance
from datetime import datetime

provenance = DataProvenance(
    source="Bureau of Labor Statistics",
    license="Public Domain",
    ingestion_timestamp=datetime.now(),
    transformation_steps=["Downloaded", "Cleaned", "Aggregated"],
    dataset_hash="abc123...",
    citation="BLS, 2024",
    url="https://www.bls.gov/",
)
```

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `source` | str | Data source name |
| `license` | str | Data license |
| `ingestion_timestamp` | datetime | When data was loaded |
| `transformation_steps` | List[str] | Processing steps applied |
| `dataset_hash` | str | SHA-256 hash of dataset |
| `version` | str | Dataset version (default: "1.0.0") |
| `citation` | str | How to cite the data |
| `url` | str | Source URL |
| `notes` | str | Additional notes |

### Methods

#### `to_markdown() -> str`

Generate a markdown table for notebook display.

```python
from IPython.display import Markdown
Markdown(provenance.to_markdown())
```

#### `to_dict() -> Dict`

Convert to dictionary for JSON serialization.

```python
import json
print(json.dumps(provenance.to_dict(), indent=2))
```

---

## compute_dataset_hash

Compute SHA-256 hash of a DataFrame.

```python
from khipu_demo.data import compute_dataset_hash
import pandas as pd

df = pd.DataFrame({"a": [1, 2, 3]})
hash_val = compute_dataset_hash(df)
print(hash_val)  # 64-character hex string
```

---

## SyntheticDataGenerator

Generator for reproducible synthetic datasets.

```python
from khipu_demo.data import SyntheticDataGenerator

generator = SyntheticDataGenerator(seed=42)
```

### Methods

#### `generate_housing_wage_panel()`

Generate panel data of housing values and wages by metro.

```python
df, provenance = generator.generate_housing_wage_panel(
    n_metros=20,
    start_year=2015,
    end_year=2024,
    frequency="annual",  # or "monthly"
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `n_metros` | int | 20 | Number of metro areas |
| `start_year` | int | 2015 | Start year |
| `end_year` | int | 2024 | End year |
| `frequency` | str | "annual" | "annual" or "monthly" |

**Returns:** Tuple of (DataFrame, DataProvenance)

**Columns:**

- `metro`: Metropolitan area name
- `period`: Year or date
- `median_home_value`: Median home value in USD
- `median_wage`: Median annual wage in USD
- `affordability_ratio`: Home value / wage
- `housing_cumul_growth_pct`: Cumulative housing growth
- `wage_cumul_growth_pct`: Cumulative wage growth
- `divergence_pct`: Housing growth - wage growth

#### `generate_gentrification_signals()`

Generate tract-level gentrification indicators.

```python
df, provenance = generator.generate_gentrification_signals(
    n_tracts=100,
    n_periods=24,
)
```

**Columns:**

- `tract_id`: Census tract ID
- `period`: Date
- `median_rent`: Median rent
- `building_permits`: Monthly building permits
- `business_churn_rate`: Business turnover rate
- `new_restaurants`: New restaurant openings
- `gentrification_stage`: none/early/active/late
- `gentrification_score`: Numeric score (0-100)

---

## generate_synthetic_data

Convenience function for generating datasets.

```python
from khipu_demo.data import generate_synthetic_data

df, provenance = generate_synthetic_data(
    dataset_type="housing_wage",  # or "gentrification"
    seed=42,
    n_metros=10,
)
```
