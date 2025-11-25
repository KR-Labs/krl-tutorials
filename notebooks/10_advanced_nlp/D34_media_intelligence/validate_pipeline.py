#!/usr/bin/env python3
"""
Validate the entire enrichment → syndication → clustering pipeline
"""

import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Load environment
env_path = os.path.expanduser('~/Documents/GitHub/KRL/krl-tutorials/.env')
load_dotenv(env_path)

print("="*80)
print("PIPELINE VALIDATION - Cell 9 → Cell 18 → Cell 19 → Cell 21")
print("="*80)
print()

# ==========================================
# STEP 1: Load Sample Data (simulating Cell 3-4)
# ==========================================
print("STEP 1: Loading sample data...")
from gdelt_connector import GDELTConnector

connector = GDELTConnector()
df = connector.query_articles(topic='housing affordability', days_back=7, max_results=50)
print(f"✓ Loaded {len(df)} articles")
print(f"  Columns: {list(df.columns)}")
print()

# ==========================================
# STEP 2: Text Enrichment (Cell 9)
# ==========================================
print("STEP 2: Testing text enrichment (Cell 9)...")
from robust_text_enrichment import RobustTextEnricher

enricher = RobustTextEnricher()

# Test on first 5 articles
print(f"   Enriching 5 articles...")
results = []
for idx in range(min(5, len(df))):
    url = df['url'].iloc[idx]
    title = df['title'].iloc[idx]
    result = enricher.enrich_article(url=url, title=title)

    # Map to expected format
    adapted = {
        'full_text': result.get('text', title),
        'extraction_method': result.get('method', 'unknown'),
        'word_count': result.get('word_count', len(title.split())),
        'success': result.get('success', False)
    }
    results.append(adapted)

success_count = sum(1 for r in results if r['success'])
print(f"✓ Enrichment complete: {success_count}/{len(results)} successful")
print(f"  Methods used: {set(r['extraction_method'] for r in results)}")
print()

# Create df_enriched (simulating full Cell 9 execution)
df_enriched = df.copy()
for idx, result in enumerate(results):
    for key, value in result.items():
        df_enriched.loc[idx, key] = value

# Fill remaining rows with title fallback
for idx in range(len(results), len(df)):
    df_enriched.loc[idx, 'full_text'] = df.loc[idx, 'title']
    df_enriched.loc[idx, 'extraction_method'] = 'title_fallback'
    df_enriched.loc[idx, 'word_count'] = len(df.loc[idx, 'title'].split())
    df_enriched.loc[idx, 'success'] = False

print(f"✓ df_enriched created: {len(df_enriched)} rows")
print(f"  Required columns present: {all(col in df_enriched.columns for col in ['full_text', 'extraction_method'])}")
print()

# ==========================================
# STEP 3: Adaptive Weighting (Cell 18)
# ==========================================
print("STEP 3: Testing adaptive weighting (Cell 18)...")
from adaptive_weighting import AdaptiveWeightCalculator

weight_calculator = AdaptiveWeightCalculator()

try:
    df_enriched['lambda_spatial'] = weight_calculator.calculate_all_lambdas(df_enriched)
    print(f"✓ Adaptive weights calculated")
    print(f"  Weight distribution:")
    for lambda_val, count in df_enriched['lambda_spatial'].value_counts().sort_index().items():
        pct = 100 * count / len(df_enriched)
        print(f"    λ={lambda_val:.2f}: {count:3d} articles ({pct:5.1f}%)")
    print()
except Exception as e:
    print(f"❌ Adaptive weighting FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ==========================================
# STEP 4: Syndication Separation (Cell 19)
# ==========================================
print("STEP 4: Testing syndication separation (Cell 19)...")
from syndication_handler import SyndicationHandler

handler = SyndicationHandler()

try:
    df_syndicated, df_local = handler.separate_content(df_enriched)
    print(f"✓ Content separated successfully")
    print(f"  Syndicated: {len(df_syndicated)} articles")
    print(f"  Local: {len(df_local)} articles")

    if len(df_local) == 0:
        print(f"\n⚠️  WARNING: df_local is EMPTY!")
        print(f"     This will cause ZeroDivisionError in clustering")
        print(f"     Likely reason: All articles classified as syndicated")
    else:
        print(f"✓ df_local has data")
    print()

except Exception as e:
    print(f"❌ Syndication separation FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ==========================================
# STEP 5: Clustering (Cell 21)
# ==========================================
print("STEP 5: Testing clustering (Cell 21)...")

if len(df_local) == 0:
    print(f"❌ SKIPPING: df_local is empty, cannot cluster")
    print()
    print("="*80)
    print("DIAGNOSIS: df_local is empty")
    print("="*80)
    print()
    print("Possible causes:")
    print("1. SyndicationHandler classified ALL articles as syndicated")
    print("2. Enrichment failed completely (all title_fallback)")
    print("3. Dataset too small or homogeneous")
    print()
    print("Fix:")
    print("- Use larger dataset (50+ articles)")
    print("- Ensure text enrichment working (check extraction_method)")
    print("- Adjust syndication threshold in SyndicationHandler")
    sys.exit(1)

from spatial_clustering import SpatialClusterer

# Prepare data
df_for_clustering = df_local.copy()
df_for_clustering['title'] = df_local.get('text_for_clustering', df_local.get('full_text', df_local['title']))

print(f"   Clustering {len(df_for_clustering)} local articles...")

clusterer_adaptive = SpatialClusterer(
    spatial_weight=0.15,
    distance_threshold=0.35,
    linkage='complete',
    min_cluster_size=15
)

try:
    # Check if lambda_spatial exists
    if 'lambda_spatial' in df_local.columns:
        df_adaptive = clusterer_adaptive.cluster_adaptive(
            df_for_clustering,
            lambda_series=df_local['lambda_spatial']
        )
    else:
        print(f"   (lambda_spatial not found, using fixed weighting)")
        df_adaptive = clusterer_adaptive.cluster(df_for_clustering)

    print(f"✓ Clustering complete: {df_adaptive['cluster'].nunique()} clusters")
    print(f"  Cluster sizes: {df_adaptive['cluster'].value_counts().to_dict()}")
    print()

except Exception as e:
    print(f"❌ Clustering FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ==========================================
# STEP 6: Evaluation (Cell 21)
# ==========================================
print("STEP 6: Testing clustering evaluation...")
from clustering_metrics import ClusteringEvaluator

evaluator = ClusteringEvaluator()

try:
    metrics = evaluator.evaluate(
        df_adaptive,
        clusterer_adaptive.embeddings,
        df_adaptive['cluster'].values
    )

    print(f"✓ Evaluation complete")
    evaluator.print_report(metrics)

except Exception as e:
    print(f"❌ Evaluation FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("="*80)
print("✅ PIPELINE VALIDATION COMPLETE - ALL STEPS PASSED")
print("="*80)
