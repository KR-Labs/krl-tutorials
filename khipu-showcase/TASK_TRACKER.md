# Khipu Showcase: Priority Task Tracker

## Phase 1 Sprint Board (0-3 Months)

### Sprint 1 (Weeks 1-2): Foundation

| ID | Task | Status | Priority | Blocked By |
|----|------|--------|----------|------------|
| P1-01 | Rate limiter implementation | ✅ DONE | P0 | - |
| P1-02 | R-tree spatial indexing module | 🔲 TODO | P0 | - |
| P1-03 | Sparse spatial weights matrix | 🔲 TODO | P0 | P1-02 |
| P1-04 | Spatial indexing benchmarks | 🔲 TODO | P1 | P1-03 |

### Sprint 2 (Weeks 3-4): EPA Integration

| ID | Task | Status | Priority | Blocked By |
|----|------|--------|----------|------------|
| P1-05 | EPA EJSCREEN connector scaffold | 🔲 TODO | P0 | - |
| P1-06 | EJSCREEN API data parsing | 🔲 TODO | P0 | P1-05 |
| P1-07 | Map EJSCREEN → EJ scoring framework | 🔲 TODO | P1 | P1-06 |
| P1-08 | Update NB21 with real EPA data | 🔲 TODO | P1 | P1-07 |

### Sprint 3 (Weeks 5-6): Dashboard MVP

| ID | Task | Status | Priority | Blocked By |
|----|------|--------|----------|------------|
| P1-09 | Plotly Dash app skeleton | 🔲 TODO | P1 | - |
| P1-10 | Resilience index visualization | 🔲 TODO | P1 | P1-09 |
| P1-11 | Data refresh mechanism | 🔲 TODO | P2 | P1-09 |
| P1-12 | Deploy dashboard to Render | 🔲 TODO | P2 | P1-10 |

### Sprint 4 (Weeks 7-8): External Validation

| ID | Task | Status | Priority | Blocked By |
|----|------|--------|----------|------------|
| P1-13 | Identify 3 published policy studies | 🔲 TODO | P1 | - |
| P1-14 | Replicate Abadie California SCM | 🔲 TODO | P0 | P1-13 |
| P1-15 | Document validation metrics | 🔲 TODO | P1 | P1-14 |
| P1-16 | Create validation notebook | 🔲 TODO | P1 | P1-15 |

---

## Phase 2 Sprint Board (3-6 Months)

### Sprint 5-6: Enterprise Causal Methods

| ID | Task | Status | Priority | Blocked By |
|----|------|--------|----------|------------|
| P2-01 | MultiUnitSCM base implementation | 🔲 TODO | P0 | Phase 1 |
| P2-02 | SDID (Synthetic DiD) algorithm | 🔲 TODO | P0 | P2-01 |
| P2-03 | Conformal inference bands | 🔲 TODO | P1 | P2-02 |
| P2-04 | Staggered adoption support | 🔲 TODO | P1 | P2-02 |
| P2-05 | Unit tests for MultiUnitSCM | 🔲 TODO | P1 | P2-04 |

### Sprint 7-8: Parallel Spatial Computing

| ID | Task | Status | Priority | Blocked By |
|----|------|--------|----------|------------|
| P2-06 | Dask-based parallel GWR | 🔲 TODO | P0 | Phase 1 |
| P2-07 | Adaptive bandwidth (AICc) | 🔲 TODO | P1 | P2-06 |
| P2-08 | GPU acceleration (optional) | 🔲 TODO | P2 | P2-06 |
| P2-09 | 100K observation benchmark | 🔲 TODO | P1 | P2-06 |

### Sprint 9-10: Climate Data Integration

| ID | Task | Status | Priority | Blocked By |
|----|------|--------|----------|------------|
| P2-10 | NOAA NCEI connector | 🔲 TODO | P1 | - |
| P2-11 | FEMA NRI integration | 🔲 TODO | P1 | - |
| P2-12 | Update NB05 with real data | 🔲 TODO | P1 | P2-10, P2-11 |
| P2-13 | Update NB23 with real data | 🔲 TODO | P1 | P2-10, P2-11 |

### Sprint 11-12: Report Automation

| ID | Task | Status | Priority | Blocked By |
|----|------|--------|----------|------------|
| P2-14 | Quarto template for policy briefs | 🔲 TODO | P1 | - |
| P2-15 | Notebook-to-report pipeline | 🔲 TODO | P1 | P2-14 |
| P2-16 | Parameterized generation | 🔲 TODO | P2 | P2-15 |
| P2-17 | Submit first paper (NB11 HTE) | 🔲 TODO | P0 | - |

---

## Notebook Enhancement Tracker

| Notebook | Current | Target | Gap | Task IDs | Status |
|----------|---------|--------|-----|----------|--------|
| 02 Gentrification | 95 | 98 | Tract-level data | Future | 🔲 |
| 03 Mobility | 94 | 97 | Causal decomposition | Future | 🔲 |
| 05 Climate | 95 | 98 | Real hazard data | P2-10,11,12 | 🔲 |
| 07 Labor | 96 | 98 | O*NET integration | Future | 🔲 |
| 10 Dashboard | 95 | 97 | Real-time deploy | P1-09-12 | 🔲 |
| 21 EJ | 96 | 98 | EPA EJSCREEN | P1-05-08 | 🔲 |
| 23 Climate Adapt | 95 | 97 | Real hazard data | P2-10,11,13 | 🔲 |

---

## Code Delivery Checklist

### R-Tree Spatial Indexing (P1-02, P1-03)

- [ ] Create `krl-geospatial-tools/src/krl_geospatial/indexing/` directory
- [ ] Implement `rtree_index.py` with `SpatialIndex` class
- [ ] Implement sparse `spatial_weights.py`
- [ ] Add unit tests in `tests/unit/test_spatial_indexing.py`
- [ ] Update `krl-geospatial-tools` exports
- [ ] Benchmark on PA county data (67 units)
- [ ] Benchmark on US county data (3,000+ units)
- [ ] Update NB13 and NB17 to use new indexing

### EPA EJSCREEN Connector (P1-05, P1-06, P1-07)

- [ ] Create `krl-data-connectors/src/krl_data_connectors/environmental/` directory
- [ ] Implement `ejscreen.py` connector
- [ ] Add rate limiting integration
- [ ] Add caching with TTL
- [ ] Add unit tests
- [ ] Create indicator mapping documentation
- [ ] Update NB21 to use real data
- [ ] Validate against manual EPA lookups

### Dashboard MVP (P1-09, P1-10, P1-11, P1-12)

- [ ] Create `khipu-showcase/dashboard/` directory
- [ ] Implement `app.py` with Plotly Dash
- [ ] Create resilience map component
- [ ] Create indicator cards component
- [ ] Create trend charts component
- [ ] Implement data refresh scheduler
- [ ] Create Dockerfile for deployment
- [ ] Deploy to Render/Railway
- [ ] Add monitoring/health checks

### External Validation (P1-14, P1-15, P1-16)

- [ ] Download Abadie et al. (2010) replication data
- [ ] Implement SCM using NB14 methods
- [ ] Compare effect estimates (should match within CI)
- [ ] Document methodology differences
- [ ] Create `24-external-validation.ipynb` notebook
- [ ] Add to showcase documentation

---

## Dependencies Map

```
Phase 1 (Foundation)
    │
    ├── Rate Limiter ✅ ──────────────────────────────┐
    │                                                  │
    ├── Spatial Indexing ────────────────────────┐    │
    │   └── Sparse Weights ──┐                   │    │
    │                        │                   │    │
    ├── EPA Connector ───────┼───────────────────┼────┤
    │   └── NB21 Update      │                   │    │
    │                        │                   │    │
    ├── Dashboard MVP ───────┼───────────────────┼────┤
    │                        │                   │    │
    └── External Validation ─┼───────────────────┼────┘
                             │                   │
                             ▼                   ▼
Phase 2 (Scale)              │                   │
    │                        │                   │
    ├── MultiUnitSCM ────────┤                   │
    │   └── Conformal Inference                  │
    │                                            │
    ├── Parallel GWR ────────────────────────────┘
    │   └── 100K Benchmark
    │
    ├── NOAA/FEMA Connectors
    │   └── NB05, NB23 Updates
    │
    └── Report Automation
        └── First Paper Submission
                             │
                             ▼
Phase 3 (Enterprise)
    │
    ├── Data Warehouse
    ├── Streaming Pipeline
    ├── Kubernetes Deployment
    └── Publication Pipeline
```

---

## Meeting Cadence

- **Daily Standup**: 15 min, async in Slack
- **Weekly Sprint Review**: Fridays, 30 min
- **Monthly Milestone Review**: Last Friday of month, 1 hour
- **Quarterly Roadmap Update**: End of each phase

---

## Definition of Done

A task is considered DONE when:

1. ✅ Code is written and passes all tests
2. ✅ Documentation is updated
3. ✅ Code review is approved
4. ✅ Changes are merged to main branch
5. ✅ Changes are pushed to GitHub
6. ✅ Any affected notebooks execute without errors

---

*Last Updated: November 29, 2025*
