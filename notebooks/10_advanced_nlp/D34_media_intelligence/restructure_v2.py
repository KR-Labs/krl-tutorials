"""
Full Cell Restructuring - V2 (Better Approach)
Instead of rebuilding, we'll:
1. Mark cells to remove (duplicates)
2. Reorder remaining cells
3. Update clustering to use enriched text
"""

import json
import shutil
from datetime import datetime

# Backup
backup_path = f'spatial_media_intelligence_demo.ipynb.backup.restructure_v2.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
shutil.copy('spatial_media_intelligence_demo.ipynb', backup_path)
print(f"✅ Created backup: {backup_path}")

# Read notebook
with open('spatial_media_intelligence_demo.ipynb', 'r') as f:
    nb = json.load(f)

cells = nb['cells']
print(f"\n📊 Original notebook: {len(cells)} cells")

# ============================================================================
# STEP 1: Map all cells
# ============================================================================

print(f"\n📋 Mapping cells...")

cell_map = {}
for i, cell in enumerate(cells):
    source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']

    # Identify cell type
    if cell['cell_type'] == 'markdown':
        if 'Part 8' in source and 'Full-Text Enrichment' in source:
            cell_map[i] = 'enrichment_header'
            print(f"   Cell {i}: Enrichment Header")
        elif 'Part 9' in source and 'Sentiment' in source:
            cell_map[i] = 'sentiment_header'
            print(f"   Cell {i}: Sentiment Header")
    elif cell['cell_type'] == 'code':
        if 'RobustTextEnricher' in source or 'text_enricher' in source:
            cell_map[i] = 'enrichment_code'
            print(f"   Cell {i}: Enrichment Code")
        elif 'AdvancedSentimentAnalyzer' in source:
            cell_map[i] = 'sentiment_code'
            print(f"   Cell {i}: Sentiment Code")
        elif 'SpatialClusterer' in source and 'fit_predict' in source:
            cell_map[i] = 'clustering_code'
            print(f"   Cell {i}: Clustering Code")

# ============================================================================
# STEP 2: Identify duplicates and choose which to keep
# ============================================================================

enrichment_headers = [i for i, t in cell_map.items() if t == 'enrichment_header']
enrichment_codes = [i for i, t in cell_map.items() if t == 'enrichment_code']
sentiment_headers = [i for i, t in cell_map.items() if t == 'sentiment_header']
sentiment_codes = [i for i, t in cell_map.items() if t == 'sentiment_code']
clustering_codes = [i for i, t in cell_map.items() if t == 'clustering_code']

print(f"\n📊 Found:")
print(f"   Enrichment headers: {enrichment_headers}")
print(f"   Enrichment codes: {enrichment_codes}")
print(f"   Sentiment headers: {sentiment_headers}")
print(f"   Sentiment codes: {sentiment_codes}")
print(f"   Clustering codes: {clustering_codes}")

# Choose which to keep (keep the later ones, as they likely have fixes)
keep_enrichment_header = max(enrichment_headers) if enrichment_headers else None
keep_enrichment_code = max(enrichment_codes) if enrichment_codes else None
keep_sentiment_header = max(sentiment_headers) if sentiment_headers else None
keep_sentiment_code = max(sentiment_codes) if sentiment_codes else None

# Mark cells to DELETE (the earlier duplicates)
cells_to_delete = []

for h in enrichment_headers:
    if h != keep_enrichment_header:
        cells_to_delete.append(h)
        print(f"\n   🗑️  Will delete enrichment header at cell {h}")

for c in enrichment_codes:
    if c != keep_enrichment_code:
        cells_to_delete.append(c)
        print(f"   🗑️  Will delete enrichment code at cell {c}")

for h in sentiment_headers:
    if h != keep_sentiment_header:
        cells_to_delete.append(h)
        print(f"   🗑️  Will delete sentiment header at cell {h}")

for c in sentiment_codes:
    if c != keep_sentiment_code:
        cells_to_delete.append(c)
        print(f"   🗑️  Will delete sentiment code at cell {c}")

# ============================================================================
# STEP 3: Extract cells to move
# ============================================================================

# Get the cells we want to move
enrichment_header_cell = cells[keep_enrichment_header] if keep_enrichment_header else None
enrichment_code_cell = cells[keep_enrichment_code] if keep_enrichment_code else None
sentiment_header_cell = cells[keep_sentiment_header] if keep_sentiment_header else None
sentiment_code_cell = cells[keep_sentiment_code] if keep_sentiment_code else None

# Find where to insert them (after data acquisition, cell 6)
insert_position = 7

print(f"\n🔀 Will move:")
print(f"   • Enrichment (cells {keep_enrichment_header}, {keep_enrichment_code}) → position {insert_position}")
print(f"   • Sentiment (cells {keep_sentiment_header}, {keep_sentiment_code}) → position {insert_position + 2}")

# ============================================================================
# STEP 4: Build new cell list
# ============================================================================

print(f"\n🏗️  Building new cell structure...")

new_cells = []

# Add all cells, skipping those we're moving
for i, cell in enumerate(cells):
    if i in cells_to_delete:
        print(f"   Skipping cell {i} (duplicate)")
        continue
    elif i in [keep_enrichment_header, keep_enrichment_code, keep_sentiment_header, keep_sentiment_code]:
        # Skip for now - we'll insert these at the right position
        print(f"   Holding cell {i} for repositioning")
        continue
    else:
        new_cells.append(cell)

    # Insert enrichment and sentiment after cell 6 (data acquisition)
    if i == 6:
        print(f"\n   📍 Inserting at position {len(new_cells)}:")
        if enrichment_header_cell:
            new_cells.append(enrichment_header_cell)
            print(f"      → Enrichment header")
        if enrichment_code_cell:
            new_cells.append(enrichment_code_cell)
            print(f"      → Enrichment code")
        if sentiment_header_cell:
            new_cells.append(sentiment_header_cell)
            print(f"      → Sentiment header")
        if sentiment_code_cell:
            new_cells.append(sentiment_code_cell)
            print(f"      → Sentiment code")

print(f"\n✅ New structure: {len(new_cells)} cells (was {len(cells)})")

# ============================================================================
# STEP 5: Update clustering cells to use enriched text
# ============================================================================

print(f"\n🔧 Updating clustering cells...")

for i, cell in enumerate(new_cells):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']

        # Update clustering to use enriched text
        if 'SpatialClusterer' in source and "'title'" in source:
            # Replace title with text_for_clustering
            original = source
            source = source.replace("text_column='title'", "text_column='text_for_clustering'")
            source = source.replace('text_column="title"', 'text_column="text_for_clustering"')

            if source != original:
                cell['source'] = source.split('\n')
                print(f"   ✓ Updated cell {i} to use text_for_clustering")

# ============================================================================
# STEP 6: Update cell IDs
# ============================================================================

for i, cell in enumerate(new_cells):
    if 'id' in cell:
        cell['id'] = f"cell-{i}"

# ============================================================================
# STEP 7: Save
# ============================================================================

nb['cells'] = new_cells

with open('spatial_media_intelligence_demo.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print(f"\n✅ Restructured notebook saved!")
print(f"\n📊 Summary:")
print(f"   • Original cells: {len(cells)}")
print(f"   • New cells: {len(new_cells)}")
print(f"   • Deleted duplicates: {len(cells_to_delete)}")
print(f"   • Moved: Enrichment + Sentiment to position 7-10")

print(f"\n💾 Backup: {backup_path}")
