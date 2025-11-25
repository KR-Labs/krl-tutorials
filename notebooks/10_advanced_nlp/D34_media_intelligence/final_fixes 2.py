"""
Final Fixes After Restructuring
1. Add missing enrichment header
2. Add adaptive sentiment code
3. Update clustering to use enriched text
"""

import json
import shutil
from datetime import datetime

# Backup
backup_path = f'spatial_media_intelligence_demo.ipynb.backup.final.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
shutil.copy('spatial_media_intelligence_demo.ipynb', backup_path)
print(f"✅ Created backup: {backup_path}")

# Read notebook
with open('spatial_media_intelligence_demo.ipynb', 'r') as f:
    nb = json.load(f)

cells = nb['cells']
print(f"\n📊 Current: {len(cells)} cells")

# ============================================================================
# FIX 1: Add enrichment header before cell 8
# ============================================================================

print(f"\n🔧 FIX 1: Adding enrichment header...")

enrichment_header = {
    "cell_type": "markdown",
    "id": "enrichment-header",
    "metadata": {},
    "source": [
        "## Part 8: Robust Full-Text Enrichment (UPGRADED)\n",
        "\n",
        "**New**: Multi-method fallback chain for 85%+ success rate:\n",
        "1. **Jina Reader API** (primary, handles paywalls)\n",
        "2. **Newspaper3k** (fallback #1)\n",
        "3. **Trafilatura** (fallback #2)\n",
        "4. **BeautifulSoup** (last resort)\n",
        "\n",
        "This creates the `text_for_clustering` field used in spatial-semantic analysis."
    ]
}

# Insert before cell 8
cells.insert(8, enrichment_header)
print(f"   ✓ Inserted enrichment header at position 8")

# ============================================================================
# FIX 2: Add adaptive sentiment to cell 11 (was 10, now 11 after insert)
# ============================================================================

print(f"\n🔧 FIX 2: Adding adaptive sentiment code to cell 11...")

# Cell 11 is the sentiment code (was 10, shifted by 1 after insert)
sentiment_cell = cells[11]
source = ''.join(sentiment_cell['source'])

# Add adaptive sentiment code after df_sentiment creation
adaptive_code = '''

    # ADAPTIVE SENTIMENT THRESHOLDS (Fix for 83% neutral problem)
    # Instead of fixed thresholds (±0.1), use data-driven thresholds
    scores = df_sentiment['sentiment_deep_score']
    score_std = scores.std()
    score_mean = scores.mean()

    # Use adaptive thresholds: 0.5 standard deviations from mean
    pos_threshold = score_mean + (0.5 * score_std)
    neg_threshold = score_mean - (0.5 * score_std)

    def adaptive_classify(score):
        """Classify sentiment using adaptive thresholds"""
        if score > pos_threshold:
            return 'positive'
        elif score < neg_threshold:
            return 'negative'
        else:
            return 'neutral'

    df_sentiment['sentiment_adaptive'] = df_sentiment['sentiment_deep_score'].apply(adaptive_classify)

    # Compare distributions
    print(f"\\n📊 Sentiment Distribution Comparison:")
    print(f"\\nFixed thresholds (±0.1):")
    if 'sentiment_deep' in df_sentiment.columns:
        print(df_sentiment['sentiment_deep'].value_counts())
    print(f"\\nAdaptive thresholds (μ ± 0.5σ):")
    print(df_sentiment['sentiment_adaptive'].value_counts())
    print(f"\\nThresholds: negative < {neg_threshold:.3f}, positive > {pos_threshold:.3f}")
'''

# Insert before "else:" or at end of if block
if 'else:' in source:
    # Insert before the else block
    parts = source.split('else:')
    new_source = parts[0] + adaptive_code + '\nelse:' + parts[1]
else:
    # Just append before end
    new_source = source + adaptive_code

cells[11]['source'] = new_source.split('\n')
print(f"   ✓ Added adaptive sentiment code to cell 11")

# ============================================================================
# FIX 3: Update clustering cells to use enriched text
# ============================================================================

print(f"\n🔧 FIX 3: Updating clustering cells...")

for i, cell in enumerate(cells):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])

        # Look for clustering code
        if 'SpatialClusterer' in source and 'fit_predict' in source:
            original = source

            # Replace text_column='title' with text_column='text_for_clustering'
            source = source.replace("text_column='title'", "text_column='text_for_clustering'")
            source = source.replace('text_column="title"', 'text_column="text_for_clustering"')

            # Also update any references to df[['title']]
            source = source.replace("df[['title']]", "df[['text_for_clustering']]")
            source = source.replace('df[["title"]]', 'df[["text_for_clustering"]]')

            if source != original:
                cells[i]['source'] = source.split('\n')
                print(f"   ✓ Updated clustering cell {i} to use text_for_clustering")

# ============================================================================
# FIX 4: Update cell IDs
# ============================================================================

for i, cell in enumerate(cells):
    if 'id' in cell:
        cell['id'] = f"cell-{i}"

# ============================================================================
# Save
# ============================================================================

nb['cells'] = cells

with open('spatial_media_intelligence_demo.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print(f"\n✅ Final fixes applied!")
print(f"\n📊 Summary:")
print(f"   • Total cells: {len(cells)}")
print(f"   • Added enrichment header")
print(f"   • Added adaptive sentiment code")
print(f"   • Updated clustering to use enriched text")

print(f"\n💾 Backup: {backup_path}")

print(f"\n🎯 Next: Run verification script to confirm all fixes")
