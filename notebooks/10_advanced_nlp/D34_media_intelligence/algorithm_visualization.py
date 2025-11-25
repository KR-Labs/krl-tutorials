"""
3D Visualization of Spatial-Semantic Distance Algorithm
Proves patent-pending innovation by showing how λ_spatial combines distances
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from typing import Optional


class AlgorithmVisualizer:
    """
    Visualize the spatial-semantic distance algorithm

    Key Insight: Shows how λ_spatial=0.15 trades off between:
    - Semantic distance (text similarity)
    - Spatial distance (geographic separation)
    - Combined distance (final clustering metric)
    """

    @staticmethod
    def visualize_distance_tradeoff(
        df: pd.DataFrame,
        semantic_dist: np.ndarray,
        spatial_dist: np.ndarray,
        combined_dist: np.ndarray,
        spatial_weight: float,
        sample_size: int = 200,
        title: str = "Patent-Pending Algorithm: Spatial-Semantic Distance Trade-off"
    ) -> go.Figure:
        """
        Create 3D scatter plot showing distance combination

        Args:
            df: Dataframe with cluster labels
            semantic_dist: Semantic distance matrix
            spatial_dist: Spatial distance matrix
            combined_dist: Combined distance matrix
            spatial_weight: λ_spatial parameter
            sample_size: Number of article pairs to visualize
            title: Plot title

        Returns:
            Plotly Figure object
        """
        # Sample article pairs for visualization
        n_articles = len(df)
        sample_indices = np.random.choice(n_articles, min(sample_size, n_articles), replace=False)

        # Get pairwise distances for sample
        semantic_sample = []
        spatial_sample = []
        combined_sample = []
        cluster_sample = []

        for i in range(len(sample_indices)):
            for j in range(i+1, min(i+20, len(sample_indices))):  # Limit pairs
                idx_i = sample_indices[i]
                idx_j = sample_indices[j]

                semantic_sample.append(semantic_dist[idx_i, idx_j])
                spatial_sample.append(spatial_dist[idx_i, idx_j])
                combined_sample.append(combined_dist[idx_i, idx_j])

                # Same cluster or different?
                same_cluster = df.iloc[idx_i]['cluster'] == df.iloc[idx_j]['cluster']
                cluster_sample.append('Same Cluster' if same_cluster else 'Different Cluster')

        # Create 3D scatter plot
        fig = go.Figure()

        # Points colored by whether they're in same cluster
        for cluster_type in ['Same Cluster', 'Different Cluster']:
            mask = np.array(cluster_sample) == cluster_type

            fig.add_trace(go.Scatter3d(
                x=np.array(semantic_sample)[mask],
                y=np.array(spatial_sample)[mask],
                z=np.array(combined_sample)[mask],
                mode='markers',
                name=cluster_type,
                marker=dict(
                    size=4,
                    color='green' if cluster_type == 'Same Cluster' else 'red',
                    opacity=0.6
                ),
                text=[f"Sem: {s:.3f}<br>Spa: {sp:.3f}<br>Comb: {c:.3f}"
                      for s, sp, c in zip(
                          np.array(semantic_sample)[mask],
                          np.array(spatial_sample)[mask],
                          np.array(combined_sample)[mask]
                      )],
                hovertemplate='%{text}<extra></extra>'
            ))

        # Add plane showing combination formula
        semantic_range = np.linspace(0, 1, 10)
        spatial_range = np.linspace(0, 1, 10)
        S, P = np.meshgrid(semantic_range, spatial_range)

        # Combined distance surface: (1-λ)*semantic + λ*spatial
        C = (1 - spatial_weight) * S + spatial_weight * P

        fig.add_trace(go.Surface(
            x=S, y=P, z=C,
            colorscale='Blues',
            opacity=0.3,
            showscale=False,
            name=f'Formula Surface (λ={spatial_weight})',
            hovertemplate='Formula Surface<extra></extra>'
        ))

        # Update layout
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16}
            },
            scene=dict(
                xaxis_title='Semantic Distance (text similarity)',
                yaxis_title='Spatial Distance (kilometers, normalized)',
                zaxis_title='Combined Distance (clustering metric)',
                xaxis=dict(range=[0, 1]),
                yaxis=dict(range=[0, 1]),
                zaxis=dict(range=[0, 1])
            ),
            width=1000,
            height=700,
            showlegend=True,
            legend=dict(x=0.7, y=0.95)
        )

        # Add annotation explaining the algorithm
        fig.add_annotation(
            text=(
                f"<b>Trade Secret Formula:</b><br>"
                f"Combined Distance = (1 - λ) × Semantic + λ × Spatial<br>"
                f"λ_spatial = {spatial_weight:.2f} (patent-pending parameter)<br><br>"
                f"<b>Interpretation:</b><br>"
                f"• Green points: Article pairs in same cluster<br>"
                f"• Red points: Article pairs in different clusters<br>"
                f"• Blue surface: Theoretical combination surface"
            ),
            xref="paper", yref="paper",
            x=0.02, y=0.98,
            showarrow=False,
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="black",
            borderwidth=1,
            font=dict(size=10),
            align="left",
            xanchor="left",
            yanchor="top"
        )

        return fig

    @staticmethod
    def create_cluster_distribution_chart(df: pd.DataFrame) -> go.Figure:
        """
        Create visual chart showing cluster size distribution

        Args:
            df: DataFrame with 'cluster' column

        Returns:
            Plotly Figure
        """
        cluster_counts = df['cluster'].value_counts().sort_index()

        fig = go.Figure(data=[
            go.Bar(
                x=[f"Cluster {i}" for i in cluster_counts.index],
                y=cluster_counts.values,
                text=[f"{count}<br>({count/len(df)*100:.1f}%)" for count in cluster_counts.values],
                textposition='auto',
                marker_color=['red' if count/len(df) > 0.4 else 'green' for count in cluster_counts.values]
            )
        ])

        fig.update_layout(
            title="Cluster Size Distribution",
            xaxis_title="Cluster",
            yaxis_title="Number of Articles",
            height=400,
            showlegend=False
        )

        # Add target line at 40%
        fig.add_hline(
            y=len(df) * 0.4,
            line_dash="dash",
            line_color="orange",
            annotation_text="Target max: 40%",
            annotation_position="right"
        )

        return fig
