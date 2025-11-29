"""
Mock API Clients for Khipu Demo

These clients provide canned responses that match production API schemas
without requiring any real credentials or network access.

SECURITY: No real API keys or credentials are used or stored.
All responses are pre-generated synthetic data.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from dataclasses import dataclass


@dataclass
class APIResponse:
    """Standard response wrapper for mock API calls."""
    data: Any
    metadata: Dict[str, Any]
    timestamp: datetime
    source: str
    is_mock: bool = True


class BaseMockClient:
    """Base class for all mock API clients."""
    
    def __init__(self, seed: int = 42):
        """
        Initialize mock client with reproducible random seed.
        
        Args:
            seed: Random seed for reproducible synthetic data
        """
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self._call_count = 0
        
    def _log_call(self, method: str, params: Dict) -> None:
        """Log API call for debugging (no sensitive data)."""
        self._call_count += 1
        
    def _create_response(self, data: Any, source: str) -> APIResponse:
        """Create standardized API response."""
        return APIResponse(
            data=data,
            metadata={
                "call_count": self._call_count,
                "seed": self.seed,
                "demo_mode": True
            },
            timestamp=datetime.now(),
            source=source,
            is_mock=True
        )


class MockEconomicClient(BaseMockClient):
    """
    Mock client for economic data APIs (FRED, BEA, etc.).
    
    Returns synthetic data matching production API schemas.
    """
    
    # Major metro areas for demo
    METROS = [
        "New York-Newark-Jersey City, NY-NJ-PA",
        "Los Angeles-Long Beach-Anaheim, CA",
        "Chicago-Naperville-Elgin, IL-IN-WI",
        "Dallas-Fort Worth-Arlington, TX",
        "Houston-The Woodlands-Sugar Land, TX",
        "Washington-Arlington-Alexandria, DC-VA-MD-WV",
        "Miami-Fort Lauderdale-Pompano Beach, FL",
        "Philadelphia-Camden-Wilmington, PA-NJ-DE-MD",
        "Atlanta-Sandy Springs-Alpharetta, GA",
        "Boston-Cambridge-Newton, MA-NH",
        "Phoenix-Mesa-Chandler, AZ",
        "San Francisco-Oakland-Berkeley, CA",
        "Seattle-Tacoma-Bellevue, WA",
        "Minneapolis-St. Paul-Bloomington, MN-WI",
        "Denver-Aurora-Lakewood, CO",
        "San Diego-Chula Vista-Carlsbad, CA",
        "Tampa-St. Petersburg-Clearwater, FL",
        "Austin-Round Rock-Georgetown, TX",
        "Detroit-Warren-Dearborn, MI",
        "Portland-Vancouver-Hillsboro, OR-WA",
    ]
    
    def get_gdp_by_metro(
        self,
        start_year: int = 2015,
        end_year: int = 2024,
        metros: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Get GDP by metropolitan area.
        
        Args:
            start_year: Start year for data
            end_year: End year for data
            metros: List of metro areas (default: top 20)
            
        Returns:
            DataFrame with columns: metro, year, gdp, gdp_growth
        """
        self._log_call("get_gdp_by_metro", {"start_year": start_year, "end_year": end_year})
        
        metros = metros or self.METROS
        years = list(range(start_year, end_year + 1))
        
        records = []
        for metro in metros:
            base_gdp = self.rng.uniform(50, 500) * 1e9  # $50B to $500B
            for i, year in enumerate(years):
                # Add realistic growth with some variation
                growth_rate = self.rng.normal(0.025, 0.015)  # ~2.5% avg growth
                if i > 0:
                    gdp = records[-1]["gdp"] * (1 + growth_rate)
                else:
                    gdp = base_gdp
                    
                records.append({
                    "metro": metro,
                    "year": year,
                    "gdp": gdp,
                    "gdp_growth": growth_rate if i > 0 else np.nan
                })
                
        return pd.DataFrame(records)
    
    def get_cpi_series(
        self,
        start_date: str = "2015-01-01",
        end_date: str = "2024-12-31",
        frequency: str = "monthly"
    ) -> pd.DataFrame:
        """
        Get Consumer Price Index time series.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            frequency: Data frequency (monthly, quarterly, annual)
            
        Returns:
            DataFrame with columns: date, cpi, cpi_yoy_change
        """
        self._log_call("get_cpi_series", {"start_date": start_date, "end_date": end_date})
        
        dates = pd.date_range(start_date, end_date, freq="MS" if frequency == "monthly" else "QS")
        base_cpi = 237.0  # Approximate 2015 CPI
        
        cpi_values = [base_cpi]
        for i in range(1, len(dates)):
            # Monthly inflation with some variation
            monthly_inflation = self.rng.normal(0.002, 0.003)  # ~2.4% annual
            cpi_values.append(cpi_values[-1] * (1 + monthly_inflation))
            
        df = pd.DataFrame({
            "date": dates,
            "cpi": cpi_values
        })
        
        # Calculate year-over-year change
        df["cpi_yoy_change"] = df["cpi"].pct_change(12) * 100
        
        return df


class MockHousingClient(BaseMockClient):
    """
    Mock client for housing data APIs (Zillow, HUD, etc.).
    
    Returns synthetic housing market data.
    """
    
    def get_zhvi_by_metro(
        self,
        start_date: str = "2015-01-01",
        end_date: str = "2024-12-31",
        metros: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Get Zillow Home Value Index by metro.
        
        Args:
            start_date: Start date
            end_date: End date
            metros: List of metros (default: top 20)
            
        Returns:
            DataFrame with: metro, date, zhvi, zhvi_yoy_change
        """
        self._log_call("get_zhvi_by_metro", {"start_date": start_date, "end_date": end_date})
        
        metros = metros or MockEconomicClient.METROS
        dates = pd.date_range(start_date, end_date, freq="MS")
        
        # Base home values by metro (vary significantly)
        base_values = {
            metro: self.rng.uniform(200000, 800000) 
            for metro in metros
        }
        
        # Higher growth metros (coastal, tech hubs)
        high_growth_metros = [
            "San Francisco-Oakland-Berkeley, CA",
            "Seattle-Tacoma-Bellevue, WA",
            "Austin-Round Rock-Georgetown, TX",
            "Denver-Aurora-Lakewood, CO",
            "Miami-Fort Lauderdale-Pompano Beach, FL"
        ]
        
        records = []
        for metro in metros:
            base = base_values[metro]
            is_high_growth = metro in high_growth_metros
            
            values = [base]
            for i in range(1, len(dates)):
                # Monthly appreciation with variation
                if is_high_growth:
                    monthly_growth = self.rng.normal(0.006, 0.008)  # ~7% annual
                else:
                    monthly_growth = self.rng.normal(0.003, 0.005)  # ~3.6% annual
                    
                # Add COVID-era surge (2020-2022)
                date = dates[i]
                if pd.Timestamp("2020-06-01") <= date <= pd.Timestamp("2022-06-01"):
                    monthly_growth += 0.005
                    
                values.append(values[-1] * (1 + monthly_growth))
            
            for date, zhvi in zip(dates, values):
                records.append({
                    "metro": metro,
                    "date": date,
                    "zhvi": zhvi
                })
                
        df = pd.DataFrame(records)
        
        # Calculate YoY change per metro
        df = df.sort_values(["metro", "date"])
        df["zhvi_yoy_change"] = df.groupby("metro")["zhvi"].pct_change(12) * 100
        
        return df
    
    def get_rent_index(
        self,
        start_date: str = "2015-01-01",
        end_date: str = "2024-12-31",
        metros: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Get rental price index by metro.
        
        Args:
            start_date: Start date
            end_date: End date
            metros: List of metros
            
        Returns:
            DataFrame with: metro, date, rent_index, rent_yoy_change
        """
        self._log_call("get_rent_index", {"start_date": start_date, "end_date": end_date})
        
        metros = metros or MockEconomicClient.METROS
        dates = pd.date_range(start_date, end_date, freq="MS")
        
        records = []
        for metro in metros:
            base_rent = self.rng.uniform(1200, 3500)
            
            rents = [base_rent]
            for i in range(1, len(dates)):
                monthly_growth = self.rng.normal(0.003, 0.004)
                rents.append(rents[-1] * (1 + monthly_growth))
            
            for date, rent in zip(dates, rents):
                records.append({
                    "metro": metro,
                    "date": date,
                    "rent_index": rent
                })
                
        df = pd.DataFrame(records)
        df = df.sort_values(["metro", "date"])
        df["rent_yoy_change"] = df.groupby("metro")["rent_index"].pct_change(12) * 100
        
        return df


class MockLaborClient(BaseMockClient):
    """
    Mock client for labor market data APIs (BLS, etc.).
    
    Returns synthetic employment and wage data.
    """
    
    def get_wages_by_metro(
        self,
        start_year: int = 2015,
        end_year: int = 2024,
        metros: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Get median wages by metropolitan area.
        
        Args:
            start_year: Start year
            end_year: End year
            metros: List of metros
            
        Returns:
            DataFrame with: metro, year, median_wage, wage_growth
        """
        self._log_call("get_wages_by_metro", {"start_year": start_year, "end_year": end_year})
        
        metros = metros or MockEconomicClient.METROS
        years = list(range(start_year, end_year + 1))
        
        # Base wages vary by metro
        high_wage_metros = [
            "San Francisco-Oakland-Berkeley, CA",
            "Seattle-Tacoma-Bellevue, WA", 
            "Washington-Arlington-Alexandria, DC-VA-MD-WV",
            "Boston-Cambridge-Newton, MA-NH",
            "New York-Newark-Jersey City, NY-NJ-PA"
        ]
        
        records = []
        for metro in metros:
            is_high_wage = metro in high_wage_metros
            base_wage = self.rng.uniform(65000, 95000) if is_high_wage else self.rng.uniform(45000, 65000)
            
            wages = [base_wage]
            for i in range(1, len(years)):
                # Real wage growth ~1-2% annually
                growth = self.rng.normal(0.025, 0.01)
                wages.append(wages[-1] * (1 + growth))
                
            for i, year in enumerate(years):
                records.append({
                    "metro": metro,
                    "year": year,
                    "median_wage": wages[i],
                    "wage_growth": (wages[i] / wages[i-1] - 1) * 100 if i > 0 else np.nan
                })
                
        return pd.DataFrame(records)
    
    def get_employment_by_metro(
        self,
        start_date: str = "2015-01-01",
        end_date: str = "2024-12-31",
        metros: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Get employment levels by metro.
        
        Args:
            start_date: Start date
            end_date: End date
            metros: List of metros
            
        Returns:
            DataFrame with: metro, date, employment, unemployment_rate
        """
        self._log_call("get_employment_by_metro", {"start_date": start_date, "end_date": end_date})
        
        metros = metros or MockEconomicClient.METROS
        dates = pd.date_range(start_date, end_date, freq="MS")
        
        records = []
        for metro in metros:
            base_employment = self.rng.uniform(500000, 5000000)
            base_unemployment = self.rng.uniform(3.5, 5.5)
            
            employment = base_employment
            unemployment = base_unemployment
            
            for date in dates:
                # COVID shock
                if pd.Timestamp("2020-03-01") <= date <= pd.Timestamp("2020-06-01"):
                    employment *= 0.95
                    unemployment += 5
                elif pd.Timestamp("2020-06-01") < date <= pd.Timestamp("2022-01-01"):
                    employment *= 1.01  # Recovery
                    unemployment = max(3.0, unemployment - 0.3)
                else:
                    employment *= (1 + self.rng.normal(0.001, 0.003))
                    unemployment += self.rng.normal(0, 0.1)
                    unemployment = max(2.5, min(10, unemployment))
                    
                records.append({
                    "metro": metro,
                    "date": date,
                    "employment": employment,
                    "unemployment_rate": unemployment
                })
                
        return pd.DataFrame(records)


class MockDemographicsClient(BaseMockClient):
    """
    Mock client for Census and demographic data.
    """
    
    def get_metro_demographics(
        self,
        year: int = 2022,
        metros: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Get demographic data by metro.
        
        Args:
            year: Census year
            metros: List of metros
            
        Returns:
            DataFrame with demographic indicators
        """
        self._log_call("get_metro_demographics", {"year": year})
        
        metros = metros or MockEconomicClient.METROS
        
        records = []
        for metro in metros:
            records.append({
                "metro": metro,
                "year": year,
                "population": int(self.rng.uniform(1e6, 10e6)),
                "median_age": self.rng.uniform(34, 42),
                "pct_college_educated": self.rng.uniform(25, 50),
                "pct_homeowner": self.rng.uniform(45, 70),
                "median_household_income": self.rng.uniform(55000, 120000),
            })
            
        return pd.DataFrame(records)


class MockEnvironmentalClient(BaseMockClient):
    """
    Mock client for EPA and environmental data.
    """
    
    def get_ej_indices(
        self,
        state: str = "CA",
        geography: str = "tract"
    ) -> pd.DataFrame:
        """
        Get Environmental Justice indices.
        
        Args:
            state: State abbreviation
            geography: Geographic level (tract, county)
            
        Returns:
            DataFrame with EJ indicators
        """
        self._log_call("get_ej_indices", {"state": state, "geography": geography})
        
        n_tracts = 500 if geography == "tract" else 50
        
        records = []
        for i in range(n_tracts):
            records.append({
                "tract_id": f"{state}{i:05d}",
                "state": state,
                "pm25_index": self.rng.uniform(0, 100),
                "ozone_index": self.rng.uniform(0, 100),
                "traffic_proximity": self.rng.uniform(0, 100),
                "superfund_proximity": self.rng.uniform(0, 100),
                "minority_pct": self.rng.uniform(5, 95),
                "low_income_pct": self.rng.uniform(5, 60),
                "ej_composite_index": self.rng.uniform(0, 100),
            })
            
        return pd.DataFrame(records)


# Alias classes for backward compatibility with tests
BLSMockClient = MockLaborClient
BEAMockClient = MockEconomicClient
CensusMockClient = MockDemographicsClient
EPAMockClient = MockEnvironmentalClient
ZillowMockClient = MockHousingClient


class CDCMockClient(BaseMockClient):
    """
    Mock client for CDC health data.
    """
    
    def get_health_outcomes(
        self,
        geography: str = "county"
    ) -> pd.DataFrame:
        """
        Get health outcomes by geography.
        
        Args:
            geography: Geographic level
            
        Returns:
            DataFrame with health indicators
        """
        self._log_call("get_health_outcomes", {"geography": geography})
        
        n_counties = 100
        
        records = []
        for i in range(n_counties):
            records.append({
                "county": f"County_{i:03d}",
                "asthma_rate": self.rng.uniform(5, 15),
                "diabetes_rate": self.rng.uniform(8, 18),
                "obesity_rate": self.rng.uniform(20, 45),
                "life_expectancy": self.rng.uniform(72, 82),
            })
            
        return pd.DataFrame(records)


# Add missing methods to clients for test compatibility
def _add_unemployment_data(self) -> pd.DataFrame:
    """Get unemployment data by state."""
    states = [
        "CA", "TX", "FL", "NY", "PA", "IL", "OH", "GA", "NC", "MI",
        "NJ", "VA", "WA", "AZ", "MA", "TN", "IN", "MO", "MD", "WI"
    ]
    
    records = []
    for state in states:
        unemployment_rate = self.rng.uniform(3, 8)
        labor_force = int(self.rng.uniform(1e6, 15e6))
        unemployed = int(labor_force * unemployment_rate / 100)
        employed = labor_force - unemployed
        
        records.append({
            "state": state,
            "unemployment_rate": unemployment_rate,
            "labor_force": labor_force,
            "employed": employed,
            "unemployed": unemployed,
        })
    
    return pd.DataFrame(records)


def _add_gdp_by_state(self) -> pd.DataFrame:
    """Get GDP by state."""
    states = [
        "CA", "TX", "FL", "NY", "PA", "IL", "OH", "GA", "NC", "MI",
        "NJ", "VA", "WA", "AZ", "MA", "TN", "IN", "MO", "MD", "WI"
    ]
    
    records = []
    for state in states:
        gdp = self.rng.uniform(100, 3000) * 1e9
        population = int(self.rng.uniform(2e6, 40e6))
        gdp_per_capita = gdp / population
        
        records.append({
            "state": state,
            "gdp": gdp,
            "population": population,
            "gdp_per_capita": gdp_per_capita,
        })
    
    return pd.DataFrame(records)


def _add_population_data(self) -> pd.DataFrame:
    """Get population by state."""
    states = [
        "CA", "TX", "FL", "NY", "PA", "IL", "OH", "GA", "NC", "MI",
        "NJ", "VA", "WA", "AZ", "MA", "TN", "IN", "MO", "MD", "WI"
    ]
    
    records = []
    for state in states:
        population = int(self.rng.uniform(2e6, 40e6))
        pop_density = self.rng.uniform(50, 500)
        median_age = self.rng.uniform(35, 42)
        
        records.append({
            "state": state,
            "population": population,
            "pop_density": pop_density,
            "median_age": median_age,
        })
    
    return pd.DataFrame(records)


def _add_housing_index(self) -> pd.DataFrame:
    """Get housing market index."""
    metros = MockEconomicClient.METROS[:10]
    
    records = []
    for metro in metros:
        records.append({
            "metro": metro,
            "housing_index": self.rng.uniform(100, 300),
            "inventory": int(self.rng.uniform(1000, 50000)),
            "days_on_market": int(self.rng.uniform(15, 60)),
        })
    
    return pd.DataFrame(records)


# Monkey-patch methods onto classes
MockLaborClient.get_unemployment_data = _add_unemployment_data
MockEconomicClient.get_gdp_by_state = _add_gdp_by_state
MockDemographicsClient.get_population_data = _add_population_data
MockHousingClient.get_housing_index = _add_housing_index


# Convenience function to get all clients
def get_demo_clients(seed: int = 42) -> Dict[str, BaseMockClient]:
    """
    Get all mock clients with consistent seed.
    
    Args:
        seed: Random seed for reproducibility
        
    Returns:
        Dictionary of initialized mock clients
    """
    return {
        "economic": MockEconomicClient(seed),
        "housing": MockHousingClient(seed),
        "labor": MockLaborClient(seed),
        "demographics": MockDemographicsClient(seed),
        "environmental": MockEnvironmentalClient(seed),
        "census": MockDemographicsClient(seed),
        "health": CDCMockClient(seed),
    }
