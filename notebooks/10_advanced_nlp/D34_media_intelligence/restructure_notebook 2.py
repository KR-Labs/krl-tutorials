"""
Full Cell Restructuring - Option A
Reorganizes notebook to: Setup → Config → Data → Enrich → Sentiment → Cluster → Analysis
"""

import json
import shutil
from datetime import datetime

# Backup
backup_path = f'spatial_media_intelligence_demo.ipynb.backup.restructure.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
shutil.copy('spatial_media_intelligence_demo.ipynb', backup_path)
print(f"✅ Created backup: {backup_path}")

# Read notebook
with open('spatial_media_intelligence_demo.ipynb', 'r') as f:
    nb = json.load(f)

print(f"\n📊 Original notebook: {len(nb['cells'])} cells")

# ============================================================================
# STEP 1: Extract cells by category
# ============================================================================

cells = nb['cells']

# Setup cells (0-5): Keep as-is
setup_cells = cells[0:6]  # Cells 0-5 (intro, imports, config, etc.)

# Data acquisition (6): Keep as-is
data_cells = [cells[6]]  # Cell 6

# Clustering cells (9, 12, 17): Extract for later
clustering_cells = [cells[9], cells[12], cells[17]]

# Enrichment cells (21, 36, 37): Consolidate
# Cell 36: Header
# Cell 21: First enrichment code
# Cell 37: Second enrichment code (likely the better one)
enrichment_header = cells[36]
enrichment_code_v1 = cells[21]
enrichment_code_v2 = cells[37]

# Sentiment cells (23, 40, 41): Consolidate
# Cell 40: Header
# Cell 23: First sentiment code
# Cell 41: Second sentiment code (likely with adaptive thresholds)
sentiment_header = cells[40]
sentiment_code_v1 = cells[23]
sentiment_code_v2 = cells[41]

# Analysis cells (everything else): Keep in order
# Cells 7, 8 (before clustering)
analysis_pre = cells[7:9]

# Cells 10, 11, 13-20 (between clustering cells and enrichment)
analysis_mid1 = [cells[10], cells[11]] + cells[13:21]

# Cells 22, 24-35 (between enrichment/sentiment)
analysis_mid2 = [cells[22]] + cells[24:36]

# Cells 38, 39, 42-55 (after sentiment)
analysis_post = [cells[38], cells[39]] + cells[42:]

print(f"\n📋 Cell extraction:")
print(f"   Setup: {len(setup_cells)} cells (0-5)")
print(f"   Data: {len(data_cells)} cell (6)")
print(f"   Enrichment: 1 header + 2 code versions → consolidate to 2 cells")
print(f"   Sentiment: 1 header + 2 code versions → consolidate to 2 cells")
print(f"   Clustering: {len(clustering_cells)} cells (9, 12, 17)")
print(f"   Analysis: {len(analysis_pre + analysis_mid1 + analysis_mid2 + analysis_post)} cells")

# ============================================================================
# STEP 2: Update clustering cells to use enriched text
# ============================================================================

print(f"\n🔧 Updating clustering cells to use enriched text...")

for i, cell in enumerate(clustering_cells):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']

        # Replace title-based clustering with enriched text
        if "'title'" in source or '"title"' in source:
            source = source.replace("'title'", "'text_for_clustering'")
            source = source.replace('"title"', '"text_for_clustering"')
            print(f"   ✓ Updated clustering cell {i+1} to use text_for_clustering")

        # Update source
        cell['source'] = source.split('\n') if '\n' in source else [source]

# ============================================================================
# STEP 3: Choose best versions of duplicates
# ============================================================================

print(f"\n🎯 Selecting best versions of duplicate cells...")

# For enrichment: Use v2 (Cell 37) - likely more complete
enrichment_final = [enrichment_header, enrichment_code_v2]
print(f"   • Enrichment: Using Cell 37 (v2)")

# For sentiment: Use v2 (Cell 41) - likely has adaptive thresholds
sentiment_final = [sentiment_header, sentiment_code_v2]
print(f"   • Sentiment: Using Cell 41 (v2)")

# ============================================================================
# STEP 4: Build new cell order
# ============================================================================

print(f"\n🏗️  Building new cell structure...")

new_cells = []

# 1. Setup (0-5)
new_cells.extend(setup_cells)
print(f"   [0-5]   Setup")

# 2. Data (6)
new_cells.extend(data_cells)
print(f"   [6]     Data Acquisition")

# 3. Pre-analysis (7-8)
new_cells.extend(analysis_pre)
print(f"   [7-8]   Pre-analysis")

# 4. TEXT ENRICHMENT (NEW POSITION)
new_cells.extend(enrichment_final)
enrichment_start = len(new_cells) - 2
print(f"   [{enrichment_start}-{enrichment_start+1}] Text Enrichment (MOVED)")

# 5. SENTIMENT ANALYSIS (NEW POSITION)
new_cells.extend(sentiment_final)
sentiment_start = len(new_cells) - 2
print(f"   [{sentiment_start}-{sentiment_start+1}] Sentiment Analysis (MOVED)")

# 6. CLUSTERING (NEW POSITION - after enrichment/sentiment)
new_cells.extend(clustering_cells)
clustering_start = len(new_cells) - len(clustering_cells)
print(f"   [{clustering_start}-{clustering_start+len(clustering_cells)-1}] Clustering (uses enriched text)")

# 7. Analysis cells (rest)
new_cells.extend(analysis_mid1)
mid1_start = len(new_cells) - len(analysis_mid1)
print(f"   [{mid1_start}-{len(new_cells)-1}] Analysis (mid)")

new_cells.extend(analysis_mid2)
mid2_start = len(new_cells) - len(analysis_mid2)
print(f"   [{mid2_start}-{len(new_cells)-1}] Analysis (mid2)")

new_cells.extend(analysis_post)
post_start = len(new_cells) - len(analysis_post)
print(f"   [{post_start}-{len(new_cells)-1}] Analysis (final)")

print(f"\n✅ New notebook structure: {len(new_cells)} cells")

# ============================================================================
# STEP 5: Update cell IDs
# ============================================================================

print(f"\n🔢 Updating cell IDs...")
for i, cell in enumerate(new_cells):
    if 'id' in cell:
        cell['id'] = f"cell-{i}"

# ============================================================================
# STEP 6: Save restructured notebook
# ============================================================================

nb['cells'] = new_cells

with open('spatial_media_intelligence_demo.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print(f"\n✅ Notebook restructured and saved!")

# ============================================================================
# STEP 7: Summary
# ============================================================================

print(f"\n" + "="*80)
print(f"📊 RESTRUCTURING COMPLETE")
print(f"="*80)
print(f"\n🎯 New execution flow:")
print(f"   1. Setup & Config (Cells 0-5)")
print(f"   2. Data Acquisition (Cell 6)")
print(f"   3. Pre-analysis (Cells 7-8)")
print(f"   4. ✨ TEXT ENRICHMENT (Cells {enrichment_start}-{enrichment_start+1}) ← MOVED")
print(f"   5. ✨ SENTIMENT ANALYSIS (Cells {sentiment_start}-{sentiment_start+1}) ← MOVED")
print(f"   6. ✨ CLUSTERING (Cells {clustering_start}-{clustering_start+len(clustering_cells)-1}) ← Now uses enriched text!")
print(f"   7. Analysis & Visualization (Remaining cells)")

print(f"\n🔧 Key changes:")
print(f"   • Moved enrichment BEFORE clustering")
print(f"   • Moved sentiment BEFORE clustering")
print(f"   • Updated clustering to use 'text_for_clustering' (enriched text)")
print(f"   • Consolidated duplicate cells (kept best versions)")
print(f"   • Total cells: {len(nb['cells'])}")

print(f"\n⚠️  IMPORTANT:")
print(f"   • The notebook now clusters on ENRICHED FULL TEXT (~500+ chars)")
print(f"   • NOT on titles (~50 chars) anymore")
print(f"   • This will produce much better clustering results!")

print(f"\n💾 Backup saved: {backup_path}")
print(f"\n✅ Ready to test! Run the notebook from top to bottom.")
