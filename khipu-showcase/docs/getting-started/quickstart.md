# Quick Start

Get up and running with Khipu showcase notebooks in 5 minutes.

## Step 1: Install the Package

```bash
pip install khipu-demo
```

## Step 2: Launch Jupyter

```bash
jupyter lab
```

## Step 3: Run Your First Analysis

Create a new notebook or open `notebooks/01-metro-housing-wage-divergence.ipynb`:

```python
# Import the demo utilities
from khipu_demo import DEMO_MODE
from khipu_demo.data import SyntheticDataGenerator
from khipu_demo.visualization import COLORBLIND_SAFE

# Verify demo mode is active
print(f"🔒 Demo Mode: {DEMO_MODE}")

# Generate sample data
generator = SyntheticDataGenerator(seed=42)
df, provenance = generator.generate_housing_wage_panel(n_metros=10)

# Preview the data
print(f"📊 Generated {len(df)} rows across {df['metro'].nunique()} metros")
df.head()
```

## Step 4: Create a Visualization

```python
import plotly.express as px

# Filter to 2024 data
df_2024 = df[df['period'] == 2024]

# Create a bar chart of divergence
fig = px.bar(
    df_2024.nlargest(10, 'divergence_pct'),
    x='metro',
    y='divergence_pct',
    title='Top 10 Metros by Housing-Wage Divergence (2024)',
    color_discrete_sequence=[COLORBLIND_SAFE['orange']],
)
fig.show()
```

## What's Next?

- Explore the full [Housing-Wage Divergence Tutorial](../notebooks/01-metro-housing-wage-divergence.ipynb)
- Learn about [Demo Mode](demo-mode.md) and how it works
- Read the [API Reference](../api/data.md) for detailed documentation

## Common Patterns

### Loading Data with Provenance

```python
from khipu_demo.data import SyntheticDataGenerator

generator = SyntheticDataGenerator(seed=42)
df, provenance = generator.generate_housing_wage_panel()

# Display provenance in notebook
from IPython.display import Markdown
Markdown(provenance.to_markdown())
```

### Using Accessible Colors

```python
from khipu_demo.visualization import get_palette, COLORBLIND_SAFE

# Get the colorblind-safe palette
colors = get_palette("colorblind")

# Use in charts
fig = px.line(df, x='period', y='value', color='category',
              color_discrete_sequence=colors)
```

### Checking WCAG Contrast

```python
from khipu_demo.visualization import check_contrast_ratio

ratio, level = check_contrast_ratio("#0072B2", "#FFFFFF")
print(f"Contrast ratio: {ratio:.1f}:1 ({level})")
```
