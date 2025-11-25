"""
Fix Clustering Text Column
Explicitly set text_column='text_for_clustering' in all clustering calls
"""

import json
import shutil
from datetime import datetime

# Backup
backup_path = f'spatial_media_intelligence_demo.ipynb.backup.clustering_fix.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
shutil.copy('spatial_media_intelligence_demo.ipynb', backup_path)
print(f"✅ Created backup: {backup_path}")

# Read notebook
with open('spatial_media_intelligence_demo.ipynb', 'r') as f:
    nb = json.load(f)

cells = nb['cells']
print(f"\n📊 Current: {len(cells)} cells")

# ============================================================================
# Update clustering cells
# ============================================================================

print(f"\n🔧 Updating clustering cells to use text_for_clustering...")

updated_count = 0

for i, cell in enumerate(cells):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])

        # Look for clustering calls
        if 'clusterer.cluster(df)' in source or 'clusterer.cluster( df )' in source:
            print(f"\n   Cell {i}: Found clusterer.cluster(df)")

            # Replace with explicit text_column parameter
            original = source
            source = source.replace(
                'clusterer.cluster(df)',
                "clusterer.cluster(df, text_column='text_for_clustering')"
            )
            source = source.replace(
                'clusterer.cluster( df )',
                "clusterer.cluster(df, text_column='text_for_clustering')"
            )

            if source != original:
                # Update cell
                cell['source'] = [source] if '\n' not in source else source.split('\n')
                print(f"      ✓ Updated to use text_for_clustering")
                updated_count += 1

                # Show the change
                print(f"      Before: ...clusterer.cluster(df)...")
                print(f"      After:  ...clusterer.cluster(df, text_column='text_for_clustering')...")

# ============================================================================
# Save
# ============================================================================

nb['cells'] = cells

with open('spatial_media_intelligence_demo.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print(f"\n✅ Clustering cells updated!")
print(f"\n📊 Summary:")
print(f"   • Updated {updated_count} clustering cells")
print(f"   • Now using text_for_clustering (enriched full text)")
print(f"   • Clustering will use ~500+ chars instead of ~50 char titles")

print(f"\n💾 Backup: {backup_path}")
