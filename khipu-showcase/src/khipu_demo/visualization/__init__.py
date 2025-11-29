"""
Visualization utilities for Khipu Demo notebooks.

This module provides:
- Accessible color palettes (colorblind-safe)
- Map visualization utilities
- Chart templates
- Accessibility compliance helpers
"""

from typing import Dict, List, Optional, Any, Tuple, Union
import warnings

# Optional dependencies - gracefully degrade if not available
try:
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    warnings.warn("matplotlib not installed. Visualization features limited.")

try:
    import plotly.express as px
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False
    warnings.warn("plotly not installed. Interactive visualizations disabled.")

import numpy as np


# ============================================================================
# ACCESSIBLE COLOR PALETTES
# ============================================================================

# Colorblind-safe palette (Wong, 2011 - Nature Methods)
COLORBLIND_SAFE = {
    "blue": "#0072B2",
    "orange": "#E69F00",
    "green": "#009E73",
    "yellow": "#F0E442",
    "sky_blue": "#56B4E9",
    "vermillion": "#D55E00",
    "reddish_purple": "#CC79A7",
    "black": "#000000",
}

# Sequential palette for choropleth maps
SEQUENTIAL_BLUE = [
    "#f7fbff", "#deebf7", "#c6dbef", "#9ecae1",
    "#6baed6", "#4292c6", "#2171b5", "#08519c", "#08306b"
]

SEQUENTIAL_GREEN = [
    "#f7fcf5", "#e5f5e0", "#c7e9c0", "#a1d99b",
    "#74c476", "#41ab5d", "#238b45", "#006d2c", "#00441b"
]

# Diverging palette for positive/negative values
DIVERGING_RdBu = [
    "#b2182b", "#d6604d", "#f4a582", "#fddbc7",
    "#f7f7f7",
    "#d1e5f0", "#92c5de", "#4393c3", "#2166ac"
]

# High contrast for accessibility
HIGH_CONTRAST = {
    "primary": "#1a1a1a",
    "secondary": "#0066cc",
    "accent": "#cc3300",
    "background": "#ffffff",
    "muted": "#666666",
}


def get_palette(name: str = "colorblind") -> List[str]:
    """
    Get a color palette by name.
    
    Args:
        name: Palette name ("colorblind", "sequential_blue", 
              "sequential_green", "diverging")
              
    Returns:
        List of hex color codes
    """
    palettes = {
        "colorblind": list(COLORBLIND_SAFE.values()),
        "sequential_blue": SEQUENTIAL_BLUE,
        "sequential_green": SEQUENTIAL_GREEN,
        "diverging": DIVERGING_RdBu,
    }
    return palettes.get(name, palettes["colorblind"])


# ============================================================================
# ACCESSIBILITY HELPERS
# ============================================================================

def check_contrast_ratio(
    foreground: str,
    background: str = "#ffffff"
) -> Tuple[float, str]:
    """
    Check WCAG contrast ratio between colors.
    
    Args:
        foreground: Foreground color (hex)
        background: Background color (hex)
        
    Returns:
        Tuple of (ratio, WCAG level)
    """
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def relative_luminance(rgb: Tuple[int, int, int]) -> float:
        srgb = [c / 255 for c in rgb]
        linear = [
            c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
            for c in srgb
        ]
        return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]
    
    l1 = relative_luminance(hex_to_rgb(foreground))
    l2 = relative_luminance(hex_to_rgb(background))
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    ratio = (lighter + 0.05) / (darker + 0.05)
    
    if ratio >= 7:
        level = "AAA"
    elif ratio >= 4.5:
        level = "AA"
    elif ratio >= 3:
        level = "AA-Large"
    else:
        level = "Fail"
    
    return ratio, level


def add_alt_text(
    fig: Any,
    description: str,
    extended_description: Optional[str] = None
) -> Dict[str, str]:
    """
    Generate accessibility metadata for a figure.
    
    Args:
        fig: Figure object (matplotlib or plotly)
        description: Short description (< 125 chars)
        extended_description: Extended description for complex charts
        
    Returns:
        Dictionary with alt text and aria-label
    """
    return {
        "alt": description[:125],
        "aria-label": description,
        "aria-describedby": extended_description or description,
    }


# ============================================================================
# CHART TEMPLATES
# ============================================================================

def setup_matplotlib_style():
    """Configure matplotlib for accessibility and consistency."""
    if not HAS_MATPLOTLIB:
        warnings.warn("matplotlib not available")
        return
    
    plt.rcParams.update({
        # Font sizes for readability
        "font.size": 12,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        
        # Line widths for visibility
        "lines.linewidth": 2,
        "axes.linewidth": 1.2,
        
        # Grid for reference
        "axes.grid": True,
        "grid.alpha": 0.3,
        
        # Figure quality
        "figure.dpi": 100,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        
        # Accessible fonts
        "font.family": ["DejaVu Sans", "Helvetica", "Arial", "sans-serif"],
    })


def create_line_chart(
    x_data: List[Any],
    y_data: Union[List[float], Dict[str, List[float]]],
    title: str,
    x_label: str,
    y_label: str,
    use_plotly: bool = True,
    accessible_colors: bool = True
) -> Any:
    """
    Create an accessible line chart.
    
    Args:
        x_data: X-axis values
        y_data: Y-axis values (single list or dict of series)
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        use_plotly: Use Plotly (True) or Matplotlib (False)
        accessible_colors: Use colorblind-safe palette
        
    Returns:
        Figure object
    """
    colors = get_palette("colorblind") if accessible_colors else None
    
    if use_plotly and HAS_PLOTLY:
        if isinstance(y_data, dict):
            fig = go.Figure()
            for i, (name, values) in enumerate(y_data.items()):
                fig.add_trace(go.Scatter(
                    x=x_data,
                    y=values,
                    mode='lines+markers',
                    name=name,
                    line=dict(color=colors[i % len(colors)] if colors else None),
                ))
        else:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x_data,
                y=y_data,
                mode='lines+markers',
                line=dict(color=colors[0] if colors else None),
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            font=dict(size=12),
            template="plotly_white",
        )
        return fig
    
    elif HAS_MATPLOTLIB:
        setup_matplotlib_style()
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if isinstance(y_data, dict):
            for i, (name, values) in enumerate(y_data.items()):
                color = colors[i % len(colors)] if colors else None
                ax.plot(x_data, values, marker='o', label=name, color=color)
            ax.legend()
        else:
            ax.plot(x_data, y_data, marker='o', color=colors[0] if colors else None)
        
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        plt.tight_layout()
        return fig
    
    else:
        raise RuntimeError("No visualization library available")


def create_bar_chart(
    categories: List[str],
    values: Union[List[float], Dict[str, List[float]]],
    title: str,
    x_label: str,
    y_label: str,
    horizontal: bool = False,
    use_plotly: bool = True,
    accessible_colors: bool = True
) -> Any:
    """
    Create an accessible bar chart.
    
    Args:
        categories: Category labels
        values: Values (single list or dict for grouped bars)
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        horizontal: Create horizontal bars
        use_plotly: Use Plotly (True) or Matplotlib (False)
        accessible_colors: Use colorblind-safe palette
        
    Returns:
        Figure object
    """
    colors = get_palette("colorblind") if accessible_colors else None
    
    if use_plotly and HAS_PLOTLY:
        if isinstance(values, dict):
            fig = go.Figure()
            for i, (name, vals) in enumerate(values.items()):
                bar_func = go.Bar(
                    name=name,
                    marker_color=colors[i % len(colors)] if colors else None,
                )
                if horizontal:
                    bar_func.x = vals
                    bar_func.y = categories
                    bar_func.orientation = 'h'
                else:
                    bar_func.x = categories
                    bar_func.y = vals
                fig.add_trace(bar_func)
        else:
            if horizontal:
                fig = go.Figure(go.Bar(
                    x=values,
                    y=categories,
                    orientation='h',
                    marker_color=colors[0] if colors else None,
                ))
            else:
                fig = go.Figure(go.Bar(
                    x=categories,
                    y=values,
                    marker_color=colors[0] if colors else None,
                ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            barmode='group',
            template="plotly_white",
        )
        return fig
    
    elif HAS_MATPLOTLIB:
        setup_matplotlib_style()
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if isinstance(values, dict):
            x = np.arange(len(categories))
            width = 0.8 / len(values)
            for i, (name, vals) in enumerate(values.items()):
                offset = (i - len(values)/2 + 0.5) * width
                color = colors[i % len(colors)] if colors else None
                if horizontal:
                    ax.barh(x + offset, vals, width, label=name, color=color)
                else:
                    ax.bar(x + offset, vals, width, label=name, color=color)
            ax.legend()
            if horizontal:
                ax.set_yticks(x)
                ax.set_yticklabels(categories)
            else:
                ax.set_xticks(x)
                ax.set_xticklabels(categories, rotation=45, ha='right')
        else:
            color = colors[0] if colors else None
            if horizontal:
                ax.barh(categories, values, color=color)
            else:
                ax.bar(categories, values, color=color)
        
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        plt.tight_layout()
        return fig
    
    else:
        raise RuntimeError("No visualization library available")


def create_choropleth_map(
    locations: List[str],
    values: List[float],
    title: str,
    color_label: str,
    location_mode: str = "USA-states",
    colorscale: str = "Blues",
    use_plotly: bool = True
) -> Any:
    """
    Create an accessible choropleth map.
    
    Args:
        locations: Location codes (state abbreviations, FIPS, etc.)
        values: Values for each location
        title: Map title
        color_label: Label for color scale
        location_mode: Plotly location mode ("USA-states", "geojson-id", etc.)
        colorscale: Color scale name
        use_plotly: Must be True for choropleth
        
    Returns:
        Plotly figure object
    """
    if not HAS_PLOTLY:
        raise RuntimeError("Plotly required for choropleth maps")
    
    fig = go.Figure(go.Choropleth(
        locations=locations,
        z=values,
        locationmode=location_mode,
        colorscale=colorscale,
        colorbar_title=color_label,
    ))
    
    fig.update_layout(
        title=title,
        geo_scope='usa',
        font=dict(size=12),
    )
    
    return fig


def create_scatter_chart(
    x_data: List[float],
    y_data: List[float],
    title: str,
    x_label: str,
    y_label: str,
    labels: Optional[List[str]] = None,
    sizes: Optional[List[float]] = None,
    colors: Optional[List[Any]] = None,
    use_plotly: bool = True,
    accessible_colors: bool = True
) -> Any:
    """
    Create an accessible scatter plot.
    
    Args:
        x_data: X-axis values
        y_data: Y-axis values
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        labels: Optional point labels
        sizes: Optional point sizes
        colors: Optional point colors/categories
        use_plotly: Use Plotly (True) or Matplotlib (False)
        accessible_colors: Use colorblind-safe palette
        
    Returns:
        Figure object
    """
    palette = get_palette("colorblind") if accessible_colors else None
    
    if use_plotly and HAS_PLOTLY:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=x_data,
            y=y_data,
            mode='markers',
            text=labels,
            marker=dict(
                size=sizes if sizes else 10,
                color=colors if colors else palette[0],
                colorscale="Viridis" if isinstance(colors[0] if colors else 0, (int, float)) else None,
                showscale=isinstance(colors[0] if colors else 0, (int, float)),
            ),
            hovertemplate='%{text}<br>%{x:.2f}, %{y:.2f}<extra></extra>' if labels else None,
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            template="plotly_white",
        )
        return fig
    
    elif HAS_MATPLOTLIB:
        setup_matplotlib_style()
        fig, ax = plt.subplots(figsize=(10, 8))
        
        scatter = ax.scatter(
            x_data, y_data,
            s=sizes if sizes else 50,
            c=colors if colors else palette[0],
            alpha=0.7,
        )
        
        if labels:
            for i, label in enumerate(labels):
                ax.annotate(label, (x_data[i], y_data[i]), fontsize=8)
        
        if colors and isinstance(colors[0], (int, float)):
            plt.colorbar(scatter, ax=ax)
        
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        plt.tight_layout()
        return fig
    
    else:
        raise RuntimeError("No visualization library available")


# ============================================================================
# NOTEBOOK DISPLAY HELPERS
# ============================================================================

def display_summary_table(
    data: Dict[str, Any],
    title: str = "Summary Statistics"
) -> str:
    """
    Generate a markdown table for summary statistics.
    
    Args:
        data: Dictionary of statistic name -> value
        title: Table title
        
    Returns:
        Markdown string
    """
    lines = [f"### {title}", "", "| Metric | Value |", "|--------|-------|"]
    for key, value in data.items():
        if isinstance(value, float):
            value_str = f"{value:,.2f}"
        else:
            value_str = str(value)
        lines.append(f"| {key} | {value_str} |")
    
    return "\n".join(lines)


def format_currency(value: float, symbol: str = "$") -> str:
    """Format a number as currency."""
    return f"{symbol}{value:,.0f}"


def format_percent(value: float, decimals: int = 1) -> str:
    """Format a number as percentage."""
    return f"{value:.{decimals}f}%"


def format_large_number(value: float) -> str:
    """Format large numbers with K/M/B suffixes."""
    if value >= 1e9:
        return f"{value/1e9:.1f}B"
    elif value >= 1e6:
        return f"{value/1e6:.1f}M"
    elif value >= 1e3:
        return f"{value/1e3:.1f}K"
    else:
        return f"{value:.0f}"
