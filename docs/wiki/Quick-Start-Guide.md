# Quick Start Guide

Get up and running with KRL Tutorials in 5 minutes!

## 🚀 5-Minute Setup

### Step 1: Clone & Navigate (30 seconds)

```bash
git clone https://github.com/KR-Labs/krl-tutorials.git
cd krl-tutorials
```

### Step 2: Install Dependencies (2-3 minutes)

```bash
pip install -r config/requirements_opensource.txt
```

### Step 3: Launch Jupyter (10 seconds)

```bash
jupyter notebook notebooks/
```

### Step 4: Open Your First Tutorial (30 seconds)

In Jupyter, navigate to:
```
01_economic/D01_income_wealth/D01_income_wealth.ipynb
```

Click **Cell → Run All** or press `Shift + Enter` to run each cell.

## 🎯 Your First Analysis

### What You'll Learn

In the first 10 minutes, you'll:
- ✅ Load real Census data on income distribution
- ✅ Calculate Gini coefficients
- ✅ Create visualizations of inequality trends
- ✅ Perform basic statistical analysis

### Expected Output

You'll see:
1. **Data tables** - Income distribution by percentile
2. **Line charts** - Income trends over time
3. **Statistical metrics** - Gini, mean, median, percentile ratios
4. **Interpretation** - What the numbers mean

## 📊 Understanding Tutorial Structure

Every tutorial follows this structure:

### 1. License & Citation
```markdown
📄 License: MIT (code) + CC-BY-SA-4.0 (content)
📖 Citation: Include BibTeX for academic use
```

### 2. Overview
- **Domain**: What topic area
- **Tier**: Complexity level (1-6)
- **Data Sources**: Where data comes from
- **Learning Objectives**: What you'll master

### 3. Prerequisites
```python
# Required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

### 4. Setup & Data Loading
```python
# Synthetic data generation (works offline!)
# Or real API data (requires API keys)
```

### 5. Tiered Analysis

#### Tier 1: Descriptive Analytics
- Summary statistics
- Data distributions
- Basic visualizations

#### Tier 2: Predictive Analytics
- Regression models
- Forecasting
- Trend analysis

#### Tier 3: Causal Inference (when applicable)
- Difference-in-differences
- Regression discontinuity
- Instrumental variables

#### Higher Tiers: Advanced Methods
- Machine learning
- Deep learning
- Network analysis

### 6. Key Findings & Insights

### 7. Conclusions & Next Steps

### 8. References
Academic sources and further reading

## 🎓 Choose Your Learning Path

### Path 1: Complete Beginner
**Goal**: Learn analytics fundamentals

1. Start with **D01 (Income & Wealth)** - Easiest domain
2. Focus on **Tier 1 sections only** - Descriptive analytics
3. Read all markdown cells carefully
4. Run cells one at a time
5. Modify parameters to see what changes

**Timeline**: 2-3 hours per tutorial

### Path 2: Analyst with Some Python
**Goal**: Master analytics techniques

1. Choose a domain you're interested in
2. Work through **Tiers 1-2** completely
3. Try modifying the code
4. Experiment with different visualizations
5. Apply to your own data

**Timeline**: 1-2 hours per tutorial

### Path 3: Data Scientist
**Goal**: Learn domain-specific methods

1. Skim Tiers 1-2 (review basics)
2. Focus on **Tiers 3-4** (advanced methods)
3. Study the methodological references
4. Adapt techniques to your projects
5. Explore multiple domains

**Timeline**: 30-60 minutes per tutorial

### Path 4: Researcher/Academic
**Goal**: Publication-ready methods

1. Review all tiers for methodology
2. Study the **References section** thoroughly
3. Understand causal inference techniques
4. Adapt code for your research
5. Cite appropriately

**Timeline**: Variable per domain

## 💡 Pro Tips

### Run Cells Sequentially
Always run cells from top to bottom. Later cells depend on earlier ones.

### Use Synthetic Data First
Most tutorials include synthetic data generation - no API keys needed initially.

### Read the Markdown
Don't skip the explanation cells! They contain crucial context.

### Experiment Safely
Make a copy before modifying:
```bash
cp D01_income_wealth.ipynb D01_MY_EXPERIMENTS.ipynb
```

### Check the Footer
Each notebook has helpful resources at the bottom.

## 🔧 Common First-Run Issues

### "ModuleNotFoundError"
**Solution**: Install missing package
```bash
pip install [package-name]
```

### "API key not found"
**Solution**: Use synthetic data sections or [set up API keys](Installation-and-Setup#api-keys-setup)

### "Kernel not responding"
**Solution**: Restart kernel (Kernel → Restart)

### "Plots not showing"
**Solution**: Add to first cell:
```python
%matplotlib inline
```

## 📚 What to Learn Next

After your first tutorial:

### Deepen in Same Domain
- Work through higher tiers
- Try alternative methods
- Explore related domains

### Expand Horizontally
- Try different domains
- Compare methodologies
- Find patterns across domains

### Apply to Real Data
- Get API keys
- Download external datasets
- Replicate published studies

### Contribute
- Fix bugs you find
- Improve documentation
- Share your insights

## 🎬 Video Walkthrough

*Coming soon: Video tutorial of the quick start process*

## 📖 Essential Reading

Before diving deep, familiarize yourself with:

1. **[Analytical Tiers Guide](Analytical-Tiers-Guide)** - Understand the framework
2. **[Data Sources](Data-Sources)** - Know where data comes from
3. **[Code Examples](Code-Examples)** - Common patterns
4. **[FAQ](FAQ)** - Answers to common questions

## ✅ Checklist: You're Ready When...

- [ ] Repository cloned successfully
- [ ] Dependencies installed without errors
- [ ] Jupyter launches and shows notebooks
- [ ] First tutorial runs completely
- [ ] You understand the tier structure
- [ ] You've explored 2-3 different domains
- [ ] You know where to get help

## 🤝 Getting Help

Stuck? Here's how to get help:

1. **Check [Troubleshooting](Troubleshooting)** - Common solutions
2. **Search [Issues](https://github.com/KR-Labs/krl-tutorials/issues)** - Someone may have had same problem
3. **Ask in [Discussions](https://github.com/KR-Labs/krl-tutorials/discussions)** - Community support
4. **Open an [Issue](https://github.com/KR-Labs/krl-tutorials/issues/new)** - Report bugs

## 🎯 Next Steps

Ready to go deeper?

- **[Learning Paths](Learning-Paths)** - Structured curricula
- **[Tutorial Catalog](Tutorial-Catalog)** - Browse all 33 tutorials
- **[Analytical Tiers](Analytical-Tiers-Guide)** - Master the framework
- **[Data Sources](Data-Sources)** - Access real data

---

**Congratulations!** You're ready to explore the world of analytics with KRL Tutorials! 🎉

---

**Last Updated**: October 2025
