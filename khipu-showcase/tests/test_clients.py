"""
Unit tests for mock clients.
"""

import pytest
import pandas as pd
import numpy as np


class TestBLSMockClient:
    """Tests for BLS mock client."""
    
    @pytest.fixture
    def client(self):
        from khipu_demo.clients import BLSMockClient
        return BLSMockClient(seed=42)
    
    def test_unemployment_data(self, client):
        """Test unemployment data generation."""
        df = client.get_unemployment_data()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert 'state' in df.columns
        assert 'unemployment_rate' in df.columns
        
        # Rates should be reasonable (0-20%)
        assert df['unemployment_rate'].min() >= 0
        assert df['unemployment_rate'].max() <= 20
    
    def test_wages_by_metro(self, client):
        """Test metro wages generation."""
        df = client.get_wages_by_metro()
        
        assert isinstance(df, pd.DataFrame)
        assert 'metro' in df.columns
        assert 'median_wage' in df.columns
        
        # Wages should be positive
        assert df['median_wage'].min() > 0
    
    def test_reproducibility(self):
        """Test that same seed produces same data."""
        from khipu_demo.clients import BLSMockClient
        
        client1 = BLSMockClient(seed=42)
        client2 = BLSMockClient(seed=42)
        
        df1 = client1.get_unemployment_data()
        df2 = client2.get_unemployment_data()
        
        pd.testing.assert_frame_equal(df1, df2)


class TestBEAMockClient:
    """Tests for BEA mock client."""
    
    @pytest.fixture
    def client(self):
        from khipu_demo.clients import BEAMockClient
        return BEAMockClient(seed=42)
    
    def test_gdp_by_state(self, client):
        """Test state GDP generation."""
        df = client.get_gdp_by_state()
        
        assert isinstance(df, pd.DataFrame)
        assert 'state' in df.columns
        assert 'gdp' in df.columns
        
        # GDP should be positive
        assert df['gdp'].min() > 0
    
    def test_gdp_by_metro(self, client):
        """Test metro GDP generation."""
        df = client.get_gdp_by_metro()
        
        assert isinstance(df, pd.DataFrame)
        assert 'metro' in df.columns
        assert 'gdp' in df.columns


class TestCensusMockClient:
    """Tests for Census mock client."""
    
    @pytest.fixture
    def client(self):
        from khipu_demo.clients import CensusMockClient
        return CensusMockClient(seed=42)
    
    def test_population_data(self, client):
        """Test population data generation."""
        df = client.get_population_data()
        
        assert isinstance(df, pd.DataFrame)
        assert 'state' in df.columns
        assert 'population' in df.columns
        
        # Population should be positive
        assert df['population'].min() > 0


class TestEPAMockClient:
    """Tests for EPA mock client."""
    
    @pytest.fixture
    def client(self):
        from khipu_demo.clients import EPAMockClient
        return EPAMockClient(seed=42)
    
    def test_ej_indices(self, client):
        """Test EJ index generation."""
        df = client.get_ej_indices()
        
        assert isinstance(df, pd.DataFrame)
        assert 'tract_id' in df.columns
        
        # EJ indices should be in reasonable range
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        assert len(numeric_cols) > 0


class TestZillowMockClient:
    """Tests for Zillow mock client."""
    
    @pytest.fixture
    def client(self):
        from khipu_demo.clients import ZillowMockClient
        return ZillowMockClient(seed=42)
    
    def test_zhvi_by_metro(self, client):
        """Test ZHVI data generation."""
        df = client.get_zhvi_by_metro()
        
        assert isinstance(df, pd.DataFrame)
        assert 'metro' in df.columns
        assert 'zhvi' in df.columns
        
        # Home values should be positive
        assert df['zhvi'].min() > 0
    
    def test_housing_index(self, client):
        """Test housing index generation."""
        df = client.get_housing_index()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0


class TestGetDemoClients:
    """Tests for the demo clients factory."""
    
    def test_get_demo_clients(self):
        """Test that all demo clients are returned."""
        from khipu_demo.clients import get_demo_clients
        
        clients = get_demo_clients(seed=42)
        
        assert isinstance(clients, dict)
        assert 'labor' in clients
        assert 'economic' in clients
        assert 'census' in clients
        assert 'environmental' in clients
        assert 'health' in clients
        assert 'housing' in clients
