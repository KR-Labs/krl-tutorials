# Khipu Demo Package
# Lightweight package for public notebook demonstrations

"""
khipu_demo - Public demonstration utilities for Khipu Socioeconomic Analysis Suite.

This package provides:
- Mock API clients that return canned responses (no real credentials needed)
- Synthetic data generators for reproducible demos
- Visualization utilities with accessibility features
- Data loading helpers for public datasets

SECURITY NOTE: This package is designed for public consumption.
No secrets, proprietary algorithms, or private data are included.
"""

__version__ = "0.1.0"
__author__ = "KR-Labs"
__license__ = "Apache-2.0"

import os
from typing import Optional

# Demo mode detection
DEMO_MODE = os.environ.get("DEMO_MODE", "true").lower() == "true"

if not DEMO_MODE:
    import warnings
    warnings.warn(
        "DEMO_MODE is not set to 'true'. Some features may not work correctly. "
        "Set DEMO_MODE=true for public demonstrations.",
        UserWarning
    )

# Package-level imports
from khipu_demo.clients import (
    MockEconomicClient,
    MockHousingClient,
    MockLaborClient,
    MockDemographicsClient,
    MockEnvironmentalClient,
)

from khipu_demo.data import (
    load_public_dataset,
    generate_synthetic_data,
    SyntheticDataGenerator,
    DataProvenance,
)

from khipu_demo.viz import (
    create_choropleth,
    create_time_series,
    create_heatmap,
    create_divergence_map,
    ThemeManager,
    AccessibilityChecker,
)

from khipu_demo.utils import (
    validate_notebook_structure,
    generate_executive_summary,
    format_provenance_block,
    check_no_secrets,
)

__all__ = [
    # Version info
    "__version__",
    "DEMO_MODE",
    
    # Clients
    "MockEconomicClient",
    "MockHousingClient", 
    "MockLaborClient",
    "MockDemographicsClient",
    "MockEnvironmentalClient",
    
    # Data
    "load_public_dataset",
    "generate_synthetic_data",
    "SyntheticDataGenerator",
    "DataProvenance",
    
    # Visualization
    "create_choropleth",
    "create_time_series",
    "create_heatmap",
    "create_divergence_map",
    "ThemeManager",
    "AccessibilityChecker",
    
    # Utilities
    "validate_notebook_structure",
    "generate_executive_summary",
    "format_provenance_block",
    "check_no_secrets",
]
