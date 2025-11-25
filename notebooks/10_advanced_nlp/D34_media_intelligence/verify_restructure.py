"""
Verify Notebook Restructuring
Checks that cell order is correct and all fixes are still in place
"""

import json

# Read restructured notebook
with open('spatial_media_intelligence_demo.ipynb', 'r') as f:
    nb = json.load(f)

print("="*80)
print("RESTRUCTURING VERIFICATION")
print("="*80)

cells = nb['cells']
print(f"\n📊 Total cells: {len(cells)}")

# ============================================================================
# Check 1: Cell order is correct
# ============================================================================

print(f"\n✅ CHECK 1: Cell Order")
print(f"-" * 40)

# Find key cells
enrichment_cells = []
sentiment_cells = []
clustering_cells = []

for i, cell in enumerate(cells):
    if cell['cell_type'] == 'markdown':
        source = ''.join(cell['source']).lower()
        if 'text enrichment' in source or 'enrichment' in source:
            if 'part' in source:  # Header cell
                enrichment_cells.append(i)
                print(f"   Cell {i}: Text Enrichment Header")

    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])

        # Enrichment code
        if 'enrich_text' in source or 'text_enricher' in source:
            enrichment_cells.append(i)
            print(f"   Cell {i}: Text Enrichment Code")

        # Sentiment code
        if 'sentiment_analyzer' in source or 'AdvancedSentimentAnalyzer' in source:
            sentiment_cells.append(i)
            print(f"   Cell {i}: Sentiment Analysis Code")

        # Clustering code
        if 'AgglomerativeClustering' in source or 'distance_matrix' in source:
            clustering_cells.append(i)
            print(f"   Cell {i}: Clustering Code")

# Verify order
enrichment_pos = min(enrichment_cells) if enrichment_cells else -1
sentiment_pos = min(sentiment_cells) if sentiment_cells else -1
clustering_pos = min(clustering_cells) if clustering_cells else -1

print(f"\n   Position summary:")
print(f"   • Enrichment starts: Cell {enrichment_pos}")
print(f"   • Sentiment starts: Cell {sentiment_pos}")
print(f"   • Clustering starts: Cell {clustering_pos}")

if enrichment_pos < clustering_pos and sentiment_pos < clustering_pos:
    print(f"\n   ✅ PASS: Enrichment and Sentiment come BEFORE Clustering")
    order_correct = True
else:
    print(f"\n   ❌ FAIL: Wrong order!")
    order_correct = False

# ============================================================================
# Check 2: Clustering uses enriched text
# ============================================================================

print(f"\n✅ CHECK 2: Clustering Uses Enriched Text")
print(f"-" * 40)

clustering_uses_enriched = False
for i in clustering_cells:
    source = ''.join(cells[i]['source'])
    if 'text_for_clustering' in source:
        print(f"   Cell {i}: ✅ Uses 'text_for_clustering'")
        clustering_uses_enriched = True
    elif "'title'" in source or '"title"' in source:
        print(f"   Cell {i}: ❌ Still uses 'title'")

if clustering_uses_enriched:
    print(f"\n   ✅ PASS: Clustering uses enriched text")
else:
    print(f"\n   ⚠️  WARNING: Clustering may still use titles")

# ============================================================================
# Check 3: All previous fixes still present
# ============================================================================

print(f"\n✅ CHECK 3: Previous Fixes Still Present")
print(f"-" * 40)

fixes = {
    'config_import': False,
    'adaptive_sentiment': False,
    'min_articles_lowered': False,
    'treemap_fix': False,
    'pilot_pricing': False,
    'no_patent_pending': True  # Default true, set false if found
}

for cell in cells:
    source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']

    # Fix 1: Config import
    if 'from config import NotebookConfig' in source:
        fixes['config_import'] = True

    # Fix 3: Adaptive sentiment
    if 'adaptive_classify' in source or 'pos_threshold = score_mean' in source:
        fixes['adaptive_sentiment'] = True

    # Fix 4: Min articles lowered
    if 'MIN_ARTICLES_PER_OUTLET' in source or 'min_articles_per_outlet: int = 2' in source:
        fixes['min_articles_lowered'] = True

    # Fix 5: Treemap fix
    if 'groupby' in source and 'treemap' in source.lower():
        fixes['treemap_fix'] = True

    # Fix 6: Pilot pricing
    if '$10,000' in source or '$10K' in source:
        fixes['pilot_pricing'] = True

    # Fix 6: No patent-pending
    if 'patent-pending' in source.lower():
        fixes['no_patent_pending'] = False

# Print results
for fix_name, present in fixes.items():
    status = "✅" if present else "❌"
    print(f"   {status} {fix_name.replace('_', ' ').title()}")

all_fixes_present = all(fixes.values())

# ============================================================================
# Check 4: No duplicate cells
# ============================================================================

print(f"\n✅ CHECK 4: No Duplicate Cells")
print(f"-" * 40)

# Count enrichment and sentiment cells
enrichment_count = len([i for i in enrichment_cells])
sentiment_count = len([i for i in sentiment_cells])

print(f"   • Enrichment cells: {enrichment_count} (expected: 2)")
print(f"   • Sentiment cells: {sentiment_count} (expected: 2)")

no_duplicates = enrichment_count <= 2 and sentiment_count <= 2

if no_duplicates:
    print(f"\n   ✅ PASS: No unexpected duplicates")
else:
    print(f"\n   ⚠️  WARNING: May have duplicate cells")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print(f"\n" + "="*80)
print(f"📊 FINAL VERIFICATION SUMMARY")
print(f"="*80)

checks = [
    ("Cell order correct", order_correct),
    ("Clustering uses enriched text", clustering_uses_enriched),
    ("All previous fixes present", all_fixes_present),
    ("No duplicate cells", no_duplicates)
]

passed = sum(1 for _, status in checks if status)
total = len(checks)

for check_name, status in checks:
    icon = "✅" if status else "❌"
    print(f"{icon} {check_name}")

print(f"\n📈 Score: {passed}/{total} checks passed")

if passed == total:
    print(f"\n🎉 ALL CHECKS PASSED! Notebook restructuring successful!")
    print(f"\n🚀 Next steps:")
    print(f"   1. Open the notebook in Jupyter")
    print(f"   2. Run 'Restart Kernel & Run All Cells'")
    print(f"   3. Verify clustering produces better results")
else:
    print(f"\n⚠️  Some checks failed. Review output above.")

print(f"\n💾 Original backed up to: spatial_media_intelligence_demo.ipynb.backup.restructure.*")
