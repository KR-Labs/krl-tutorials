# KRL Analytics Suite - Tutorial Videos Script Guide

> Video tutorial scripts for the KRL Analytics Suite
> Target: 10-15 minute videos each

---

## Video 1: Introduction to Spatial Causal Inference

**Duration**: 12 minutes
**Level**: Beginner

### Script Outline

**[0:00-1:00] Opening**
- "Welcome to the KRL Analytics Suite tutorial series"
- "Today we'll learn how to combine spatial analysis with causal inference"
- Show: khipu-showcase notebook gallery

**[1:00-3:00] Why Spatial Causal Inference?**
- Traditional causal methods assume independence
- Spatial data violates this assumption
- Example: Policy effects spread across borders
- Show: Map of treatment spillover effects

**[3:00-6:00] The KRL Approach**
- Integrate spatial econometrics with causal methods
- Demo: Import key packages
```python
from krl_geospatial.econometrics import ParallelGWR, morans_i
from krl_models.causal import SyntheticControlMethod
```
- Explain the two-step workflow

**[6:00-10:00] Live Demo: Environmental Policy Analysis**
- Load EJSCREEN data
- Test for spatial autocorrelation
- Fit GWR to identify heterogeneous effects
- Interpret local coefficients
- Create publication-ready map

**[10:00-12:00] Wrap-up**
- Recap key concepts
- Preview next video (Synthetic Control)
- Call to action: Try NB04 and NB21

---

## Video 2: Synthetic Control Method Deep Dive

**Duration**: 15 minutes
**Level**: Intermediate

### Script Outline

**[0:00-2:00] Opening**
- "The Synthetic Control Method is the gold standard for policy evaluation"
- Reference: Abadie et al. (2010) California Prop 99
- What you'll learn today

**[2:00-5:00] Theory**
- The counterfactual problem
- Building a synthetic control unit
- Weight constraints (sum to 1, non-negative)
- Mathematical formulation:
  $$\hat{Y}_{1t}^{N} = \sum_{j=2}^{J+1} w_j Y_{jt}$$

**[5:00-10:00] KRL Implementation**
```python
from krl_models.causal import SyntheticControlMethod

scm = SyntheticControlMethod()
result = scm.fit(Y, treated_unit=0, treatment_period=50)
```
- Walk through each parameter
- Explain output structure
- Visualize: Treatment vs Synthetic

**[10:00-13:00] Inference & Robustness**
- Placebo tests (in-space and in-time)
- RMSPE ratio
- Leave-one-out sensitivity
- Demo: Running validation

**[13:00-15:00] Wrap-up**
- When to use SCM vs DiD
- Multi-unit extension (next video)
- Resources: NB14, NB25, Validation notebook

---

## Video 3: Parallel GWR for Large Datasets

**Duration**: 10 minutes
**Level**: Intermediate/Advanced

### Script Outline

**[0:00-1:30] The Problem**
- GWR is computationally expensive: O(n²k)
- Real datasets have 10k-100k+ observations
- Traditional implementations are too slow

**[1:30-4:00] ParallelGWR Solution**
- Dask-based parallelization
- GPU acceleration option
- Memory-efficient chunking
- Show benchmark: 4-8x speedup

**[4:00-7:00] Demo**
```python
from krl_geospatial.econometrics import ParallelGWR

model = ParallelGWR(
    backend='dask',
    n_workers=8,
    kernel='bisquare',
)
result = model.fit(y, X, coords)
```
- Run on 10k point dataset
- Compare backends
- View local coefficient maps

**[7:00-9:00] Advanced Features**
- Adaptive bandwidth
- Bandwidth selection methods
- Spatial heterogeneity tests
- GPU usage with CuPy

**[9:00-10:00] Wrap-up**
- Performance tips
- When to use parallel vs sequential
- Resource: NB17

---

## Video 4: Production Dashboard Deployment

**Duration**: 12 minutes
**Level**: Advanced

### Script Outline

**[0:00-2:00] From Prototype to Production**
- Development vs Production requirements
- Security, scalability, monitoring
- The KRL deployment framework

**[2:00-5:00] Configuration**
```python
from krl_dashboard import (
    DeploymentConfig,
    SSLConfig,
    AuthConfig,
)

config = DeploymentConfig(
    provider=CloudProvider.KUBERNETES,
    ssl=SSLConfig(mode=SSLMode.LETS_ENCRYPT),
    auth=AuthConfig(provider=AuthProvider.OAUTH2),
)
```
- Walk through each section
- Security best practices

**[5:00-8:00] Generate Artifacts**
- Dockerfile
- docker-compose.yml
- Kubernetes manifests
- NGINX configuration
- AWS CloudFormation

**[8:00-11:00] Deploy Demo**
- Local Docker deployment
- Kubernetes cluster setup
- SSL certificate configuration
- Health checks and monitoring

**[11:00-12:00] Wrap-up**
- CI/CD integration
- Monitoring dashboards
- Resources: deployment docs

---

## Video 5: External Validation - Replicating Published Studies

**Duration**: 15 minutes
**Level**: Intermediate

### Script Outline

**[0:00-2:00] Why Validation Matters**
- Trust through replication
- Academic credibility
- Bug detection

**[2:00-7:00] SCM Validation: Abadie et al. (2010)**
- California Prop 99 study
- Load NB_VALIDATION_SCM
- Step through replication
- Compare results to published

**[7:00-12:00] DiD Validation: Card & Krueger (1994)**
- Minimum wage study
- Load NB_VALIDATION_DID
- Reconstruct dataset
- Run DiD estimation
- Compare to published results

**[12:00-14:00] Interpreting Deviations**
- Data reconstruction effects
- Optimizer differences
- Random seed sensitivity
- When deviations are acceptable

**[14:00-15:00] Wrap-up**
- Add your own validations
- Citation practices
- Resources: validation/ folder

---

## Production Notes

### Recording Setup
- Resolution: 1920x1080
- Frame rate: 30fps
- Audio: 48kHz, mono
- Screen recording: OBS Studio
- Code font: JetBrains Mono, 16pt

### Visual Assets Needed
- KRL logo intro (5 sec)
- Transition slides
- Notebook screenshots
- Architecture diagrams
- Benchmark charts

### Post-Production
- Add captions (auto-generated + reviewed)
- Chapter markers at section boundaries
- End screen with related videos
- Description with timestamps and links

---

*© 2025 KR-Labs. All rights reserved.*
