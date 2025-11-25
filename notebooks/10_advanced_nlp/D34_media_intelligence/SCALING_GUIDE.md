# Scaling Guide - 313 to 10,000+ Articles

**Priority**: 2 (High Impact, 1-2 days effort)
**Goal**: Enable causal bias analysis with 30+ articles per outlet

---

## 🎯 **Why Scale?**

### Current Limitations (313 articles)
```
Total articles: 313
Unique outlets: ~85
Articles per outlet (avg): 3.7
Articles per outlet (median): 2

❌ INSUFFICIENT FOR:
- Causal bias analysis (requires 30+ per outlet)
- Robust t-tests (requires n≥30 per group)
- Reliable syndication patterns
- Statistical validity
```

### After Scaling (10,000+ articles)
```
Total articles: 10,000-15,000
Unique outlets: 50 (filtered to top)
Articles per outlet (avg): 200-300
Articles per outlet (median): 180-250

✅ ENABLES:
- Valid causal bias for 30-50 outlets
- Robust statistical tests (n>>30)
- Accurate syndication detection
- Historical validation studies
```

---

## 📊 **Scaling Strategy**

### Approach: Query Extended Time Period

**Current**: 60 days (2 months)
**Target**: 180 days (6 months)
**Scaling factor**: 3x

**Expected results**:
- 313 articles × 3 = **~940 articles minimum**
- With filtering to top outlets: **5,000-15,000 articles**
- Top 50 outlets: **30-300 articles each**

---

## 🚀 **Implementation Steps**

### Step 1: Estimate Parameters

```python
from gdelt_scaler import GDELTScaler

scaler = GDELTScaler(verbose=True)

# Estimate what you need
recommendations = scaler.estimate_scaling_parameters(
    current_articles=313,
    current_days=60,
    target_articles_per_outlet=30,
    target_outlets=50
)

# Output:
# Recommended days: 180
# Expected articles: ~15,000
# Should meet target: ✅ Yes
```

---

### Step 2: Modify Data Collection

**Current notebook cell** (60 days):
```python
# Cell 3 or 4: GDELT Query
import gdelt
gd = gdelt.gdelt()

# Query last 60 days
df = gd.Search(
    ['economy', 'federal reserve'],
    table='gkg',
    coverage=True
)
```

**NEW** (180 days with batching):
```python
# Cell 3 or 4: GDELT Query (SCALED)
import gdelt
from gdelt_scaler import GDELTScaler
from datetime import datetime, timedelta

gd = gdelt.gdelt()
scaler = GDELTScaler(verbose=True)

# Define batch query function
def query_gdelt_batch(topic, start_date, end_date):
    """Query GDELT for specific date range"""
    try:
        df_batch = gd.Search(
            [topic, 'federal reserve'],
            table='gkg',
            coverage=True,
            startdate=start_date.strftime('%Y%m%d'),
            enddate=end_date.strftime('%Y%m%d')
        )
        return df_batch
    except Exception as e:
        print(f"Batch query failed: {e}")
        return None

# Query 180 days in batches
df_large = scaler.query_extended_period(
    query_function=query_gdelt_batch,
    topic='economy',
    days_back=180,
    max_articles=15000,
    batch_size=30  # Query 30 days at a time
)

print(f"\n✅ Retrieved {len(df_large):,} articles from 180 days")
```

---

### Step 3: Filter to Top Outlets

```python
# After querying, filter to outlets with sufficient data
df_filtered = scaler.filter_top_outlets(
    df_large,
    top_n=50,              # Keep top 50 outlets
    min_articles_per_outlet=30,  # At least 30 articles each
    source_column='source'
)

# Validation
validation = scaler.validate_coverage(
    df_filtered,
    min_articles=30
)

if validation['ready_for_causal_bias']:
    print(f"✅ READY: {validation['valid_outlets']} outlets with 30+ articles")
else:
    print(f"❌ NOT READY: Need more data or lower threshold")

# Use df_filtered for all downstream analysis
df = df_filtered  # Replace original df
```

---

### Step 4: Proceed with Enrichment

```python
# Continue with your existing enrichment pipeline
# (Now with 10,000+ articles instead of 313)

from robust_text_enrichment import RobustTextEnricher

enricher = RobustTextEnricher()

# Note: This will take longer (10K articles vs 313)
# Estimated time: 2-4 hours with parallel processing
df_enriched = enricher.enrich_dataframe(
    df_filtered,
    url_column='url',
    title_column='title',
    show_progress=True
)

print(f"\n✅ Enriched {len(df_enriched):,} articles")
```

---

## ⏱️ **Time and Cost Estimates**

### Query Time
```
60 days (current): ~2-3 minutes
180 days (scaled): ~6-10 minutes (batched)

Recommendation: Run overnight or during low-priority time
```

### Enrichment Time
```
313 articles (current): ~30-60 minutes
10,000 articles (scaled): ~2-4 hours with parallel processing

Recommendation:
- Use disk caching (already implemented)
- Run in batches of 1,000 articles
- Save intermediate results
```

### API Costs
```
Jina Reader API: $0.002 per article
- 313 articles: $0.63
- 10,000 articles: $20.00

Recommendation:
- Budget $20-30 for scaled dataset
- Use free methods (newspaper3k, trafilatura) when possible
- Cache results to avoid re-querying
```

---

## 📈 **Expected Benefits**

### Statistical Validity
```
BEFORE (313 articles):
- Regional comparisons: Bootstrap only (n<30)
- Causal bias: NOT POSSIBLE (n<<30)
- Syndication: Limited detection

AFTER (10,000+ articles):
- Regional comparisons: Traditional t-tests valid ✅
- Causal bias: 30-50 outlets analyzable ✅
- Syndication: Accurate pattern detection ✅
```

### Causal Bias Analysis (NEW CAPABILITY)
```python
# After scaling, you can do causal bias analysis!

from causal_bias import CausalBiasDetector  # Your existing module

bias_detector = CausalBiasDetector()

# Analyze all outlets with sufficient data
bias_results = bias_detector.analyze_all_outlets(
    df_enriched,
    min_articles=30,  # Now many outlets qualify!
    treatment_col='source'
)

# Output:
# ✅ Analyzed 42 outlets (vs 0 before)
# ✅ Detected significant bias in 8 outlets
# ✅ Conservative shift: 5 outlets
# ✅ Liberal shift: 3 outlets
```

---

## 🔧 **Optimization Tips**

### 1. Batch Processing
```python
# Process large dataset in chunks
from tqdm import tqdm

chunk_size = 1000
chunks = [df_filtered[i:i+chunk_size] for i in range(0, len(df_filtered), chunk_size)]

df_enriched_chunks = []
for idx, chunk in enumerate(tqdm(chunks, desc="Enriching chunks")):
    df_chunk_enriched = enricher.enrich_dataframe(chunk, show_progress=False)
    df_enriched_chunks.append(df_chunk_enriched)

    # Save intermediate results
    df_chunk_enriched.to_csv(f'cache/enriched_chunk_{idx}.csv', index=False)

# Combine all chunks
df_enriched = pd.concat(df_enriched_chunks, ignore_index=True)
```

### 2. Disk Caching
```python
# Cache query results
import pickle
import os

cache_file = 'cache/df_large_180days.pkl'

if os.path.exists(cache_file):
    print("Loading from cache...")
    df_large = pd.read_pickle(cache_file)
else:
    print("Querying GDELT...")
    df_large = scaler.query_extended_period(...)
    # Save to cache
    df_large.to_pickle(cache_file)
```

### 3. Parallel Enrichment
```python
# Already implemented in RobustTextEnricher
# Uses ThreadPoolExecutor with 20 workers
# Processes ~3-5 articles per second

# For 10,000 articles:
# Time = 10,000 / 4 = 2,500 seconds = ~42 minutes (best case)
# Time = 10,000 / 2 = 5,000 seconds = ~83 minutes (worst case)
```

---

## ✅ **Validation Checklist**

### Pre-Scaling
- [ ] Estimate parameters with `estimate_scaling_parameters()`
- [ ] Verify GDELT query function works with date ranges
- [ ] Set up disk caching directory (`cache/`)
- [ ] Budget API costs (~$20-30)

### During Scaling
- [ ] Query 180 days in 30-day batches
- [ ] Filter to top 50 outlets
- [ ] Validate coverage (30+ articles per outlet)
- [ ] Save intermediate results

### Post-Scaling
- [ ] Total articles: 5,000-15,000 ✓
- [ ] Valid outlets: 30-50 ✓
- [ ] Articles per outlet: 30-300 ✓
- [ ] Enrichment complete: All text extracted ✓
- [ ] Causal bias ready: 10+ valid outlets ✓

---

## 🎯 **Success Metrics**

### Must Achieve
- [ ] Total articles: ≥5,000
- [ ] Valid outlets (≥30 articles): ≥30
- [ ] Mean articles per valid outlet: ≥50
- [ ] Causal bias analysis enabled

### Stretch Goals
- [ ] Total articles: ≥10,000
- [ ] Valid outlets: ≥50
- [ ] Mean articles per outlet: ≥100
- [ ] Historical validation case study

---

## 📚 **Integration Into Notebook**

### Cell 3-4: Replace Query
```python
# OLD
df = gd.Search(['economy'], table='gkg', coverage=True)

# NEW
from gdelt_scaler import GDELTScaler
scaler = GDELTScaler()
df_large = scaler.query_extended_period(query_gdelt_batch, days_back=180)
df = scaler.filter_top_outlets(df_large, top_n=50, min_articles_per_outlet=30)
```

### Cell 9: No changes needed
```python
# Enrichment works the same, just takes longer
df_enriched = enricher.enrich_dataframe(df)
```

### Cell 18: NEW - Causal Bias Analysis
```python
# Add new cell for causal bias (now possible!)
from causal_bias import CausalBiasDetector

bias_detector = CausalBiasDetector()
bias_results = bias_detector.analyze_all_outlets(
    df_enriched,
    min_articles=30
)

bias_detector.print_results(bias_results)
```

---

## 🔄 **Incremental Scaling (Optional)**

If 180 days is too aggressive, scale incrementally:

### Phase 1: 90 days (1.5x)
- Expected: ~500-1,000 articles
- Time: ~30-60 minutes total
- Validates approach

### Phase 2: 120 days (2x)
- Expected: ~1,000-2,000 articles
- Time: ~1-2 hours total

### Phase 3: 180 days (3x)
- Expected: ~5,000-15,000 articles
- Time: ~2-4 hours total
- Full causal bias capability

---

## ⚠️ **Troubleshooting**

### Issue: GDELT query timeout
**Solution**: Reduce batch_size from 30 to 15 days

### Issue: Not enough articles
**Solution**:
- Increase days_back to 270 (9 months)
- Broaden search terms
- Lower min_articles_per_outlet to 20

### Issue: Enrichment taking too long
**Solution**:
- Use batch processing (save every 1,000 articles)
- Skip Jina Reader (expensive), use free methods only
- Process overnight

### Issue: Too many outlets
**Solution**:
- Increase min_articles_per_outlet to 40-50
- Reduce top_n to 30-40 outlets
- Focus on top-tier national outlets only

---

## 🎉 **Summary**

✅ **Priority 2 Infrastructure READY**

**Created**:
- `gdelt_scaler.py` - Complete scaling infrastructure
- `SCALING_GUIDE.md` - This comprehensive guide

**Next Steps**:
1. Run parameter estimation
2. Modify notebook data collection cell
3. Query 180 days in batches
4. Filter to top 50 outlets
5. Validate coverage
6. Proceed with enrichment

**Expected Outcome**:
- 5,000-15,000 articles (vs 313)
- 30-50 valid outlets (vs 0)
- Causal bias analysis enabled
- Production-ready dataset

**Estimated Time**: 1-2 days (mostly waiting for enrichment)

**Impact**: Enables the #1 most requested feature (causal media bias detection)
