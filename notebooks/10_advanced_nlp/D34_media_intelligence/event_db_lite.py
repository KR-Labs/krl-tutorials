"""
Lightweight Event Database Analytics for In-Memory Prototyping

This module provides the same analytics as event_db/ but works with
pandas DataFrames directly (no PostgreSQL required).

Perfect for MVP/prototype workflows:
1. Fetch data from GDELT via connector
2. Apply analytics in-memory
3. Validate approach before infrastructure investment

Author: KRL Team
"""

import logging
from typing import Dict, List, Optional, Tuple, Set
from datetime import datetime

import numpy as np
import pandas as pd
import networkx as nx
from sklearn.cluster import DBSCAN

logger = logging.getLogger(__name__)


class CAMEOMapperLite:
    """Lightweight CAMEO event code mapper (no file I/O)."""
    
    CAMEO_MAPPING = {
        # Labor & Employment
        '14': ('labor_and_employment', 'labor_action', 0.95),
        '145': ('labor_and_employment', 'labor_action', 1.0),
        '1451': ('labor_and_employment', 'labor_action', 1.0),
        '06': ('labor_and_employment', 'policy_announcement', 0.80),
        '061': ('labor_and_employment', 'policy_announcement', 0.85),
        
        # Health & Social Policy
        '02': ('health_and_social_policy', 'humanitarian_aid', 0.75),
        '07': ('health_and_social_policy', 'humanitarian_aid', 0.90),
        '071': ('health_and_social_policy', 'humanitarian_aid', 0.95),
        '072': ('health_and_social_policy', 'healthcare_provision', 0.95),
        '087': ('health_and_social_policy', 'healthcare_provision', 0.90),
        
        # Inequality & Poverty
        '12': ('inequality_and_poverty', 'discrimination', 0.85),
        '13': ('inequality_and_poverty', 'discrimination', 0.80),
        '18': ('inequality_and_poverty', 'violence_against_civilians', 0.90),
        '181': ('inequality_and_poverty', 'violence_against_civilians', 0.95),
        '182': ('inequality_and_poverty', 'violence_against_civilians', 0.95),
        
        # Education & Youth
        '141': ('education_and_youth', 'student_protest', 0.90),
        '1411': ('education_and_youth', 'student_protest', 0.95),
        '04': ('education_and_youth', 'policy_announcement', 0.70),
        
        # Governance & Corruption
        '10': ('governance_and_corruption', 'legal_action', 0.90),
        '101': ('governance_and_corruption', 'legal_action', 0.95),
        '11': ('governance_and_corruption', 'sanctions', 0.90),
        '19': ('governance_and_corruption', 'military_action', 0.85),
        '172': ('governance_and_corruption', 'sanctions', 0.90),
        
        # Climate & Environment
        '143': ('climate_and_environment', 'environmental_protest', 0.90),
        '20': ('climate_and_environment', 'environmental_disaster', 0.80),
    }
    
    def categorize_event(self, event_code: str) -> Dict:
        """Categorize event by CAMEO code."""
        if not event_code:
            return {'domain': 'uncategorized', 'category': 'unknown', 'confidence': 0.0}
        
        event_code = str(event_code)
        
        # Try exact match
        if event_code in self.CAMEO_MAPPING:
            domain, category, confidence = self.CAMEO_MAPPING[event_code]
            return {'domain': domain, 'category': category, 'confidence': confidence}
        
        # Try root code (first 2 digits)
        root_code = event_code[:2]
        if root_code in self.CAMEO_MAPPING:
            domain, category, confidence = self.CAMEO_MAPPING[root_code]
            return {'domain': domain, 'category': category, 'confidence': confidence * 0.8}
        
        # Try base code (first digit)
        base_code = event_code[:1]
        if base_code in self.CAMEO_MAPPING:
            domain, category, confidence = self.CAMEO_MAPPING[base_code]
            return {'domain': domain, 'category': category, 'confidence': confidence * 0.6}
        
        return {'domain': 'uncategorized', 'category': 'unknown', 'confidence': 0.0}
    
    def categorize_dataframe(self, df: pd.DataFrame, event_code_col: str = 'EventCode') -> pd.DataFrame:
        """Apply CAMEO categorization to DataFrame.
        
        Args:
            df: DataFrame with event code column
            event_code_col: Name of column containing CAMEO codes
            
        Returns:
            DataFrame with added columns: socioeconomic_domain, socioeconomic_category, category_confidence
        """
        if event_code_col not in df.columns:
            logger.warning(f"Column '{event_code_col}' not found")
            df['socioeconomic_domain'] = 'uncategorized'
            df['socioeconomic_category'] = 'unknown'
            df['category_confidence'] = 0.0
            return df
        
        categorization = df[event_code_col].apply(self.categorize_event)
        df['socioeconomic_domain'] = categorization.apply(lambda x: x['domain'])
        df['socioeconomic_category'] = categorization.apply(lambda x: x['category'])
        df['category_confidence'] = categorization.apply(lambda x: x['confidence'])
        
        return df


class ActorNetworkAnalyzerLite:
    """Lightweight actor network analyzer (works with DataFrames)."""
    
    def build_interactions_df(
        self,
        events_df: pd.DataFrame,
        actor1_col: str = 'Actor1Code',
        actor2_col: str = 'Actor2Code',
        goldstein_col: str = 'GoldsteinScale',
        tone_col: str = 'AvgTone',
        event_code_col: str = 'EventCode',
        domain_filter: Optional[str] = None
    ) -> pd.DataFrame:
        """Build actor interactions DataFrame from events.
        
        Args:
            events_df: DataFrame with event data
            actor1_col: Column name for actor 1
            actor2_col: Column name for actor 2
            goldstein_col: Column name for Goldstein scale
            tone_col: Column name for tone
            event_code_col: Column name for event codes
            domain_filter: Filter by socioeconomic domain (optional)
            
        Returns:
            DataFrame with columns: actor1, actor2, event_count, avg_goldstein, avg_tone
        """
        df = events_df.copy()
        
        # Apply domain filter
        if domain_filter and 'socioeconomic_domain' in df.columns:
            df = df[df['socioeconomic_domain'] == domain_filter]
        
        # Remove rows with missing actors
        df = df.dropna(subset=[actor1_col, actor2_col])
        
        if len(df) == 0:
            return pd.DataFrame(columns=['actor1', 'actor2', 'event_count', 'avg_goldstein', 'avg_tone'])
        
        # Aggregate interactions
        interactions = df.groupby([actor1_col, actor2_col]).agg({
            goldstein_col: 'mean',
            tone_col: 'mean',
            event_code_col: 'count'
        }).reset_index()
        
        interactions.columns = ['actor1', 'actor2', 'avg_goldstein', 'avg_tone', 'event_count']
        
        return interactions
    
    def build_graph(
        self,
        interactions: pd.DataFrame,
        directed: bool = True,
        weight_by: str = 'event_count',
        min_interactions: int = 2
    ) -> nx.Graph:
        """Build NetworkX graph from interactions.
        
        Args:
            interactions: DataFrame from build_interactions_df()
            directed: True for directed graph, False for undirected
            weight_by: Edge weight attribute
            min_interactions: Minimum interactions to include edge
            
        Returns:
            NetworkX Graph or DiGraph
        """
        # Filter by minimum interactions
        interactions = interactions[interactions['event_count'] >= min_interactions]
        
        G = nx.DiGraph() if directed else nx.Graph()
        
        for _, row in interactions.iterrows():
            G.add_edge(
                row['actor1'],
                row['actor2'],
                weight=row[weight_by],
                event_count=row['event_count'],
                avg_goldstein=row['avg_goldstein'],
                avg_tone=row['avg_tone']
            )
        
        logger.info(f"Built graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        return G
    
    def get_top_actors(
        self,
        G: nx.Graph,
        metric: str = 'degree',
        n: int = 20
    ) -> List[Tuple[str, float]]:
        """Get top actors by centrality metric.
        
        Args:
            G: NetworkX graph
            metric: 'degree', 'betweenness', or 'eigenvector'
            n: Number of top actors
            
        Returns:
            List of (actor, score) tuples
        """
        if G.number_of_nodes() == 0:
            return []
        
        if metric == 'degree':
            centrality = nx.degree_centrality(G)
        elif metric == 'betweenness':
            k = min(500, G.number_of_nodes())
            centrality = nx.betweenness_centrality(G, k=k)
        elif metric == 'eigenvector':
            try:
                centrality = nx.eigenvector_centrality(G, max_iter=1000)
            except:
                centrality = {node: 0.0 for node in G.nodes()}
        else:
            raise ValueError(f"Unknown metric: {metric}")
        
        scores = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        return scores[:n]
    
    def detect_communities(self, G: nx.Graph) -> Dict[str, int]:
        """Detect communities using greedy modularity."""
        G_undirected = G.to_undirected() if G.is_directed() else G
        
        if G_undirected.number_of_nodes() == 0:
            return {}
        
        communities_gen = nx.community.greedy_modularity_communities(G_undirected)
        communities = {}
        for i, comm in enumerate(communities_gen):
            for node in comm:
                communities[node] = i
        
        return communities


class GeoEventAnalyzerLite:
    """Lightweight geospatial analyzer (works with DataFrames)."""
    
    def cluster_events(
        self,
        df: pd.DataFrame,
        lat_col: str = 'ActionGeo_Lat',
        lon_col: str = 'ActionGeo_Long',
        eps_km: float = 50,
        min_samples: int = 10
    ) -> pd.DataFrame:
        """Cluster events using DBSCAN.
        
        Args:
            df: DataFrame with lat/lon columns
            lat_col: Latitude column name
            lon_col: Longitude column name
            eps_km: Maximum distance between points (km)
            min_samples: Minimum samples per cluster
            
        Returns:
            DataFrame with 'cluster_id' column added
        """
        # Filter to geolocated events
        geo_df = df.dropna(subset=[lat_col, lon_col]).copy()
        
        if len(geo_df) == 0:
            df['cluster_id'] = -1
            return df
        
        # Convert km to degrees (approximate)
        eps_deg = eps_km / 111.0
        
        # Extract coordinates
        coords = geo_df[[lat_col, lon_col]].values
        
        # Run DBSCAN
        clustering = DBSCAN(eps=eps_deg, min_samples=min_samples, metric='euclidean')
        geo_df['cluster_id'] = clustering.fit_predict(coords)
        
        # Merge back to original df
        df = df.merge(
            geo_df[['cluster_id']],
            left_index=True,
            right_index=True,
            how='left'
        )
        df['cluster_id'] = df['cluster_id'].fillna(-1).astype(int)
        
        num_clusters = len(set(df['cluster_id'])) - (1 if -1 in df['cluster_id'].values else 0)
        logger.info(f"Detected {num_clusters} clusters")
        
        return df
    
    def get_hotspots(
        self,
        df: pd.DataFrame,
        lat_col: str = 'ActionGeo_Lat',
        lon_col: str = 'ActionGeo_Long',
        goldstein_col: str = 'GoldsteinScale',
        tone_col: str = 'AvgTone',
        top_n: int = 10
    ) -> pd.DataFrame:
        """Identify event hotspots.
        
        Args:
            df: DataFrame with cluster_id column
            lat_col: Latitude column name
            lon_col: Longitude column name
            goldstein_col: Goldstein scale column name
            tone_col: Tone column name
            top_n: Number of top clusters
            
        Returns:
            DataFrame with hotspot statistics
        """
        if 'cluster_id' not in df.columns:
            logger.warning("No cluster_id column found")
            return pd.DataFrame()
        
        # Filter out noise points
        clustered = df[df['cluster_id'] != -1]
        
        if len(clustered) == 0:
            return pd.DataFrame()
        
        # Aggregate by cluster
        hotspots = clustered.groupby('cluster_id').agg({
            lat_col: 'mean',
            lon_col: 'mean',
            goldstein_col: 'mean',
            tone_col: 'mean',
            'cluster_id': 'count'
        }).reset_index()
        
        hotspots.columns = ['cluster_id', 'center_lat', 'center_lon', 
                           'avg_goldstein', 'avg_tone', 'event_count']
        
        # Sort by event count
        hotspots = hotspots.sort_values('event_count', ascending=False).head(top_n)
        
        return hotspots
