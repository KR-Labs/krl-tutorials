"""
Actor Network Analysis for GDELT Events

Constructs and analyzes networks of actors (countries, organizations, groups)
based on their interactions in GDELT Event Database.

Features:
- Directed/undirected graph construction
- Community detection (Louvain)
- Centrality metrics (degree, betweenness, eigenvector)
- Temporal network evolution
- Subgraph extraction by domain

Author: KRL Team
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set

import networkx as nx
import pandas as pd
import psycopg2
from psycopg2 import sql

from .config import DATABASE_CONFIG

logger = logging.getLogger(__name__)


class ActorNetworkAnalyzer:
    """Analyzes actor interaction networks from GDELT events."""
    
    def __init__(self, db_config: Optional[Dict] = None):
        """Initialize network analyzer.
        
        Args:
            db_config: PostgreSQL connection config (defaults to DATABASE_CONFIG)
        """
        self.db_config = db_config or DATABASE_CONFIG
    
    def fetch_interactions(
        self,
        start_date: datetime,
        end_date: datetime,
        domain: Optional[str] = None,
        min_goldstein: Optional[float] = None,
        max_goldstein: Optional[float] = None,
        countries: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """Fetch actor interactions from database.
        
        Args:
            start_date: Start of time window
            end_date: End of time window
            domain: Filter by socioeconomic domain (optional)
            min_goldstein: Minimum Goldstein scale (optional)
            max_goldstein: Maximum Goldstein scale (optional)
            countries: Filter by country codes (optional)
            
        Returns:
            DataFrame with columns: actor1, actor2, event_count, avg_goldstein, avg_tone
        """
        conn = psycopg2.connect(**self.db_config)
        
        # Build query with filters
        query = """
            SELECT
                actor1_code AS actor1,
                actor2_code AS actor2,
                COUNT(*) AS event_count,
                AVG(goldstein_scale) AS avg_goldstein,
                AVG(avg_tone) AS avg_tone,
                ARRAY_AGG(DISTINCT event_code) AS event_types
            FROM gdelt_events
            WHERE
                event_date BETWEEN %(start_date)s AND %(end_date)s
                AND actor1_code IS NOT NULL
                AND actor2_code IS NOT NULL
        """
        
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        
        if domain:
            query += " AND socioeconomic_domain = %(domain)s"
            params['domain'] = domain
        
        if min_goldstein is not None:
            query += " AND goldstein_scale >= %(min_goldstein)s"
            params['min_goldstein'] = min_goldstein
        
        if max_goldstein is not None:
            query += " AND goldstein_scale <= %(max_goldstein)s"
            params['max_goldstein'] = max_goldstein
        
        if countries:
            query += " AND (actor1_country_code = ANY(%(countries)s) OR actor2_country_code = ANY(%(countries)s))"
            params['countries'] = countries
        
        query += """
            GROUP BY actor1_code, actor2_code
            HAVING COUNT(*) >= 5
            ORDER BY event_count DESC
        """
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        logger.info(f"Fetched {len(df):,} actor pairs from {start_date} to {end_date}")
        return df
    
    def build_graph(
        self,
        interactions: pd.DataFrame,
        directed: bool = True,
        weight_by: str = 'event_count'
    ) -> nx.Graph:
        """Build NetworkX graph from interactions.
        
        Args:
            interactions: DataFrame from fetch_interactions()
            directed: True for directed graph, False for undirected
            weight_by: Edge weight attribute ('event_count', 'avg_goldstein', 'avg_tone')
            
        Returns:
            NetworkX Graph or DiGraph
        """
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
        
        logger.info(f"Built {'directed' if directed else 'undirected'} graph: "
                   f"{G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        
        return G
    
    def detect_communities(self, G: nx.Graph) -> Dict[str, int]:
        """Detect communities using Louvain algorithm.
        
        Args:
            G: NetworkX graph
            
        Returns:
            Dict mapping node -> community_id
        """
        # Convert to undirected for community detection
        G_undirected = G.to_undirected() if G.is_directed() else G
        
        try:
            import community as community_louvain  # python-louvain package
            communities = community_louvain.best_partition(G_undirected)
            logger.info(f"Detected {len(set(communities.values()))} communities")
            return communities
        except ImportError:
            logger.warning("python-louvain not installed, using greedy modularity")
            communities_gen = nx.community.greedy_modularity_communities(G_undirected)
            communities = {}
            for i, comm in enumerate(communities_gen):
                for node in comm:
                    communities[node] = i
            logger.info(f"Detected {len(communities_gen)} communities")
            return communities
    
    def calculate_centrality(self, G: nx.Graph) -> Dict[str, Dict[str, float]]:
        """Calculate node centrality metrics.
        
        Args:
            G: NetworkX graph
            
        Returns:
            Dict mapping node -> {'degree', 'betweenness', 'eigenvector'}
        """
        logger.info("Calculating centrality metrics...")
        
        # Degree centrality
        degree_cent = nx.degree_centrality(G)
        
        # Betweenness centrality (sample for large graphs)
        if G.number_of_nodes() > 1000:
            betweenness_cent = nx.betweenness_centrality(G, k=min(1000, G.number_of_nodes()))
        else:
            betweenness_cent = nx.betweenness_centrality(G)
        
        # Eigenvector centrality (with fallback)
        try:
            eigenvector_cent = nx.eigenvector_centrality(G, max_iter=1000)
        except nx.PowerIterationFailedConvergence:
            logger.warning("Eigenvector centrality failed to converge, using zeros")
            eigenvector_cent = {node: 0.0 for node in G.nodes()}
        
        # Combine into single dict
        centrality = {}
        for node in G.nodes():
            centrality[node] = {
                'degree': degree_cent[node],
                'betweenness': betweenness_cent[node],
                'eigenvector': eigenvector_cent[node]
            }
        
        return centrality
    
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
            n: Number of top actors to return
            
        Returns:
            List of (actor, score) tuples
        """
        centrality = self.calculate_centrality(G)
        scores = [(node, centrality[node][metric]) for node in centrality]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:n]
    
    def get_subgraph(
        self,
        G: nx.Graph,
        nodes: Set[str],
        k_hop: int = 1
    ) -> nx.Graph:
        """Extract subgraph around specified nodes.
        
        Args:
            G: NetworkX graph
            nodes: Set of nodes to include
            k_hop: Include neighbors up to k hops away
            
        Returns:
            Subgraph containing nodes and their k-hop neighborhood
        """
        if k_hop == 0:
            return G.subgraph(nodes)
        
        # Get k-hop neighborhood
        neighborhood = set(nodes)
        for _ in range(k_hop):
            new_neighbors = set()
            for node in neighborhood:
                if node in G:
                    new_neighbors.update(G.neighbors(node))
            neighborhood.update(new_neighbors)
        
        subgraph = G.subgraph(neighborhood)
        logger.info(f"Extracted subgraph: {subgraph.number_of_nodes()} nodes, "
                   f"{subgraph.number_of_edges()} edges")
        
        return subgraph
    
    def analyze_temporal_evolution(
        self,
        start_date: datetime,
        end_date: datetime,
        window_days: int = 7,
        domain: Optional[str] = None
    ) -> List[Dict]:
        """Analyze network evolution over time windows.
        
        Args:
            start_date: Start date
            end_date: End date
            window_days: Size of time window in days
            domain: Socioeconomic domain filter (optional)
            
        Returns:
            List of dicts with: {'window_start', 'window_end', 'num_nodes', 'num_edges', 
                                 'density', 'avg_clustering', 'num_communities'}
        """
        results = []
        current_start = start_date
        
        while current_start < end_date:
            current_end = min(current_start + timedelta(days=window_days), end_date)
            
            # Fetch interactions for window
            interactions = self.fetch_interactions(
                current_start,
                current_end,
                domain=domain
            )
            
            if len(interactions) == 0:
                logger.warning(f"No interactions found for {current_start} to {current_end}")
                current_start = current_end
                continue
            
            # Build graph
            G = self.build_graph(interactions, directed=False)
            
            # Calculate metrics
            density = nx.density(G)
            avg_clustering = nx.average_clustering(G) if G.number_of_nodes() > 0 else 0.0
            communities = self.detect_communities(G)
            num_communities = len(set(communities.values()))
            
            results.append({
                'window_start': current_start,
                'window_end': current_end,
                'num_nodes': G.number_of_nodes(),
                'num_edges': G.number_of_edges(),
                'density': density,
                'avg_clustering': avg_clustering,
                'num_communities': num_communities
            })
            
            current_start = current_end
        
        logger.info(f"Analyzed {len(results)} time windows")
        return results
    
    def export_for_visualization(
        self,
        G: nx.Graph,
        output_path: str,
        format: str = 'gexf'
    ):
        """Export graph for visualization in Gephi, Cytoscape, etc.
        
        Args:
            G: NetworkX graph
            output_path: Path to save file
            format: 'gexf', 'graphml', 'gml', or 'json'
        """
        try:
            if format == 'gexf':
                nx.write_gexf(G, output_path)
            elif format == 'graphml':
                nx.write_graphml(G, output_path)
            elif format == 'gml':
                nx.write_gml(G, output_path)
            elif format == 'json':
                import json
                from networkx.readwrite import json_graph
                data = json_graph.node_link_data(G)
                with open(output_path, 'w') as f:
                    json.dump(data, f, indent=2)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            logger.info(f"Exported graph to {output_path} ({format})")
        except Exception as e:
            logger.error(f"Failed to export graph: {e}")


def main():
    """Example usage."""
    logging.basicConfig(level=logging.INFO)
    
    analyzer = ActorNetworkAnalyzer()
    
    # Analyze last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Fetch labor-related interactions
    interactions = analyzer.fetch_interactions(
        start_date,
        end_date,
        domain='labor_and_employment'
    )
    
    print(f"\n=== Labor Network Analysis ({start_date.date()} to {end_date.date()}) ===")
    print(f"Actor pairs: {len(interactions):,}")
    
    if len(interactions) > 0:
        # Build graph
        G = analyzer.build_graph(interactions, directed=False)
        
        # Top actors by degree
        top_actors = analyzer.get_top_actors(G, metric='degree', n=10)
        print("\nTop 10 Actors (by degree centrality):")
        for actor, score in top_actors:
            print(f"  {actor}: {score:.4f}")
        
        # Community detection
        communities = analyzer.detect_communities(G)
        print(f"\nCommunities detected: {len(set(communities.values()))}")


if __name__ == '__main__':
    main()
