"""
Unit tests for data utilities.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime


class TestDataProvenance:
    """Tests for DataProvenance class."""
    
    def test_create_provenance(self):
        """Test creating a provenance record."""
        from khipu_demo.data import DataProvenance
        
        provenance = DataProvenance(
            source="Test Source",
            license="MIT",
            ingestion_timestamp=datetime.now(),
            transformation_steps=["Step 1", "Step 2"],
            dataset_hash="abc123",
        )
        
        assert provenance.source == "Test Source"
        assert provenance.license == "MIT"
        assert len(provenance.transformation_steps) == 2
    
    def test_to_markdown(self):
        """Test markdown generation."""
        from khipu_demo.data import DataProvenance
        
        provenance = DataProvenance(
            source="Test Source",
            license="MIT",
            ingestion_timestamp=datetime.now(),
            transformation_steps=["Step 1"],
            dataset_hash="abc123",
            url="https://example.com",
        )
        
        md = provenance.to_markdown()
        
        assert "Test Source" in md
        assert "MIT" in md
        assert "https://example.com" in md
    
    def test_to_dict(self):
        """Test dictionary conversion."""
        from khipu_demo.data import DataProvenance
        
        provenance = DataProvenance(
            source="Test Source",
            license="MIT",
            ingestion_timestamp=datetime.now(),
            transformation_steps=["Step 1"],
            dataset_hash="abc123",
        )
        
        d = provenance.to_dict()
        
        assert isinstance(d, dict)
        assert d["source"] == "Test Source"
        assert d["license"] == "MIT"


class TestComputeDatasetHash:
    """Tests for dataset hashing."""
    
    def test_hash_dataframe(self):
        """Test hashing a DataFrame."""
        from khipu_demo.data import compute_dataset_hash
        
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        hash_val = compute_dataset_hash(df)
        
        assert isinstance(hash_val, str)
        assert len(hash_val) == 64  # SHA-256 hex length
    
    def test_hash_reproducibility(self):
        """Test that same data produces same hash."""
        from khipu_demo.data import compute_dataset_hash
        
        df1 = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        df2 = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        
        assert compute_dataset_hash(df1) == compute_dataset_hash(df2)
    
    def test_hash_different_data(self):
        """Test that different data produces different hash."""
        from khipu_demo.data import compute_dataset_hash
        
        df1 = pd.DataFrame({"a": [1, 2, 3]})
        df2 = pd.DataFrame({"a": [1, 2, 4]})
        
        assert compute_dataset_hash(df1) != compute_dataset_hash(df2)


class TestSyntheticDataGenerator:
    """Tests for SyntheticDataGenerator."""
    
    @pytest.fixture
    def generator(self):
        from khipu_demo.data import SyntheticDataGenerator
        return SyntheticDataGenerator(seed=42)
    
    def test_housing_wage_panel(self, generator):
        """Test housing-wage panel generation."""
        df, provenance = generator.generate_housing_wage_panel(
            n_metros=5,
            start_year=2020,
            end_year=2023,
        )
        
        assert isinstance(df, pd.DataFrame)
        assert df['metro'].nunique() == 5
        assert 'median_home_value' in df.columns
        assert 'median_wage' in df.columns
        assert 'divergence_pct' in df.columns
        
        # Check provenance
        assert provenance.source is not None
        assert provenance.dataset_hash is not None
    
    def test_housing_wage_monthly(self, generator):
        """Test monthly frequency generation."""
        df, _ = generator.generate_housing_wage_panel(
            n_metros=2,
            start_year=2023,
            end_year=2023,
            frequency="monthly",
        )
        
        # Should have 12 months * 2 metros = 24 rows
        assert len(df) == 24
    
    def test_gentrification_signals(self, generator):
        """Test gentrification signals generation."""
        df, provenance = generator.generate_gentrification_signals(
            n_tracts=10,
            n_periods=6,
        )
        
        assert isinstance(df, pd.DataFrame)
        assert df['tract_id'].nunique() == 10
        assert 'median_rent' in df.columns
        assert 'gentrification_stage' in df.columns
        
        # Check stages are valid
        valid_stages = {'none', 'early', 'active', 'late'}
        assert set(df['gentrification_stage'].unique()).issubset(valid_stages)
    
    def test_reproducibility(self):
        """Test that same seed produces same data."""
        from khipu_demo.data import SyntheticDataGenerator
        
        gen1 = SyntheticDataGenerator(seed=42)
        gen2 = SyntheticDataGenerator(seed=42)
        
        df1, _ = gen1.generate_housing_wage_panel(n_metros=5)
        df2, _ = gen2.generate_housing_wage_panel(n_metros=5)
        
        pd.testing.assert_frame_equal(df1, df2)


class TestGenerateSyntheticData:
    """Tests for the convenience function."""
    
    def test_housing_wage(self):
        """Test housing_wage dataset type."""
        from khipu_demo.data import generate_synthetic_data
        
        df, provenance = generate_synthetic_data("housing_wage", n_metros=3)
        
        assert isinstance(df, pd.DataFrame)
        assert 'median_home_value' in df.columns
    
    def test_gentrification(self):
        """Test gentrification dataset type."""
        from khipu_demo.data import generate_synthetic_data
        
        df, provenance = generate_synthetic_data("gentrification", n_tracts=5)
        
        assert isinstance(df, pd.DataFrame)
        assert 'gentrification_stage' in df.columns
    
    def test_unknown_type(self):
        """Test error on unknown dataset type."""
        from khipu_demo.data import generate_synthetic_data
        
        with pytest.raises(ValueError, match="Unknown dataset type"):
            generate_synthetic_data("unknown_type")
