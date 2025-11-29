# KRL Analytics Suite - Release Notes

## Version 2.0.0 - "Khipu" Release

**Release Date**: November 30, 2025

> Named after the Incan recording device, this release weaves together spatial analysis, 
> causal inference, and data connectivity into a unified analytics framework.

---

## 🎯 Highlights

### Multi-Unit Synthetic Control Method
- Estimate treatment effects for **multiple treated units simultaneously**
- Hierarchical SCM for nested data structures (region → state → county)
- Cross-validated weight selection with K-fold CV
- Uncertainty quantification: bootstrap, placebo, conformal inference

### Parallel GWR
- **Dask-based parallelization** for multi-core CPU (4-8x speedup)
- **GPU acceleration** via CuPy for 10-50x performance gains
- Adaptive and fixed bandwidth with 6 kernel options
- Memory-efficient chunked processing for 100k+ observations

### Production Dashboard Deployment
- Multi-cloud support: AWS, GCP, Azure, Kubernetes, Docker
- SSL/TLS configuration with Let's Encrypt integration
- OAuth2/OIDC/JWT authentication
- Prometheus metrics and health check endpoints
- Auto-scaling with HPA configuration

### External Validations
- **Abadie et al. (2010)**: California Prop 99 SCM replication
- **Card & Krueger (1994)**: Minimum wage DiD replication
- Validation notebooks with comparison to published results

---

## 📦 Package Updates

### krl-geospatial-tools v2.0.0
- ✨ NEW: `ParallelGWR` class with Dask/GPU backends
- ✨ NEW: `SpatialIndex` with R-tree acceleration
- ✨ NEW: `RTreeQueenWeights`, `RTreeKNNWeights`, `RTreeDistanceBandWeights`
- 🚀 IMPROVED: Spatial weight construction 10x faster
- 🐛 FIXED: Edge case in adaptive bandwidth selection

### krl-model-zoo v2.0.0
- ✨ NEW: `MultiUnitSCM` for multiple treated units
- ✨ NEW: `HierarchicalSCM` for nested structures
- ✨ NEW: `AggregationType` enum (average, median, weighted)
- 🚀 IMPROVED: SCM optimization convergence
- 📚 DOCS: Comprehensive docstrings with examples

### krl-data-connectors v2.0.0
- ✨ NEW: `EJScreenConnector` for EPA environmental justice data
- ✨ NEW: `AirQualityConnector` for EPA AQS data
- ✨ NEW: `WaterQualityConnector` for EPA WQP data
- ✨ NEW: `NOAAClimateConnector` for climate data
- ✨ NEW: `SuperfundConnector` for NPL sites
- 🚀 IMPROVED: Rate limiting with exponential backoff
- 🐛 FIXED: Census API pagination handling

### krl-dashboard v2.0.0
- ✨ NEW: `DeploymentConfig` for production setup
- ✨ NEW: `DeploymentGenerator` for Docker/K8s/AWS
- ✨ NEW: `SSLConfig`, `AuthConfig`, `MonitoringConfig`
- ✨ NEW: CLI with `krl-dashboard run|deploy|status`
- 🚀 IMPROVED: Streamlit 1.28+ compatibility
- 📚 DOCS: Deployment guides for all major clouds

---

## 🔧 Breaking Changes

### krl-geospatial-tools
- `GeographicallyWeightedRegression` now returns `RegressionResult` instead of dict
- Spatial weights classes moved from `krl_geospatial.weights` to `krl_geospatial.indexing`

### krl-model-zoo
- `SyntheticControlMethod.fit()` parameter `treatment_time` renamed to `treatment_period`
- `SyntheticControlResult.effect` renamed to `treatment_effect`

### krl-data-connectors
- All connectors now require explicit API keys (no more defaults)
- `FREDConnector.get_data()` renamed to `get_series()`

---

## 📈 Performance Improvements

| Component | v1.x | v2.0 | Improvement |
|-----------|------|------|-------------|
| Spatial Index Build (10k) | 2.1s | 0.2s | **10x faster** |
| Queen Weights (5k) | 4.5s | 0.4s | **11x faster** |
| GWR Fit (2k obs) | 45s | 6s | **7.5x faster** |
| SCM Fit (50 units) | 0.8s | 0.3s | **2.7x faster** |

---

## 📚 Documentation

- **API Reference**: Comprehensive documentation for all public APIs
- **Quick Start Guide**: Get running in 5 minutes
- **Video Scripts**: Tutorial outlines for 5 video series
- **Benchmark Suite**: Automated performance testing

---

## 🔬 Validation Studies

### Abadie et al. (2010) Replication
- California Proposition 99 tobacco control study
- SCM weights match published (Utah, Nevada, Montana, Colorado, Connecticut)
- Treatment effect: ~20 packs/capita reduction (matches paper)
- Pre-treatment RMSPE: < 5 (excellent fit)

### Card & Krueger (1994) Replication
- New Jersey minimum wage natural experiment
- DiD effect: +2.75 FTE (published: +2.76)
- Confirms no negative employment effect

---

## 🛠 Installation

```bash
# Stable release
pip install krl-geospatial-tools krl-model-zoo krl-data-connectors krl-dashboard

# With all extras
pip install krl-geospatial-tools[all] krl-model-zoo[all]

# Development
pip install krl-analytics-suite[dev]
```

---

## 🙏 Acknowledgments

- Abadie, Diamond, & Hainmueller for Synthetic Control Method
- Card & Krueger for natural experiment methodology
- Fotheringham, Brunsdon, & Charlton for GWR foundations
- The Dask and CuPy communities for parallel computing tools
- EPA for EJSCREEN and environmental data APIs

---

## 📋 Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for complete commit history.

---

## 🔮 Roadmap

### v2.1.0 (Q1 2026)
- Bayesian SCM with uncertainty quantification
- Spatial DiD with spillover effects
- Real-time dashboard streaming

### v2.2.0 (Q2 2026)
- Causal discovery algorithms
- Network treatment effects
- AutoML for spatial models

---

*© 2025 KR-Labs. Apache-2.0 License.*
