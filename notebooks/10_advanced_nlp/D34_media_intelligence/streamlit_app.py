"""
Streamlit Dashboard for Event Database

Interactive web dashboard for exploring:
- Event search and filtering
- Actor network visualization
- Geospatial analysis
- Domain-specific insights

Run with: streamlit run streamlit_app.py

Author: KRL Team
"""

import logging
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static

from event_db.actor_networks import ActorNetworkAnalyzer
from event_db.cameo_mapping import CAMEOMapper
from event_db.geo_analysis import GeoEventAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="Event Database Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize analyzers
@st.cache_resource
def get_analyzers():
    """Initialize analyzers (cached)."""
    return {
        'network': ActorNetworkAnalyzer(),
        'geo': GeoEventAnalyzer(),
        'cameo': CAMEOMapper()
    }

analyzers = get_analyzers()


# Sidebar filters
st.sidebar.title("🔍 Filters")

# Date range
default_end = datetime.now() - timedelta(days=1)
default_start = default_end - timedelta(days=30)

start_date = st.sidebar.date_input(
    "Start Date",
    value=default_start,
    max_value=default_end
)
end_date = st.sidebar.date_input(
    "End Date",
    value=default_end,
    max_value=datetime.now()
)

# Domain filter
domains = [
    "All Domains",
    "labor_and_employment",
    "health_and_social_policy",
    "inequality_and_poverty",
    "education_and_youth",
    "governance_and_corruption",
    "climate_and_environment"
]
selected_domain = st.sidebar.selectbox("Socioeconomic Domain", domains)
domain_filter = None if selected_domain == "All Domains" else selected_domain

# Main content
st.title("🌍 Event Database Analytics Dashboard")
st.markdown(f"**Analysis Period:** {start_date} to {end_date}")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔗 Actor Networks", "🗺️ Geospatial", "📈 Trends"])


# TAB 1: Overview
with tab1:
    st.header("Event Overview")
    
    # Fetch events
    with st.spinner("Loading events..."):
        try:
            df = analyzers['geo'].fetch_geo_events(
                datetime.combine(start_date, datetime.min.time()),
                datetime.combine(end_date, datetime.min.time()),
                domain=domain_filter
            )
            
            if len(df) == 0:
                st.warning("No events found for selected filters.")
            else:
                # Summary metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Events", f"{len(df):,}")
                
                with col2:
                    avg_goldstein = df['goldstein_scale'].mean()
                    st.metric("Avg Goldstein Scale", f"{avg_goldstein:.2f}")
                
                with col3:
                    avg_tone = df['avg_tone'].mean()
                    st.metric("Avg Tone", f"{avg_tone:.2f}")
                
                with col4:
                    num_countries = df['country'].nunique()
                    st.metric("Countries", num_countries)
                
                # Domain distribution
                st.subheader("Events by Domain")
                domain_counts = df['socioeconomic_domain'].value_counts()
                fig = px.bar(
                    x=domain_counts.index,
                    y=domain_counts.values,
                    labels={'x': 'Domain', 'y': 'Event Count'},
                    title="Event Distribution by Socioeconomic Domain"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Top countries
                st.subheader("Top 10 Countries")
                country_counts = df['country'].value_counts().head(10)
                fig = px.bar(
                    x=country_counts.values,
                    y=country_counts.index,
                    orientation='h',
                    labels={'x': 'Event Count', 'y': 'Country'},
                    title="Events by Country"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Event table
                st.subheader("Recent Events")
                display_cols = ['event_date', 'country', 'location_name', 
                               'socioeconomic_domain', 'goldstein_scale', 'avg_tone']
                st.dataframe(df[display_cols].head(100), use_container_width=True)
        
        except Exception as e:
            st.error(f"Failed to load events: {e}")
            logger.error(f"Overview tab error: {e}")


# TAB 2: Actor Networks
with tab2:
    st.header("Actor Network Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("Network Settings")
        directed = st.checkbox("Directed Graph", value=False)
        top_n = st.slider("Top Actors", min_value=5, max_value=50, value=20)
    
    with col1:
        with st.spinner("Building actor network..."):
            try:
                interactions = analyzers['network'].fetch_interactions(
                    datetime.combine(start_date, datetime.min.time()),
                    datetime.combine(end_date, datetime.min.time()),
                    domain=domain_filter
                )
                
                if len(interactions) == 0:
                    st.warning("No actor interactions found.")
                else:
                    # Build graph
                    G = analyzers['network'].build_graph(interactions, directed=directed)
                    
                    # Graph stats
                    st.metric("Actor Pairs", len(interactions))
                    col1_1, col1_2, col1_3 = st.columns(3)
                    with col1_1:
                        st.metric("Nodes", G.number_of_nodes())
                    with col1_2:
                        st.metric("Edges", G.number_of_edges())
                    with col1_3:
                        density = G.number_of_edges() / (G.number_of_nodes() * (G.number_of_nodes() - 1) / 2)
                        st.metric("Density", f"{density:.4f}")
                    
                    # Top actors
                    st.subheader(f"Top {top_n} Actors (by Degree Centrality)")
                    top_actors = analyzers['network'].get_top_actors(G, metric='degree', n=top_n)
                    
                    actor_df = pd.DataFrame(top_actors, columns=['Actor', 'Centrality'])
                    fig = px.bar(
                        actor_df,
                        x='Centrality',
                        y='Actor',
                        orientation='h',
                        title="Actor Centrality"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Community detection
                    st.subheader("Community Detection")
                    communities = analyzers['network'].detect_communities(G)
                    num_communities = len(set(communities.values()))
                    st.metric("Communities Detected", num_communities)
                    
                    # Group by community
                    comm_groups = {}
                    for actor, comm_id in communities.items():
                        if comm_id not in comm_groups:
                            comm_groups[comm_id] = []
                        comm_groups[comm_id].append(actor)
                    
                    # Show top 5 communities
                    sorted_comms = sorted(comm_groups.items(), key=lambda x: len(x[1]), reverse=True)[:5]
                    for comm_id, actors in sorted_comms:
                        with st.expander(f"Community {comm_id} ({len(actors)} actors)"):
                            st.write(", ".join(actors[:20]))
            
            except Exception as e:
                st.error(f"Failed to build network: {e}")
                logger.error(f"Network tab error: {e}")


# TAB 3: Geospatial
with tab3:
    st.header("Geospatial Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("Clustering Settings")
        eps_km = st.slider("Cluster Radius (km)", min_value=10, max_value=200, value=50, step=10)
        min_samples = st.slider("Min Samples", min_value=5, max_value=50, value=10, step=5)
    
    with col1:
        with st.spinner("Analyzing geospatial patterns..."):
            try:
                df = analyzers['geo'].fetch_geo_events(
                    datetime.combine(start_date, datetime.min.time()),
                    datetime.combine(end_date, datetime.min.time()),
                    domain=domain_filter
                )
                
                if len(df) == 0:
                    st.warning("No geolocated events found.")
                else:
                    # Cluster events
                    df = analyzers['geo'].cluster_events(df, eps_km=eps_km, min_samples=min_samples)
                    
                    # Get hotspots
                    hotspots = analyzers['geo'].get_hotspots(df, top_n=10)
                    
                    # Hotspots table
                    st.subheader("Top 10 Event Hotspots")
                    st.dataframe(hotspots, use_container_width=True)
                    
                    # Create heatmap
                    st.subheader("Event Heatmap")
                    analyzers['geo'].create_heatmap(
                        df,
                        'temp_heatmap.html',
                        zoom=2
                    )
                    with open('temp_heatmap.html', 'r') as f:
                        html_content = f.read()
                    st.components.v1.html(html_content, height=500)
                    
                    # Country aggregation
                    st.subheader("Events by Country")
                    country_stats = analyzers['geo'].aggregate_by_country(df)
                    
                    fig = px.scatter_geo(
                        country_stats,
                        lat='center_lat',
                        lon='center_lon',
                        size='event_count',
                        hover_name='country',
                        hover_data=['event_count', 'avg_goldstein', 'avg_tone'],
                        title="Global Event Distribution"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            except Exception as e:
                st.error(f"Failed to analyze geospatial data: {e}")
                logger.error(f"Geospatial tab error: {e}")


# TAB 4: Trends
with tab4:
    st.header("Temporal Trends")
    
    with st.spinner("Computing trends..."):
        try:
            df = analyzers['geo'].fetch_geo_events(
                datetime.combine(start_date, datetime.min.time()),
                datetime.combine(end_date, datetime.min.time()),
                domain=domain_filter
            )
            
            if len(df) == 0:
                st.warning("No events found.")
            else:
                # Daily event counts
                daily_counts = df.groupby('event_date').size().reset_index(name='count')
                
                fig = px.line(
                    daily_counts,
                    x='event_date',
                    y='count',
                    title="Daily Event Counts",
                    labels={'event_date': 'Date', 'count': 'Events'}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Goldstein scale over time
                daily_goldstein = df.groupby('event_date')['goldstein_scale'].mean().reset_index()
                
                fig = px.line(
                    daily_goldstein,
                    x='event_date',
                    y='goldstein_scale',
                    title="Average Goldstein Scale Over Time",
                    labels={'event_date': 'Date', 'goldstein_scale': 'Avg Goldstein'}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Domain trends
                st.subheader("Domain Trends")
                domain_daily = df.groupby(['event_date', 'socioeconomic_domain']).size().reset_index(name='count')
                
                fig = px.line(
                    domain_daily,
                    x='event_date',
                    y='count',
                    color='socioeconomic_domain',
                    title="Event Trends by Domain",
                    labels={'event_date': 'Date', 'count': 'Events'}
                )
                st.plotly_chart(fig, use_container_width=True)
        
        except Exception as e:
            st.error(f"Failed to compute trends: {e}")
            logger.error(f"Trends tab error: {e}")


# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Event Database v0.1.0**")
st.sidebar.markdown("Built with Streamlit + GDELT")
