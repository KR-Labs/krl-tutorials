# Interactive Configuration Guide

## ✅ Configuration System Added

The notebook now has a **user-friendly configuration system** that makes it easy to customize analysis parameters without hunting through code.

---

## 🎛️ How It Works

### Location in Notebook
The configuration appears **right after setup** (after cell 3), before any analysis begins.

### Two Configuration Cells

**Cell 1: Main Configuration**
- All parameters in one place
- Clear comments explaining each option
- Visual separators for organization
- Summary display showing what will run

**Cell 2: Quick Presets**
- Pre-configured scenarios for common use cases
- Uncomment to instantly apply settings
- Examples: Quick Demo, Standard Analysis, Comprehensive Research

---

## 📊 Configuration Parameters

### 1. Topic Configuration
```python
TOPIC = 'housing affordability'  # Change to any policy topic
```

**Alternative Topics Available:**
- Climate change policy
- Artificial intelligence regulation
- Student loan forgiveness
- Renewable energy subsidies
- Minimum wage increase
- Universal basic income
- Police reform
- Healthcare reform
- Immigration policy
- Cryptocurrency regulation

**How to Use:**
- **Option A**: Change `TOPIC` directly
- **Option B**: Uncomment alternative: `TOPIC = ALTERNATIVE_TOPICS[0]`

---

### 2. Time Period Configuration
```python
DAYS_BACK = 21  # How many days of coverage to analyze
MAX_ARTICLES = 1000  # Maximum articles to retrieve
```

**Recommendations:**
- **7 days**: Quick snapshot, trending issues
- **14-21 days**: Standard analysis (recommended)
- **30+ days**: Long-term trends

**Max Articles:**
- **200-300**: Quick demo/testing
- **500-800**: Standard analysis
- **1000+**: Comprehensive (slower)

---

### 3. Clustering Configuration
```python
SPATIAL_WEIGHT = 0.15  # λ_spatial parameter (trade secret)
DISTANCE_THRESHOLD = 0.5  # Clustering sensitivity
```

**Spatial Weight (λ):**
- **0.0**: Pure semantic (no geography)
- **0.15**: Balanced (recommended, patent-pending)
- **0.30**: More geographic influence
- **1.0**: Pure geographic

**Distance Threshold:**
- **0.3**: Many small clusters (fine-grained)
- **0.5**: Balanced (recommended)
- **0.7**: Fewer large clusters (coarse)

---

### 4. Text Enrichment Configuration
```python
ENABLE_TEXT_ENRICHMENT = True  # Fetch full article text
MAX_ARTICLES_TO_ENRICH = 100  # Limit for cost control
```

**When to Enable:**
- ✅ **True**: Better sentiment/analysis, slower, uses API credits
- ❌ **False**: Title-only, faster, no API costs

**Cost Control:**
- **50-100**: Demo/testing (~$0.50-1.00)
- **200-300**: Standard (~$2-3)
- **500+**: Comprehensive (~$5+)

---

### 5. Advanced Features Configuration
```python
ENABLE_ADVANCED_SENTIMENT = True  # Aspect-based sentiment
ENABLE_CAUSAL_BIAS = True  # Causal bias detection
ENABLE_ADVANCED_VIZ = True  # Sankey, Treemap, Network graphs
MIN_ARTICLES_PER_OUTLET = 5  # For causal bias analysis
```

**Toggle Features:**
- **Advanced Sentiment**: Requires text enrichment for best results
- **Causal Bias**: Needs enough articles per outlet (5+ recommended)
- **Advanced Viz**: Expensive to compute, but impressive for demos
- **Min Articles**: Higher = fewer outlets but more reliable bias estimates

---

### 6. Output Configuration
```python
OUTPUT_DIR = 'analysis_outputs'
SAVE_INTERMEDIATE_FILES = True
```

**Output Directory**: Where results are saved
**Save Intermediate**: Keep CSVs at each analysis step (useful for debugging)

---

## 🎯 Quick Presets

### PRESET 1: Quick Demo
**Use when**: Testing, showing basic features, no API keys needed

```python
# Uncomment this block:
TOPIC = 'climate change policy'
DAYS_BACK = 7
MAX_ARTICLES = 200
ENABLE_TEXT_ENRICHMENT = False
ENABLE_ADVANCED_SENTIMENT = False
ENABLE_CAUSAL_BIAS = False
ENABLE_ADVANCED_VIZ = True
```

**Runtime**: ~5 minutes
**Cost**: $0
**Shows**: Spatial clustering + basic visualizations

---

### PRESET 2: Standard Analysis (Recommended)
**Use when**: Customer demos, typical analysis

```python
# Uncomment this block:
TOPIC = 'housing affordability'
DAYS_BACK = 21
MAX_ARTICLES = 800
ENABLE_TEXT_ENRICHMENT = True
MAX_ARTICLES_TO_ENRICH = 200
ENABLE_ADVANCED_SENTIMENT = True
ENABLE_CAUSAL_BIAS = True
ENABLE_ADVANCED_VIZ = True
```

**Runtime**: ~30-40 minutes
**Cost**: ~$2-3
**Shows**: Full pipeline with all features

---

### PRESET 3: Comprehensive Research
**Use when**: Deep analysis, research projects, have time/budget

```python
# Uncomment this block:
TOPIC = 'artificial intelligence regulation'
DAYS_BACK = 30
MAX_ARTICLES = 2000
ENABLE_TEXT_ENRICHMENT = True
MAX_ARTICLES_TO_ENRICH = 500
ENABLE_ADVANCED_SENTIMENT = True
ENABLE_CAUSAL_BIAS = True
MIN_ARTICLES_PER_OUTLET = 10
ENABLE_ADVANCED_VIZ = True
```

**Runtime**: ~1-2 hours
**Cost**: ~$5-10
**Shows**: Maximum quality, most reliable bias estimates

---

## 💡 Usage Examples

### Example 1: Change Topic to "Student Loan Forgiveness"

**Before (Bad):**
1. Scroll to cell 23
2. Find `topic='housing affordability'`
3. Change to `topic='student loan forgiveness'`
4. Scroll to cell 25
5. Find `days_back=21`
6. Change if needed
7. Repeat for other cells...

**After (Good):**
```python
# Just change line 5 in configuration cell:
TOPIC = 'student loan forgiveness'

# Hit Run All → Done!
```

---

### Example 2: Quick Demo for Customer Call

**Scenario**: Need fast demo, no API keys setup yet

```python
# Uncomment PRESET 1 in quick presets cell
# Runtime: 5 minutes, Cost: $0
```

**Result**: Shows spatial clustering, 3D visualization, advanced charts
**Missing**: Full-text analysis, sentiment, causal bias
**Good for**: "Here's how it works" without expensive features

---

### Example 3: Full Analysis for Important Customer

**Scenario**: High-priority customer, want to impress

```python
# Uncomment PRESET 2 in quick presets cell
# Runtime: 30-40 minutes, Cost: $2-3
```

**Result**: Everything enabled, publication-quality
**Shows**: Full pipeline, all visualizations, bias detection
**Good for**: "This is what you're paying $75K/year for"

---

### Example 4: Test Different Clustering Parameters

**Scenario**: Cluster imbalance (one cluster has 80% of articles)

```python
# Try more geographic influence:
SPATIAL_WEIGHT = 0.25  # Increase from 0.15
DISTANCE_THRESHOLD = 0.4  # Lower for finer clusters

# Or try pure semantic:
SPATIAL_WEIGHT = 0.0  # No geography
DISTANCE_THRESHOLD = 0.5
```

**Result**: Different cluster distributions
**Use**: Compare which parameter set gives best balance

---

## 🔧 What Cells Use Configuration

All key analysis cells now use these parameters:

| Cell | Parameters Used | Purpose |
|------|----------------|---------|
| Data Acquisition | `TOPIC`, `DAYS_BACK`, `MAX_ARTICLES` | Fetch articles |
| Clustering | `SPATIAL_WEIGHT`, `DISTANCE_THRESHOLD` | Cluster articles |
| Text Enrichment | `ENABLE_TEXT_ENRICHMENT`, `MAX_ARTICLES_TO_ENRICH` | Get full text |
| Sentiment Analysis | `ENABLE_ADVANCED_SENTIMENT` | Analyze sentiment |
| Causal Bias | `ENABLE_CAUSAL_BIAS`, `MIN_ARTICLES_PER_OUTLET` | Detect bias |
| Advanced Viz | `ENABLE_ADVANCED_VIZ` | Show enterprise charts |

---

## ✅ Benefits for Customer Demos

### Before Configuration System
**Customer**: "Can you analyze climate policy instead?"
**You**: "Um, let me scroll through the notebook... find the right cell... change this parameter... oh wait, there's another one in cell 45... hold on..."
**Customer**: 😴 *loses interest*

### After Configuration System
**Customer**: "Can you analyze climate policy instead?"
**You**: "Sure! *Changes line 5 at top* Done. Running now..."
**Customer**: 😲 "That was fast!"

---

## 📝 Configuration Summary Display

After setting parameters, the notebook displays:

```
================================================================================
🎛️  ANALYSIS CONFIGURATION SUMMARY
================================================================================

📊 Topic: 'housing affordability'
📅 Time Period: 21 days back
📈 Max Articles: 1,000
🎯 Spatial Weight (λ): 0.15
🔍 Distance Threshold: 0.5

🔧 Features:
   • Text Enrichment: ✅ Enabled (max 100 articles)
   • Advanced Sentiment: ✅ Enabled
   • Causal Bias: ✅ Enabled (min 5 articles/outlet)
   • Advanced Viz: ✅ Enabled

💾 Output Directory: analysis_outputs/
================================================================================

✅ Configuration loaded! Ready to run analysis.
💡 TIP: Change any parameter above and re-run this cell to update.
```

This gives you **instant confirmation** of what will run before spending 30 minutes on analysis.

---

## 🚨 Troubleshooting

### Issue: "No articles found for this topic"
**Fix**:
- Try broader topic: `'immigration'` vs `'immigration policy reform'`
- Increase `DAYS_BACK` to 30
- Increase `MAX_ARTICLES` to 2000

### Issue: "Insufficient data for causal bias"
**Fix**:
- Increase `DAYS_BACK` (more articles = more per outlet)
- Decrease `MIN_ARTICLES_PER_OUTLET` from 5 to 3
- Choose topic with more media coverage

### Issue: "Text enrichment too slow/expensive"
**Fix**:
- Set `ENABLE_TEXT_ENRICHMENT = False` for quick test
- Reduce `MAX_ARTICLES_TO_ENRICH` to 50
- Use PRESET 1 (Quick Demo)

### Issue: "Cluster imbalance (one cluster has 80%)"
**Fix**:
- Increase `SPATIAL_WEIGHT` to 0.25 (more geographic)
- Decrease `DISTANCE_THRESHOLD` to 0.4 (finer clusters)
- Increase `DAYS_BACK` and `MAX_ARTICLES` (more data)

---

## 💰 Cost Estimation by Configuration

| Configuration | Runtime | API Cost | Best For |
|--------------|---------|----------|----------|
| **PRESET 1: Quick Demo** | 5 min | $0 | Testing, no API keys |
| **PRESET 2: Standard** | 30-40 min | $2-3 | Customer demos |
| **PRESET 3: Comprehensive** | 1-2 hours | $5-10 | Research projects |
| **Custom (text=off)** | 10 min | $0 | Quick iteration |
| **Custom (max enrichment)** | 2-3 hours | $10+ | Publication quality |

---

## 🎯 Recommended Configurations by Use Case

### Use Case: Customer Discovery Call (15 min demo)
```python
# PRESET 2 (run before call)
TOPIC = [customer's policy area]
DAYS_BACK = 14
ENABLE_TEXT_ENRICHMENT = True
MAX_ARTICLES_TO_ENRICH = 100
```
**Why**: Balanced features, reasonable runtime, impressive results

---

### Use Case: Internal Testing (iterate quickly)
```python
# PRESET 1 (fast iteration)
TOPIC = 'test topic'
DAYS_BACK = 7
ENABLE_TEXT_ENRICHMENT = False  # Skip for speed
ENABLE_ADVANCED_VIZ = False  # Skip for speed
```
**Why**: Fast feedback loop for development

---

### Use Case: Academic Paper / Publication
```python
# PRESET 3 (maximum quality)
TOPIC = 'research topic'
DAYS_BACK = 60
MAX_ARTICLES = 5000
ENABLE_TEXT_ENRICHMENT = True
MAX_ARTICLES_TO_ENRICH = 1000
MIN_ARTICLES_PER_OUTLET = 15
```
**Why**: Most reliable results, best for citations

---

### Use Case: Live Customer Demo (change on the fly)
```python
# Keep default config loaded, but:
# 1. Have alternative topics ready:
ALTERNATIVE_TOPICS = [
    'climate change',  # If customer asks
    'healthcare',      # If customer asks
    'education'        # If customer asks
]

# 2. During demo, just change:
TOPIC = ALTERNATIVE_TOPICS[0]
# Re-run config cell + Run All
```
**Why**: Adaptable to customer interests in real-time

---

## ✅ Final Checklist

Before customer demo:
- [ ] Review configuration at top of notebook
- [ ] Set `TOPIC` to customer's policy area
- [ ] Choose appropriate preset (recommend PRESET 2)
- [ ] Check API keys if `ENABLE_TEXT_ENRICHMENT = True`
- [ ] Run configuration cell to see summary
- [ ] Verify all features show ✅ Enabled (or intentionally disabled)
- [ ] Test run with smaller dataset first

---

**The configuration system makes your notebook demo-ready and customer-friendly!** 🎉

No more hunting through code. No more "where do I change this?" Just change parameters at the top and go.
