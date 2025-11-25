#!/usr/bin/env python3
"""
Test the adaptive min_cluster_size logic
"""

# Simulate different dataset sizes
test_cases = [
    ("Small dataset", 30),
    ("Medium dataset", 50),
    ("Medium-large dataset", 100),
    ("Large dataset", 200),
    ("Very large dataset", 500),
]

print("="*80)
print("ADAPTIVE min_cluster_size CALCULATOR")
print("="*80)
print()

print("Formula: max(5, len(df_local) // 10)")
print()
print(f"{'Dataset Size':<25} {'min_cluster_size':<20} {'Rationale'}")
print("-"*80)

for label, size in test_cases:
    threshold = max(5, size // 10)
    pct = (threshold / size) * 100
    print(f"{label:<25} {threshold:<20} ({pct:.1f}% of dataset)")

print()
print("="*80)
print("BENEFITS")
print("="*80)
print()
print("✓ Prevents empty results with small datasets")
print("✓ Maintains quality standards with large datasets")
print("✓ No manual tuning required")
print("✓ Scales automatically with data size")
print()
print("Example outcomes:")
print("  • 30 articles → min_size=5  → Keeps clusters with 5+ articles")
print("  • 50 articles → min_size=5  → Keeps clusters with 5+ articles")
print("  • 100 articles → min_size=10 → Keeps clusters with 10+ articles")
print("  • 200 articles → min_size=20 → Keeps clusters with 20+ articles")
print("  • 500 articles → min_size=50 → Keeps clusters with 50+ articles")
