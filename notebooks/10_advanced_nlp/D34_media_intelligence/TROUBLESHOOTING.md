# Troubleshooting Guide - GDELT Media Intelligence Notebook

## Common Issues and Solutions

### Issue 1: "ModuleNotFoundError: No module named 'krl_data_connectors'"

**Symptom:**
```
ModuleNotFoundError: No module named 'krl_data_connectors'
RuntimeError: GDELT connector required but not found
```

**Cause:** The krl-data-connectors package is not installed or not in Python's path.

**Solutions:**

#### Option 1: Run Installation Cell Again
1. **Restart the kernel** (Kernel → Restart Kernel)
2. **Run Cell 2** (Configuration)
3. **Run Cell 3** (Installation) - Watch for success messages
4. **Run Cell 4** (Imports)

The installation cell should output:
```
✓ krl-data-connectors ready at: /path/to/krl-data-connectors
```

#### Option 2: Manual Installation
If Cell 3 fails, install manually:

```bash
# In a terminal
cd "/Users/bcdelo/Documents/GitHub/KRL/Private IP/krl-data-connectors"
pip install -e .
```

Then restart the kernel and run from Cell 2.

#### Option 3: Update Paths
If krl-data-connectors is in a different location:

1. Edit **Cell 3** (Installation cell)
2. Update the `possible_paths` list with your actual path:
   ```python
   possible_paths = [
       Path("/YOUR/ACTUAL/PATH/krl-data-connectors"),
       # ... other paths
   ]
   ```
3. Restart kernel and run from Cell 2

---

### Issue 2: GDELT API Returns No Results

**Symptom:**
```
ValueError: No articles returned from GDELT API
```

**Causes:**
- Query too specific (no matches in timespan)
- GDELT service temporarily down
- Network connectivity issue

**Solutions:**

#### Broaden Your Query
Try a more general query:
```python
# Instead of:
QUERY = 'very specific niche topic AND sourcelang:eng'

# Try:
QUERY = 'labor strikes'  # Simpler
# or
QUERY = 'healthcare'
```

#### Extend Timespan
```python
# Instead of:
TIMESPAN_DAYS = 7

# Try:
TIMESPAN_DAYS = 21  # More days = more articles
```

#### Test GDELT Service
Visit https://api.gdeltproject.org/api/v2/doc/doc to verify service is up.

---

### Issue 3: Data Quality Validation Failed

**Symptom:**
```
ValueError: Data quality validation failed. Cannot proceed with analysis.
```

**Causes:**
- Not enough articles returned
- Too few English articles
- Missing required data

**Solutions:**

#### Lower Quality Thresholds
Edit **Cell 2** (Configuration):
```python
MIN_ARTICLES = 10      # Instead of 30
MIN_ENGLISH_PCT = 0.50  # Instead of 0.70
```

#### Add Language Filter to Query
```python
QUERY = 'your topic AND sourcelang:eng'  # Ensures English results
```

#### Check Validation Output
The validation cell shows specific errors:
- "Only X articles (minimum: Y)" → Broaden query or extend timespan
- "Only X% English articles" → Add `sourcelang:eng` to query

---

### Issue 4: NLTK Download Errors

**Symptom:**
```
LookupError: Resource 'punkt' not found
LookupError: Resource 'vader_lexicon' not found
```

**Solution:**

Run this in a code cell:
```python
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')
```

Or download all:
```python
import nltk
nltk.download('all')  # Downloads everything (may take a while)
```

---

### Issue 5: Visualization Not Showing

**Symptom:**
- Plots don't appear
- Only text output visible

**Solutions:**

#### For Jupyter Lab
```bash
# Install plotly extension
jupyter labextension install jupyterlab-plotly
```

#### For Jupyter Notebook
Plotly should work out of the box. If not:
```python
import plotly.io as pio
pio.renderers.default = "notebook"  # Add to imports cell
```

#### Switch to Matplotlib
Edit **Cell 2** (Configuration):
```python
INTERACTIVE_PLOTS = False  # Use matplotlib instead of plotly
```

---

### Issue 6: "Private IP" Path Not Found

**Symptom:**
```
Could not find krl-data-connectors in workspace
```

**Cause:** The "Private IP" folder name has a space, which can cause path issues.

**Solutions:**

#### Use Full Quoted Path
In **Cell 3**, ensure paths use `Path()` constructor:
```python
Path("/Users/bcdelo/Documents/GitHub/KRL/Private IP/krl-data-connectors")
```

#### Or Rename Folder (Optional)
```bash
# In terminal
cd /Users/bcdelo/Documents/GitHub/KRL
mv "Private IP" Private_IP
```

Then update paths in Cell 3:
```python
Path("/Users/bcdelo/Documents/GitHub/KRL/Private_IP/krl-data-connectors")
```

---

### Issue 7: Kernel Crashes or Memory Error

**Symptom:**
- Kernel dies during processing
- "Memory error" or "Killed"

**Solutions:**

#### Reduce Dataset Size
Edit **Cell 2**:
```python
MAX_ARTICLES = 100     # Instead of 250
TIMESPAN_DAYS = 3      # Instead of 7
```

#### Restart Kernel
Kernel → Restart Kernel & Clear All Outputs

#### Close Other Notebooks
If running multiple notebooks, close unused ones to free memory.

---

### Issue 8: Topic Modeling Errors

**Symptom:**
```
ValueError: n_samples=X should be >= n_clusters=Y
ValueError: Vocabulary size too small
```

**Causes:**
- Not enough articles for the number of topics
- Very short titles with few unique words

**Solutions:**

#### Reduce Number of Topics
In **Cell 8** (Topic Modeling), change:
```python
n_topics = 3  # Instead of 5
```

#### Broaden Query
Get more articles with more diverse vocabulary:
```python
TIMESPAN_DAYS = 14  # More days
QUERY = 'broader topic'  # Less specific
```

#### Adjust Vectorizer Parameters
In **Cell 8**:
```python
vectorizer = CountVectorizer(
    max_features=200,  # Instead of 500
    min_df=1,          # Instead of 2 (less strict)
    max_df=0.9,        # Instead of 0.8
    ngram_range=(1, 1)  # Only unigrams (simpler)
)
```

---

## Verification Checklist

Before running the full notebook, verify:

- [ ] **krl-data-connectors installed**
  - Cell 3 shows: `✓ krl-data-connectors ready at: /path/...`

- [ ] **GDELT connector imports successfully**
  - Cell 4 shows: `✓ GDELT connector imported successfully`

- [ ] **Configuration makes sense**
  - Query is not overly specific
  - Timespan is reasonable (7-21 days)
  - Thresholds are achievable

- [ ] **NLTK resources downloaded**
  - Cell 4 completes without errors

If all checkmarks pass, the notebook should run successfully.

---

## Still Having Issues?

### Check Your Environment

```python
# Run in a code cell to check versions
import sys
import pandas as pd
import sklearn
import nltk
import plotly

print(f"Python: {sys.version}")
print(f"Pandas: {pd.__version__}")
print(f"Scikit-learn: {sklearn.__version__}")
print(f"NLTK: {nltk.__version__}")
print(f"Plotly: {plotly.__version__}")
```

**Minimum Requirements:**
- Python 3.8+
- Pandas 1.3+
- Scikit-learn 1.0+
- NLTK 3.6+
- Plotly 5.0+

### Get Detailed Error Info

Add to the top of any failing cell:
```python
import traceback
try:
    # ... your code ...
except Exception as e:
    traceback.print_exc()
    raise
```

This shows the full error stack trace.

---

## Quick Reset Procedure

If everything is broken and you want to start fresh:

1. **Kernel → Restart Kernel & Clear All Outputs**
2. **Run Cell 2** (Configuration)
3. **Run Cell 3** (Installation) - Watch for errors
4. **Run Cell 4** (Imports) - Should succeed if Cell 3 worked
5. **Run All Below** (Cell → Run All Below)

If Cell 4 fails, the issue is with krl-data-connectors installation.

---

## Getting Help

If none of these solutions work:

1. **Note the exact error message** (copy/paste the full traceback)
2. **Note which cell failed** (Cell number)
3. **Check krl-data-connectors repository** for issues/updates
4. **Verify GDELT service status** at https://www.gdeltproject.org/

Common patterns:
- Cell 3 fails → Installation/path problem
- Cell 4 fails → Import problem
- Cell 5 fails → GDELT API/network problem
- Cell 6+ fails → Data quality or analysis problem
