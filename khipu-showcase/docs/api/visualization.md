# Visualization Module API

The `khipu_demo.visualization` module provides accessible visualization utilities.

## Color Palettes

### COLORBLIND_SAFE

Wong (2011) colorblind-safe palette from Nature Methods.

```python
from khipu_demo.visualization import COLORBLIND_SAFE

# Dictionary of named colors
print(COLORBLIND_SAFE)
# {
#     "blue": "#0072B2",
#     "orange": "#E69F00",
#     "green": "#009E73",
#     "yellow": "#F0E442",
#     "sky_blue": "#56B4E9",
#     "vermillion": "#D55E00",
#     "reddish_purple": "#CC79A7",
#     "black": "#000000",
# }
```

### get_palette

Get a color palette by name.

```python
from khipu_demo.visualization import get_palette

# Available palettes:
# - "colorblind" (default)
# - "sequential_blue"
# - "sequential_green"
# - "diverging"

colors = get_palette("colorblind")  # List of hex colors
```

---

## Accessibility Helpers

### check_contrast_ratio

Check WCAG contrast ratio between colors.

```python
from khipu_demo.visualization import check_contrast_ratio

ratio, level = check_contrast_ratio("#000000", "#ffffff")
print(f"Ratio: {ratio:.1f}:1, Level: {level}")
# Ratio: 21.0:1, Level: AAA
```

**WCAG Levels:**

| Level | Ratio | Use Case |
|-------|-------|----------|
| AAA | ≥ 7:1 | Enhanced contrast |
| AA | ≥ 4.5:1 | Normal text |
| AA-Large | ≥ 3:1 | Large text (18pt+) |
| Fail | < 3:1 | Insufficient contrast |

### add_alt_text

Generate accessibility metadata for figures.

```python
from khipu_demo.visualization import add_alt_text

metadata = add_alt_text(
    fig=my_figure,
    description="Bar chart showing housing growth by metro",
    extended_description="Detailed methodology...",
)
# Returns: {"alt": "...", "aria-label": "...", "aria-describedby": "..."}
```

---

## Chart Creation

### setup_matplotlib_style

Configure matplotlib for accessibility.

```python
from khipu_demo.visualization import setup_matplotlib_style

setup_matplotlib_style()
# Sets font sizes, line widths, grid, etc.
```

### create_line_chart

Create an accessible line chart.

```python
from khipu_demo.visualization import create_line_chart

fig = create_line_chart(
    x_data=[2020, 2021, 2022, 2023],
    y_data={"Series A": [10, 20, 30, 40], "Series B": [15, 25, 35, 45]},
    title="My Chart",
    x_label="Year",
    y_label="Value",
    use_plotly=True,  # False for matplotlib
    accessible_colors=True,
)
fig.show()
```

### create_bar_chart

Create an accessible bar chart.

```python
from khipu_demo.visualization import create_bar_chart

fig = create_bar_chart(
    categories=["A", "B", "C"],
    values=[10, 20, 30],
    title="My Bar Chart",
    x_label="Category",
    y_label="Value",
    horizontal=False,
)
```

### create_choropleth_map

Create a choropleth map (requires Plotly).

```python
from khipu_demo.visualization import create_choropleth_map

fig = create_choropleth_map(
    locations=["CA", "TX", "FL", "NY"],
    values=[100, 80, 60, 90],
    title="Values by State",
    color_label="Value",
    location_mode="USA-states",
    colorscale="Blues",
)
```

### create_scatter_chart

Create an accessible scatter plot.

```python
from khipu_demo.visualization import create_scatter_chart

fig = create_scatter_chart(
    x_data=[1, 2, 3, 4],
    y_data=[10, 20, 15, 25],
    title="Scatter Plot",
    x_label="X",
    y_label="Y",
    labels=["Point A", "Point B", "Point C", "Point D"],
)
```

---

## Formatters

### format_currency

Format a number as currency.

```python
from khipu_demo.visualization import format_currency

format_currency(1000000)     # "$1,000,000"
format_currency(1000, "€")   # "€1,000"
```

### format_percent

Format a number as percentage.

```python
from khipu_demo.visualization import format_percent

format_percent(12.345)       # "12.3%"
format_percent(12.345, 2)    # "12.35%"
```

### format_large_number

Format large numbers with K/M/B suffixes.

```python
from khipu_demo.visualization import format_large_number

format_large_number(1234567890)  # "1.2B"
format_large_number(1234567)     # "1.2M"
format_large_number(1234)        # "1.2K"
```

---

## Display Helpers

### display_summary_table

Generate a markdown table for summary statistics.

```python
from khipu_demo.visualization import display_summary_table
from IPython.display import Markdown

stats = {
    "Mean": 42.5,
    "Median": 40.0,
    "Std Dev": 5.2,
}

md = display_summary_table(stats, title="Summary Statistics")
Markdown(md)
```
