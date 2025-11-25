"""
Fix Cell Order - Move Adaptive Weighting After Enrichment
The adaptive weighting cells need to run AFTER df_enriched is created
"""

import json
import shutil
from datetime import datetime

# Backup
backup_path = f'spatial_media_intelligence_demo.ipynb.backup.order_fix.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
shutil.copy('spatial_media_intelligence_demo.ipynb', backup_path)
print(f"✅ Created backup: {backup_path}")

# Read notebook
with open('spatial_media_intelligence_demo.ipynb', 'r') as f:
    nb = json.load(f)

cells = nb['cells']
print(f"\n📊 Current: {len(cells)} cells")

# ============================================================================
# Find key cells
# ============================================================================

enrichment_cell_idx = None
adaptive_weighting_cells = []
comparison_cells = []

for i, cell in enumerate(cells):
    source = ''.join(cell['source'])

    # Find enrichment cell
    if cell['cell_type'] == 'code' and 'RobustTextEnricher' in source and 'df_enriched' in source:
        enrichment_cell_idx = i
        print(f"\n✅ Found enrichment cell at index {i}")

    # Find adaptive weighting cells
    if cell['cell_type'] == 'markdown' and 'Part 8.5' in source and 'Adaptive' in source:
        adaptive_weighting_cells.append(i)
        print(f"✅ Found adaptive weighting header at index {i}")

    if cell['cell_type'] == 'code' and 'AdaptiveWeightCalculator' in source and 'calculate_all_lambdas' in source:
        adaptive_weighting_cells.append(i)
        print(f"✅ Found adaptive weighting code at index {i}")

    # Find comparison cells
    if cell['cell_type'] == 'markdown' and 'Part 2' in source and 'COMPARISON' in source:
        comparison_cells.append(i)
        print(f"✅ Found comparison header at index {i}")

    if cell['cell_type'] == 'code' and 'cluster_adaptive' in source and 'lambda_series' in source:
        comparison_cells.append(i)
        print(f"✅ Found comparison code at index {i}")

if enrichment_cell_idx is None:
    print("\n❌ Could not find enrichment cell!")
    exit(1)

if len(adaptive_weighting_cells) == 0:
    print("\n❌ Could not find adaptive weighting cells!")
    exit(1)

print(f"\n📍 Current positions:")
print(f"   Enrichment: {enrichment_cell_idx}")
print(f"   Adaptive weighting: {adaptive_weighting_cells}")
print(f"   Comparison: {comparison_cells}")

# ============================================================================
# Check if order is wrong
# ============================================================================

all_adaptive_cells = sorted(adaptive_weighting_cells + comparison_cells)

if all_adaptive_cells[0] < enrichment_cell_idx:
    print(f"\n⚠️  PROBLEM: Adaptive weighting cells ({all_adaptive_cells[0]}) are BEFORE enrichment ({enrichment_cell_idx})")
    print(f"   This causes: NameError: name 'df_enriched' is not defined")
    print(f"\n🔧 Fixing: Moving adaptive weighting cells AFTER enrichment...")

    # Extract the cells to move
    cells_to_move = []
    for idx in sorted(all_adaptive_cells, reverse=True):
        cells_to_move.insert(0, cells.pop(idx))

    print(f"   • Removed {len(cells_to_move)} cells from positions {all_adaptive_cells}")

    # Find new enrichment position (it shifted)
    new_enrichment_idx = None
    for i, cell in enumerate(cells):
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            if 'RobustTextEnricher' in source and 'df_enriched' in source:
                new_enrichment_idx = i
                break

    if new_enrichment_idx is None:
        print("❌ Lost track of enrichment cell after moving!")
        exit(1)

    # Insert after enrichment
    insert_position = new_enrichment_idx + 1

    for i, cell in enumerate(cells_to_move):
        cells.insert(insert_position + i, cell)

    print(f"   • Inserted {len(cells_to_move)} cells at position {insert_position}")
    print(f"\n✅ Fixed! New order:")
    print(f"   Enrichment: {new_enrichment_idx}")
    print(f"   Adaptive weighting: {insert_position} to {insert_position + len(cells_to_move) - 1}")

    # Save
    nb['cells'] = cells
    with open('spatial_media_intelligence_demo.ipynb', 'w') as f:
        json.dump(nb, f, indent=1)

    print(f"\n✅ Cell order fixed!")
    print(f"\n📊 Summary:")
    print(f"   • Total cells: {len(cells)}")
    print(f"   • Cells moved: {len(cells_to_move)}")
    print(f"   • New order: Data → Enrichment → Adaptive Weighting → Clustering")

    print(f"\n💾 Backup: {backup_path}")
    print(f"\n🎯 Next: Run the notebook again - df_enriched will now exist when needed!")

else:
    print(f"\n✅ Order is correct - adaptive weighting is already after enrichment")
    print(f"   No changes needed!")
