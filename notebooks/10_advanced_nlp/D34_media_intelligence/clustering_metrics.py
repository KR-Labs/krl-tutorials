"""
Comprehensive Clustering Quality Metrics

Provides detailed evaluation beyond simple Silhouette score:
- Silhouette Score (cluster separation)
- Davies-Bouldin Index (cluster compactness)
- Calinski-Harabasz Score (variance ratio)
- Cluster balance metrics (entropy, size distribution)
- Per-cluster quality assessment

Use this to:
1. Compare clustering methods (fixed vs adaptive)
2. Tune clustering parameters
3. Identify problematic clusters for manual review
"""

from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score,
    silhouette_samples
)
from sklearn.metrics.pairwise import cosine_distances
import numpy as np
import pandas as pd
from typing import Dict, Optional


class ClusteringEvaluator:
    """
    Comprehensive clustering quality metrics

    Metrics Explained:
    - Silhouette Score: Measures how similar objects are to their own cluster
      vs other clusters. Range: -1 to 1, higher is better.
      - > 0.5: Strong structure
      - 0.3-0.5: Reasonable structure
      - < 0.3: Weak structure

    - Davies-Bouldin Index: Average similarity ratio of each cluster with its
      most similar cluster. Lower is better. No fixed range.

    - Calinski-Harabasz Score: Ratio of between-cluster to within-cluster
      variance. Higher is better. No fixed range.

    - Balance Entropy: Measures evenness of cluster size distribution.
      Higher = more balanced. Theoretical max = log(n_clusters).

    - Per-Cluster Silhouette: Identifies clusters with poor internal cohesion
      (candidates for splitting or removal)
    """

    def evaluate(
        self,
        df_clustered: pd.DataFrame,
        embeddings: np.ndarray,
        labels: np.ndarray
    ) -> Dict:
        """
        Calculate comprehensive clustering quality metrics

        Args:
            df_clustered: Dataframe with cluster assignments
            embeddings: Article embeddings (n_samples, n_features)
            labels: Cluster labels (n_samples,)

        Returns:
            Dict with all metrics
        """

        # Validate input
        if len(labels) == 0 or len(embeddings) == 0:
            return {
                'error': 'empty_dataset',
                'message': 'No valid clusters to evaluate',
                'n_clusters': 0,
                'silhouette_score': None,
                'davies_bouldin': None,
                'calinski_harabasz': None
            }

        # Calculate distance matrix
        semantic_dist = cosine_distances(embeddings)

        # Core metrics
        try:
            silhouette = silhouette_score(
                semantic_dist,
                labels,
                metric='precomputed'
            )
        except:
            silhouette = None

        try:
            davies_bouldin = davies_bouldin_score(embeddings, labels)
        except:
            davies_bouldin = None

        try:
            calinski_harabasz = calinski_harabasz_score(embeddings, labels)
        except:
            calinski_harabasz = None

        # Cluster balance metrics
        cluster_sizes = pd.Series(labels).value_counts()
        n_clusters = len(cluster_sizes)

        # Balance entropy (higher = more balanced)
        cluster_probs = cluster_sizes / len(labels)
        balance_entropy = -(cluster_probs * np.log(cluster_probs)).sum()

        # Size statistics
        largest_cluster_pct = cluster_sizes.max() / len(labels)
        avg_cluster_size = cluster_sizes.mean()
        median_cluster_size = cluster_sizes.median()
        std_cluster_size = cluster_sizes.std()

        # Per-cluster quality
        silhouette_per_cluster = {}
        try:
            sample_silhouette = silhouette_samples(
                semantic_dist,
                labels,
                metric='precomputed'
            )

            for cluster_id in np.unique(labels):
                if cluster_id >= 0:  # Skip noise (-1)
                    mask = labels == cluster_id
                    silhouette_per_cluster[cluster_id] = sample_silhouette[mask].mean()
        except:
            pass

        # Identify worst and best clusters
        worst_cluster = None
        best_cluster = None
        if silhouette_per_cluster:
            worst_cluster = min(silhouette_per_cluster.items(), key=lambda x: x[1])
            best_cluster = max(silhouette_per_cluster.items(), key=lambda x: x[1])

        return {
            'silhouette_score': silhouette,
            'davies_bouldin': davies_bouldin,
            'calinski_harabasz': calinski_harabasz,
            'n_clusters': n_clusters,
            'n_noise': (labels == -1).sum() if -1 in labels else 0,
            'largest_cluster_pct': largest_cluster_pct,
            'balance_entropy': balance_entropy,
            'avg_cluster_size': avg_cluster_size,
            'median_cluster_size': median_cluster_size,
            'std_cluster_size': std_cluster_size,
            'silhouette_per_cluster': silhouette_per_cluster,
            'worst_cluster': worst_cluster,
            'best_cluster': best_cluster,
        }

    def print_report(self, results: Dict):
        """
        Print formatted evaluation report

        Args:
            results: Dict from evaluate() method
        """

        print("="*80)
        print("CLUSTERING QUALITY EVALUATION")
        print("="*80)

        # Handle error case
        if 'error' in results:
            print(f"\n❌ ERROR: {results['message']}")
            print(f"   No clusters available for evaluation")
            print("="*80)
            return

        # Semantic quality
        print(f"\n🎯 Semantic Quality:")

        if results['silhouette_score'] is not None:
            sil = results['silhouette_score']
            print(f"   Silhouette: {sil:.3f} (higher better, range -1 to 1)")

            if sil > 0.5:
                assessment = "✅ STRONG structure"
            elif sil > 0.3:
                assessment = "🟡 REASONABLE structure"
            else:
                assessment = "⚠️  WEAK structure"
            print(f"              {assessment}")
        else:
            print(f"   Silhouette: N/A")

        if results['davies_bouldin'] is not None:
            print(f"   Davies-Bouldin: {results['davies_bouldin']:.3f} (lower better)")

        if results['calinski_harabasz'] is not None:
            print(f"   Calinski-Harabasz: {results['calinski_harabasz']:.1f} (higher better)")

        # Cluster structure
        print(f"\n📊 Cluster Structure:")
        print(f"   Number of clusters: {results['n_clusters']}")

        if results['n_noise'] > 0:
            print(f"   Noise points: {results['n_noise']}")

        print(f"   Average size: {results['avg_cluster_size']:.1f} articles")
        print(f"   Median size: {results['median_cluster_size']:.0f} articles")
        print(f"   Std dev: {results['std_cluster_size']:.1f} articles")
        print(f"   Largest cluster: {results['largest_cluster_pct']:.1%}")

        # Balance assessment
        max_entropy = np.log(results['n_clusters']) if results['n_clusters'] > 1 else 1
        balance_pct = (results['balance_entropy'] / max_entropy) * 100 if max_entropy > 0 else 0

        print(f"   Balance entropy: {results['balance_entropy']:.2f}")
        print(f"   Balance: {balance_pct:.0f}% of theoretical maximum")

        if balance_pct > 80:
            print(f"              ✅ Well balanced")
        elif balance_pct > 60:
            print(f"              🟡 Moderately balanced")
        else:
            print(f"              ⚠️  Imbalanced (some very large clusters)")

        # Per-cluster quality
        if results['worst_cluster'] and results['best_cluster']:
            worst_id, worst_quality = results['worst_cluster']
            best_id, best_quality = results['best_cluster']

            print(f"\n🔍 Cluster Quality Range:")
            print(f"   Worst: Cluster {worst_id} (silhouette={worst_quality:.3f})")
            print(f"   Best: Cluster {best_id} (silhouette={best_quality:.3f})")

            if worst_quality < 0:
                print(f"\n   ⚠️  Cluster {worst_id} has NEGATIVE silhouette!")
                print(f"      This cluster may need manual review or splitting.")

        print("="*80)

    def compare_methods(
        self,
        results_a: Dict,
        results_b: Dict,
        method_a_name: str = "Method A",
        method_b_name: str = "Method B"
    ):
        """
        Print side-by-side comparison of two clustering methods

        Args:
            results_a: Results dict from method A
            results_b: Results dict from method B
            method_a_name: Name for method A (e.g., "Fixed λ=0.15")
            method_b_name: Name for method B (e.g., "Adaptive λ")
        """

        print("="*80)
        print("CLUSTERING METHOD COMPARISON")
        print("="*80)

        print(f"\n{method_a_name:30s} vs {method_b_name}")
        print("-"*80)

        # Silhouette
        sil_a = results_a.get('silhouette_score')
        sil_b = results_b.get('silhouette_score')

        if sil_a is not None and sil_b is not None:
            winner = method_b_name if sil_b > sil_a else method_a_name
            improvement = ((sil_b - sil_a) / abs(sil_a)) * 100 if sil_a != 0 else 0

            print(f"\nSilhouette Score (higher better):")
            print(f"   {method_a_name}: {sil_a:.3f}")
            print(f"   {method_b_name}: {sil_b:.3f}")
            print(f"   Winner: {winner} ({improvement:+.1f}% improvement)")

        # Davies-Bouldin
        db_a = results_a.get('davies_bouldin')
        db_b = results_b.get('davies_bouldin')

        if db_a is not None and db_b is not None:
            winner = method_b_name if db_b < db_a else method_a_name
            improvement = ((db_a - db_b) / db_a) * 100 if db_a != 0 else 0

            print(f"\nDavies-Bouldin Index (lower better):")
            print(f"   {method_a_name}: {db_a:.3f}")
            print(f"   {method_b_name}: {db_b:.3f}")
            print(f"   Winner: {winner} ({improvement:+.1f}% improvement)")

        # Number of clusters
        print(f"\nNumber of Clusters:")
        print(f"   {method_a_name}: {results_a['n_clusters']}")
        print(f"   {method_b_name}: {results_b['n_clusters']}")

        # Largest cluster
        print(f"\nLargest Cluster:")
        print(f"   {method_a_name}: {results_a['largest_cluster_pct']:.1%}")
        print(f"   {method_b_name}: {results_b['largest_cluster_pct']:.1%}")

        # Overall assessment
        print(f"\n{'='*80}")
        print(f"OVERALL ASSESSMENT")
        print(f"{'='*80}")

        wins_a = 0
        wins_b = 0

        if sil_a is not None and sil_b is not None:
            if sil_b > sil_a:
                wins_b += 1
            else:
                wins_a += 1

        if db_a is not None and db_b is not None:
            if db_b < db_a:
                wins_b += 1
            else:
                wins_a += 1

        if results_b['largest_cluster_pct'] < results_a['largest_cluster_pct']:
            wins_b += 1
        else:
            wins_a += 1

        if wins_b > wins_a:
            print(f"\n✅ {method_b_name} WINS ({wins_b}/{wins_a + wins_b} metrics)")
            print(f"   Recommendation: Use {method_b_name} for better clustering quality")
        elif wins_a > wins_b:
            print(f"\n✅ {method_a_name} WINS ({wins_a}/{wins_a + wins_b} metrics)")
            print(f"   Recommendation: Use {method_a_name} for better clustering quality")
        else:
            print(f"\n🤝 TIE ({wins_a}/{wins_a + wins_b} metrics each)")
            print(f"   Recommendation: Either method is acceptable")

        print("="*80)


# Example usage
if __name__ == "__main__":
    print(__doc__)

    print("\n" + "="*80)
    print("EXAMPLE USAGE")
    print("="*80)

    print("""
# In your notebook, after clustering:

from clustering_metrics import ClusteringEvaluator

evaluator = ClusteringEvaluator()

# Evaluate clustering quality
results = evaluator.evaluate(
    df_clustered,
    clusterer.embeddings,
    df_clustered['cluster'].values
)

# Print report
evaluator.print_report(results)

# Compare two methods
results_fixed = evaluator.evaluate(df_fixed, embeddings_fixed, labels_fixed)
results_adaptive = evaluator.evaluate(df_adaptive, embeddings_adaptive, labels_adaptive)

evaluator.compare_methods(
    results_fixed,
    results_adaptive,
    method_a_name="Fixed λ=0.15",
    method_b_name="Adaptive λ"
)
""")
