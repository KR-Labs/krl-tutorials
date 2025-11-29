# KRL Analytics Suite - Quick Start Guide

> Get up and running with KRL in 5 minutes
> Version: 2.0.0

---

## Installation

```bash
# Core packages
pip install krl-geospatial-tools krl-model-zoo krl-data-connectors krl-dashboard

# Optional: GPU support
pip install cupy-cuda12x  # For CUDA 12.x

# Optional: Parallel processing
pip install dask[complete] distributed
```

## Your First Analysis

### 1. Spatial Analysis with GWR

```python
import numpy as np
import geopandas as gpd
from krl_geospatial.econometrics import ParallelGWR

# Load your spatial data
gdf = gpd.read_file("your_data.geojson")

# Extract coordinates and variables
coords = np.column_stack([
    gdf.geometry.centroid.x,
    gdf.geometry.centroid.y
])
y = gdf['outcome'].values
X = gdf[['predictor1', 'predictor2']].values

# Fit Parallel GWR
model = ParallelGWR(backend='dask', kernel='gaussian')
result = model.fit(y, X, coords)

# View results
print(f"Global R²: {result.r_squared:.4f}")
print(f"Bandwidth: {result.bandwidth:.2f}")

# Map local coefficients
gdf['local_beta1'] = result.local_coefficients[:, 1]
gdf.plot(column='local_beta1', cmap='RdYlBu')
```

### 2. Causal Impact with Synthetic Control

```python
import pandas as pd
from krl_models.causal import SyntheticControlMethod

# Panel data: rows=time, columns=units
Y = pd.read_csv("panel_data.csv", index_col=0).values

# Fit SCM
scm = SyntheticControlMethod()
result = scm.fit(
    outcome_matrix=Y,
    treated_unit=0,           # California
    treatment_period=19,      # 1989 (Prop 99)
)

# Results
print(f"Treatment Effect: {result.treatment_effect:.2f}")
print(f"Donor Weights: {result.weights}")
```

### 3. Environmental Justice Data

```python
from krl_data_connectors.environment import EJScreenConnector

# Initialize connector
ej = EJScreenConnector()

# Query by location
data = ej.get_ejscreen_data(
    latitude=34.0522,
    longitude=-118.2437,
    buffer_miles=1.0,
)

# Access indicators
print(f"PM2.5: {data.pm25}")
print(f"Cancer Risk: {data.cancer_risk}")
print(f"Low Income %: {data.low_income_pct}")
```

### 4. Launch Dashboard

```python
from krl_dashboard import create_production_config, DeploymentGenerator

# Create config
config = create_production_config(
    name="my-dashboard",
    ssl_mode="disabled",  # Use 'lets_encrypt' in production
    auth_provider="none",
)

# Generate Docker files
generator = DeploymentGenerator(config)
generator.generate_all("deploy/")

# Run locally
# cd deploy && docker-compose up
```

---

## Key Concepts

### Spatial Weights

```python
from krl_geospatial.indexing import RTreeQueenWeights, RTreeKNNWeights

# Queen contiguity (shared edge or vertex)
W_queen = RTreeQueenWeights(gdf).to_sparse()

# K-nearest neighbors
W_knn = RTreeKNNWeights(gdf, k=5).to_sparse()
```

### Bandwidth Selection

```python
# Automatic selection
model = ParallelGWR()
result = model.fit(y, X, coords, bandwidth_method='aicc')

# Fixed bandwidth
result = model.fit(y, X, coords, bandwidth=50.0)

# Adaptive (k-NN)
model = ParallelGWR(adaptive=True)
result = model.fit(y, X, coords, bandwidth=100)  # 100 nearest neighbors
```

### Uncertainty Quantification

```python
from krl_models.causal import MultiUnitSCM

mscm = MultiUnitSCM()
result = mscm.fit(Y, treated_units, treatment_periods)

# Bootstrap confidence intervals
ci = result.bootstrap_ci(n_bootstrap=1000, alpha=0.05)

# Placebo tests
placebo = result.placebo_test(n_permutations=500)
print(f"p-value: {placebo.p_value:.4f}")
```

---

## Next Steps

1. **Explore Notebooks**: See `/notebooks/` for 25+ worked examples
2. **API Reference**: Full documentation in `docs/API_REFERENCE.md`
3. **Validation Studies**: Replications in `notebooks/validation/`

## Support

- GitHub Issues: [KR-Labs/krl-analytics](https://github.com/KR-Labs)
- Documentation: [docs.krlabs.dev](https://docs.krlabs.dev)
- Email: support@krlabs.dev

---

*© 2025 KR-Labs. Apache-2.0 License.*
