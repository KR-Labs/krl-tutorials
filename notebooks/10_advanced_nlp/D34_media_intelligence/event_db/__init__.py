"""
GDELT Event Database Module

Production-grade event ingestion, actor network analysis, and geospatial clustering.
"""

__version__ = "0.1.0"
__author__ = "KR-Labs"

from .event_ingestion import GDELTEventIngestion
from .cameo_mapping import CAMEOMapper
from .actor_networks import ActorNetworkAnalyzer
from .geo_analysis import GeoEventAnalyzer

__all__ = [
    "GDELTEventIngestion",
    "CAMEOMapper",
    "ActorNetworkAnalyzer",
    "GeoEventAnalyzer",
]
