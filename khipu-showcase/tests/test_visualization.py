"""
Unit tests for visualization utilities.
"""

import pytest


class TestColorPalettes:
    """Tests for color palettes."""
    
    def test_colorblind_safe_palette(self):
        """Test colorblind-safe palette is defined."""
        from khipu_demo.visualization import COLORBLIND_SAFE
        
        assert isinstance(COLORBLIND_SAFE, dict)
        assert len(COLORBLIND_SAFE) >= 7  # Wong palette has 8 colors
        
        # All values should be hex colors
        for color in COLORBLIND_SAFE.values():
            assert color.startswith('#')
            assert len(color) == 7
    
    def test_get_palette(self):
        """Test get_palette function."""
        from khipu_demo.visualization import get_palette
        
        palette = get_palette("colorblind")
        assert isinstance(palette, list)
        assert len(palette) >= 7
        
        # All items should be hex colors
        for color in palette:
            assert color.startswith('#')
    
    def test_get_palette_sequential(self):
        """Test sequential palettes."""
        from khipu_demo.visualization import get_palette
        
        blue = get_palette("sequential_blue")
        green = get_palette("sequential_green")
        
        assert len(blue) == 9
        assert len(green) == 9
    
    def test_get_palette_diverging(self):
        """Test diverging palette."""
        from khipu_demo.visualization import get_palette
        
        div = get_palette("diverging")
        assert len(div) == 9
    
    def test_get_palette_unknown(self):
        """Test fallback for unknown palette."""
        from khipu_demo.visualization import get_palette
        
        # Should return colorblind palette as default
        palette = get_palette("nonexistent")
        assert len(palette) >= 7


class TestContrastRatio:
    """Tests for contrast ratio checker."""
    
    def test_check_contrast_ratio(self):
        """Test contrast ratio calculation."""
        from khipu_demo.visualization import check_contrast_ratio
        
        # Black on white should be high contrast
        ratio, level = check_contrast_ratio("#000000", "#ffffff")
        assert ratio >= 21  # Max possible is 21:1
        assert level == "AAA"
    
    def test_low_contrast(self):
        """Test low contrast detection."""
        from khipu_demo.visualization import check_contrast_ratio
        
        # Similar grays should fail
        ratio, level = check_contrast_ratio("#777777", "#888888")
        assert level == "Fail"
    
    def test_aa_large(self):
        """Test AA-Large level."""
        from khipu_demo.visualization import check_contrast_ratio
        
        # Moderate contrast
        ratio, level = check_contrast_ratio("#666666", "#ffffff")
        assert level in ["AA", "AAA", "AA-Large"]


class TestAltText:
    """Tests for accessibility metadata."""
    
    def test_add_alt_text(self):
        """Test alt text generation."""
        from khipu_demo.visualization import add_alt_text
        
        metadata = add_alt_text(
            fig=None,  # Figure not needed for metadata
            description="A bar chart showing housing growth by metro area",
            extended_description="Detailed description with methodology",
        )
        
        assert "alt" in metadata
        assert "aria-label" in metadata
        assert "aria-describedby" in metadata
        assert len(metadata["alt"]) <= 125


class TestFormatters:
    """Tests for formatting utilities."""
    
    def test_format_currency(self):
        """Test currency formatting."""
        from khipu_demo.visualization import format_currency
        
        assert format_currency(1000) == "$1,000"
        assert format_currency(1000000) == "$1,000,000"
        assert format_currency(1000, "€") == "€1,000"
    
    def test_format_percent(self):
        """Test percentage formatting."""
        from khipu_demo.visualization import format_percent
        
        assert format_percent(12.345) == "12.3%"
        assert format_percent(12.345, 2) == "12.35%"
        assert format_percent(12.345, 0) == "12%"
    
    def test_format_large_number(self):
        """Test large number formatting."""
        from khipu_demo.visualization import format_large_number
        
        assert format_large_number(1234567890) == "1.2B"
        assert format_large_number(1234567) == "1.2M"
        assert format_large_number(1234) == "1.2K"
        assert format_large_number(123) == "123"


class TestDisplaySummaryTable:
    """Tests for summary table generation."""
    
    def test_display_summary_table(self):
        """Test markdown table generation."""
        from khipu_demo.visualization import display_summary_table
        
        data = {
            "Mean": 42.5,
            "Median": 40.0,
            "Count": 100,
        }
        
        md = display_summary_table(data, title="Test Stats")
        
        assert "### Test Stats" in md
        assert "| Metric | Value |" in md
        assert "Mean" in md
        assert "42.50" in md
