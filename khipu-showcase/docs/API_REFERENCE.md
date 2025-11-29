# KRL Analytics Suite - API Reference

> Comprehensive API documentation for the KRL Analytics Suite
> Version: 2.0.0 | Last Updated: November 30, 2025

---

## Table of Contents

1. [KRL Geospatial Tools](#krl-geospatial-tools)
2. [KRL Model Zoo](#krl-model-zoo)
3. [KRL Data Connectors](#krl-data-connectors)
4. [KRL Dashboard](#krl-dashboard)
5. [KRL Causal Policy Toolkit](#krl-causal-policy-toolkit)
6. [KRL Network Analysis](#krl-network-analysis)

---

# KRL Geospatial Tools

## Spatial Indexing

### `SpatialIndex`

R-tree spatial index for efficient spatial queries.

```python
from krl_geospatial.indexing import SpatialIndex

# Create index from GeoDataFrame
index = SpatialIndex()
index.build_from_geodataframe(gdf, leaf_capacity=100)

# Query methods
neighbors = index.query_nearest(point, k=5)
intersecting = index.query_intersects(bbox)
within = index.query_within(polygon)
```

**Methods:**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `build_from_geodataframe()` | `gdf: GeoDataFrame, leaf_capacity: int=100` | `None` | Build index from geometries |
| `query_nearest()` | `geometry, k: int=1` | `List[int]` | Find k nearest neighbors |
| `query_intersects()` | `geometry` | `List[int]` | Find intersecting geometries |
| `query_within()` | `geometry` | `List[int]` | Find geometries within bounds |
| `save()` | `path: str` | `None` | Serialize index to file |
| `load()` | `path: str` | `SpatialIndex` | Load index from file |

### `RTreeQueenWeights`

R-tree accelerated Queen contiguity weights.

```python
from krl_geospatial.indexing import RTreeQueenWeights

weights = RTreeQueenWeights(gdf)
W = weights.to_sparse()
```

---

## Econometrics

### `ParallelGWR`

High-performance Geographically Weighted Regression.

```python
from krl_geospatial.econometrics import ParallelGWR

# Initialize with parallel backend
pgwr = ParallelGWR(
    kernel='gaussian',      # 'gaussian', 'bisquare', 'tricube'
    adaptive=False,         # True for k-NN bandwidth
    backend='dask',         # 'sequential', 'dask', 'joblib', 'gpu'
    n_workers=4,
    chunk_size=1000,
)

# Fit model
result = pgwr.fit(
    y=outcome,
    X=predictors,
    coords=coordinates,
    bandwidth=None,         # Auto-select if None
    bandwidth_method='aicc' # 'aic', 'aicc', 'bic', 'cv'
)

# Access results
print(result.r_squared)
print(result.local_coefficients)
print(result.bandwidth)
```

**ParallelGWRResult Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `coefficients` | `np.ndarray` | Global mean coefficients |
| `local_coefficients` | `np.ndarray` | Location-specific coefficients (n × k) |
| `local_std_errors` | `np.ndarray` | Location-specific standard errors |
| `local_t_stats` | `np.ndarray` | Location-specific t-statistics |
| `local_r_squared` | `np.ndarray` | Location-specific R² |
| `r_squared` | `float` | Global R² |
| `bandwidth` | `float` | Selected/used bandwidth |
| `execution_time` | `float` | Fit time in seconds |

### `GeographicallyWeightedRegression`

Standard GWR implementation (sequential).

```python
from krl_geospatial.econometrics import GeographicallyWeightedRegression

gwr = GeographicallyWeightedRegression(kernel='gaussian', adaptive=False)
result = gwr.fit(y, X, coords, bandwidth=0.5)
```

### `SpatialLag` / `SpatialError`

Spatial regression models.

```python
from krl_geospatial.econometrics import SpatialLag, SpatialError

# Spatial Lag Model: y = ρWy + Xβ + ε
lag_model = SpatialLag()
result = lag_model.fit(y, X, W)

# Spatial Error Model: y = Xβ + u, where u = λWu + ε
error_model = SpatialError()
result = error_model.fit(y, X, W)
```

---

## Autocorrelation Tests

### Global Tests

```python
from krl_geospatial.econometrics import morans_i, gearys_c

# Moran's I
I, p_value = morans_i(y, W)

# Geary's C
C, p_value = gearys_c(y, W)
```

### Local Tests

```python
from krl_geospatial.econometrics import local_morans_i, getis_ord_gi_star

# Local Moran's I (LISA)
lisa = local_morans_i(y, W)

# Getis-Ord Gi*
gi_star = getis_ord_gi_star(y, W)
```

---

# KRL Model Zoo

## Causal Inference

### `SyntheticControlMethod`

Synthetic Control Method for causal inference.

```python
from krl_models.causal import SyntheticControlMethod

scm = SyntheticControlMethod()
result = scm.fit(
    outcome_matrix=Y,           # (T × N) panel data
    treated_unit=0,             # Index of treated unit
    treatment_period=50,        # Time of intervention
    covariates=X,               # Optional predictors
)

# Get results
print(result.weights)           # Donor weights
print(result.treatment_effect)  # Post-treatment ATT
print(result.pre_treatment_fit) # RMSPE
```

### `MultiUnitSCM`

Multi-unit Synthetic Control for multiple treated units.

```python
from krl_models.causal import MultiUnitSCM, AggregationType

mscm = MultiUnitSCM(
    aggregation=AggregationType.WEIGHTED_AVERAGE,
    cross_validation=True,
    n_folds=5,
)

result = mscm.fit(
    outcome_matrix=Y,
    treated_units=[0, 3, 7],
    treatment_periods=[50, 52, 48],
    covariates=X,
)

# Access unit-specific and aggregate effects
print(result.unit_effects)      # Dict of per-unit effects
print(result.aggregate_effect)  # Aggregated ATT
print(result.aggregate_se)      # Aggregated standard error
```

### `HierarchicalSCM`

Hierarchical Synthetic Control for nested structures.

```python
from krl_models.causal import HierarchicalSCM

hscm = HierarchicalSCM(levels=['region', 'state', 'county'])
result = hscm.fit(
    outcome_matrix=Y,
    treated_units=treated,
    treatment_periods=periods,
    hierarchy=hierarchy_df,
)
```

### `DifferenceInDifferences`

Difference-in-Differences estimation.

```python
from krl_models.causal import DifferenceInDifferences

did = DifferenceInDifferences()
result = did.fit(
    y=outcome,
    treatment=treatment_indicator,
    post=post_period_indicator,
    covariates=X,
)

print(result.treatment_effect)  # ATT
print(result.std_error)
print(result.conf_int)          # 95% CI
print(result.p_value)
```

### `RegressionDiscontinuity`

Regression Discontinuity Design.

```python
from krl_models.causal import RegressionDiscontinuity

rdd = RegressionDiscontinuity(
    kernel='triangular',
    bandwidth='optimal',  # or fixed value
)

result = rdd.fit(
    y=outcome,
    running_variable=score,
    cutoff=0.5,
)
```

### `CausalForest`

Heterogeneous treatment effects via causal forests.

```python
from krl_models.causal import CausalForest

cf = CausalForest(
    n_estimators=1000,
    min_samples_leaf=5,
    honesty=True,
)

cf.fit(X, treatment, y)
cate = cf.predict(X_new)  # Conditional Average Treatment Effects
```

---

## Time Series

### `SARIMA`

Seasonal ARIMA forecasting.

```python
from krl_models.econometric import SARIMA

model = SARIMA(order=(1,1,1), seasonal_order=(1,1,1,12))
model.fit(y)
forecast = model.predict(steps=24)
```

### `Prophet`

Facebook Prophet wrapper.

```python
from krl_models.econometric import Prophet

model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
model.fit(df)  # DataFrame with 'ds' and 'y' columns
forecast = model.predict(periods=365)
```

---

## Volatility Models

### `GARCH` / `EGARCH` / `GJR_GARCH`

```python
from krl_models.volatility import GARCH, EGARCH, GJR_GARCH

# Standard GARCH(1,1)
garch = GARCH(p=1, q=1)
garch.fit(returns)
volatility = garch.conditional_volatility

# EGARCH for leverage effects
egarch = EGARCH(p=1, q=1)
egarch.fit(returns)

# GJR-GARCH for asymmetric volatility
gjr = GJR_GARCH(p=1, o=1, q=1)
gjr.fit(returns)
```

---

# KRL Data Connectors

## Environment Module

### `EJScreenConnector`

EPA EJSCREEN environmental justice data.

```python
from krl_data_connectors.environment import EJScreenConnector

connector = EJScreenConnector(api_key="your_key")

# Query by coordinates
data = connector.get_ejscreen_data(
    latitude=40.7128,
    longitude=-74.0060,
    buffer_miles=1.0,
)

# Query by FIPS code
data = connector.get_block_group_data(fips="360610001001")

# Get indicators
pm25 = data.get_indicator(EJIndicator.PM25)
ej_index = data.get_ej_index(EJIndex.CANCER_RISK)
```

**EJIndicator Enum:**

| Indicator | Description |
|-----------|-------------|
| `PM25` | Particulate Matter 2.5 |
| `OZONE` | Ozone concentration |
| `DIESEL_PM` | Diesel particulate matter |
| `CANCER_RISK` | Air toxics cancer risk |
| `RESP_HAZARD` | Respiratory hazard index |
| `TRAFFIC` | Traffic proximity |
| `LEAD_PAINT` | Lead paint indicator |
| `SUPERFUND` | Proximity to Superfund sites |
| `RMP` | Proximity to RMP facilities |
| `TSDF` | Proximity to hazardous waste |
| `WASTEWATER` | Wastewater discharge |
| `UST` | Underground storage tanks |

### `AirQualityConnector`

EPA Air Quality System data.

```python
from krl_data_connectors.environment import AirQualityConnector

aqs = AirQualityConnector(email="you@email.com", api_key="key")
data = aqs.get_daily_data(
    parameter="88101",  # PM2.5
    state="06",
    county="037",
    start_date="2024-01-01",
    end_date="2024-12-31",
)
```

### `NOAAClimateConnector`

NOAA Climate Data Online.

```python
from krl_data_connectors.environment import NOAAClimateConnector

noaa = NOAAClimateConnector(token="your_token")
data = noaa.get_daily_summaries(
    station_id="GHCND:USW00094728",
    start_date="2024-01-01",
    end_date="2024-12-31",
    datatypes=["TMAX", "TMIN", "PRCP"],
)
```

---

## Economic Data

### `FREDConnector`

Federal Reserve Economic Data.

```python
from krl_data_connectors.economic import FREDConnector

fred = FREDConnector(api_key="your_key")

# Single series
gdp = fred.get_series("GDP")

# Multiple series
data = fred.get_multiple_series(["GDP", "UNRATE", "CPIAUCSL"])

# Search
results = fred.search("unemployment rate")
```

### `BLSConnector`

Bureau of Labor Statistics data.

```python
from krl_data_connectors.economic import BLSConnector

bls = BLSConnector(api_key="your_key")
data = bls.get_series(
    series_ids=["LAUCN040010000000005"],
    start_year=2020,
    end_year=2024,
)
```

### `CensusConnector`

US Census Bureau data.

```python
from krl_data_connectors.economic import CensusConnector

census = CensusConnector(api_key="your_key")

# ACS 5-year estimates
data = census.get_acs5(
    year=2022,
    variables=["B01001_001E", "B19013_001E"],
    geography="tract",
    state="06",
    county="037",
)
```

---

# KRL Dashboard

## Configuration

### `DeploymentConfig`

Production deployment configuration.

```python
from krl_dashboard import (
    DeploymentConfig,
    SSLConfig,
    AuthConfig,
    MonitoringConfig,
    CloudProvider,
    SSLMode,
    AuthProvider,
)

config = DeploymentConfig(
    name="my-dashboard",
    environment="production",
    provider=CloudProvider.KUBERNETES,
    port=8501,
    workers=4,
    replicas=3,
    
    ssl=SSLConfig(
        mode=SSLMode.LETS_ENCRYPT,
        domain="dashboard.example.com",
        email="admin@example.com",
    ),
    
    auth=AuthConfig(
        provider=AuthProvider.OAUTH2,
        client_id="...",
        client_secret="...",
    ),
    
    monitoring=MonitoringConfig(
        enabled=True,
        metrics_enabled=True,
        health_check_enabled=True,
    ),
)
```

### `DeploymentGenerator`

Generate deployment artifacts.

```python
from krl_dashboard import DeploymentGenerator

generator = DeploymentGenerator(config)

# Generate all artifacts
generator.generate_all(output_dir="deploy/")

# Or individually
dockerfile = generator.generate_dockerfile()
k8s = generator.generate_kubernetes_manifests()
nginx = generator.generate_nginx_config()
cloudformation = generator.generate_aws_cloudformation()
```

---

## Data Pipeline

### `DataPipeline`

ETL pipeline for dashboard data.

```python
from krl_dashboard import DataPipeline, TransformStep

pipeline = DataPipeline(name="economic_indicators")

pipeline.add_source("fred", FREDDataSource(series=["GDP", "UNRATE"]))
pipeline.add_transform(TransformStep(
    name="normalize",
    func=lambda df: (df - df.mean()) / df.std()
))
pipeline.add_output("cache", MemoryCache(ttl=3600))

result = pipeline.run()
```

### `MemoryCache` / `DiskCache`

Caching layers.

```python
from krl_dashboard import MemoryCache, DiskCache, cached

# Memory cache with LRU
cache = MemoryCache(max_size=1000, ttl=3600)
cache.set("key", value)
value = cache.get("key")

# Disk cache
disk_cache = DiskCache(path="./cache", ttl=86400)

# Decorator
@cached(cache=cache, key_func=lambda x: f"data_{x}")
def fetch_data(id):
    return expensive_query(id)
```

---

# Quick Reference

## Import Patterns

```python
# Geospatial
from krl_geospatial.econometrics import ParallelGWR, SpatialLag, morans_i
from krl_geospatial.indexing import SpatialIndex, RTreeQueenWeights

# Models
from krl_models.causal import (
    SyntheticControlMethod,
    MultiUnitSCM,
    DifferenceInDifferences,
    CausalForest,
)

# Data
from krl_data_connectors.environment import EJScreenConnector
from krl_data_connectors.economic import FREDConnector

# Dashboard
from krl_dashboard import DeploymentConfig, DataPipeline
```

## Common Workflows

### Causal Impact Analysis

```python
# 1. Load data
data = pd.read_csv("panel_data.csv")

# 2. Fit SCM
scm = SyntheticControlMethod()
result = scm.fit(Y, treated_unit=0, treatment_period=50)

# 3. Validate with placebo
placebo = scm.placebo_test(n_permutations=1000)

# 4. Report
print(f"ATT: {result.treatment_effect:.2f}")
print(f"p-value: {placebo.p_value:.4f}")
```

### Spatial Analysis Pipeline

```python
# 1. Build spatial index
index = SpatialIndex()
index.build_from_geodataframe(gdf)

# 2. Create weights
weights = RTreeQueenWeights(gdf)
W = weights.to_sparse()

# 3. Test for autocorrelation
I, p = morans_i(gdf['outcome'], W)

# 4. Fit spatial model
if p < 0.05:
    model = ParallelGWR(backend='dask')
    result = model.fit(y, X, coords)
```

---

*© 2025 KR-Labs. All rights reserved.*
