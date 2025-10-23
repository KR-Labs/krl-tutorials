# Analytical Tiers Guide

Understanding the 6-tier analytics framework used throughout KRL Tutorials.

## Overview

KRL Tutorials organize analytics into **6 progressive tiers** that represent increasing complexity and sophistication. This framework helps you:

- 📊 Understand what type of analysis you're performing
- 🎯 Choose appropriate methods for your questions
- 📈 Progress systematically from basics to advanced
- 🔬 Communicate analytical rigor to stakeholders

## The 6 Tiers

### Tier 1: Descriptive Analytics
**"What happened?"**

#### Purpose
Summarize and describe historical data without making predictions or causal claims.

#### Common Techniques
- Summary statistics (mean, median, mode, std dev)
- Frequency distributions
- Crosstabulations
- Data visualization (histograms, bar charts, line plots)
- Percentile analysis
- Year-over-year comparisons

#### Example Questions
- What is the median household income?
- How has unemployment changed over time?
- What percentage of the population has health insurance?

#### Code Example
```python
# Tier 1: Descriptive Analytics
df.describe()  # Summary statistics
df['income'].mean()  # Average income
df.groupby('year')['metric'].agg(['mean', 'median', 'std'])

# Visualization
df.plot(x='year', y='value', kind='line')
```

#### When to Use
- Initial data exploration
- Creating dashboards and reports
- Establishing baseline metrics
- Communicating trends to non-technical audiences

---

### Tier 2: Predictive Analytics
**"What will happen?"**

#### Purpose
Use historical data to make predictions about future outcomes or unknown values.

#### Common Techniques
- Linear regression
- Time series forecasting (ARIMA, exponential smoothing)
- Classification models (logistic regression, decision trees)
- Random forests
- Gradient boosting machines

#### Example Questions
- What will unemployment be next quarter?
- Which individuals are likely to default on loans?
- How will housing prices change over the next year?

#### Code Example
```python
# Tier 2: Predictive Analytics
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA

# Regression
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

# Time series forecast
model = ARIMA(data, order=(1, 1, 1))
results = model.fit()
forecast = results.forecast(steps=12)
```

#### When to Use
- Forecasting future trends
- Risk scoring and assessment
- Demand planning
- Identifying high-risk groups

#### ⚠️ Important Limitations
- Predictions ≠ causal relationships
- "Correlation is not causation"
- Cannot answer "why" questions definitively

---

### Tier 3: Causal Inference
**"What caused this?"**

#### Purpose
Establish cause-and-effect relationships between variables using quasi-experimental or experimental methods.

#### Common Techniques
- Randomized Controlled Trials (RCTs)
- Difference-in-Differences (DiD)
- Regression Discontinuity Design (RDD)
- Instrumental Variables (IV)
- Propensity Score Matching (PSM)
- Synthetic Control Methods

#### Example Questions
- Did the policy change increase employment?
- What is the causal effect of education on earnings?
- Did the intervention reduce crime rates?

#### Code Example
```python
# Tier 3: Difference-in-Differences
import statsmodels.formula.api as smf

# DiD regression
model = smf.ols('''
    outcome ~ treated * post + 
    year_fe + state_fe
''', data=df)
results = model.fit(cov_type='cluster', cov_kwds={'groups': df['state']})

# Extract DiD estimate
did_estimate = results.params['treated:post']
```

#### When to Use
- Evaluating policy interventions
- Understanding treatment effects
- Testing hypotheses about causation
- Informing policy decisions

#### ⚠️ Identification Challenges
- Requires strong assumptions (parallel trends, no anticipation, etc.)
- Selection bias must be addressed
- External validity considerations

---

### Tier 4: Unsupervised Learning
**"What patterns exist?"**

#### Purpose
Discover hidden structures, patterns, and groupings in data without predefined labels.

#### Common Techniques
- Clustering (K-means, hierarchical, DBSCAN)
- Principal Component Analysis (PCA)
- Factor Analysis
- Topic modeling (LDA)
- Association rule mining
- Anomaly detection

#### Example Questions
- What natural groups exist in the population?
- What are the main drivers of variation?
- Which observations are outliers?
- What underlying factors explain the data?

#### Code Example
```python
# Tier 4: Unsupervised Learning
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# K-means clustering
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(X)

# PCA for dimensionality reduction
pca = PCA(n_components=3)
principal_components = pca.fit_transform(X)
explained_variance = pca.explained_variance_ratio_
```

#### When to Use
- Customer segmentation
- Identifying subpopulations
- Data compression
- Feature engineering
- Exploratory analysis

---

### Tier 5: Advanced Machine Learning
**"How can we optimize prediction?"**

#### Purpose
Apply sophisticated ML algorithms for complex prediction, classification, and optimization tasks.

#### Common Techniques
- Deep neural networks
- Ensemble methods (XGBoost, LightGBM, CatBoost)
- Support Vector Machines (SVM)
- Reinforcement learning
- Natural Language Processing (NLP)
- Computer Vision

#### Example Questions
- What is the optimal treatment assignment?
- Can we predict rare events with high accuracy?
- What combination of factors maximizes outcomes?

#### Code Example
```python
# Tier 5: Advanced ML
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV

# XGBoost with hyperparameter tuning
model = XGBClassifier()
param_grid = {
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.2],
    'n_estimators': [100, 200, 300]
}

grid_search = GridSearchCV(model, param_grid, cv=5)
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_
```

#### When to Use
- High-stakes prediction problems
- Large, complex datasets
- Non-linear relationships
- Image or text data

#### ⚠️ Considerations
- Requires substantial data
- Computational resources needed
- Interpretability trade-offs
- Overfitting risks

---

### Tier 6: Network & Spatial Analysis
**"How are things connected?"**

#### Purpose
Analyze relationships, connections, and spatial patterns in networked or geographic data.

#### Common Techniques
- Social network analysis
- Graph algorithms (centrality, communities)
- Spatial autocorrelation (Moran's I)
- Geographic weighted regression
- Spatial point patterns
- Geospatial clustering

#### Example Questions
- Who are the most influential actors in the network?
- How do outcomes cluster geographically?
- What is the spatial spillover effect?
- Which communities exist in the network?

#### Code Example
```python
# Tier 6: Network Analysis
import networkx as nx
from pysal.explore import esda
from pysal.lib import weights

# Network centrality
G = nx.Graph(edge_list)
centrality = nx.betweenness_centrality(G)
communities = nx.community.greedy_modularity_communities(G)

# Spatial autocorrelation
w = weights.Queen.from_dataframe(gdf)
moran = esda.Moran(gdf['value'], w)
print(f"Moran's I: {moran.I}, p-value: {moran.p_sim}")
```

#### When to Use
- Social network data
- Geographic analysis
- Contagion/diffusion studies
- Infrastructure analysis
- Supply chain optimization

---

## Tier Progression Strategy

### Learning Path
```
Tier 1 (Descriptive) → Foundation for everything
    ↓
Tier 2 (Predictive) → Learn to forecast
    ↓
Tier 3 (Causal) → Understand causation
    ↓
Tier 4 (Unsupervised) → Find patterns
    ↓
Tier 5 (Advanced ML) → Optimize predictions
    ↓
Tier 6 (Network/Spatial) → Analyze connections
```

### When to Skip Tiers
- **Skip to Tier 2**: If you're comfortable with basic statistics
- **Skip to Tier 3**: If you have causal inference training
- **Skip to Tier 5**: If you're an experienced data scientist (but review domain context!)

### When NOT to Skip
- Never skip Tier 1 in a new domain (need context)
- Never skip Tier 3 for policy evaluation
- Never skip methodological validation

## Choosing the Right Tier

### Decision Tree

```
What is your goal?
│
├─ Describe what happened
│   └─ USE: Tier 1 (Descriptive)
│
├─ Predict future outcomes
│   ├─ Simple linear relationships
│   │   └─ USE: Tier 2 (Predictive - Basic)
│   └─ Complex non-linear patterns
│       └─ USE: Tier 5 (Advanced ML)
│
├─ Establish causation
│   └─ USE: Tier 3 (Causal Inference)
│
├─ Find hidden patterns/groups
│   └─ USE: Tier 4 (Unsupervised)
│
└─ Analyze connections/networks
    └─ USE: Tier 6 (Network/Spatial)
```

## Common Mistakes by Tier

### Tier 1 Mistakes
- ❌ Over-interpreting correlations as causation
- ❌ Ignoring distributional assumptions
- ❌ Cherry-picking statistics

### Tier 2 Mistakes
- ❌ Extrapolating beyond data range
- ❌ Ignoring multicollinearity
- ❌ Not validating predictions

### Tier 3 Mistakes
- ❌ Weak identification strategies
- ❌ Violation of parallel trends
- ❌ Ignoring selection bias

### Tier 4 Mistakes
- ❌ Not scaling data before clustering
- ❌ Choosing arbitrary number of clusters
- ❌ Over-interpreting cluster meanings

### Tier 5 Mistakes
- ❌ Overfitting to training data
- ❌ Not tuning hyperparameters
- ❌ Ignoring interpretability

### Tier 6 Mistakes
- ❌ Ignoring spatial autocorrelation
- ❌ Inappropriate distance metrics
- ❌ Not accounting for edge effects

## Tier-Specific Resources

### Books by Tier
- **Tier 1-2**: "Python for Data Analysis" (McKinney)
- **Tier 3**: "Causal Inference: The Mixtape" (Cunningham)
- **Tier 4**: "Pattern Recognition and Machine Learning" (Bishop)
- **Tier 5**: "Deep Learning" (Goodfellow et al.)
- **Tier 6**: "Social Network Analysis" (Wasserman & Faust)

### Courses by Tier
- **Tier 1-2**: Coursera - "Applied Data Science with Python"
- **Tier 3**: MIT 14.32 - "Econometric Data Science"
- **Tier 4-5**: fast.ai - "Practical Deep Learning"
- **Tier 6**: Stanford CS224W - "Machine Learning with Graphs"

## Integration Across Tiers

Many analyses benefit from combining tiers:

```python
# Example: Complete analysis pipeline
# Tier 1: Describe the data
summary_stats = df.describe()

# Tier 2: Predict outcomes
predictions = model.predict(X)

# Tier 3: Establish causation
causal_effect = did_analysis(df)

# Tier 4: Find subgroups
clusters = kmeans.fit_predict(features)

# Tier 2 again: Predict within clusters
for cluster in clusters:
    cluster_model.fit(X[cluster])
```

## Next Steps

- **[Learning Paths](Learning-Paths)** - Structured curricula by tier
- **[Code Examples](Code-Examples)** - Tier-specific code patterns
- **[Tutorial Catalog](Tutorial-Catalog)** - Find tutorials by tier
- **[Data Sources](Data-Sources)** - Tier-appropriate data access

---

**Last Updated**: October 2025
