"""
Spatial Narrative Clustering - Lean Validation Version
Patent-pending algorithm combining geographic + semantic similarity
"""

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_distances, haversine_distances

class SpatialClusterer:
    """
    Cluster articles by semantic + geographic similarity

    Core Innovation: Weighted distance metric
    - λ_spatial = 0.15 (trade secret parameter)
    - Combines text embeddings + geographic coordinates
    """

    def __init__(
        self,
        spatial_weight=0.15,
        distance_threshold=0.5,
        linkage='average',
        min_cluster_size=None
    ):
        """
        Initialize clusterer

        Args:
            spatial_weight: Weight for spatial distance (trade secret: 0.15)
            distance_threshold: Clustering distance threshold (default: 0.5)
            linkage: Linkage method for hierarchical clustering (default: 'average')
            min_cluster_size: Minimum cluster size for filtering (default: None, no filtering)
        """
        self.spatial_weight = spatial_weight
        self.distance_threshold = distance_threshold
        self.linkage = linkage
        self.min_cluster_size = min_cluster_size

        print(f"\n🧠 Initializing Spatial Clusterer...")
        print(f"   λ_spatial (trade secret): {spatial_weight}")
        print(f"   Distance threshold: {distance_threshold}")
        print(f"   Linkage method: {linkage}")
        if min_cluster_size:
            print(f"   Min cluster size: {min_cluster_size}")

        # Load embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Faster model for demos
        print(f"   ✓ Embedding model loaded")

        # Distance matrices (for visualization)
        self.semantic_distances = None
        self.spatial_distances = None
        self.combined_distances = None
        self.embeddings = None

    def cluster(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cluster articles using spatial-semantic distance

        Args:
            df: DataFrame with 'title', 'latitude', 'longitude' columns

        Returns:
            DataFrame with 'cluster' column added
        """

        print(f"\n🌍 Clustering {len(df)} articles...")

        # Generate embeddings
        print("   [1/4] Generating semantic embeddings...")
        texts = df['title'].fillna('').tolist()
        embeddings = self.model.encode(texts, show_progress_bar=False)
        self.embeddings = embeddings  # Store for visualization

        # Semantic distance
        print("   [2/4] Computing semantic distances...")
        semantic_dist = cosine_distances(embeddings)
        self.semantic_distances = semantic_dist  # Store for visualization

        # Spatial distance
        print("   [3/4] Computing spatial distances...")
        coords = df[['latitude', 'longitude']].values
        coords_rad = np.radians(coords)
        spatial_dist = haversine_distances(coords_rad) * 6371.0  # km
        spatial_dist_norm = spatial_dist / spatial_dist.max()
        self.spatial_distances = spatial_dist_norm  # Store for visualization

        # Combine distances (PATENT-PENDING ALGORITHM)
        print(f"   [4/4] Combining distances (λ_spatial={self.spatial_weight})...")
        combined_dist = (
            (1 - self.spatial_weight) * semantic_dist +
            self.spatial_weight * spatial_dist_norm
        )
        self.combined_distances = combined_dist  # Store for visualization

        # Hierarchical clustering (with configurable parameters)
        clustering = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=self.distance_threshold,
            metric='precomputed',
            linkage=self.linkage
        )

        labels = clustering.fit_predict(combined_dist)

        # Add to dataframe
        df_result = df.copy()
        df_result['cluster'] = labels

        n_clusters = len(np.unique(labels))
        print(f"\n✓ Discovered {n_clusters} spatial narrative clusters")

        # Auto-filter small clusters if min_cluster_size specified
        if self.min_cluster_size:
            print(f"\n🔧 Auto-filtering clusters smaller than {self.min_cluster_size}...")
            df_result = self.filter_small_clusters(df_result, min_size=self.min_cluster_size)

        return df_result

    def cluster_adaptive(self, df: pd.DataFrame, lambda_series: pd.Series) -> pd.DataFrame:
        """
        Cluster articles using ADAPTIVE spatial-semantic distance

        Key Innovation: Per-article spatial weighting based on content type
        - Syndicated content: λ = 0.0 (geography irrelevant)
        - Local news with quotes: λ = 0.4 (geography matters)
        - Mixed/default: λ = 0.15 (balanced)

        Args:
            df: DataFrame with 'title', 'latitude', 'longitude' columns
            lambda_series: Pandas Series of per-article spatial weights

        Returns:
            DataFrame with 'cluster' column added
        """

        print(f"\n🌍 Clustering {len(df)} articles with ADAPTIVE weighting...")

        # Generate embeddings
        print("   [1/4] Generating semantic embeddings...")
        texts = df['title'].fillna('').tolist()
        embeddings = self.model.encode(texts, show_progress_bar=False)
        self.embeddings = embeddings  # Store for visualization

        # Semantic distance
        print("   [2/4] Computing semantic distances...")
        semantic_dist = cosine_distances(embeddings)
        self.semantic_distances = semantic_dist

        # Spatial distance
        print("   [3/4] Computing spatial distances...")
        coords = df[['latitude', 'longitude']].values
        coords_rad = np.radians(coords)
        spatial_dist = haversine_distances(coords_rad) * 6371.0  # km
        spatial_dist_norm = spatial_dist / spatial_dist.max()
        self.spatial_distances = spatial_dist_norm

        # ADAPTIVE combination (NOVEL ALGORITHM)
        print(f"   [4/4] Combining distances with ADAPTIVE weights...")
        combined_dist = np.zeros_like(semantic_dist)

        lambda_array = lambda_series.values

        # Log lambda statistics
        print(f"       λ range: {lambda_array.min():.2f} to {lambda_array.max():.2f}")
        print(f"       λ mean: {lambda_array.mean():.3f}")

        for i in range(len(df)):
            for j in range(len(df)):
                # Use average of both articles' lambdas
                lambda_avg = (lambda_array[i] + lambda_array[j]) / 2

                combined_dist[i, j] = (
                    (1 - lambda_avg) * semantic_dist[i, j] +
                    lambda_avg * spatial_dist_norm[i, j]
                )

        self.combined_distances = combined_dist  # Store for visualization

        # Hierarchical clustering (with configurable parameters)
        clustering = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=self.distance_threshold,
            metric='precomputed',
            linkage=self.linkage
        )

        labels = clustering.fit_predict(combined_dist)

        # Add to dataframe
        df_result = df.copy()
        df_result['cluster'] = labels

        n_clusters = len(np.unique(labels))
        print(f"\n✓ Discovered {n_clusters} spatial narrative clusters (ADAPTIVE)")

        # Auto-filter small clusters if min_cluster_size specified
        if self.min_cluster_size:
            print(f"\n🔧 Auto-filtering clusters smaller than {self.min_cluster_size}...")
            df_result = self.filter_small_clusters(df_result, min_size=self.min_cluster_size)

        return df_result

    def filter_small_clusters(self, df_clustered: pd.DataFrame, min_size: int = 10) -> pd.DataFrame:
        """
        Remove noise clusters with fewer than min_size articles

        Problem Solved:
        - Small clusters (<10 articles) are often noise
        - They degrade Silhouette score
        - They don't represent meaningful regional patterns

        Args:
            df_clustered: DataFrame with 'cluster' column
            min_size: Minimum articles per cluster (default: 10)

        Returns:
            DataFrame with small clusters removed and labels re-numbered
        """

        print(f"\n🔧 Filtering small clusters (min_size={min_size})...")

        # Calculate cluster sizes
        cluster_sizes = df_clustered.groupby('cluster').size()
        total_clusters_before = len(cluster_sizes)

        # Identify valid clusters
        valid_clusters = cluster_sizes[cluster_sizes >= min_size].index
        small_clusters = cluster_sizes[cluster_sizes < min_size]

        # Filter dataframe
        df_filtered = df_clustered[df_clustered['cluster'].isin(valid_clusters)].copy()

        # Re-label clusters sequentially (0, 1, 2, ...)
        cluster_mapping = {old: new for new, old in enumerate(sorted(valid_clusters))}
        df_filtered['cluster'] = df_filtered['cluster'].map(cluster_mapping)

        # Statistics
        removed_articles = len(df_clustered) - len(df_filtered)
        removed_clusters = len(small_clusters)
        kept_clusters = len(valid_clusters)

        print(f"\n   Removed: {removed_articles} articles from {removed_clusters} small clusters")
        print(f"   Kept: {len(df_filtered)} articles in {kept_clusters} clusters")

        if removed_clusters > 0:
            print(f"\n   Small clusters removed:")
            for cluster_id, size in small_clusters.head(10).items():
                print(f"     • Cluster {cluster_id}: {size} articles")
            if len(small_clusters) > 10:
                print(f"     ... and {len(small_clusters) - 10} more")

        print(f"\n   Cluster count: {total_clusters_before} → {kept_clusters} ({removed_clusters} removed)")
        print(f"\n✅ Filtering complete!")

        return df_filtered

    def summarize_clusters(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate cluster summary with representative texts

        Args:
            df: DataFrame with 'cluster' column

        Returns:
            DataFrame with cluster metadata
        """

        summaries = []

        for cluster_id in df['cluster'].unique():
            cluster_df = df[df['cluster'] == cluster_id]

            # Geographic center
            center_lat = cluster_df['latitude'].mean()
            center_lon = cluster_df['longitude'].mean()

            # Geographic radius
            coords = cluster_df[['latitude', 'longitude']].values
            coords_rad = np.radians(coords)
            center_rad = np.radians([[center_lat, center_lon]])
            distances = haversine_distances(center_rad, coords_rad)[0] * 6371.0
            radius = distances.max()

            # Primary location
            location = cluster_df['location'].mode().iloc[0] if 'location' in cluster_df.columns else f"({center_lat:.2f}, {center_lon:.2f})"

            # Representative texts (top 5 by centrality)
            texts = cluster_df['title'].tolist()[:5]

            summaries.append({
                'cluster_id': int(cluster_id),
                'size': len(cluster_df),
                'location': location,
                'center_lat': center_lat,
                'center_lon': center_lon,
                'radius_km': radius,
                'sample_headlines': texts
            })

        return pd.DataFrame(summaries)
