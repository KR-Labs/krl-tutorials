"""
Data loading and synthetic data generation utilities.

This module provides:
- Loaders for public datasets (Census, BLS, BEA, etc.)
- Synthetic data generators for demo purposes
- Data provenance tracking
"""

from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from dataclasses import dataclass, field
import hashlib
import json
import pandas as pd
import numpy as np
from pathlib import Path


@dataclass
class DataProvenance:
    """
    Track data provenance for reproducibility and auditing.
    
    Every dataset used in notebooks should have a provenance record.
    """
    source: str
    license: str
    ingestion_timestamp: datetime
    transformation_steps: List[str]
    dataset_hash: str
    version: str = "1.0.0"
    citation: str = ""
    url: str = ""
    notes: str = ""
    
    def to_markdown(self) -> str:
        """Generate markdown block for notebook display."""
        return f"""
### Data Provenance

| Field | Value |
|-------|-------|
| **Source** | {self.source} |
| **License** | {self.license} |
| **URL** | {self.url} |
| **Ingestion** | {self.ingestion_timestamp.isoformat()} |
| **Version** | {self.version} |
| **Hash** | `{self.dataset_hash[:16]}...` |

**Transformation Steps:**
{chr(10).join(f"- {step}" for step in self.transformation_steps)}

**Citation:** {self.citation}
"""

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "source": self.source,
            "license": self.license,
            "ingestion_timestamp": self.ingestion_timestamp.isoformat(),
            "transformation_steps": self.transformation_steps,
            "dataset_hash": self.dataset_hash,
            "version": self.version,
            "citation": self.citation,
            "url": self.url,
            "notes": self.notes,
        }


def compute_dataset_hash(df: pd.DataFrame) -> str:
    """
    Compute SHA-256 hash of a DataFrame for provenance tracking.
    
    Args:
        df: DataFrame to hash
        
    Returns:
        Hex string of SHA-256 hash
    """
    # Convert to bytes in a reproducible way
    data_bytes = df.to_csv(index=False).encode('utf-8')
    return hashlib.sha256(data_bytes).hexdigest()


def load_public_dataset(
    name: str,
    cache_dir: Optional[Path] = None
) -> tuple[pd.DataFrame, DataProvenance]:
    """
    Load a public dataset by name.
    
    Available datasets:
    - "metro_gdp": GDP by metropolitan area (BEA)
    - "metro_housing": Housing values by metro (synthetic based on Zillow patterns)
    - "metro_wages": Wages by metro (BLS patterns)
    - "metro_employment": Employment by metro (BLS patterns)
    - "ej_indices": Environmental Justice indices (EPA EJScreen patterns)
    
    Args:
        name: Dataset name
        cache_dir: Optional cache directory
        
    Returns:
        Tuple of (DataFrame, DataProvenance)
    """
    from khipu_demo.clients import get_demo_clients
    
    clients = get_demo_clients(seed=42)
    
    dataset_configs = {
        "metro_gdp": {
            "client": "economic",
            "method": "get_gdp_by_metro",
            "source": "Bureau of Economic Analysis (synthetic approximation)",
            "license": "Public Domain",
            "url": "https://www.bea.gov/data/gdp/gdp-metropolitan-area",
            "citation": "U.S. Bureau of Economic Analysis, GDP by Metropolitan Area",
        },
        "metro_housing": {
            "client": "housing",
            "method": "get_zhvi_by_metro",
            "source": "Zillow Research (synthetic approximation)",
            "license": "Zillow Group Terms of Use",
            "url": "https://www.zillow.com/research/data/",
            "citation": "Zillow, ZHVI All Homes Time Series",
        },
        "metro_wages": {
            "client": "labor",
            "method": "get_wages_by_metro",
            "source": "Bureau of Labor Statistics (synthetic approximation)",
            "license": "Public Domain",
            "url": "https://www.bls.gov/oes/",
            "citation": "U.S. Bureau of Labor Statistics, Occupational Employment and Wage Statistics",
        },
        "metro_employment": {
            "client": "labor",
            "method": "get_employment_by_metro",
            "source": "Bureau of Labor Statistics (synthetic approximation)",
            "license": "Public Domain",
            "url": "https://www.bls.gov/lau/",
            "citation": "U.S. Bureau of Labor Statistics, Local Area Unemployment Statistics",
        },
        "ej_indices": {
            "client": "environmental",
            "method": "get_ej_indices",
            "source": "EPA EJScreen (synthetic approximation)",
            "license": "Public Domain",
            "url": "https://www.epa.gov/ejscreen",
            "citation": "U.S. EPA, EJScreen Environmental Justice Mapping Tool",
        },
    }
    
    if name not in dataset_configs:
        available = ", ".join(dataset_configs.keys())
        raise ValueError(f"Unknown dataset: {name}. Available: {available}")
    
    config = dataset_configs[name]
    client = clients[config["client"]]
    method = getattr(client, config["method"])
    
    # Load data
    df = method()
    
    # Create provenance
    provenance = DataProvenance(
        source=config["source"],
        license=config["license"],
        ingestion_timestamp=datetime.now(),
        transformation_steps=[
            "Generated synthetic data matching production API schema",
            "Applied reproducible random seed (42)",
            "No PII or proprietary data included",
        ],
        dataset_hash=compute_dataset_hash(df),
        citation=config["citation"],
        url=config["url"],
        notes="This is synthetic data for demonstration purposes only.",
    )
    
    return df, provenance


class SyntheticDataGenerator:
    """
    Generator for synthetic demo datasets with realistic patterns.
    
    All generated data is reproducible via seed and contains
    no real PII or proprietary information.
    """
    
    def __init__(self, seed: int = 42):
        """
        Initialize generator with reproducible seed.
        
        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        
    def generate_housing_wage_panel(
        self,
        n_metros: int = 20,
        start_year: int = 2015,
        end_year: int = 2024,
        frequency: str = "annual"
    ) -> tuple[pd.DataFrame, DataProvenance]:
        """
        Generate panel dataset of housing values and wages by metro.
        
        This creates a realistic divergence pattern where housing
        outpaces wages in some metros but not others.
        
        Args:
            n_metros: Number of metro areas
            start_year: Start year
            end_year: End year
            frequency: "annual" or "monthly"
            
        Returns:
            Tuple of (DataFrame, DataProvenance)
        """
        from khipu_demo.clients import MockEconomicClient
        
        metros = MockEconomicClient.METROS[:n_metros]
        
        if frequency == "annual":
            periods = list(range(start_year, end_year + 1))
            n_periods = len(periods)
        else:
            periods = pd.date_range(
                f"{start_year}-01-01", 
                f"{end_year}-12-31", 
                freq="MS"
            )
            n_periods = len(periods)
        
        # Define metro characteristics
        # High divergence metros: housing >> wages
        high_divergence = [
            "San Francisco-Oakland-Berkeley, CA",
            "Los Angeles-Long Beach-Anaheim, CA",
            "Seattle-Tacoma-Bellevue, WA",
            "Denver-Aurora-Lakewood, CO",
            "Miami-Fort Lauderdale-Pompano Beach, FL",
            "Austin-Round Rock-Georgetown, TX",
        ]
        
        # Low divergence: housing ≈ wages
        low_divergence = [
            "Detroit-Warren-Dearborn, MI",
            "Minneapolis-St. Paul-Bloomington, MN-WI",
            "Philadelphia-Camden-Wilmington, PA-NJ-DE-MD",
        ]
        
        records = []
        for metro in metros:
            # Base values
            base_housing = self.rng.uniform(250000, 700000)
            base_wage = self.rng.uniform(50000, 85000)
            
            # Growth rates based on divergence category
            if metro in high_divergence:
                housing_growth = self.rng.uniform(0.06, 0.10)  # 6-10% annual
                wage_growth = self.rng.uniform(0.02, 0.035)    # 2-3.5% annual
            elif metro in low_divergence:
                housing_growth = self.rng.uniform(0.02, 0.04)  # 2-4% annual
                wage_growth = self.rng.uniform(0.025, 0.04)    # 2.5-4% annual
            else:
                housing_growth = self.rng.uniform(0.04, 0.07)  # 4-7% annual
                wage_growth = self.rng.uniform(0.02, 0.035)    # 2-3.5% annual
            
            # Generate time series
            housing_values = [base_housing]
            wage_values = [base_wage]
            
            for i in range(1, n_periods):
                if frequency == "annual":
                    h_growth = housing_growth + self.rng.normal(0, 0.02)
                    w_growth = wage_growth + self.rng.normal(0, 0.01)
                else:
                    h_growth = (housing_growth / 12) + self.rng.normal(0, 0.005)
                    w_growth = (wage_growth / 12) + self.rng.normal(0, 0.002)
                
                housing_values.append(housing_values[-1] * (1 + h_growth))
                wage_values.append(wage_values[-1] * (1 + w_growth))
            
            for i, period in enumerate(periods):
                housing = housing_values[i]
                wage = wage_values[i]
                
                # Calculate metrics
                affordability_ratio = housing / wage
                
                # Cumulative growth from base
                housing_cumul_growth = (housing / base_housing - 1) * 100
                wage_cumul_growth = (wage / base_wage - 1) * 100
                divergence = housing_cumul_growth - wage_cumul_growth
                
                records.append({
                    "metro": metro,
                    "period": period,
                    "median_home_value": housing,
                    "median_wage": wage,
                    "affordability_ratio": affordability_ratio,
                    "housing_cumul_growth_pct": housing_cumul_growth,
                    "wage_cumul_growth_pct": wage_cumul_growth,
                    "divergence_pct": divergence,
                })
        
        df = pd.DataFrame(records)
        
        provenance = DataProvenance(
            source="Synthetic Data Generator (khipu_demo)",
            license="Apache 2.0",
            ingestion_timestamp=datetime.now(),
            transformation_steps=[
                f"Generated {n_metros} metros with {n_periods} periods",
                f"Applied seed={self.seed} for reproducibility",
                "Created realistic housing-wage divergence patterns",
                "No real data or PII included",
            ],
            dataset_hash=compute_dataset_hash(df),
            citation="KR-Labs, Khipu Demo Synthetic Data Generator, 2025",
            url="https://github.com/KR-Labs/khipu-showcase",
            notes="Synthetic data for demonstration only. Patterns approximate real trends.",
        )
        
        return df, provenance
    
    def generate_gentrification_signals(
        self,
        n_tracts: int = 100,
        n_periods: int = 24
    ) -> tuple[pd.DataFrame, DataProvenance]:
        """
        Generate tract-level gentrification indicator panel.
        
        Args:
            n_tracts: Number of census tracts
            n_periods: Number of monthly periods
            
        Returns:
            Tuple of (DataFrame, DataProvenance)
        """
        periods = pd.date_range("2022-01-01", periods=n_periods, freq="MS")
        
        # Create tracts with different gentrification stages
        records = []
        for tract_id in range(n_tracts):
            # Assign gentrification stage
            stage = self.rng.choice(
                ["none", "early", "active", "late"],
                p=[0.4, 0.25, 0.25, 0.1]
            )
            
            base_rent = self.rng.uniform(800, 2000)
            base_permits = self.rng.integers(0, 20)
            
            for i, period in enumerate(periods):
                if stage == "early":
                    rent_growth = 0.008 + self.rng.normal(0, 0.003)
                    permit_mult = 1.5
                    business_churn = 0.15
                elif stage == "active":
                    rent_growth = 0.015 + self.rng.normal(0, 0.005)
                    permit_mult = 2.5
                    business_churn = 0.25
                elif stage == "late":
                    rent_growth = 0.005 + self.rng.normal(0, 0.002)
                    permit_mult = 1.2
                    business_churn = 0.08
                else:
                    rent_growth = 0.002 + self.rng.normal(0, 0.002)
                    permit_mult = 1.0
                    business_churn = 0.05
                
                rent = base_rent * (1 + rent_growth) ** i
                permits = int(base_permits * permit_mult * (1 + self.rng.normal(0, 0.3)))
                permits = max(0, permits)
                
                records.append({
                    "tract_id": f"06037{tract_id:05d}",
                    "period": period,
                    "median_rent": rent,
                    "building_permits": permits,
                    "business_churn_rate": business_churn + self.rng.normal(0, 0.03),
                    "new_restaurants": int(self.rng.poisson(3 if stage in ["early", "active"] else 1)),
                    "gentrification_stage": stage,
                    "gentrification_score": {"none": 0, "early": 30, "active": 65, "late": 85}[stage] + self.rng.normal(0, 10),
                })
        
        df = pd.DataFrame(records)
        
        provenance = DataProvenance(
            source="Synthetic Data Generator (khipu_demo)",
            license="Apache 2.0",
            ingestion_timestamp=datetime.now(),
            transformation_steps=[
                f"Generated {n_tracts} tracts with {n_periods} monthly periods",
                "Created gentrification stage classifications",
                "Applied realistic indicator correlations",
            ],
            dataset_hash=compute_dataset_hash(df),
            citation="KR-Labs, Khipu Demo Synthetic Data Generator, 2025",
        )
        
        return df, provenance


def generate_synthetic_data(
    dataset_type: str,
    seed: int = 42,
    **kwargs
) -> tuple[pd.DataFrame, DataProvenance]:
    """
    Convenience function to generate synthetic datasets.
    
    Args:
        dataset_type: Type of dataset ("housing_wage", "gentrification")
        seed: Random seed
        **kwargs: Additional arguments for generator
        
    Returns:
        Tuple of (DataFrame, DataProvenance)
    """
    generator = SyntheticDataGenerator(seed=seed)
    
    if dataset_type == "housing_wage":
        return generator.generate_housing_wage_panel(**kwargs)
    elif dataset_type == "gentrification":
        return generator.generate_gentrification_signals(**kwargs)
    else:
        raise ValueError(f"Unknown dataset type: {dataset_type}")
