"""
Fix Causal Bias Duplicate Cell
Removes Cell 27 which is a misplaced duplicate causing NameError
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

print(f"\n📊 Original notebook: {len(nb['cells'])} cells")

# Show Cell 27 (the problem)
print(f"\n⚠️  Cell 27 (DUPLICATE - will be removed):")
cell_27_source = ''.join(nb['cells'][27].get('source', []))
print(cell_27_source[:200] + "...")

# Verify it's the problematic cell
if 'bias_detector.estimate_propensity_scores' in cell_27_source and 'df_confounders' in cell_27_source:
    print(f"\n✅ Confirmed: Cell 27 uses bias_detector before it's initialized")

    # Delete Cell 27
    del nb['cells'][27]
    print(f"✅ Deleted Cell 27")

    # Update cell IDs
    for i, cell in enumerate(nb['cells']):
        if 'id' in cell:
            cell['id'] = f"cell-{i}"

    print(f"\n📊 Updated notebook: {len(nb['cells'])} cells")

    # Write fixed notebook
    with open('spatial_media_intelligence_demo.ipynb', 'w') as f:
        json.dump(nb, f, indent=1)

    print(f"\n✅ Notebook fixed!")
    print(f"\n📋 Summary:")
    print(f"   • Removed misplaced Cell 27 (causal bias duplicate)")
    print(f"   • Proper causal bias section remains at Part 10 (now Cells 43-47)")
    print(f"   • Updated cell IDs")
    print(f"\n🎯 The NameError should be fixed now!")
    print(f"\n💡 Proper execution order:")
    print(f"   1. Run cells 1-43 (setup through sentiment)")
    print(f"   2. Cell 44: Part 10 header")
    print(f"   3. Cell 45: Initialize bias_detector and prepare df_confounders")
    print(f"   4. Cell 46: Estimate propensity scores (now works!)")
    print(f"   5. Cell 47+: Analyze and visualize")
else:
    print(f"\n⚠️  Cell 27 doesn't match expected pattern. Manual review needed.")
