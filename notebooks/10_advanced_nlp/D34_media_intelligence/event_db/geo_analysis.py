"""
Geospatial Analysis for GDELT Events

Analyzes geographic patterns in GDELT events:
- Spatial clustering (DBSCAN)
- Hotspot detection
- Heatmap generation
- Country/region aggregation

Author: KRL Team
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import folium
import numpy as np
import pandas as pd
import psycopg2
from folium.plugins import HeatMap, MarkerCluster
from sklearn.cluster import DBSCAN

from .config import DATABASE_CONFIG

logger = logging.getLogger(__name__)


class GeoEventAnalyzer:
    """Analyzes geographic patterns in GDELT events."""
    
    def __init__(self, db_config: Optional[Dict] = None):
        """Initialize geospatial analyzer.
        
        Args:
            db_config: PostgreSQL connection config (defaults to DATABASE_CONFIG)
        """
        self.db_config = db_config or DATABASE_CONFIG
    
    def fetch_geo_events(
        self,
        start_date: datetime,
        end_date: datetime,
        domain: Optional[str] = None,
        countries: Optional[List[str]] = None,
        bbox: Optional[Tuple[float, float, float, float]] = None
    ) -> pd.DataFrame:
        """Fetch events with geospatial data.
        
        Args:
            start_date: Start of time window
            end_date: End of time window
            domain: Filter by socioeconomic domain (optional)
            countries: Filter by country codes (optional)
            bbox: Bounding box (min_lat, min_lon, max_lat, max_lon) (optional)
            
        Returns:
            DataFrame with columns: event_id, event_date, lat, lon, event_code, 
                                   goldstein_scale, avg_tone, socioeconomic_domain
        """
        conn = psycopg2.connect(**self.db_config)
        
        query = """
            SELECT
                event_id,
                event_date,
                action_geo_lat AS lat,
                action_geo_long AS lon,
                action_geo_country_code AS country,
                action_geo_fullname AS location_name,
                event_code,
                goldstein_scale,
                avg_tone,
                socioeconomic_domain,
                socioeconomic_category
            FROM gdelt_events
            WHERE
                event_date BETWEEN %(start_date)s AND %(end_date)s
                AND action_geo_lat IS NOT NULL
                AND action_geo_long IS NOT NULL
        """
        
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        
        if domain:
            query += " AND socioeconomic_domain = %(domain)s"
            params['domain'] = domain
        
        if countries:
            query += " AND action_geo_country_code = ANY(%(countries)s)"
            params['countries'] = countries
        
        if bbox:
            min_lat, min_lon, max_lat, max_lon = bbox
            query += """ AND action_geo_lat BETWEEN %(min_lat)s AND %(max_lat)s
                         AND action_geo_long BETWEEN %(min_lon)s AND %(max_lon)s"""
            params.update({
                'min_lat': min_lat,
                'min_lon': min_lon,
                'max_lat': max_lat,
                'max_lon': max_lon
            })
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        logger.info(f"Fetched {len(df):,} geolocated events")
        return df
    
    def cluster_events(
        self,
        df: pd.DataFrame,
        eps_km: float = 50,
        min_samples: int = 10
    ) -> pd.DataFrame:
        """Cluster events using DBSCAN.
        
        Args:
            df: DataFrame from fetch_geo_events()
            eps_km: Maximum distance between points (in km)
            min_samples: Minimum samples per cluster
            
        Returns:
            DataFrame with 'cluster_id' column added
        """
        if len(df) == 0:
            logger.warning("No events to cluster")
            return df
        
        # Convert km to degrees (approximate)
        eps_deg = eps_km / 111.0  # 1 degree ≈ 111 km
        
        # Extract coordinates
        coords = df[['lat', 'lon']].values
        
        # Run DBSCAN
        clustering = DBSCAN(eps=eps_deg, min_samples=min_samples, metric='haversine')
        df['cluster_id'] = clustering.fit_predict(np.radians(coords))
        
        # Count clusters (excluding noise, cluster_id=-1)
        num_clusters = len(set(df['cluster_id'])) - (1 if -1 in df['cluster_id'].values else 0)
        num_noise = (df['cluster_id'] == -1).sum()
        
        logger.info(f"Detected {num_clusters} clusters, {num_noise} noise points")
        return df
    
    def get_hotspots(
        self,
        df: pd.DataFrame,
        top_n: int = 10
    ) -> pd.DataFrame:
        """Identify event hotspots (top clusters).
        
        Args:
            df: DataFrame with 'cluster_id' column (from cluster_events())
            top_n: Number of top clusters to return
            
        Returns:
            DataFrame with cluster statistics
        """
        # Filter out noise points
        clustered = df[df['cluster_id'] != -1]
        
        # Aggregate by cluster
        hotspots = clustered.groupby('cluster_id').agg({
            'event_id': 'count',
            'lat': 'mean',
            'lon': 'mean',
            'goldstein_scale': 'mean',
            'avg_tone': 'mean',
            'location_name': lambda x: x.mode()[0] if len(x) > 0 else None
        }).reset_index()
        
        hotspots.columns = ['cluster_id', 'event_count', 'center_lat', 'center_lon', 
                           'avg_goldstein', 'avg_tone', 'location_name']
        
        # Sort by event count
        hotspots = hotspots.sort_values('event_count', ascending=False).head(top_n)
        
        logger.info(f"Identified {len(hotspots)} hotspots")
        return hotspots
    
    def create_heatmap(
        self,
        df: pd.DataFrame,
        output_path: str,
        center: Optional[Tuple[float, float]] = None,
        zoom: int = 6
    ):
        """Create interactive heatmap with Folium.
        
        Args:
            df: DataFrame from fetch_geo_events()
            output_path: Path to save HTML file
            center: Map center (lat, lon) (defaults to data centroid)
            zoom: Initial zoom level
        """
        if len(df) == 0:
            logger.warning("No events to visualize")
            return
        
        # Calculate center if not provided
        if center is None:
            center = (df['lat'].median(), df['lon'].median())
        
        # Create base map
        m = folium.Map(location=center, zoom_start=zoom, tiles='OpenStreetMap')
        
        # Add heatmap layer
        heat_data = df[['lat', 'lon']].values.tolist()
        HeatMap(heat_data, radius=15, blur=25, max_zoom=13).add_to(m)
        
        # Save
        m.save(output_path)
        logger.info(f"Saved heatmap to {output_path}")
    
    def create_cluster_map(
        self,
        df: pd.DataFrame,
        hotspots: pd.DataFrame,
        output_path: str,
        center: Optional[Tuple[float, float]] = None,
        zoom: int = 6
    ):
        """Create interactive cluster map with markers.
        
        Args:
            df: DataFrame with cluster_id column
            hotspots: DataFrame from get_hotspots()
            output_path: Path to save HTML file
            center: Map center (lat, lon) (defaults to data centroid)
            zoom: Initial zoom level
        """
        if len(df) == 0:
            logger.warning("No events to visualize")
            return
        
        # Calculate center if not provided
        if center is None:
            center = (df['lat'].median(), df['lon'].median())
        
        # Create base map
        m = folium.Map(location=center, zoom_start=zoom, tiles='CartoDB positron')
        
        # Add marker cluster for all events
        marker_cluster = MarkerCluster(name='All Events').add_to(m)
        
        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=3,
                color='blue',
                fill=True,
                fill_opacity=0.4,
                popup=f"Event {row['event_id']}<br>Cluster: {row['cluster_id']}"
            ).add_to(marker_cluster)
        
        # Add hotspot markers
        for _, hotspot in hotspots.iterrows():
            folium.Marker(
                location=[hotspot['center_lat'], hotspot['center_lon']],
                icon=folium.Icon(color='red', icon='fire'),
                popup=f"""
                    <b>Hotspot {hotspot['cluster_id']}</b><br>
                    Events: {hotspot['event_count']}<br>
                    Location: {hotspot['location_name']}<br>
                    Avg Goldstein: {hotspot['avg_goldstein']:.2f}<br>
                    Avg Tone: {hotspot['avg_tone']:.2f}
                """
            ).add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Save
        m.save(output_path)
        logger.info(f"Saved cluster map to {output_path}")
    
    def aggregate_by_country(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:
        """Aggregate events by country.
        
        Args:
            df: DataFrame from fetch_geo_events()
            
        Returns:
            DataFrame with country-level statistics
        """
        country_stats = df.groupby('country').agg({
            'event_id': 'count',
            'goldstein_scale': 'mean',
            'avg_tone': 'mean',
            'lat': 'mean',
            'lon': 'mean'
        }).reset_index()
        
        country_stats.columns = ['country', 'event_count', 'avg_goldstein', 
                                'avg_tone', 'center_lat', 'center_lon']
        
        country_stats = country_stats.sort_values('event_count', ascending=False)
        
        logger.info(f"Aggregated events across {len(country_stats)} countries")
        return country_stats
    
    def create_choropleth(
        self,
        country_stats: pd.DataFrame,
        output_path: str,
        metric: str = 'event_count'
    ):
        """Create choropleth map by country.
        
        Args:
            country_stats: DataFrame from aggregate_by_country()
            output_path: Path to save HTML file
            metric: Metric to visualize ('event_count', 'avg_goldstein', 'avg_tone')
        """
        # Create base map
        m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')
        
        # Load country boundaries (requires folium with GeoJSON support)
        # Note: For production, you'd load actual country GeoJSON
        # This is a simplified example
        
        # Add country markers instead of full choropleth
        for _, row in country_stats.iterrows():
            folium.CircleMarker(
                location=[row['center_lat'], row['center_lon']],
                radius=np.log1p(row[metric]) * 3,  # Scale by metric
                color='red',
                fill=True,
                fill_opacity=0.6,
                popup=f"""
                    <b>{row['country']}</b><br>
                    Events: {row['event_count']}<br>
                    Avg Goldstein: {row['avg_goldstein']:.2f}<br>
                    Avg Tone: {row['avg_tone']:.2f}
                """
            ).add_to(m)
        
        # Save
        m.save(output_path)
        logger.info(f"Saved choropleth to {output_path}")


def main():
    """Example usage."""
    logging.basicConfig(level=logging.INFO)
    
    analyzer = GeoEventAnalyzer()
    
    # Analyze last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Fetch labor-related events
    df = analyzer.fetch_geo_events(
        start_date,
        end_date,
        domain='labor_and_employment'
    )
    
    print(f"\n=== Geospatial Analysis ({start_date.date()} to {end_date.date()}) ===")
    print(f"Geolocated events: {len(df):,}")
    
    if len(df) > 0:
        # Cluster events
        df = analyzer.cluster_events(df, eps_km=50, min_samples=10)
        
        # Get hotspots
        hotspots = analyzer.get_hotspots(df, top_n=10)
        print("\nTop 10 Hotspots:")
        for _, hotspot in hotspots.iterrows():
            print(f"  {hotspot['location_name']}: {hotspot['event_count']} events "
                  f"(Goldstein: {hotspot['avg_goldstein']:.2f})")
        
        # Create visualizations
        analyzer.create_heatmap(df, 'labor_heatmap.html')
        analyzer.create_cluster_map(df, hotspots, 'labor_clusters.html')
        print("\nSaved visualizations to labor_heatmap.html and labor_clusters.html")


if __name__ == '__main__':
    main()
