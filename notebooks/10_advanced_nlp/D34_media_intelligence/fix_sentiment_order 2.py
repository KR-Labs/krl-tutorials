"""
Fix Sentiment Section Order
Swap Part 9 and Part 9.5 so sentiment analysis comes before diagnostics
"""

import json
import shutil
from datetime import datetime

# Backup
backup_path = f'spatial_media_intelligence_demo.ipynb.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
shutil.copy('spatial_media_intelligence_demo.ipynb', backup_path)
print(f"✅ Created backup: {backup_path}")

# Read notebook
with open('spatial_media_intelligence_demo.ipynb', 'r') as f:
    nb = json.load(f)

print(f"\n📊 Current notebook: {len(nb['cells'])} cells")

print(f"\n⚠️  Current order (WRONG):")
print(f"   Cell 38: Part 9.5 header (diagnostics)")
print(f"   Cell 39: Run diagnostics (uses df_sentiment) ❌")
print(f"   Cell 40: Part 9 header (sentiment analysis)")
print(f"   Cell 41: Create df_sentiment ✅")

# Extract the 4 cells
cell_38 = nb['cells'][38]  # Part 9.5 header
cell_39 = nb['cells'][39]  # Diagnostics code
cell_40 = nb['cells'][40]  # Part 9 header
cell_41 = nb['cells'][41]  # Sentiment analysis code

# Swap them: Put Part 9 before Part 9.5
nb['cells'][38] = cell_40  # Part 9 header (was Cell 40)
nb['cells'][39] = cell_41  # Sentiment analysis code (was Cell 41)
nb['cells'][40] = cell_38  # Part 9.5 header (was Cell 38)
nb['cells'][41] = cell_39  # Diagnostics code (was Cell 39)

print(f"\n✅ Swapped sections:")
print(f"   Cell 38: Part 9 header (sentiment analysis) ✅")
print(f"   Cell 39: Create df_sentiment ✅")
print(f"   Cell 40: Part 9.5 header (diagnostics) ✅")
print(f"   Cell 41: Run diagnostics (uses df_sentiment) ✅")

# Update cell IDs
for i, cell in enumerate(nb['cells']):
    if 'id' in cell:
        cell['id'] = f"cell-{i}"

# Write fixed notebook
with open('spatial_media_intelligence_demo.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print(f"\n✅ Notebook fixed!")
print(f"\n📋 Summary:")
print(f"   • Swapped Part 9 and Part 9.5 sections")
print(f"   • Sentiment analysis now runs BEFORE diagnostics")
print(f"   • df_sentiment is created before it's used")
print(f"\n🎯 The NameError should be fixed now!")
print(f"\n💡 Proper execution order:")
print(f"   1. Cell 38-39: Part 9 - Create df_sentiment")
print(f"   2. Cell 40-41: Part 9.5 - Run diagnostics on df_sentiment")
