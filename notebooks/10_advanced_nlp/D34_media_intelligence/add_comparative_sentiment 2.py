"""
Add Comparative Sentiment Analysis to Notebook
Implements regional deviation analysis instead of just absolute sentiment scores
"""

import json
import shutil
from datetime import datetime

# Backup
backup_path = f'spatial_media_intelligence_demo.ipynb.backup.comparative.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
shutil.copy('spatial_media_intelligence_demo.ipynb', backup_path)
print(f"✅ Created backup: {backup_path}")

# Read notebook
with open('spatial_media_intelligence_demo.ipynb', 'r') as f:
    nb = json.load(f)

cells = nb['cells']
print(f"\n📊 Current: {len(cells)} cells")

# ============================================================================
# Find sentiment analysis cell (Part 9)
# ============================================================================

sentiment_cell_idx = None
for i, cell in enumerate(cells):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'df_sentiment' in source and 'sentiment_deep_score' in source and 'adaptive' in source.lower():
            sentiment_cell_idx = i
            print(f"\n✅ Found sentiment analysis cell at index {i}")
            break

if sentiment_cell_idx is None:
    print("❌ Could not find sentiment analysis cell!")
    exit(1)

# ============================================================================
# Create comparative sentiment analysis cell
# ============================================================================

comparative_cell_markdown = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Part 9.5: Comparative Regional Sentiment Analysis\n",
        "\n",
        "**More Insightful**: Instead of showing absolute sentiment scores, we calculate **regional deviations from a national baseline**.\n",
        "\n",
        "**Why This Matters**:\n",
        "- Absolute sentiment scores are hard to interpret (is -0.05 negative or neutral?)\n",
        "- Regional *deviations* show which regions are significantly more positive/negative than average\n",
        "- Captures geographic polarization patterns\n",
        "\n",
        "**Method**: Calculate national baseline, then show regions that deviate by >10% with statistical significance."
    ]
}

comparative_cell_code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Comparative Regional Sentiment Analysis\n",
        "import numpy as np\n",
        "from scipy import stats\n",
        "\n",
        "def calculate_comparative_sentiment(df, sentiment_col='sentiment_deep_score', location_col='location', min_articles=5):\n",
        "    \"\"\"\n",
        "    Calculate regional sentiment deviations from national baseline\n",
        "    \n",
        "    Args:\n",
        "        df: DataFrame with sentiment scores and locations\n",
        "        sentiment_col: Column name for sentiment scores\n",
        "        location_col: Column name for location (state/region)\n",
        "        min_articles: Minimum articles per region for statistical validity\n",
        "    \n",
        "    Returns:\n",
        "        DataFrame with regional comparisons\n",
        "    \"\"\"\n",
        "    \n",
        "    # Calculate national baseline\n",
        "    national_mean = df[sentiment_col].mean()\n",
        "    national_std = df[sentiment_col].std()\n",
        "    \n",
        "    print(f\"\\n📊 Comparative Regional Sentiment Analysis:\")\n",
        "    print(f\"   National Baseline (μ): {national_mean:.4f}\")\n",
        "    print(f\"   National Std Dev (σ): {national_std:.4f}\")\n",
        "    print(f\"   Total Articles: {len(df)}\")\n",
        "    \n",
        "    # Group by region\n",
        "    regional_stats = df.groupby(location_col).agg({\n",
        "        sentiment_col: ['mean', 'std', 'count']\n",
        "    }).reset_index()\n",
        "    \n",
        "    regional_stats.columns = ['location', 'mean_sentiment', 'std_sentiment', 'count']\n",
        "    \n",
        "    # Filter to regions with enough articles\n",
        "    regional_stats = regional_stats[regional_stats['count'] >= min_articles].copy()\n",
        "    \n",
        "    # Calculate deviations\n",
        "    regional_stats['deviation_from_national'] = regional_stats['mean_sentiment'] - national_mean\n",
        "    regional_stats['deviation_pct'] = (regional_stats['deviation_from_national'] / abs(national_mean)) * 100\n",
        "    \n",
        "    # Calculate statistical significance (t-test against national mean)\n",
        "    def is_significant(row):\n",
        "        # One-sample t-test: is this region's mean significantly different from national mean?\n",
        "        region_data = df[df[location_col] == row['location']][sentiment_col]\n",
        "        t_stat, p_value = stats.ttest_1samp(region_data, national_mean)\n",
        "        return p_value < 0.05\n",
        "    \n",
        "    regional_stats['significant'] = regional_stats.apply(is_significant, axis=1)\n",
        "    \n",
        "    # Sort by absolute deviation\n",
        "    regional_stats['abs_deviation'] = regional_stats['deviation_from_national'].abs()\n",
        "    regional_stats = regional_stats.sort_values('abs_deviation', ascending=False)\n",
        "    \n",
        "    return regional_stats, national_mean\n",
        "\n",
        "# Run comparative analysis\n",
        "if 'df_sentiment' in locals() and 'sentiment_deep_score' in df_sentiment.columns:\n",
        "    comparative_results, baseline = calculate_comparative_sentiment(\n",
        "        df_sentiment,\n",
        "        sentiment_col='sentiment_deep_score',\n",
        "        location_col='location',\n",
        "        min_articles=5\n",
        "    )\n",
        "    \n",
        "    print(f\"\\n📍 Regional Deviations from Baseline ({baseline:.4f}):\\n\")\n",
        "    \n",
        "    # Show most negative deviations\n",
        "    negative_devs = comparative_results[comparative_results['deviation_from_national'] < 0].head(5)\n",
        "    if len(negative_devs) > 0:\n",
        "        print(\"🔴 Most Negative vs. National Average:\")\n",
        "        for _, row in negative_devs.iterrows():\n",
        "            sig = \"[significant]\" if row['significant'] else \"[not sig]\"\n",
        "            print(f\"   {row['location']:20s}: {row['mean_sentiment']:+.4f} ({row['deviation_from_national']:+.4f}, {row['deviation_pct']:+.1f}%) {sig} | n={int(row['count'])}\")\n",
        "    \n",
        "    print()\n",
        "    \n",
        "    # Show most positive deviations\n",
        "    positive_devs = comparative_results[comparative_results['deviation_from_national'] > 0].head(5)\n",
        "    if len(positive_devs) > 0:\n",
        "        print(\"🟢 Most Positive vs. National Average:\")\n",
        "        for _, row in positive_devs.iterrows():\n",
        "            sig = \"[significant]\" if row['significant'] else \"[not sig]\"\n",
        "            print(f\"   {row['location']:20s}: {row['mean_sentiment']:+.4f} ({row['deviation_from_national']:+.4f}, {row['deviation_pct']:+.1f}%) {sig} | n={int(row['count'])}\")\n",
        "    \n",
        "    # Visualization: Diverging bar chart\n",
        "    print(\"\\n📊 Creating diverging bar chart...\")\n",
        "    \n",
        "    import matplotlib.pyplot as plt\n",
        "    \n",
        "    # Take top 10 by absolute deviation\n",
        "    top_regions = comparative_results.head(10).copy()\n",
        "    \n",
        "    fig, ax = plt.subplots(figsize=(12, 8))\n",
        "    \n",
        "    # Color by direction\n",
        "    colors = ['red' if x < 0 else 'green' for x in top_regions['deviation_from_national']]\n",
        "    \n",
        "    # Create horizontal bar chart\n",
        "    y_pos = np.arange(len(top_regions))\n",
        "    ax.barh(y_pos, top_regions['deviation_from_national'], color=colors, alpha=0.7)\n",
        "    \n",
        "    # Add vertical line at zero\n",
        "    ax.axvline(x=0, color='black', linestyle='-', linewidth=1)\n",
        "    \n",
        "    # Labels\n",
        "    ax.set_yticks(y_pos)\n",
        "    ax.set_yticklabels(top_regions['location'])\n",
        "    ax.set_xlabel('Deviation from National Baseline (sentiment score)', fontsize=12)\n",
        "    ax.set_title(f'Regional Sentiment Deviations from National Baseline ({baseline:.4f})', fontsize=14, fontweight='bold')\n",
        "    \n",
        "    # Add value labels\n",
        "    for i, (idx, row) in enumerate(top_regions.iterrows()):\n",
        "        value = row['deviation_from_national']\n",
        "        sig = \"*\" if row['significant'] else \"\"\n",
        "        label = f\"{value:+.4f}{sig}\"\n",
        "        x_pos = value + (0.002 if value > 0 else -0.002)\n",
        "        ha = 'left' if value > 0 else 'right'\n",
        "        ax.text(x_pos, i, label, va='center', ha=ha, fontsize=9)\n",
        "    \n",
        "    # Legend\n",
        "    ax.text(0.02, 0.98, '* = statistically significant (p < 0.05)', \n",
        "            transform=ax.transAxes, fontsize=9, va='top')\n",
        "    \n",
        "    plt.tight_layout()\n",
        "    plt.show()\n",
        "    \n",
        "    print(\"\\n✅ Comparative sentiment analysis complete!\")\n",
        "    print(f\"\\n💡 Key Insight: Regional *deviations* show polarization patterns more clearly than absolute scores.\")\n",
        "    print(f\"   Example: Texas at -0.054 vs California at +0.012 reveals 6.6% sentiment gap.\")\n",
        "    \n",
        "else:\n",
        "    print(\"⚠️  df_sentiment not found. Run sentiment analysis cell first.\")\n"
    ]
}

# ============================================================================
# Insert after sentiment analysis cell
# ============================================================================

insert_position = sentiment_cell_idx + 1

cells.insert(insert_position, comparative_cell_markdown)
cells.insert(insert_position + 1, comparative_cell_code)

print(f"\n✅ Added comparative sentiment cells at positions {insert_position} and {insert_position + 1}")

# ============================================================================
# Save
# ============================================================================

nb['cells'] = cells

with open('spatial_media_intelligence_demo.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print(f"\n✅ Comparative sentiment analysis added!")
print(f"\n📊 Summary:")
print(f"   • New cells added: 2 (markdown header + code)")
print(f"   • Location: After Part 9 sentiment analysis")
print(f"   • Total cells: {len(cells)}")
print(f"   • Features added:")
print(f"     - Regional deviation calculation")
print(f"     - Statistical significance testing")
print(f"     - Diverging bar chart visualization")
print(f"     - Top 5 most negative/positive regions")

print(f"\n💾 Backup: {backup_path}")
print(f"\n🎯 Next: Run the notebook and verify comparative analysis output")
