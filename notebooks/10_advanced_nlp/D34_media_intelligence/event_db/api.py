"""
FastAPI REST API for Event Database

Provides HTTP endpoints for:
- Event search and filtering
- Actor network queries
- Geospatial queries
- Aggregations and statistics

Author: KRL Team
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .actor_networks import ActorNetworkAnalyzer
from .cameo_mapping import CAMEOMapper
from .event_ingestion import GDELTEventIngestion
from .geo_analysis import GeoEventAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Event Database API",
    description="REST API for GDELT Event Database analytics",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzers
network_analyzer = ActorNetworkAnalyzer()
geo_analyzer = GeoEventAnalyzer()
cameo_mapper = CAMEOMapper()


# Pydantic models
class EventSearchParams(BaseModel):
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    domain: Optional[str] = Field(None, description="Socioeconomic domain")
    countries: Optional[List[str]] = Field(None, description="Country codes")
    min_goldstein: Optional[float] = Field(None, description="Minimum Goldstein scale")
    max_goldstein: Optional[float] = Field(None, description="Maximum Goldstein scale")
    limit: int = Field(100, description="Maximum results to return")


class NetworkParams(BaseModel):
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    domain: Optional[str] = Field(None, description="Socioeconomic domain")
    directed: bool = Field(True, description="Directed graph")
    top_n: int = Field(20, description="Number of top actors")


class GeoParams(BaseModel):
    start_date: str = Field(..., description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., description="End date (YYYY-MM-DD)")
    domain: Optional[str] = Field(None, description="Socioeconomic domain")
    countries: Optional[List[str]] = Field(None, description="Country codes")
    cluster_eps_km: float = Field(50, description="DBSCAN epsilon (km)")
    cluster_min_samples: int = Field(10, description="DBSCAN min samples")


# Root endpoint
@app.get("/")
def read_root():
    """API health check."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "endpoints": [
            "/events/search",
            "/events/domains",
            "/network/actors",
            "/network/communities",
            "/geo/hotspots",
            "/geo/country-stats"
        ]
    }


# Event endpoints
@app.get("/events/search")
def search_events(
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)"),
    domain: Optional[str] = Query(None, description="Socioeconomic domain"),
    limit: int = Query(100, description="Max results")
):
    """Search events with filters."""
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        df = geo_analyzer.fetch_geo_events(start, end, domain=domain)
        df = df.head(limit)
        
        return {
            "count": len(df),
            "events": df.to_dict(orient='records')
        }
    except Exception as e:
        logger.error(f"Event search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/events/domains")
def get_domains():
    """Get available socioeconomic domains."""
    return {
        "domains": [
            {
                "id": "labor_and_employment",
                "name": "Labor & Employment",
                "description": "Labor actions, strikes, union activity"
            },
            {
                "id": "health_and_social_policy",
                "name": "Health & Social Policy",
                "description": "Healthcare, welfare, humanitarian aid"
            },
            {
                "id": "inequality_and_poverty",
                "name": "Inequality & Poverty",
                "description": "Economic disparities, discrimination"
            },
            {
                "id": "education_and_youth",
                "name": "Education & Youth",
                "description": "Education policy, student protests"
            },
            {
                "id": "governance_and_corruption",
                "name": "Governance & Corruption",
                "description": "Government actions, corruption, legal"
            },
            {
                "id": "climate_and_environment",
                "name": "Climate & Environment",
                "description": "Environmental disasters, climate policy"
            }
        ]
    }


# Network endpoints
@app.post("/network/actors")
def get_top_actors(params: NetworkParams):
    """Get top actors by centrality."""
    try:
        start = datetime.strptime(params.start_date, "%Y-%m-%d")
        end = datetime.strptime(params.end_date, "%Y-%m-%d")
        
        # Fetch interactions
        interactions = network_analyzer.fetch_interactions(
            start, end, domain=params.domain
        )
        
        if len(interactions) == 0:
            return {"actors": [], "message": "No interactions found"}
        
        # Build graph
        G = network_analyzer.build_graph(interactions, directed=params.directed)
        
        # Get top actors
        top_actors = network_analyzer.get_top_actors(G, metric='degree', n=params.top_n)
        
        return {
            "actors": [
                {"actor": actor, "score": score}
                for actor, score in top_actors
            ],
            "graph_stats": {
                "nodes": G.number_of_nodes(),
                "edges": G.number_of_edges()
            }
        }
    except Exception as e:
        logger.error(f"Actor network failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/network/communities")
def detect_communities(params: NetworkParams):
    """Detect actor communities."""
    try:
        start = datetime.strptime(params.start_date, "%Y-%m-%d")
        end = datetime.strptime(params.end_date, "%Y-%m-%d")
        
        # Fetch interactions
        interactions = network_analyzer.fetch_interactions(
            start, end, domain=params.domain
        )
        
        if len(interactions) == 0:
            return {"communities": [], "message": "No interactions found"}
        
        # Build graph
        G = network_analyzer.build_graph(interactions, directed=False)
        
        # Detect communities
        communities = network_analyzer.detect_communities(G)
        
        # Group actors by community
        community_groups = {}
        for actor, comm_id in communities.items():
            if comm_id not in community_groups:
                community_groups[comm_id] = []
            community_groups[comm_id].append(actor)
        
        return {
            "num_communities": len(community_groups),
            "communities": [
                {
                    "id": comm_id,
                    "size": len(actors),
                    "actors": actors[:10]  # Top 10 per community
                }
                for comm_id, actors in sorted(community_groups.items(), 
                                              key=lambda x: len(x[1]), 
                                              reverse=True)
            ]
        }
    except Exception as e:
        logger.error(f"Community detection failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Geospatial endpoints
@app.post("/geo/hotspots")
def get_hotspots(params: GeoParams):
    """Get event hotspots (clustered locations)."""
    try:
        start = datetime.strptime(params.start_date, "%Y-%m-%d")
        end = datetime.strptime(params.end_date, "%Y-%m-%d")
        
        # Fetch geo events
        df = geo_analyzer.fetch_geo_events(
            start, end, 
            domain=params.domain, 
            countries=params.countries
        )
        
        if len(df) == 0:
            return {"hotspots": [], "message": "No geolocated events found"}
        
        # Cluster events
        df = geo_analyzer.cluster_events(
            df, 
            eps_km=params.cluster_eps_km,
            min_samples=params.cluster_min_samples
        )
        
        # Get hotspots
        hotspots = geo_analyzer.get_hotspots(df, top_n=10)
        
        return {
            "hotspots": hotspots.to_dict(orient='records'),
            "total_events": len(df)
        }
    except Exception as e:
        logger.error(f"Hotspot detection failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/geo/country-stats")
def get_country_stats(params: GeoParams):
    """Get aggregated statistics by country."""
    try:
        start = datetime.strptime(params.start_date, "%Y-%m-%d")
        end = datetime.strptime(params.end_date, "%Y-%m-%d")
        
        # Fetch geo events
        df = geo_analyzer.fetch_geo_events(
            start, end,
            domain=params.domain,
            countries=params.countries
        )
        
        if len(df) == 0:
            return {"countries": [], "message": "No geolocated events found"}
        
        # Aggregate by country
        country_stats = geo_analyzer.aggregate_by_country(df)
        
        return {
            "countries": country_stats.to_dict(orient='records'),
            "total_events": len(df)
        }
    except Exception as e:
        logger.error(f"Country stats failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Run with: uvicorn api:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
