# Quick Start: Optimized Treatment Effect Estimation

## TL;DR

Use this configuration for maximum precision with minimal runtime:

```python
from krl_policy import TreatmentEffectEstimator

te_estimator = TreatmentEffectEstimator(
    method='doubly_robust',
    n_bootstrap=2000,
    adaptive_bootstrap=False,
    n_jobs=-1,
    random_state=42
)

te_estimator.fit(
    data=your_data,
    treatment_col='treatment',
    outcome_col='outcome',
    covariate_cols=['covariate1', 'covariate2']
)

print(f"ATE: {te_estimator.effect_:.2f}")
print(f"95% CI: [{te_estimator.ci_[0]:.2f}, {te_estimator.ci_[1]:.2f}]")
print(f"P-value: {te_estimator.p_value_:.4f}")
```

## Key Parameters

| Parameter | Value | Reason |
|-----------|-------|--------|
| `n_bootstrap` | 2000 | Stable CI endpoints, minimal p-value jitter |
| `adaptive_bootstrap` | False | Use full iteration count |
| `n_jobs` | -1 | Parallel processing across all CPU cores |

## Expected Performance

- **Runtime**: <1 second for n=52
- **Accuracy**: High-fidelity inference (B=2000)
- **Stability**: Minimal cross-run variance in SE/CI

## Bootstrap Count Guide

- **B=200**: Quick exploration (CI jitter, unstable p-values)
- **B=1000**: Stable endpoints (moderate p-value variance)
- **B=2000**: High precision (**RECOMMENDED**)
- **B>5000**: Diminishing returns

## Installation

```bash
pip install joblib tqdm  # For parallel processing and progress bars
```

## Full Documentation

- [TREATMENT_EFFECT_OPTIMIZATION.md](./TREATMENT_EFFECT_OPTIMIZATION.md) - Technical details
- [OPTIMIZATION_SUMMARY.md](./OPTIMIZATION_SUMMARY.md) - Performance summary

---

© 2025 KR-Labs
