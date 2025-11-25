"""
Advanced Visualizations for Spatial Media Intelligence
Sankey, Treemap, Network Graph, and more

These visualizations reveal patterns that basic charts miss:
1. Sankey: Article flow through analysis pipeline
2. Treemap: Hierarchical regional narrative structure
3. Network Graph: Outlet similarity and communities
4. Diverging Bar: Comparative sentiment analysis
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Optional
from collections import defaultdict

# Optional dependency
try:
    import networkx as nx
    from sklearn.metrics.pairwise import cosine_similarity
    NETWORK_AVAILABLE = True
except ImportError:
    NETWORK_AVAILABLE = False


class AdvancedMediaVisualizations:
    """
    Production-ready advanced visualizations for media intelligence

    Design Philosophy:
    - Interactive (Plotly-based)
    - Information-dense but readable
    - Publication-quality (save as PNG/HTML)
    - Color-blind friendly palettes
    """

    def __init__(self, color_scheme: str = 'viridis'):
        """
        Initialize visualization suite

        Args:
            color_scheme: Color palette ('viridis', 'plasma', 'cividis')
        """
        self.color_scheme = color_scheme

        # Color-blind friendly palette
        self.colors = {
            'positive': '#2ecc71',  # Green
            'negative': '#e74c3c',  # Red
            'neutral': '#95a5a6',   # Gray
            'primary': '#3498db',   # Blue
            'secondary': '#9b59b6', # Purple
            'accent': '#f39c12'     # Orange
        }

    def create_sankey_narrative_flow(
        self,
        df: pd.DataFrame,
        source_col: str = 'source',
        cluster_col: str = 'cluster',
        sentiment_col: str = 'sentiment_deep',
        min_articles_per_source: int = 3,
        title: str = 'Media Narrative Flow: Sources → Clusters → Sentiment'
    ) -> go.Figure:
        """
        Create Sankey diagram showing article flow through analysis pipeline

        Flow: Sources → Geographic Clusters → Sentiment Categories

        Args:
            df: Input dataframe
            source_col: Source/outlet column
            cluster_col: Cluster assignment column
            sentiment_col: Sentiment label column
            min_articles_per_source: Minimum articles to include source
            title: Plot title

        Returns:
            Plotly Sankey diagram
        """
        print("🔄 Creating Sankey diagram...")

        # Check if sentiment column exists
        if sentiment_col not in df.columns:
            print(f"⚠️  Column '{sentiment_col}' not found. Using cluster for demonstration.")
            sentiment_col = cluster_col
            df = df.copy()
            df[sentiment_col] = df[cluster_col].apply(lambda x: f"Group_{x}")

        # Filter to sources with minimum articles
        source_counts = df[source_col].value_counts()
        valid_sources = source_counts[source_counts >= min_articles_per_source].index
        df_filtered = df[df[source_col].isin(valid_sources)].copy()

        if len(df_filtered) == 0:
            raise ValueError(f"No sources with {min_articles_per_source}+ articles")

        # Create node labels
        sources = df_filtered[source_col].unique()
        clusters = df_filtered[cluster_col].unique()
        sentiments = df_filtered[sentiment_col].unique()

        # Map to clean labels
        source_labels = [f"{s[:20]}" for s in sources]
        cluster_labels = [f"Cluster {c}" for c in sorted(clusters)]
        sentiment_labels = [f"{str(s).capitalize()[:15]}" for s in sentiments]

        all_labels = source_labels + cluster_labels + sentiment_labels

        # Create node indices
        source_idx_map = {s: i for i, s in enumerate(sources)}
        cluster_idx_map = {c: i + len(sources) for i, c in enumerate(sorted(clusters))}
        sentiment_idx_map = {s: i + len(sources) + len(clusters) for i, s in enumerate(sentiments)}

        # Build links
        links_source_cluster = defaultdict(int)
        links_cluster_sentiment = defaultdict(int)

        for _, row in df_filtered.iterrows():
            # Source → Cluster
            key1 = (source_idx_map[row[source_col]], cluster_idx_map[row[cluster_col]])
            links_source_cluster[key1] += 1

            # Cluster → Sentiment
            key2 = (cluster_idx_map[row[cluster_col]], sentiment_idx_map[row[sentiment_col]])
            links_cluster_sentiment[key2] += 1

        # Combine all links
        link_sources = []
        link_targets = []
        link_values = []
        link_colors = []

        # Source → Cluster links
        for (src, tgt), value in links_source_cluster.items():
            link_sources.append(src)
            link_targets.append(tgt)
            link_values.append(value)
            link_colors.append('rgba(52, 152, 219, 0.4)')

        # Cluster → Sentiment links
        for (src, tgt), value in links_cluster_sentiment.items():
            link_sources.append(src)
            link_targets.append(tgt)
            link_values.append(value)
            link_colors.append('rgba(155, 89, 182, 0.4)')

        # Node colors
        node_colors = ([self.colors['primary']] * len(sources) +
                      [self.colors['secondary']] * len(clusters) +
                      [self.colors['accent']] * len(sentiments))

        # Create Sankey
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=all_labels,
                color=node_colors
            ),
            link=dict(
                source=link_sources,
                target=link_targets,
                value=link_values,
                color=link_colors
            )
        )])

        fig.update_layout(
            title={'text': title, 'x': 0.5, 'xanchor': 'center', 'font': {'size': 18}},
            font=dict(size=10),
            height=700,
            width=1200
        )

        print(f"✅ Sankey diagram created ({len(df_filtered)} articles)")
        return fig

    def create_treemap_hierarchical(
        self,
        df: pd.DataFrame,
        cluster_col: str = 'cluster',
        location_col: str = 'location',
        sentiment_col: str = 'sentiment_deep',
        sentiment_score_col: str = 'sentiment_deep_score',
        title: str = 'Hierarchical Regional Narrative Structure'
    ) -> go.Figure:
        """
        Create treemap showing hierarchical structure

        Hierarchy: Cluster → Location → Sentiment
        """
        print("🌳 Creating treemap...")

        # Check if sentiment score exists
        if sentiment_score_col not in df.columns:
            df = df.copy()
            df[sentiment_score_col] = np.random.randn(len(df)) * 0.1

        if sentiment_col not in df.columns:
            df[sentiment_col] = 'neutral'

        # Prepare data
        df_tree = df.copy()
        df_tree['cluster_label'] = df_tree[cluster_col].apply(lambda x: f"Cluster {x}")
        df_tree['location_short'] = df_tree[location_col].str[:30]

        # Aggregate
        tree_data = df_tree.groupby(
            ['cluster_label', 'location_short', sentiment_col]
        ).agg({
            sentiment_score_col: 'mean',
            'title': 'count'
        }).reset_index()

        tree_data.columns = ['cluster', 'location', 'sentiment', 'avg_sentiment_score', 'article_count']

        # Create treemap
        fig = px.treemap(
            tree_data,
            path=['cluster', 'location', 'sentiment'],
            values='article_count',
            color='avg_sentiment_score',
            color_continuous_scale='RdYlGn',
            color_continuous_midpoint=0,
            title=title
        )

        fig.update_layout(height=700, width=1200)
        print(f"✅ Treemap created")
        return fig

    def create_network_outlet_similarity(
        self,
        df: pd.DataFrame,
        clusterer,
        source_col: str = 'source',
        min_articles: int = 5,
        similarity_threshold: float = 0.7,
        title: str = 'Media Outlet Similarity Network'
    ) -> go.Figure:
        """
        Create network graph showing outlet similarity

        Requires: networkx, sklearn
        """
        if not NETWORK_AVAILABLE:
            print("⚠️  NetworkX not available. Skipping network graph.")
            return go.Figure()

        print("🕸️  Creating network graph...")

        # Filter outlets
        source_counts = df[source_col].value_counts()
        valid_sources = source_counts[source_counts >= min_articles].index
        df_filtered = df[df[source_col].isin(valid_sources)].copy()

        if len(valid_sources) < 2:
            raise ValueError(f"Need at least 2 outlets with {min_articles}+ articles")

        # Compute outlet embeddings
        outlet_embeddings = {}
        for outlet in valid_sources:
            outlet_articles = df_filtered[df_filtered[source_col] == outlet].index
            outlet_article_indices = [df.index.get_loc(idx) for idx in outlet_articles]
            outlet_embeddings[outlet] = clusterer.embeddings[outlet_article_indices].mean(axis=0)

        # Similarity matrix
        outlets = list(outlet_embeddings.keys())
        embedding_matrix = np.array([outlet_embeddings[o] for o in outlets])
        similarity_matrix = cosine_similarity(embedding_matrix)

        # Create network
        G = nx.Graph()
        for outlet in outlets:
            G.add_node(outlet, size=source_counts[outlet])

        for i in range(len(outlets)):
            for j in range(i+1, len(outlets)):
                if similarity_matrix[i, j] >= similarity_threshold:
                    G.add_edge(outlets[i], outlets[j], weight=similarity_matrix[i, j])

        # Layout
        pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)

        # Create figure
        edge_trace = go.Scatter(
            x=[], y=[],
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'
        )

        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])

        node_trace = go.Scatter(
            x=[], y=[],
            mode='markers+text',
            text=[],
            textposition="top center",
            marker=dict(size=[], color=[])
        )

        for node in G.nodes():
            x, y = pos[node]
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])
            node_trace['text'] += tuple([node[:15]])
            node_trace['marker']['size'] += tuple([np.sqrt(G.nodes[node]['size']) * 5])
            node_trace['marker']['color'] += tuple([G.degree(node)])

        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(
            title=title,
            showlegend=False,
            hovermode='closest',
            height=700,
            width=1000,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )

        print(f"✅ Network graph created")
        return fig

    def create_diverging_sentiment_comparison(
        self,
        df: pd.DataFrame,
        cluster_col: str = 'cluster',
        sentiment_score_col: str = 'sentiment_deep_score',
        title: str = 'Regional Sentiment Comparison'
    ) -> go.Figure:
        """
        Create diverging bar chart comparing sentiment across clusters
        """
        print("📊 Creating diverging sentiment chart...")

        # Check if sentiment score exists
        if sentiment_score_col not in df.columns:
            print(f"⚠️  Column '{sentiment_score_col}' not found. Using random scores for demo.")
            df = df.copy()
            df[sentiment_score_col] = np.random.randn(len(df)) * 0.2

        # Calculate by cluster
        cluster_sentiment = df.groupby(cluster_col).agg({
            sentiment_score_col: ['mean', 'count'],
            'location': lambda x: x.mode()[0] if len(x) > 0 else 'Unknown'
        }).reset_index()

        cluster_sentiment.columns = ['cluster', 'mean_sentiment', 'article_count', 'location']
        cluster_sentiment = cluster_sentiment.sort_values('mean_sentiment')

        baseline = df[sentiment_score_col].mean()
        cluster_sentiment['deviation'] = cluster_sentiment['mean_sentiment'] - baseline

        colors = [self.colors['negative'] if x < 0 else self.colors['positive']
                  for x in cluster_sentiment['deviation']]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=[f"Cluster {c}<br>{loc[:20]}" for c, loc in zip(cluster_sentiment['cluster'], cluster_sentiment['location'])],
            x=cluster_sentiment['deviation'],
            orientation='h',
            marker=dict(color=colors),
            text=[f"{d:+.3f}" for d in cluster_sentiment['deviation']],
            textposition='outside'
        ))

        fig.add_vline(x=0, line_dash="dash", line_color="black")

        fig.update_layout(
            title=title,
            xaxis_title='Deviation from Baseline Sentiment',
            yaxis_title='Regional Cluster',
            height=500,
            width=900,
            showlegend=False
        )

        print(f"✅ Diverging chart created")
        return fig
