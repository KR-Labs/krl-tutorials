# Strategic Development Plan: Khipu Showcase Portfolio
## Addressing Gaps & Weaknesses from A+ (98/100) Audit

**Plan Date:** November 29, 2025  
**Target Grade:** 100/100  
**Timeline:** 12 months (3 phases)  
**Owner:** KR-Labs Engineering

---

## Executive Summary

The audit identified **2 points** of improvement potential across three categories:
1. **Enterprise-tier algorithms** (1 pt): MultiUnitSCM, parallel GWR simulated
2. **Real-time infrastructure** (0.5 pt): Dashboard framework, not deployment  
3. **External validation** (0.5 pt): No published outcome comparisons

This plan addresses these gaps while also implementing the **immediate, near-term, and strategic** recommendations from the audit.

---

## Phase 1: Immediate Priorities (0-3 Months)

### 1.1 Rate Limiting & API Stability ✅ COMPLETED
**Status:** Implemented November 29, 2025

- [x] Token bucket algorithm for FRED (120 req/min)
- [x] Sliding window for BLS (50 req/10s burst, 500/day)
- [x] Daily quota tracking with persistence
- [x] Exponential backoff with jitter
- [x] Error threshold lockout for BEA (30 errors/min → 1hr)

**Location:** `krl-data-connectors/src/krl_data_connectors/core/rate_limiter.py`

---

### 1.2 Spatial Indexing Optimization
**Gap:** O(n²) spatial operations → O(n log n)  
**Notebooks Affected:** 17 (Spatial Causal Fusion), 13 (Regional Development)

#### Implementation Tasks

| Task | Priority | Effort | Owner |
|------|----------|--------|-------|
| Add R-tree spatial index to `krl-geospatial-tools` | HIGH | 3 days | TBD |
| Implement KD-tree fallback for point data | MEDIUM | 2 days | TBD |
| Update spatial weights matrix to use sparse representation | HIGH | 2 days | TBD |
| Benchmark before/after on 10K+ county dataset | HIGH | 1 day | TBD |

#### Code Location
```
krl-geospatial-tools/src/krl_geospatial/
├── indexing/
│   ├── __init__.py
│   ├── rtree_index.py      # NEW: R-tree implementation
│   ├── kdtree_index.py     # NEW: KD-tree for points
│   └── spatial_weights.py  # UPDATE: Sparse matrix support
```

#### Success Metrics
- [ ] 10x speedup on 10K observation spatial weights
- [ ] Memory reduction >50% via sparse matrices
- [ ] Unit tests for all indexing operations

---

### 1.3 EPA EJSCREEN Integration
**Gap:** Environmental burden data simulated  
**Notebook Affected:** 21 (Environmental Justice Scoring)

#### Implementation Tasks

| Task | Priority | Effort | Owner |
|------|----------|--------|-------|
| Create EPA EJSCREEN connector | HIGH | 5 days | TBD |
| Map EJSCREEN indicators to EJ scoring framework | MEDIUM | 2 days | TBD |
| Add demographic index crosswalks | MEDIUM | 2 days | TBD |
| Update NB21 to use real EPA data | HIGH | 1 day | TBD |

#### Data Fields to Integrate
- PM2.5 levels
- Ozone concentrations
- Diesel particulate matter
- Traffic proximity
- Superfund proximity
- Hazardous waste proximity
- Wastewater discharge
- Lead paint indicators

#### Code Location
```
krl-data-connectors/src/krl_data_connectors/
├── environmental/
│   ├── __init__.py
│   ├── ejscreen.py         # NEW: EPA EJSCREEN connector
│   └── air_quality.py      # NEW: AirNow API connector
```

---

### 1.4 Real-Time Dashboard MVP
**Gap:** Dashboard framework exists, not deployed  
**Notebook Affected:** 10 (Urban Resilience Dashboard)

#### Implementation Tasks

| Task | Priority | Effort | Owner |
|------|----------|--------|-------|
| Create Plotly Dash app skeleton | HIGH | 2 days | TBD |
| Implement resilience index visualization | MEDIUM | 3 days | TBD |
| Add data refresh mechanism (hourly) | MEDIUM | 2 days | TBD |
| Deploy to Render/Railway for demo | LOW | 1 day | TBD |

#### Architecture
```
khipu-showcase/
├── dashboard/
│   ├── app.py              # NEW: Main Dash application
│   ├── components/
│   │   ├── resilience_map.py
│   │   ├── indicator_cards.py
│   │   └── trend_charts.py
│   ├── data/
│   │   └── refresh.py      # Scheduled data updates
│   └── Dockerfile
```

---

### 1.5 External Validation Study
**Gap:** No published outcome comparisons  
**Impact:** 0.5 point improvement potential

#### Implementation Tasks

| Task | Priority | Effort | Owner |
|------|----------|--------|-------|
| Identify 3-5 published policy evaluations with public data | HIGH | 3 days | TBD |
| Replicate key findings using portfolio methods | HIGH | 5 days | TBD |
| Document comparison metrics (effect size, CI overlap) | MEDIUM | 2 days | TBD |
| Add validation notebook to portfolio | MEDIUM | 1 day | TBD |

#### Candidate Studies for Validation
1. **Card & Krueger (1994)** - Minimum wage RDD → Compare to NB15
2. **Abadie et al. (2010)** - California smoking SCM → Compare to NB14
3. **Chetty et al. (2016)** - Opportunity Atlas mobility → Compare to NB03
4. **Currie & Walker (2011)** - E-ZPass pollution health → Compare to NB21

---

## Phase 2: Near-Term Enhancements (3-6 Months)

### 2.1 Enterprise MultiUnitSCM with Conformal Inference
**Gap:** Staggered adoption synthetic control simulated  
**Notebook Affected:** 14 (Synthetic Control Policy Lab)

#### Implementation Tasks

| Task | Priority | Effort | Owner |
|------|----------|--------|-------|
| Implement Synthetic Difference-in-Differences (SDID) | HIGH | 5 days | TBD |
| Add conformal inference bands for uncertainty | HIGH | 4 days | TBD |
| Support staggered treatment timing | MEDIUM | 3 days | TBD |
| Add unit-specific effect estimation | MEDIUM | 3 days | TBD |

#### Technical Specifications
```python
class MultiUnitSCM:
    """
    Synthetic control for multiple treated units with staggered adoption.
    
    Implements:
    - Synthetic Difference-in-Differences (Arkhangelsky et al. 2021)
    - Conformal inference bands (Chernozhukov et al. 2021)
    - Unit-specific treatment effects with aggregation
    """
    
    def fit(self, Y, treatment_matrix, covariates=None):
        """
        Args:
            Y: (n_units, n_periods) outcome panel
            treatment_matrix: (n_units, n_periods) binary treatment indicator
            covariates: Optional (n_units, n_covariates) pre-treatment predictors
        """
        pass
    
    def get_unit_effects(self) -> pd.DataFrame:
        """Return unit-specific ATT with conformal intervals."""
        pass
    
    def aggregate_effect(self, weights='equal') -> Dict:
        """Aggregate effects across units."""
        pass
```

#### Code Location
```
krl-causal-policy-toolkit/src/krl_policy/
├── synthetic_control/
│   ├── __init__.py
│   ├── single_unit.py      # Existing
│   ├── multi_unit.py       # NEW: MultiUnitSCM
│   └── conformal.py        # NEW: Conformal inference
```

---

### 2.2 Parallel Geographically Weighted Regression
**Gap:** GWR remains O(n² × k)  
**Notebook Affected:** 17 (Spatial Causal Fusion)

#### Implementation Tasks

| Task | Priority | Effort | Owner |
|------|----------|--------|-------|
| Implement Dask-based parallel GWR | HIGH | 5 days | TBD |
| Add adaptive bandwidth selection (AICc) | MEDIUM | 3 days | TBD |
| Support GPU acceleration via CuPy (optional) | LOW | 3 days | TBD |
| Benchmark on 100K+ observations | MEDIUM | 2 days | TBD |

#### Architecture
```python
class ParallelGWR:
    """
    Geographically Weighted Regression with parallel execution.
    
    Scaling:
    - <10K obs: Single-threaded (direct NumPy)
    - 10K-100K obs: Dask multicore
    - >100K obs: Dask distributed cluster
    """
    
    def __init__(self, n_jobs=-1, backend='dask'):
        self.n_jobs = n_jobs
        self.backend = backend  # 'dask', 'ray', 'joblib'
    
    def fit(self, X, y, coords, bandwidth='adaptive'):
        """Fit GWR with spatial partitioning."""
        pass
    
    def predict(self, X_new, coords_new) -> np.ndarray:
        """Predict with local coefficients."""
        pass
```

---

### 2.3 NOAA Climate Hazard Integration
**Gap:** Climate hazard data simulated  
**Notebook Affected:** 05 (Climate Resilience Economics), 23 (Climate Adaptation)

#### Implementation Tasks

| Task | Priority | Effort | Owner |
|------|----------|--------|-------|
| Create NOAA NCEI connector | HIGH | 5 days | TBD |
| Integrate FEMA National Risk Index | HIGH | 3 days | TBD |
| Add First Street Foundation flood risk API | MEDIUM | 3 days | TBD |
| Map hazard types to notebook framework | MEDIUM | 2 days | TBD |

#### Data Sources
1. **NOAA NCEI** - Historical storm events, billion-dollar disasters
2. **FEMA NRI** - Expected annual loss by hazard type
3. **First Street** - Property-level flood/fire/heat risk
4. **USGS** - Earthquake hazard maps

---

### 2.4 Automated Report Generation
**Gap:** PDF generation framework exists, not operational  
**Impact:** Enhanced production-readiness

#### Implementation Tasks

| Task | Priority | Effort | Owner |
|------|----------|--------|-------|
| Create Quarto template for policy briefs | MEDIUM | 3 days | TBD |
| Implement notebook-to-report pipeline | MEDIUM | 4 days | TBD |
| Add parameterized report generation | LOW | 2 days | TBD |
| Create branded PDF templates | LOW | 2 days | TBD |

#### Report Types
1. **Executive Summary** (2 pages) - Key findings, recommendations
2. **Technical Appendix** (10+ pages) - Methods, robustness, data
3. **Stakeholder Brief** (4 pages) - Non-technical summary
4. **Data Documentation** (auto-generated) - Lineage, quality metrics

---

## Phase 3: Strategic Investments (6-12 Months)

### 3.1 Cross-Notebook Data Warehouse
**Gap:** No unified data layer across notebooks  
**Impact:** Foundation for enterprise deployment

#### Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Data Warehouse Layer                      │
├─────────────────────────────────────────────────────────────┤
│  PostgreSQL + PostGIS                                        │
│  ├── raw_data (API responses, cached)                       │
│  ├── processed (normalized, joined)                         │
│  ├── features (engineered for models)                       │
│  └── outputs (model results, visualizations)                │
├─────────────────────────────────────────────────────────────┤
│  Redis Cache Layer                                           │
│  └── API responses (1-hour TTL)                             │
├─────────────────────────────────────────────────────────────┤
│  dbt Transformations                                         │
│  ├── staging models                                         │
│  ├── intermediate models                                    │
│  └── mart models (analysis-ready)                           │
└─────────────────────────────────────────────────────────────┘
```

#### Implementation Tasks

| Task | Priority | Effort | Owner |
|------|----------|--------|-------|
| Set up PostgreSQL + PostGIS schema | HIGH | 3 days | TBD |
| Create dbt project for transformations | MEDIUM | 5 days | TBD |
| Build data loading pipelines from connectors | MEDIUM | 4 days | TBD |
| Add data quality tests (Great Expectations) | MEDIUM | 3 days | TBD |

---

### 3.2 Streaming Data Pipeline
**Gap:** Real-time monitoring not implemented  
**Notebook Affected:** 10 (Urban Resilience Dashboard)

#### Architecture
```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Data APIs   │ → │   Kafka      │ → │   Flink      │
│  (FRED, BLS) │    │   Topics     │    │   Processing │
└──────────────┘    └──────────────┘    └──────────────┘
                                              │
                                              ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Dashboard   │ ← │   Redis      │ ← │   TimescaleDB│
│  (Plotly)    │    │   Cache      │    │   (Metrics)  │
└──────────────┘    └──────────────┘    └──────────────┘
```

#### Implementation Tasks

| Task | Priority | Effort | Owner |
|------|----------|--------|-------|
| Set up Kafka for event streaming | LOW | 3 days | TBD |
| Implement Flink jobs for aggregation | LOW | 5 days | TBD |
| Create TimescaleDB for time-series storage | MEDIUM | 2 days | TBD |
| Connect dashboard to real-time feeds | MEDIUM | 3 days | TBD |

---

### 3.3 Kubernetes Deployment
**Gap:** Scalable deployment infrastructure  
**Impact:** Enterprise production capability

#### Implementation Tasks

| Task | Priority | Effort | Owner |
|------|----------|--------|-------|
| Create Helm charts for each service | MEDIUM | 5 days | TBD |
| Set up GKE/EKS cluster configuration | LOW | 3 days | TBD |
| Implement autoscaling for compute-heavy jobs | LOW | 2 days | TBD |
| Add monitoring (Prometheus + Grafana) | LOW | 3 days | TBD |

---

### 3.4 Academic Publication Pipeline
**Target:** 3-5 papers in top policy journals

#### Candidate Papers

| Paper Title | Target Journal | Notebook Basis | Status |
|-------------|----------------|----------------|--------|
| "Heterogeneous Treatment Effects in Workforce Policy" | J. Policy Analysis | NB11 | Draft Q1 |
| "Spatial Causal Inference with HAC Standard Errors" | Spatial Econ Analysis | NB17 | Draft Q2 |
| "Max-P Regionalization for Policy Zone Design" | Geographical Analysis | NB13 | Draft Q2 |
| "Synthetic Control with Pre-Trend Validation" | J. Causal Inference | NB14 | Draft Q3 |
| "Integrated Policy Analytics: A Framework" | J. Comp. Policy Anal. | NB16 | Draft Q4 |

#### Publication Tasks

| Task | Priority | Effort | Owner |
|------|----------|--------|-------|
| Draft NB11 paper (HTE) | HIGH | 20 days | TBD |
| Internal review cycle | MEDIUM | 10 days | TBD |
| Submit to journal | HIGH | 1 day | TBD |
| Respond to R&R | MEDIUM | 15 days | TBD |

---

## Notebook-Specific Improvement Plan

### Notebooks Needing Enhancement (Audit "Conditional" Status)

| Notebook | Current Grade | Gap | Action | Target Grade |
|----------|--------------|-----|--------|--------------|
| 02 Gentrification | 95 | State-level only | Add tract-level via Census Professional tier | 98 |
| 03 Mobility | 94 | No causal decomposition | Add Kitagawa-Blinder-Oaxaca decomposition | 97 |
| 05 Climate | 95 | Simulated hazards | Integrate NOAA/FEMA data | 98 |
| 07 Labor | 96 | Simplified skills taxonomy | Add O*NET task data integration | 98 |
| 10 Dashboard | 95 | No real-time | Deploy Plotly Dash MVP | 97 |
| 21 EJ | 96 | Simulated burdens | Integrate EPA EJSCREEN | 98 |

---

## Resource Requirements

### Engineering Team

| Role | FTE | Phase 1 | Phase 2 | Phase 3 |
|------|-----|---------|---------|---------|
| Backend Engineer | 1.0 | Connectors, indexing | GWR, SCM | Data warehouse |
| Data Engineer | 0.5 | API integration | Report gen | Streaming |
| ML Engineer | 0.5 | - | Parallel ML | Kubernetes |
| DevOps | 0.25 | Dashboard deploy | - | K8s setup |

### Infrastructure Costs (Estimated)

| Resource | Monthly Cost | Phase |
|----------|-------------|-------|
| PostgreSQL (RDS) | $200 | Phase 2 |
| Redis (ElastiCache) | $50 | Phase 1 |
| Kubernetes (EKS) | $500 | Phase 3 |
| Kafka (MSK) | $200 | Phase 3 |
| Dashboard hosting | $20 | Phase 1 |

---

## Success Metrics

### Phase 1 (Month 3)
- [ ] All API calls rate-limited (no 429 errors)
- [ ] Spatial operations 10x faster on 10K obs
- [ ] EPA EJSCREEN data live in NB21
- [ ] Dashboard MVP deployed and accessible
- [ ] 1 external validation completed

### Phase 2 (Month 6)
- [ ] MultiUnitSCM operational with conformal bands
- [ ] Parallel GWR handles 100K observations
- [ ] NOAA climate data integrated
- [ ] Automated PDF reports generating
- [ ] 1 paper submitted to journal

### Phase 3 (Month 12)
- [ ] Data warehouse operational
- [ ] Real-time dashboard with <5min latency
- [ ] Kubernetes cluster deployed
- [ ] 3 papers submitted
- [ ] Portfolio grade: 100/100

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| API rate limits despite throttling | LOW | HIGH | Implement circuit breaker pattern |
| EPA EJSCREEN API deprecation | LOW | MEDIUM | Cache historical snapshots |
| GWR scaling hits memory limits | MEDIUM | MEDIUM | Implement chunked processing |
| Journal rejection | MEDIUM | LOW | Pre-register analysis plans |
| Infrastructure cost overrun | LOW | LOW | Use spot instances, serverless |

---

## Appendix: Detailed Task Breakdown

### A. R-Tree Spatial Indexing (Priority: HIGH)

```python
# Target implementation in krl-geospatial-tools

from rtree import index
import numpy as np
from scipy.sparse import csr_matrix

class SpatialIndex:
    """
    R-tree spatial index for efficient neighbor queries.
    
    Reduces spatial weights computation from O(n²) to O(n log n).
    """
    
    def __init__(self, coordinates: np.ndarray):
        """
        Build R-tree index from coordinate array.
        
        Args:
            coordinates: (n, 2) array of [lon, lat] pairs
        """
        self.idx = index.Index()
        self.coordinates = coordinates
        
        for i, (x, y) in enumerate(coordinates):
            self.idx.insert(i, (x, y, x, y))
    
    def query_radius(self, center: tuple, radius: float) -> list:
        """Find all points within radius of center."""
        x, y = center
        bbox = (x - radius, y - radius, x + radius, y + radius)
        candidates = list(self.idx.intersection(bbox))
        
        # Filter by actual distance
        distances = np.linalg.norm(
            self.coordinates[candidates] - np.array(center), 
            axis=1
        )
        return [c for c, d in zip(candidates, distances) if d <= radius]
    
    def build_weights_matrix(self, bandwidth: float) -> csr_matrix:
        """
        Build sparse spatial weights matrix.
        
        Returns:
            Sparse CSR matrix with kernel weights
        """
        n = len(self.coordinates)
        rows, cols, data = [], [], []
        
        for i in range(n):
            neighbors = self.query_radius(self.coordinates[i], bandwidth)
            for j in neighbors:
                if i != j:
                    dist = np.linalg.norm(
                        self.coordinates[i] - self.coordinates[j]
                    )
                    weight = 1 - (dist / bandwidth)  # Triangular kernel
                    rows.append(i)
                    cols.append(j)
                    data.append(weight)
        
        W = csr_matrix((data, (rows, cols)), shape=(n, n))
        
        # Row-standardize
        row_sums = np.array(W.sum(axis=1)).flatten()
        row_sums[row_sums == 0] = 1  # Avoid division by zero
        W = W.multiply(1 / row_sums[:, np.newaxis])
        
        return W
```

### B. EPA EJSCREEN Connector (Priority: HIGH)

```python
# Target implementation in krl-data-connectors

from typing import Dict, List, Optional
import pandas as pd
import requests

class EJSCREENConnector:
    """
    Connector for EPA EJSCREEN environmental justice data.
    
    Data includes:
    - Environmental indicators (PM2.5, ozone, diesel PM, etc.)
    - Demographic indicators (minority %, low income %, etc.)
    - EJ index scores
    """
    
    BASE_URL = "https://ejscreen.epa.gov/mapper/ejscreenRESTbroker.aspx"
    
    def __init__(self, cache_ttl: int = 86400):
        self.cache_ttl = cache_ttl
        self.session = requests.Session()
    
    def get_block_group_data(
        self, 
        state_fips: str, 
        county_fips: str
    ) -> pd.DataFrame:
        """
        Retrieve EJSCREEN data for all block groups in a county.
        
        Args:
            state_fips: 2-digit state FIPS code
            county_fips: 3-digit county FIPS code
            
        Returns:
            DataFrame with environmental and demographic indicators
        """
        params = {
            "namestr": "",
            "geometry": "",
            "distance": 0,
            "unit": "9035",
            "aession": "",
            "f": "json",
            "fips": f"{state_fips}{county_fips}"
        }
        
        response = self.session.get(self.BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        return self._parse_response(data)
    
    def _parse_response(self, data: Dict) -> pd.DataFrame:
        """Parse EJSCREEN API response into DataFrame."""
        records = []
        for feature in data.get("features", []):
            props = feature.get("properties", {})
            records.append({
                "block_group_id": props.get("ID"),
                "pm25": props.get("PM25"),
                "ozone": props.get("OZONE"),
                "diesel_pm": props.get("DSLPM"),
                "traffic_proximity": props.get("PTRAF"),
                "superfund_proximity": props.get("PNPL"),
                "rmp_proximity": props.get("PRMP"),
                "hazwaste_proximity": props.get("PTSDF"),
                "wastewater": props.get("PWDIS"),
                "lead_paint": props.get("LDPNT"),
                "minority_pct": props.get("MINORPCT"),
                "low_income_pct": props.get("LOWINCPCT"),
                "under5_pct": props.get("UNDER5PCT"),
                "over64_pct": props.get("OVER64PCT"),
                "ej_index_pm25": props.get("P_PM25"),
                "ej_index_ozone": props.get("P_OZONE"),
            })
        
        return pd.DataFrame(records)
```

---

## Sign-Off

**Plan Approved By:** ___________________  
**Date:** ___________________  
**Review Cycle:** Monthly progress reviews

---

*This document is a living plan. Update task status weekly and revise priorities based on emerging needs.*
