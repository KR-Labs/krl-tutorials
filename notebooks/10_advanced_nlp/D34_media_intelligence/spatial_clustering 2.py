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

    def __init__(self, spatial_weight=0.15):
        """
        Initialize clusterer

        Args:
            spatial_weight: Weight for spatial distance (trade secret: 0.15)
        """
        self.spatial_weight = spatial_weight
        print(f"\n🧠 Initializing Spatial Clusterer...")
        print(f"   λ_spatial (trade secret): {spatial_weight}")

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

        # Hierarchical clustering
        clustering = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=0.5,
            metric='precomputed',
            linkage='average'
        )

        labels = clustering.fit_predict(combined_dist)

        # Add to dataframe
        df['cluster'] = labels

        n_clusters = len(np.unique(labels))
        print(f"\n✓ Discovered {n_clusters} spatial narrative clusters")

        return df

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

        # Hierarchical clustering (same as fixed method)
        clustering = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=0.5,
            metric='precomputed',
            linkage='average'
        )

        labels = clustering.fit_predict(combined_dist)

        # Add to dataframe
        df_result = df.copy()
        df_result['cluster'] = labels

        n_clusters = len(np.unique(labels))
        print(f"\n✓ Discovered {n_clusters} spatial narrative clusters (ADAPTIVE)")

        return df_result

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
