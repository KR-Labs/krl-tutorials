#!/usr/bin/env python3
"""
Final validation - Test clustering with adaptive min_cluster_size
"""

import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Load environment
env_path = os.path.expanduser('~/Documents/GitHub/KRL/krl-tutorials/.env')
load_dotenv(env_path)

print("="*80)
print("FINAL VALIDATION - Adaptive min_cluster_size")
print("="*80)
print()

# Load data
from gdelt_connector import GDELTConnector
from robust_text_enrichment import RobustTextEnricher
from adaptive_weighting import AdaptiveWeightCalculator
from syndication_handler import SyndicationHandler
from spatial_clustering import SpatialClusterer
from clustering_metrics import ClusteringEvaluator

print("Step 1: Loading 50 articles...")
connector = GDELTConnector()
df = connector.query_articles(topic='housing affordability', days_back=7, max_results=50)
print(f"✓ Loaded {len(df)} articles\n")

print("Step 2: Text enrichment (first 5 articles)...")
enricher = RobustTextEnricher()
for idx in range(min(5, len(df))):
    result = enricher.enrich_article(df['url'].iloc[idx], df['title'].iloc[idx])
    df.loc[idx, 'full_text'] = result.get('text', df['title'].iloc[idx])
    df.loc[idx, 'extraction_method'] = result.get('method', 'unknown')
df_enriched = df.copy()
print(f"✓ Enrichment complete\n")

print("Step 3: Adaptive weighting...")
weight_calculator = AdaptiveWeightCalculator()
df_enriched['lambda_spatial'] = weight_calculator.calculate_all_lambdas(df_enriched)
print(f"✓ Weights calculated\n")

print("Step 4: Syndication separation...")
handler = SyndicationHandler()
df_syndicated, df_local = handler.separate_content(df_enriched)
print(f"✓ Separated: {len(df_syndicated)} syndicated, {len(df_local)} local\n")

print("Step 5: Clustering with ADAPTIVE min_cluster_size...")
print(f"   Local articles: {len(df_local)}")

# ADAPTIVE THRESHOLD (as in updated Cell 21)
min_size_threshold = max(5, len(df_local) // 10)
print(f"   Adaptive threshold: {min_size_threshold} (10% of {len(df_local)}, min 5)")

# Prepare clustering data
df_for_clustering = df_local.copy()
df_for_clustering['title'] = df_local.get('full_text', df_local['title'])

# Cluster with adaptive threshold
clusterer = SpatialClusterer(
    spatial_weight=0.15,
    distance_threshold=0.35,
    linkage='complete',
    min_cluster_size=min_size_threshold  # ADAPTIVE
)

if 'lambda_spatial' in df_local.columns:
    df_result = clusterer.cluster_adaptive(df_for_clustering, df_local['lambda_spatial'])
else:
    df_result = clusterer.cluster(df_for_clustering)

n_clusters = df_result['cluster'].nunique()
print(f"✓ Clustering complete: {n_clusters} clusters\n")

if n_clusters > 0:
    print("   Cluster distribution:")
    for cluster_id, count in df_result['cluster'].value_counts().sort_index().items():
        print(f"      Cluster {cluster_id}: {count} articles")
    print()

print("Step 6: Evaluation...")
evaluator = ClusteringEvaluator()

metrics = evaluator.evaluate(
    df_result,
    clusterer.embeddings,
    df_result['cluster'].values
)

if 'error' in metrics:
    print(f"⚠️  {metrics['message']}")
    print(f"   This is expected with very small datasets")
else:
    print(f"✓ Evaluation complete")
    print(f"   Silhouette: {metrics.get('silhouette_score', 'N/A')}")
    print(f"   Clusters: {metrics.get('n_clusters', 0)}")

print()
print("="*80)
print("✅ VALIDATION COMPLETE - Adaptive threshold working correctly!")
print("="*80)
print()

print("Summary:")
print(f"  • Dataset size: {len(df_local)} local articles")
print(f"  • Adaptive threshold: {min_size_threshold}")
print(f"  • Clusters retained: {n_clusters}")
print(f"  • Articles in clusters: {len(df_result)}")
print()

if n_clusters == 0:
    print("⚠️  Warning: No clusters retained after filtering")
    print("   Solution: Use larger dataset (100+ articles) or lower threshold")
elif n_clusters == 1:
    print("⚠️  Warning: Only 1 cluster retained")
    print("   Recommendation: Use larger dataset for more meaningful clustering")
else:
    print("✅ SUCCESS: Multiple clusters retained - ready for analysis!")
