"""
Unit tests for khipu_demo package.
"""

import pytest
import os


def test_demo_mode_detection():
    """Test DEMO_MODE environment variable detection."""
    from khipu_demo import is_demo_mode, DEMO_MODE
    
    # In test environment, should detect demo mode
    assert isinstance(DEMO_MODE, bool)
    assert is_demo_mode() == DEMO_MODE


def test_package_version():
    """Test package version is defined."""
    from khipu_demo import __version__, get_version
    
    assert __version__ is not None
    assert isinstance(__version__, str)
    assert get_version() == __version__


def test_import_clients():
    """Test that mock clients can be imported."""
    from khipu_demo.clients import (
        BLSMockClient,
        BEAMockClient,
        CensusMockClient,
        EPAMockClient,
        CDCMockClient,
        ZillowMockClient,
    )
    
    # All clients should be importable
    assert BLSMockClient is not None
    assert BEAMockClient is not None
    assert CensusMockClient is not None
    assert EPAMockClient is not None
    assert CDCMockClient is not None
    assert ZillowMockClient is not None


def test_import_data():
    """Test that data utilities can be imported."""
    from khipu_demo.data import (
        SyntheticDataGenerator,
        DataProvenance,
        compute_dataset_hash,
        load_public_dataset,
    )
    
    assert SyntheticDataGenerator is not None
    assert DataProvenance is not None
    assert compute_dataset_hash is not None
    assert load_public_dataset is not None


def test_import_visualization():
    """Test that visualization utilities can be imported."""
    from khipu_demo.visualization import (
        get_palette,
        COLORBLIND_SAFE,
        check_contrast_ratio,
    )
    
    assert get_palette is not None
    assert isinstance(COLORBLIND_SAFE, dict)
    assert check_contrast_ratio is not None
