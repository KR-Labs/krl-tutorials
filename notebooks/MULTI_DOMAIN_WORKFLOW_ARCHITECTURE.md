# Multi-Domain Workflow Architecture
**Version:** 1.0.0  
**Date:** November 10, 2025  
**Purpose:** Integration guide for Sprint 7 neural network enhancements with krl-data-connectors

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture Components](#architecture-components)
3. [Workflow Design Patterns](#workflow-design-patterns)
4. [Connector Selection Guidelines](#connector-selection-guidelines)
5. [Equity Factor Engineering](#equity-factor-engineering)
6. [Causal DAG Construction](#causal-dag-construction)
7. [Model Selection Matrix](#model-selection-matrix)
8. [Example Workflows](#example-workflows)
9. [Performance Optimization](#performance-optimization)
10. [Best Practices](#best-practices)

---

## 1. Overview

This document describes how to build end-to-end multi-domain workflows that combine:
- **krl-data-connectors:** 67 connectors across 24 domains (12 Community + 47 Professional + 8 Enterprise)
- **krl-model-zoo Sprint 7 enhancements:** Equity-Weighted Attention, Causal Recurrence Gates, Causal Positional Encoding

### Key Innovation

Traditional ML workflows treat all features equally. Our workflows enable:
1. **Fairness-aware predictions** via equity-weighted attention (demographic factors)
2. **Causally-constrained forecasting** via DAG-based gate masking (domain knowledge)
3. **Graph-aware embeddings** via causal positional encoding (relationship structure)

### Workflow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MULTI-DOMAIN WORKFLOW                         │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 1: DATA INGESTION (krl-data-connectors)                  │
│                                                                   │
│  • Select 2-5 connectors across domains                         │
│  • Retrieve raw data (time series, cross-sectional, panel)      │
│  • Handle API authentication and rate limiting                   │
│  • Example: NCES + Census + FRED                                │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 2: FEATURE ENGINEERING                                    │
│                                                                   │
│  A. Equity Factors (for LSTM)                                    │
│     • Extract demographic indicators (poverty, minority %)       │
│     • Normalize to [0, 1] range                                  │
│     • Create tensor: (batch_size, n_equity_dims)                │
│                                                                   │
│  B. Causal DAG (for GRU/Transformer)                            │
│     • Define variable relationships (domain knowledge)           │
│     • Build NetworkX DiGraph                                     │
│     • Validate acyclicity (no cycles)                            │
│                                                                   │
│  C. Temporal Features                                            │
│     • Create sequences: (batch, seq_len, features)              │
│     • Handle missing data (interpolation, forward fill)          │
│     • Split train/validation/test                                │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 3: MODEL TRAINING (krl-model-zoo enhancements)           │
│                                                                   │
│  Option A: LSTM with Equity-Weighted Attention                   │
│    lstm = load_lstm(use_equity_attention=True, n_equity_dims=3) │
│    out, _ = lstm(X, equity_factors=equity_factors)              │
│                                                                   │
│  Option B: GRU with Causal Recurrence Gates                      │
│    gru = load_gru(use_causal_gates=True, causal_dag=dag)       │
│    out, _ = gru(X)                                               │
│                                                                   │
│  Option C: Transformer with Causal Positional Encoding           │
│    transformer = load_transformer(use_causal_pe=True,           │
│                                  causal_dag=dag,                 │
│                                  variable_names=['x1', 'x2'])    │
│    out = transformer(X)                                          │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 4: EVALUATION & INSIGHTS                                  │
│                                                                   │
│  • Standard metrics: MSE, MAE, R²                               │
│  • Fairness metrics: Demographic parity, equal opportunity       │
│  • Causal validation: DAG consistency, path analysis             │
│  • Visualization: Attention weights, feature importance          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Architecture Components

### 2.1 Data Layer (krl-data-connectors)

**67 Connectors Across 24 Domains:**

| Domain | Connectors | Examples |
|--------|-----------|----------|
| **Economic** | 9 | FRED (Basic/Full), BLS (Basic/Enhanced), BEA, World Bank, OECD |
| **Demographic** | 5 | Census ACS (Public/Detailed), CBP, SSA |
| **Labor** | 3 | LEHD (Basic/Full), OSHA |
| **Health** | 9 | CDC, HRSA, County Health Rankings, NIH, BRFSS, SAMHSA |
| **Education** | 3 | NCES, College Scorecard, IPEDS |
| **Environmental** | 6 | EPA (EJScreen, Air/Water Quality), NOAA, USGS |
| **Housing** | 3 | HUD, Zillow, Eviction Lab |
| **Crime** | 4 | FBI UCR, Bureau of Justice, Victims of Crime |
| **Geographic** | 2 | USGS Earthquakes, Census TIGER |
| **Financial** | 5 | SEC, FDIC, HMDA, IRS990, Treasury |
| **Energy** | 2 | EIA (Basic/Full) |
| **Agricultural** | 2 | USDA NASS, Food Atlas |
| **Science** | 2 | NSF, USPTO |
| **Transportation** | 2 | FAA, NHTS |
| **Political** | 3 | FEC, LegiScan, MIT Election Lab |
| **Social** | 1 | Eviction Lab (also in Housing) |
| **Broadband** | 1 | FCC Broadband |
| **Media** | 1 | GDELT |
| **Mobility** | 1 | Opportunity Insights |
| **Local Gov** | 1 | Local Gov Finance |
| **Transit** | 1 | Transit |
| **Technology** | 1 | FCC Broadband |
| **Veterans** | 1 | Veterans Affairs (VA) |
| **Child Welfare** | 1 | ACF (Admin for Children & Families) |

**Tier Distribution:**
- **Community (12):** FREE, unobfuscated, no license required
- **Professional (47):** $149-599/mo, obfuscated, license validation
- **Enterprise (8):** $999-5,000/mo, device binding, custom SLAs

### 2.2 Enhancement Layer (krl-model-zoo Sprint 7)

**Three Proprietary Enhancements:**

#### A. Equity-Weighted Attention (LSTM)
```python
class EquityWeightedAttention(nn.Module):
    """
    Combines temporal patterns with demographic equity factors.
    
    Algorithm:
        attention = λ_eq * equity_scores + λ_temp * temporal_scores
        context = Σ(attention_weights * hidden_states)
    
    Parameters:
        hidden_dim: LSTM hidden state dimension
        n_equity_dims: Number of equity factors (e.g., 3)
        lambda_eq: Equity weight (default=0.7, 70%)
    """
```

**Use Cases:**
- Education: School performance prediction with fairness constraints
- Healthcare: Patient outcome forecasting with demographic equity
- Economic: Job growth prediction considering underserved communities

#### B. Causal Recurrence Gates (GRU)
```python
class CausalRecurrenceGates(nn.Module):
    """
    DAG-based masking on GRU gate activations.
    
    Algorithm:
        causal_mask[i,j] = 1 if path(i→j) exists in DAG else 0
        masked_input = gate_input * causal_mask
    
    Parameters:
        hidden_size: GRU hidden state dimension
        n_variables: Number of features
        causal_dag: NetworkX DiGraph (optional)
    """
```

**Use Cases:**
- Multi-domain causal analysis (healthcare → education → employment)
- Economic forecasting with structural relationships
- Policy impact prediction with intervention constraints

#### C. Causal Positional Encoding (Transformer)
```python
class CausalPositionalEncoding(nn.Module):
    """
    Graph-aware positional embeddings for transformers.
    
    Algorithm:
        PE_anc(v, 2i) = sin(ancestor_depth(v) / 10000^(2i/d_model))
        PE_desc(v, 2i+1) = cos(descendant_depth(v) / 10000^(2i/d_model))
        PE_final(v) = PE(v) / (1 + hub_penalty * out_degree(v))
    
    Parameters:
        d_model: Transformer embedding dimension
        causal_dag: NetworkX DiGraph
        variable_names: List of variable names
        hub_penalty_coef: Penalty for high out-degree nodes
    """
```

**Use Cases:**
- Economic indicator forecasting with structural models
- Healthcare pathway analysis (symptoms → diagnosis → treatment)
- Education progression modeling (K-12 → college → career)

---

## 3. Workflow Design Patterns

### Pattern 1: Single-Domain + Equity Analysis

**Scenario:** Predict school performance with fairness constraints

**Data Sources:**
- NCES (education data)
- Census ACS (demographics)

**Workflow:**
1. Fetch school-level data (enrollment, test scores, graduation rates)
2. Extract equity factors (poverty rate, minority %, rural status)
3. Train LSTM with equity attention
4. Evaluate fairness metrics

**Code Structure:**
```python
# 1. Data ingestion
nces = NCESConnector()
census = CensusACSPublicConnector()

schools = nces.fetch(data_type="school", state="CA", year=2022)
demographics = census.fetch(geography="county", variables=["poverty_rate", "minority_pct"])

# 2. Feature engineering
equity_factors = extract_equity_factors(schools, demographics)
X, y = prepare_sequences(schools, seq_len=20)

# 3. Model training
lstm = load_lstm(use_equity_attention=True, n_equity_dims=3)
out, _ = lstm(X, equity_factors=equity_factors)

# 4. Evaluation
fairness_score = evaluate_demographic_parity(out, demographics)
```

### Pattern 2: Multi-Domain + Causal Analysis

**Scenario:** Analyze healthcare → education causal pathways

**Data Sources:**
- CDC (health outcomes)
- NCES (education performance)
- Census (demographics, connective tissue)

**Workflow:**
1. Define causal DAG: health → cognitive_development → test_scores
2. Fetch multi-domain data
3. Train GRU with causal gates
4. Validate causal paths

**Code Structure:**
```python
# 1. Causal DAG
dag = nx.DiGraph()
dag.add_edges_from([
    ('childhood_health', 'cognitive_dev'),
    ('cognitive_dev', 'test_scores'),
    ('poverty_rate', 'childhood_health'),
    ('poverty_rate', 'test_scores')
])

# 2. Data ingestion
cdc = CDCWonderConnector()
nces = NCESConnector()
census = CensusACSPublicConnector()

health = cdc.fetch(indicator="child_health", geography="county")
education = nces.fetch(data_type="performance", geography="district")
demographics = census.fetch(geography="county", variables=["poverty_rate"])

# 3. Feature engineering
X, variable_names = merge_multi_domain(health, education, demographics)

# 4. Model training
gru = load_gru(use_causal_gates=True, n_variables=len(variable_names), causal_dag=dag)
out, _ = gru(X)

# 5. Causal validation
validate_dag_consistency(out, dag)
```

### Pattern 3: Economic Forecasting + Graph Structure

**Scenario:** Forecast GDP using economic indicator relationships

**Data Sources:**
- FRED (unemployment, interest rates)
- BLS (employment, wages)
- BEA (GDP, income)

**Workflow:**
1. Build economic DAG: unemployment → wages → consumer_spending → GDP
2. Fetch time series
3. Train Transformer with causal PE
4. Compare with standard PE

**Code Structure:**
```python
# 1. Economic DAG
dag = nx.DiGraph()
dag.add_edges_from([
    ('unemployment', 'wages'),
    ('wages', 'consumer_spending'),
    ('consumer_spending', 'GDP'),
    ('interest_rates', 'consumer_spending'),
    ('interest_rates', 'GDP')
])
variable_names = ['unemployment', 'wages', 'consumer_spending', 'GDP', 'interest_rates']

# 2. Data ingestion
fred = FREDBasicConnector()
bls = BLSBasicConnector()
bea = BEAConnector()

unemployment = fred.fetch(query_type="series", series_id="UNRATE")
wages = bls.fetch(query_type="series", series_id="CES0500000003")
gdp = bea.fetch(dataset="NIPA", table="T10101")

# 3. Feature engineering
X = prepare_multivariate_sequences([unemployment, wages, gdp], seq_len=30)

# 4. Model training
transformer = load_transformer(
    use_causal_pe=True,
    causal_dag=dag,
    variable_names=variable_names
)
out = transformer(X)

# 5. Comparison
transformer_standard = load_transformer(use_causal_pe=False)
out_standard = transformer_standard(X)
compare_forecasts(out, out_standard)
```

---

## 4. Connector Selection Guidelines

### 4.1 By Use Case

| Use Case | Primary Connectors | Supporting Connectors |
|----------|-------------------|---------------------|
| **Education Equity** | NCES, College Scorecard | Census ACS, HRSA (school health) |
| **Healthcare Access** | CDC, HRSA, County Health Rankings | Census (demographics), EPA (environmental) |
| **Economic Development** | FRED, BLS, BEA | Census CBP (business), LEHD (employment) |
| **Housing Affordability** | HUD, Zillow, Eviction Lab | Census (income), BLS (wages) |
| **Crime Prevention** | FBI UCR, Bureau of Justice | Census (demographics), NCES (education) |
| **Environmental Justice** | EPA EJScreen, NOAA | Census (demographics), HRSA (health) |
| **Workforce Development** | BLS, LEHD, OSHA | NCES (education), Census (demographics) |
| **Policy Impact** | Multiple domains | Causal DAG required |

### 4.2 By Data Type

| Data Type | Connectors | Frequency | Granularity |
|-----------|-----------|-----------|-------------|
| **Time Series** | FRED, BLS, NOAA Climate | Daily/Monthly | National/State |
| **Panel Data** | LEHD, County Health Rankings | Quarterly/Annual | County/District |
| **Cross-Sectional** | Census ACS, NCES | Annual/5-year | Tract/Block Group |
| **Event Data** | FDA Approvals, USGS Earthquakes | Real-time | Point-level |
| **Administrative** | SEC Filings, IRS990 | Varies | Entity-level |

### 4.3 Tier Selection Strategy

**Community Tier (FREE):**
- Best for: Proof-of-concept, education, research
- Limitations: Limited features, rate limits, public data only
- Example: FRED_Basic, BLS_Basic, NCES_School_Directory

**Professional Tier ($149-599/mo):**
- Best for: Production apps, consulting, SMB products
- Features: Full API access, higher rate limits, advanced connectors
- Example: FRED_Full, BLS_Enhanced, CDC_Full

**Enterprise Tier ($999-5,000/mo):**
- Best for: Government agencies, large corporations, sensitive analysis
- Features: Device binding, custom SLAs, dedicated support, sensitive data
- Example: FBI_UCR_Detailed, SAMHSA, Veterans_Affairs

---

## 5. Equity Factor Engineering

### 5.1 What Are Equity Factors?

Demographic and socioeconomic indicators used to ensure predictions don't discriminate against underserved populations.

**Common Equity Factors:**
1. **Poverty Rate:** % population below poverty line
2. **Minority Percentage:** % non-white population
3. **Rural Status:** Urban/Rural classification
4. **Education Level:** % with bachelor's degree or higher
5. **Unemployment Rate:** % unemployed in labor force
6. **Health Access:** Per-capita physicians, hospitals
7. **Internet Access:** % with broadband access
8. **Disability Rate:** % with disabilities

### 5.2 Extraction Patterns

#### Pattern A: Census ACS (Demographics)
```python
census = CensusACSPublicConnector()

# Poverty rate (Table B17001)
poverty = census.fetch(
    geography="county",
    variables=["B17001_002E"],  # Below poverty level
    year=2022
)
poverty_rate = poverty["B17001_002E"] / poverty["B01003_001E"]  # Total pop

# Minority percentage
minority = census.fetch(
    geography="county",
    variables=["B02001_002E"],  # White alone
    year=2022
)
minority_pct = 1 - (minority["B02001_002E"] / minority["B01003_001E"])
```

#### Pattern B: County Health Rankings (Health)
```python
chr = CountyHealthRankingsConnector()

health_data = chr.fetch(state="CA", year=2023)

# Extract health equity factors
health_equity = health_data[[
    "primary_care_physicians_per_100k",
    "percent_uninsured",
    "percent_food_insecure"
]]
```

#### Pattern C: NCES (Education)
```python
nces = NCESConnector()

schools = nces.fetch(data_type="school", state="CA", year=2022)

# School-level equity factors
school_equity = schools[[
    "percent_free_lunch",  # Economic disadvantage
    "percent_english_learners",  # Language barriers
    "title_i_status"  # Federal funding for low-income
]]
```

### 5.3 Normalization

**Always normalize equity factors to [0, 1] range:**
```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
equity_factors_normalized = scaler.fit_transform(equity_factors)

# Convert to PyTorch tensor
equity_tensor = torch.FloatTensor(equity_factors_normalized)
# Shape: (batch_size, n_equity_dims)
```

### 5.4 Integration with LSTM

```python
lstm = load_lstm(
    input_size=10,
    hidden_size=64,
    num_layers=2,
    output_size=1,
    use_equity_attention=True,
    n_equity_dims=3  # poverty_rate, minority_pct, rural_status
)

# Forward pass
X = torch.randn(32, 20, 10)  # (batch, seq_len, features)
equity_factors = torch.randn(32, 3)  # (batch, n_equity_dims)

out, hidden = lstm(X, equity_factors=equity_factors)

# Attention mechanism combines:
# - 70% weight on equity scores (demographic fairness)
# - 30% weight on temporal patterns (historical trends)
```

---

## 6. Causal DAG Construction

### 6.1 Domain Knowledge → DAG

**Step 1: Identify Variables**
List all features in your dataset.

**Step 2: Define Relationships**
For each pair (X, Y), ask: "Does X causally influence Y?"

**Step 3: Build NetworkX DiGraph**
```python
import networkx as nx

dag = nx.DiGraph()
dag.add_edges_from([
    ('X1', 'X2'),  # X1 → X2
    ('X2', 'X3'),  # X2 → X3
    ('X1', 'X3')   # X1 → X3 (direct path)
])
```

**Step 4: Validate Acyclicity**
```python
assert nx.is_directed_acyclic_graph(dag), "Graph contains cycles!"
```

### 6.2 Example DAGs by Domain

#### Education Pathway
```python
education_dag = nx.DiGraph()
education_dag.add_edges_from([
    # Socioeconomic → Academic
    ('poverty_rate', 'teacher_quality'),
    ('poverty_rate', 'student_achievement'),
    
    # School Resources → Outcomes
    ('teacher_quality', 'student_achievement'),
    ('per_pupil_spending', 'teacher_quality'),
    ('per_pupil_spending', 'student_achievement'),
    
    # Academic → Post-Secondary
    ('student_achievement', 'college_enrollment'),
    ('college_enrollment', 'earnings_potential')
])
```

#### Healthcare Cascade
```python
healthcare_dag = nx.DiGraph()
healthcare_dag.add_edges_from([
    # Social Determinants → Health Access
    ('poverty_rate', 'health_insurance_coverage'),
    ('rural_status', 'physician_availability'),
    
    # Access → Outcomes
    ('health_insurance_coverage', 'preventive_care_utilization'),
    ('physician_availability', 'health_outcomes'),
    
    # Preventive → Chronic Disease
    ('preventive_care_utilization', 'chronic_disease_prevalence'),
    ('chronic_disease_prevalence', 'mortality_rate')
])
```

#### Economic Structure
```python
economic_dag = nx.DiGraph()
economic_dag.add_edges_from([
    # Labor Market
    ('unemployment_rate', 'wage_growth'),
    ('education_level', 'unemployment_rate'),
    
    # Consumer Behavior
    ('wage_growth', 'consumer_spending'),
    ('interest_rates', 'consumer_spending'),
    
    # Aggregate Demand
    ('consumer_spending', 'GDP_growth'),
    ('business_investment', 'GDP_growth'),
    
    # Feedback
    ('GDP_growth', 'unemployment_rate')
])
```

### 6.3 Integration with GRU

```python
gru = load_gru(
    input_size=5,
    hidden_size=64,
    num_layers=2,
    output_size=1,
    use_causal_gates=True,
    n_variables=5,
    causal_dag=dag
)

# Causal gate mechanism:
# 1. Compute causal mask from DAG (transitive closure)
# 2. Mask non-causal connections to zero
# 3. Apply masked gates to hidden states

X = torch.randn(32, 20, 5)  # (batch, seq_len, features)
out, hidden = gru(X)
```

### 6.4 Integration with Transformer

```python
transformer = load_transformer(
    d_model=64,
    nhead=4,
    num_layers=2,
    input_size=5,
    output_size=1,
    use_causal_pe=True,
    causal_dag=dag,
    variable_names=['var1', 'var2', 'var3', 'var4', 'var5']
)

# Causal positional encoding:
# 1. Ancestor depth (sin): How far back causally?
# 2. Descendant depth (cos): How far forward causally?
# 3. Hub penalty: Reduce weight for high out-degree variables

X = torch.randn(32, 10, 5)  # (batch, seq_len, features)
out = transformer(X)
```

---

## 7. Model Selection Matrix

| Criterion | LSTM + Equity Attention | GRU + Causal Gates | Transformer + Causal PE |
|-----------|------------------------|-------------------|------------------------|
| **Best For** | Fairness-critical predictions | Multi-domain causal analysis | Long-range dependencies with structure |
| **Data Requirement** | Equity factors (demographics) | Causal DAG (domain knowledge) | Causal DAG + variable names |
| **Sequence Length** | Short-medium (10-50 steps) | Short-medium (10-50 steps) | Long (50-500 steps) |
| **Interpretability** | Attention weights → equity impact | Gate masks → causal paths | PE norms → variable importance |
| **Computational Cost** | Low (LSTM + attention) | Low (GRU + masking) | High (Transformer + PE) |
| **Training Stability** | High (LSTM gradients) | High (GRU gradients) | Medium (Transformer needs warmup) |
| **Example Use Cases** | School performance, patient outcomes | Healthcare → education pathways | Economic forecasting, policy impact |

### Decision Tree

```
Do you need fairness-aware predictions?
├─ YES → Use LSTM + Equity Attention
│         (Education, healthcare, housing applications)
│
└─ NO → Do you have multi-domain causal relationships?
        ├─ YES → Do you need long-range dependencies?
        │        ├─ YES → Use Transformer + Causal PE
        │        │         (Economic forecasting, complex systems)
        │        │
        │        └─ NO → Use GRU + Causal Gates
        │                  (Healthcare → education, policy analysis)
        │
        └─ NO → Use standard models (Community tier)
                (Exploratory analysis, benchmarking)
```

---

## 8. Example Workflows

### Workflow 1: Education Equity Analysis

**File:** `education_equity_lstm.ipynb`

**Objective:** Predict school performance with fairness constraints across demographic groups.

**Data Sources:**
- NCES (school directory, performance data)
- Census ACS (demographics)

**Enhancement:** LSTM + Equity-Weighted Attention

**Steps:**
1. Fetch school data (enrollment, test scores, graduation rates)
2. Extract equity factors (poverty rate, minority %, rural status)
3. Normalize features and create sequences
4. Train LSTM with equity attention (λ_eq=0.7)
5. Evaluate fairness metrics (demographic parity, equal opportunity)
6. Visualize attention weights by demographic group

### Workflow 2: Healthcare Causal Analysis

**File:** `healthcare_causal_gru.ipynb`

**Objective:** Analyze causal pathways from social determinants to health outcomes.

**Data Sources:**
- CDC WONDER (health outcomes)
- County Health Rankings (access, behaviors)
- Census ACS (demographics)

**Enhancement:** GRU + Causal Recurrence Gates

**Steps:**
1. Define healthcare DAG (poverty → access → utilization → outcomes)
2. Fetch multi-domain data
3. Merge datasets by county FIPS code
4. Build sequences and align to DAG variables
5. Train GRU with causal gates
6. Validate causal paths (intervention analysis)

### Workflow 3: Economic Forecasting with Transformer

**File:** `economic_forecasting_transformer.ipynb`

**Objective:** Forecast GDP using structural economic relationships.

**Data Sources:**
- FRED (unemployment, interest rates, money supply)
- BLS (employment, wages)
- BEA (GDP, income)

**Enhancement:** Transformer + Causal Positional Encoding

**Steps:**
1. Build economic DAG (unemployment → wages → spending → GDP)
2. Fetch time series (monthly, 10 years)
3. Align series and create multivariate sequences
4. Train Transformer with causal PE
5. Compare with standard PE (ablation study)
6. Forecast 12 months ahead and evaluate MAE/RMSE

---

## 9. Performance Optimization

### 9.1 Data Loading

**Use Batch Loading:**
```python
from torch.utils.data import DataLoader, TensorDataset

dataset = TensorDataset(X_train, y_train, equity_train)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)
```

**Cache Connector Results:**
```python
import joblib

@joblib.Memory(location=".cache").cache
def fetch_nces_data(state, year):
    nces = NCESConnector()
    return nces.fetch(data_type="school", state=state, year=year)
```

### 9.2 Model Training

**Use Mixed Precision:**
```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for epoch in range(num_epochs):
    for X, y, equity in dataloader:
        optimizer.zero_grad()
        
        with autocast():
            out, _ = lstm(X, equity_factors=equity)
            loss = criterion(out, y)
        
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
```

**Learning Rate Scheduling:**
```python
from torch.optim.lr_scheduler import CosineAnnealingLR

scheduler = CosineAnnealingLR(optimizer, T_max=num_epochs)

for epoch in range(num_epochs):
    train_one_epoch()
    scheduler.step()
```

### 9.3 Feature Engineering

**Parallel Processing:**
```python
from joblib import Parallel, delayed

def extract_equity(row):
    return {
        'poverty_rate': row['poverty'] / row['population'],
        'minority_pct': 1 - (row['white'] / row['population']),
        'rural': 1 if row['urban'] == 0 else 0
    }

equity_factors = Parallel(n_jobs=-1)(
    delayed(extract_equity)(row) for _, row in df.iterrows()
)
```

### 9.4 DAG Construction

**Cache Transitive Closure:**
```python
@functools.lru_cache(maxsize=1)
def compute_transitive_closure(dag_hash):
    # Hash DAG structure for caching
    closure = nx.transitive_closure(dag)
    return closure
```

---

## 10. Best Practices

### 10.1 Data Quality

✅ **DO:**
- Validate data before training (missing values, outliers)
- Use consistent time periods across connectors
- Document data preprocessing steps
- Version control data pipelines

❌ **DON'T:**
- Mix different geographic levels (state vs county)
- Ignore temporal alignment (quarterly vs annual data)
- Use leaked features (future information)
- Skip exploratory data analysis

### 10.2 Equity Factor Selection

✅ **DO:**
- Choose factors relevant to prediction task
- Normalize all factors to same scale
- Consider intersectionality (multiple factors)
- Validate with domain experts

❌ **DON'T:**
- Use protected attributes directly (race, gender)
- Include collinear factors (multicollinearity)
- Ignore temporal changes in demographics
- Assume equal importance (use λ_eq tuning)

### 10.3 Causal DAG Design

✅ **DO:**
- Base on domain knowledge, not data-driven discovery
- Validate acyclicity (nx.is_directed_acyclic_graph)
- Document edge justifications (literature, expert opinion)
- Test DAG sensitivity (ablation studies)

❌ **DON'T:**
- Infer DAG from correlation alone
- Include all possible edges (overfitting)
- Use automatic DAG learning without validation
- Ignore temporal ordering (future → past edges)

### 10.4 Model Training

✅ **DO:**
- Use train/validation/test splits (60/20/20)
- Monitor both standard and fairness metrics
- Save best models by multiple criteria
- Log hyperparameters and results

❌ **DON'T:**
- Train on test data (data leakage)
- Optimize only for accuracy (ignore fairness)
- Use fixed hyperparameters without tuning
- Skip ablation studies (standard vs enhanced)

### 10.5 Production Deployment

✅ **DO:**
- Version models and data pipelines
- Monitor prediction drift over time
- Implement fallback to Community tier connectors
- Document license requirements per tier

❌ **DON'T:**
- Deploy without license validation
- Ignore API rate limits (connector failures)
- Skip model retraining (stale predictions)
- Use Professional/Enterprise connectors without proper licensing

---

## Next Steps

1. **Explore Example Notebooks:**
   - `education_equity_lstm.ipynb`
   - `healthcare_causal_gru.ipynb`
   - `economic_forecasting_transformer.ipynb`

2. **Review Documentation:**
   - `krl-data-connectors/README.md` (connector details)
   - `krl-model-zoo/docs/SPRINT7_PATENT_SAFE_ENHANCEMENTS.md` (enhancement specs)

3. **Join Community:**
   - GitHub Discussions: Report issues, share workflows
   - Monthly Office Hours: Get help with custom DAGs

4. **Upgrade to Professional:**
   - Access 47 additional connectors
   - Higher API rate limits
   - Priority support

---

**Last Updated:** November 10, 2025  
**Version:** 1.0.0  
**Contributors:** KR-Labs Development Team
