"""
Apply ALL 6 Fixes in One Script
This ensures all changes are persisted to the notebook file
"""

import json
import shutil
from datetime import datetime

print("="*80)
print("APPLYING ALL 6 TECHNICAL FIXES TO NOTEBOOK")
print("="*80)

# Backup
backup_path = f'spatial_media_intelligence_demo.ipynb.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
shutil.copy('spatial_media_intelligence_demo.ipynb', backup_path)
print(f"\n✅ Backup created: {backup_path}\n")

# Read notebook
with open('spatial_media_intelligence_demo.ipynb', 'r') as f:
    nb = json.load(f)

print(f"📊 Current notebook: {len(nb['cells'])} cells\n")

changes_made = []

# ============================================================================
# FIX 1: Update Cell 5 to use config.py
# ============================================================================
print("🔧 FIX 1: Updating configuration cell...")

config_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "from config import NotebookConfig, STANDARD_ANALYSIS\n",
        "\n",
        "# Use standard analysis preset\n",
        "config = STANDARD_ANALYSIS\n",
        "config.display()\n",
        "\n",
        "# Export variables for backward compatibility\n",
        "TOPIC = config.topic\n",
        "DAYS_BACK = config.days_back\n",
        "MAX_ARTICLES = config.max_articles\n",
        "SPATIAL_WEIGHT = config.spatial_weight\n",
        "DISTANCE_THRESHOLD = config.distance_threshold\n",
        "ENABLE_TEXT_ENRICHMENT = config.enable_text_enrichment\n",
        "MAX_ARTICLES_TO_ENRICH = config.max_articles_to_enrich\n",
        "ENABLE_ADVANCED_SENTIMENT = config.enable_advanced_sentiment\n",
        "ENABLE_CAUSAL_BIAS = config.enable_causal_bias\n",
        "ENABLE_ADVANCED_VIZ = config.enable_advanced_viz\n",
        "MIN_ARTICLES_PER_OUTLET = config.min_articles_per_outlet"
    ]
}

nb['cells'][5] = config_cell
changes_made.append("✅ Fix 1: Cell 5 now uses config.py")
print("   ✅ Cell 5 updated to import and use config.py\n")

# ============================================================================
# FIX 2: Update Cell 0 (Introduction) with honest language
# ============================================================================
print("🔧 FIX 2: Updating main introduction...")

new_intro = """# Spatial Media Intelligence: GDELT-Based Policy Analysis

**Author**: Brandon DeLo
**Date**: November 2025
**Project**: Khipu Media Intelligence Platform

---

## Overview

This notebook demonstrates a **policy analysis tool** that combines:
- **Semantic embeddings** (NLP-based text similarity)
- **Geographic coordinates** (spatial distance)
- **Empirically optimized weighting**: λ_spatial = 0.15

### Key Innovation

Traditional media monitoring tools (Meltwater, Brandwatch) show:
- ❌ Volume over time
- ❌ Generic sentiment analysis
- ❌ **Zero spatial awareness**

Our platform reveals:
- ✅ **Regional narrative patterns** (how coverage differs by location)
- ✅ **Geographic clustering** (which locations frame stories similarly)
- ✅ **Early warning signals** (detect emerging regional patterns)

### Value Proposition

**For**: Policy analysts at think tanks and advocacy organizations
**Who**: Need to understand regional variation in policy reception
**Our Tool**: Combines GDELT's global news database with spatial-semantic analysis
**Unlike**: Meltwater, Brandwatch (which lack geographic clustering)
**We Provide**: Automated identification of regional narrative patterns

**Pilot Pricing**: $10,000 (3 months, 5 custom analyses)

**Success Metric**: Can you identify potential sources of regional opposition
that you wouldn't have found with your current tools?

---"""

nb['cells'][0] = {
    "cell_type": "markdown",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": new_intro.split('\n')
}
changes_made.append("✅ Fix 2: Cell 0 introduction updated with honest framing")
print("   ✅ Cell 0 updated with honest value prop\n")

# ============================================================================
# FIX 3: Replace ALL instances of misleading language
# ============================================================================
print("🔧 FIX 3: Replacing misleading language throughout notebook...")

replacements = [
    ("patent-pending algorithm", "novel spatial-semantic clustering approach"),
    ("Patent-Pending Algorithm", "Novel Spatial-Semantic Clustering Approach"),
    ("PATENT-PENDING", "NOVEL"),
    ("trade secret parameter", "empirically optimized weighting factor"),
    ("Trade secret parameter", "Empirically optimized weighting factor"),
    ("Trade Secret Formula", "Clustering Formula"),
    ("trade secret", "empirically optimized"),
    ("$75,000/year", "$10,000 pilot (3 months)"),
    ("$75K/year", "$10K pilot"),
    ("Would you pay $75K/year", "Would you pay $10K for a 3-month pilot"),
]

language_changes = 0
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    original = source

    for old, new in replacements:
        source = source.replace(old, new)

    if source != original:
        cell['source'] = source.split('\n')
        nb['cells'][i] = cell
        language_changes += 1

changes_made.append(f"✅ Fix 3: Updated language in {language_changes} cells")
print(f"   ✅ Updated misleading language in {language_changes} cells\n")

# ============================================================================
# FIX 4: Add adaptive sentiment thresholds
# ============================================================================
print("🔧 FIX 4: Adding adaptive sentiment thresholds...")

# Find sentiment analysis cell
sentiment_cell_idx = None
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    if 'AdvancedSentimentAnalyzer' in source and 'analyze_dataframe' in source:
        sentiment_cell_idx = i
        break

if sentiment_cell_idx:
    adaptive_sentiment_code = """from advanced_sentiment import AdvancedSentimentAnalyzer

# Initialize sentiment analyzer
sentiment_analyzer = AdvancedSentimentAnalyzer()

# Analyze sentiment on full text (or titles if enrichment disabled)
if sentiment_analyzer.enabled:
    df_sentiment = sentiment_analyzer.analyze_dataframe(
        df_enriched if 'df_enriched' in locals() else df_clustered,
        text_column='full_text' if 'full_text' in (df_enriched if 'df_enriched' in locals() else df_clustered).columns else 'title',
        analyze_aspects=True
    )

    # ========================================================================
    # ADAPTIVE SENTIMENT THRESHOLDS (Fix for 83% neutral problem)
    # ========================================================================

    scores = df_sentiment['sentiment_deep_score']
    score_std = scores.std()
    score_mean = scores.mean()

    print(f"\\n📊 Sentiment Score Distribution:")
    print(f"   • Mean: {score_mean:.3f}")
    print(f"   • Std Dev: {score_std:.3f}")
    print(f"   • Range: [{scores.min():.3f}, {scores.max():.3f}]")

    # Use adaptive thresholds: 0.5 standard deviations from mean
    pos_threshold = score_mean + (0.5 * score_std)
    neg_threshold = score_mean - (0.5 * score_std)

    print(f"\\n🎯 Adaptive Thresholds (vs fixed ±0.1):")
    print(f"   • Positive if score > {pos_threshold:.3f}")
    print(f"   • Negative if score < {neg_threshold:.3f}")
    print(f"   • Neutral otherwise")

    # Reclassify with adaptive thresholds
    def adaptive_classify(score):
        if score > pos_threshold:
            return 'positive'
        elif score < neg_threshold:
            return 'negative'
        else:
            return 'neutral'

    df_sentiment['sentiment_adaptive'] = df_sentiment['sentiment_deep_score'].apply(adaptive_classify)

    # Compare distributions
    print(f"\\n📈 Classification Comparison:")
    print(f"\\nOriginal (fixed threshold ±0.1):")
    print(df_sentiment['sentiment_deep'].value_counts())
    print(f"\\nAdaptive (data-driven thresholds):")
    print(df_sentiment['sentiment_adaptive'].value_counts())

    # Use adaptive classification going forward
    df_sentiment['sentiment'] = df_sentiment['sentiment_adaptive']

    # Check if adaptive helped
    adaptive_neutral_pct = (df_sentiment['sentiment_adaptive'] == 'neutral').sum() / len(df_sentiment)
    if adaptive_neutral_pct < 0.7:
        print(f"\\n✅ Adaptive thresholds improved distribution!")
    else:
        print(f"\\n⚠️  Still {adaptive_neutral_pct*100:.1f}% neutral - topic may be genuinely neutral")

    print(f"\\n📊 Sentiment Analysis Complete:")
    print(f"   Articles analyzed: {len(df_sentiment)}")
    print(f"   Average sentiment: {df_sentiment['sentiment_deep_score'].mean():.3f}")
else:
    print("\\n⚠️  Sentiment model not available")
    df_sentiment = df_enriched.copy() if 'df_enriched' in locals() else df_clustered.copy()
"""

    nb['cells'][sentiment_cell_idx] = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": adaptive_sentiment_code.split('\n')
    }
    changes_made.append(f"✅ Fix 4: Cell {sentiment_cell_idx} now uses adaptive sentiment thresholds")
    print(f"   ✅ Cell {sentiment_cell_idx} updated with adaptive thresholds\n")
else:
    print("   ⚠️  Could not find sentiment cell to update\n")

# ============================================================================
# FIX 5: Lower causal bias threshold from 5 to 2
# ============================================================================
print("🔧 FIX 5: Lowering causal bias minimum articles...")

for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))

    if 'analyze_all_outlets' in source and 'min_articles' in source:
        # Replace hardcoded 5 with MIN_ARTICLES_PER_OUTLET
        source = source.replace('min_articles=5', 'min_articles=MIN_ARTICLES_PER_OUTLET')

        # Add comment if not present
        if 'LOWERED' not in source and 'MIN_ARTICLES_PER_OUTLET' in source:
            source = source.replace(
                'bias_results = bias_detector.analyze_all_outlets(',
                '# LOWERED from 5 to 2 to enable analysis with smaller datasets\n' +
                'bias_results = bias_detector.analyze_all_outlets('
            )

        cell['source'] = source.split('\n')
        nb['cells'][i] = cell
        changes_made.append(f"✅ Fix 5: Cell {i} causal bias threshold lowered to MIN_ARTICLES_PER_OUTLET (2)")
        print(f"   ✅ Cell {i} updated: min_articles now uses config (default: 2)\n")
        break

# ============================================================================
# FIX 6: Fix treemap bug with data aggregation
# ============================================================================
print("🔧 FIX 6: Fixing treemap duplicate cluster bug...")

treemap_fixed = 0
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))

    if 'create_treemap_hierarchical' in source and 'fig_treemap' in source:
        fixed_treemap = """# Create Treemap (with duplicate prevention fix)
if ENABLE_ADVANCED_VIZ:
    try:
        print("\\n🌳 Creating treemap...")

        # FIX: Aggregate data first to prevent duplicates
        treemap_data = df_clustered.groupby(['cluster', 'location']).agg({
            'sentiment_score': 'mean' if 'sentiment_score' in df_clustered.columns else 'size',
            'cluster': 'size'
        }).reset_index()

        if 'sentiment_score' in df_clustered.columns:
            treemap_data = treemap_data.rename(columns={'sentiment_score': 'avg_sentiment', 'cluster': 'count'})
        else:
            treemap_data.columns = ['cluster', 'location', 'count']
            treemap_data['avg_sentiment'] = 0

        print(f"   • Aggregated to {len(treemap_data)} unique cluster-location pairs")

        # Create treemap with validated data
        fig_treemap = advanced_viz.create_treemap_hierarchical(
            treemap_data,
            cluster_col='cluster',
            location_col='location',
            sentiment_col='avg_sentiment',
            sentiment_score_col='avg_sentiment',
            title='Hierarchical Regional Narrative Structure'
        )

        fig_treemap.show()
        print("\\n💡 Treemap created successfully")

    except Exception as e:
        print(f"\\n⚠️  Could not create Treemap: {e}")
        print("   Creating fallback visualization...")

        import plotly.express as px
        cluster_sizes = df_clustered['cluster'].value_counts().reset_index()
        cluster_sizes.columns = ['cluster', 'count']

        fig_simple = px.bar(
            cluster_sizes,
            x='cluster',
            y='count',
            title='Cluster Distribution (Fallback)'
        )
        fig_simple.show()
else:
    print("⏭️  Treemap skipped (advanced viz disabled)")
"""

        cell['source'] = fixed_treemap.split('\n')
        nb['cells'][i] = cell
        treemap_fixed += 1
        print(f"   ✅ Cell {i} treemap fixed with data aggregation")

changes_made.append(f"✅ Fix 6: Fixed {treemap_fixed} treemap cells")
print(f"   Total treemap cells fixed: {treemap_fixed}\n")

# ============================================================================
# Update cell IDs and save
# ============================================================================
for i, cell in enumerate(nb['cells']):
    if 'id' in cell:
        cell['id'] = f"cell-{i}"

# Save
with open('spatial_media_intelligence_demo.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print("="*80)
print("✅ ALL FIXES APPLIED AND SAVED")
print("="*80)
print(f"\nChanges made:")
for change in changes_made:
    print(f"   {change}")

print(f"\n📁 Backup saved: {backup_path}")
print(f"📊 Notebook cells: {len(nb['cells'])}")
print("\n✅ Ready to reload notebook and test!")
print("="*80)
