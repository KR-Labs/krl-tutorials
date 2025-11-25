"""
GDELT Data Scaler - Scale from 313 to 10,000+ Articles

Problem:
Current dataset has 313 articles (avg 3.7 per outlet), insufficient for:
- Causal bias analysis (requires 30+ articles per outlet)
- Robust regional sentiment (n≥30 for traditional tests)
- Reliable syndication pattern detection

Solution:
Query 180 days (vs current 60 days) and filter to top 50 outlets
Expected result: 5,000-15,000 articles with 30-50+ per outlet

Usage:
    from gdelt_scaler import GDELTScaler

    scaler = GDELTScaler()
    df_large = scaler.query_extended_period(
        topic='economy',
        days_back=180,
        max_articles=15000
    )

    df_filtered = scaler.filter_top_outlets(df_large, top_n=50)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, List
import time


class GDELTScaler:
    """
    Scale GDELT data collection from 313 to 10,000+ articles

    Methods:
    - query_extended_period(): Query 180 days instead of 60
    - filter_top_outlets(): Filter to outlets with sufficient data
    - validate_coverage(): Ensure 30+ articles per outlet
    - batch_process(): Handle large datasets efficiently
    """

    def __init__(self, verbose: bool = True):
        """
        Initialize GDELT scaler

        Args:
            verbose: Print progress messages
        """
        self.verbose = verbose

    def query_extended_period(
        self,
        query_function,  # Your existing GDELT query function
        topic: str = 'economy',
        days_back: int = 180,
        max_articles: int = 15000,
        batch_size: int = 30
    ) -> pd.DataFrame:
        """
        Query GDELT for extended time period

        Args:
            query_function: Existing GDELT query function (from your notebook)
            topic: Search topic (default: 'economy')
            days_back: Number of days to query (default: 180 for 6 months)
            max_articles: Maximum articles to retrieve (default: 15000)
            batch_size: Days per batch to avoid timeouts (default: 30)

        Returns:
            DataFrame with all articles from extended period
        """

        if self.verbose:
            print(f"\n{'='*80}")
            print(f"SCALING GDELT DATA COLLECTION")
            print(f"{'='*80}")
            print(f"\nParameters:")
            print(f"  Topic: {topic}")
            print(f"  Period: {days_back} days ({days_back/30:.1f} months)")
            print(f"  Max articles: {max_articles:,}")
            print(f"  Batch size: {batch_size} days")

        # Calculate date ranges for batching
        end_date = datetime.now()
        all_articles = []

        num_batches = (days_back + batch_size - 1) // batch_size  # Ceiling division

        if self.verbose:
            print(f"\n🔄 Processing {num_batches} batches...")

        for batch_idx in range(num_batches):
            batch_start_days = batch_idx * batch_size
            batch_end_days = min((batch_idx + 1) * batch_size, days_back)

            batch_start_date = end_date - timedelta(days=batch_end_days)
            batch_end_date = end_date - timedelta(days=batch_start_days)

            if self.verbose:
                print(f"\n  Batch {batch_idx + 1}/{num_batches}: {batch_start_date.strftime('%Y-%m-%d')} to {batch_end_date.strftime('%Y-%m-%d')}")

            try:
                # Call your existing query function
                # Note: You'll need to modify this to accept date ranges
                df_batch = query_function(
                    topic=topic,
                    start_date=batch_start_date,
                    end_date=batch_end_date
                )

                if df_batch is not None and len(df_batch) > 0:
                    all_articles.append(df_batch)
                    if self.verbose:
                        print(f"    ✓ Retrieved {len(df_batch)} articles")

                # Check if we've hit max
                total_so_far = sum(len(df) for df in all_articles)
                if total_so_far >= max_articles:
                    if self.verbose:
                        print(f"\n  ℹ️  Reached max_articles limit ({max_articles:,})")
                    break

                # Rate limiting
                time.sleep(1)  # Be nice to GDELT servers

            except Exception as e:
                if self.verbose:
                    print(f"    ⚠️  Batch failed: {str(e)}")
                continue

        # Combine all batches
        if not all_articles:
            if self.verbose:
                print(f"\n❌ No articles retrieved")
            return pd.DataFrame()

        df_combined = pd.concat(all_articles, ignore_index=True)

        # Remove duplicates (same URL)
        df_combined = df_combined.drop_duplicates(subset=['url'], keep='first')

        # Limit to max_articles if needed
        if len(df_combined) > max_articles:
            df_combined = df_combined.head(max_articles)

        if self.verbose:
            print(f"\n{'='*80}")
            print(f"📊 COLLECTION SUMMARY")
            print(f"{'='*80}")
            print(f"  Total articles: {len(df_combined):,}")
            print(f"  Unique outlets: {df_combined['source'].nunique() if 'source' in df_combined.columns else 'N/A'}")
            print(f"  Date range: {df_combined['date'].min() if 'date' in df_combined.columns else 'N/A'} to {df_combined['date'].max() if 'date' in df_combined.columns else 'N/A'}")

        return df_combined

    def filter_top_outlets(
        self,
        df: pd.DataFrame,
        top_n: int = 50,
        min_articles_per_outlet: int = 30,
        source_column: str = 'source'
    ) -> pd.DataFrame:
        """
        Filter to top N outlets with sufficient article count

        Args:
            df: Input dataframe
            top_n: Number of top outlets to keep (default: 50)
            min_articles_per_outlet: Minimum articles required (default: 30)
            source_column: Column name for outlet/source (default: 'source')

        Returns:
            DataFrame filtered to top outlets
        """

        if self.verbose:
            print(f"\n{'='*80}")
            print(f"FILTERING TO TOP OUTLETS")
            print(f"{'='*80}")

        # Calculate articles per outlet
        outlet_counts = df[source_column].value_counts()

        if self.verbose:
            print(f"\n📊 Outlet Statistics (Before Filtering):")
            print(f"  Total outlets: {len(outlet_counts)}")
            print(f"  Articles per outlet (mean): {outlet_counts.mean():.1f}")
            print(f"  Articles per outlet (median): {outlet_counts.median():.0f}")
            print(f"  Outlets with ≥{min_articles_per_outlet} articles: {(outlet_counts >= min_articles_per_outlet).sum()}")

        # Filter to outlets with minimum articles
        valid_outlets = outlet_counts[outlet_counts >= min_articles_per_outlet]

        if len(valid_outlets) == 0:
            if self.verbose:
                print(f"\n⚠️  No outlets have {min_articles_per_outlet}+ articles!")
                print(f"  Recommendation: Lower min_articles_per_outlet or increase days_back")
            return pd.DataFrame()

        # Take top N
        top_outlets = valid_outlets.head(top_n).index
        df_filtered = df[df[source_column].isin(top_outlets)].copy()

        # Recalculate statistics
        final_counts = df_filtered[source_column].value_counts()

        if self.verbose:
            print(f"\n📊 Outlet Statistics (After Filtering):")
            print(f"  Selected outlets: {len(top_outlets)}")
            print(f"  Total articles: {len(df_filtered):,}")
            print(f"  Articles per outlet (mean): {final_counts.mean():.1f}")
            print(f"  Articles per outlet (median): {final_counts.median():.0f}")
            print(f"  Articles per outlet (min): {final_counts.min()}")
            print(f"  Articles per outlet (max): {final_counts.max()}")

        # Show top outlets
        if self.verbose:
            print(f"\n🔝 Top 10 Outlets:")
            for idx, (outlet, count) in enumerate(final_counts.head(10).items(), 1):
                print(f"  {idx:2d}. {outlet:<40s} {count:4d} articles")

        return df_filtered

    def validate_coverage(
        self,
        df: pd.DataFrame,
        min_articles: int = 30,
        source_column: str = 'source'
    ) -> dict:
        """
        Validate that dataset has sufficient coverage for causal bias analysis

        Args:
            df: Input dataframe
            min_articles: Minimum articles per outlet for valid bias analysis
            source_column: Column name for outlet/source

        Returns:
            Dict with validation results
        """

        outlet_counts = df[source_column].value_counts()
        valid_outlets = outlet_counts[outlet_counts >= min_articles]

        validation = {
            'total_articles': len(df),
            'total_outlets': len(outlet_counts),
            'valid_outlets': len(valid_outlets),
            'valid_articles': df[df[source_column].isin(valid_outlets.index)].shape[0],
            'coverage_pct': (len(valid_outlets) / len(outlet_counts)) * 100 if len(outlet_counts) > 0 else 0,
            'ready_for_causal_bias': len(valid_outlets) >= 10,  # Need at least 10 outlets
            'min_articles_per_outlet': min_articles,
            'avg_articles_per_valid_outlet': valid_outlets.mean() if len(valid_outlets) > 0 else 0
        }

        if self.verbose:
            print(f"\n{'='*80}")
            print(f"VALIDATION RESULTS")
            print(f"{'='*80}")
            print(f"\n📊 Coverage:")
            print(f"  Total articles: {validation['total_articles']:,}")
            print(f"  Total outlets: {validation['total_outlets']}")
            print(f"  Valid outlets (≥{min_articles} articles): {validation['valid_outlets']}")
            print(f"  Coverage: {validation['coverage_pct']:.1f}%")
            print(f"\n🎯 Causal Bias Analysis:")
            if validation['ready_for_causal_bias']:
                print(f"  ✅ READY - {validation['valid_outlets']} outlets with {min_articles}+ articles")
                print(f"  Average articles per outlet: {validation['avg_articles_per_valid_outlet']:.1f}")
            else:
                print(f"  ❌ NOT READY - Need at least 10 outlets with {min_articles}+ articles")
                print(f"  Current: {validation['valid_outlets']} outlets")
                print(f"  Recommendation: Increase days_back or lower min_articles threshold")

        return validation

    def estimate_scaling_parameters(
        self,
        current_articles: int = 313,
        current_days: int = 60,
        target_articles_per_outlet: int = 30,
        target_outlets: int = 50
    ) -> dict:
        """
        Estimate optimal scaling parameters

        Args:
            current_articles: Current dataset size (default: 313)
            current_days: Current query period (default: 60 days)
            target_articles_per_outlet: Target articles per outlet (default: 30)
            target_outlets: Target number of outlets (default: 50)

        Returns:
            Dict with recommendations
        """

        # Calculate target total articles
        target_total = target_articles_per_outlet * target_outlets

        # Estimate required days (linear scaling assumption)
        scaling_factor = target_total / current_articles
        estimated_days = int(current_days * scaling_factor)

        # Cap at 180 days (6 months) for practical reasons
        recommended_days = min(estimated_days, 180)
        expected_articles = int((recommended_days / current_days) * current_articles)

        recommendations = {
            'target_total_articles': target_total,
            'scaling_factor': scaling_factor,
            'estimated_days_needed': estimated_days,
            'recommended_days': recommended_days,
            'expected_articles': expected_articles,
            'should_meet_target': expected_articles >= target_total
        }

        if self.verbose:
            print(f"\n{'='*80}")
            print(f"SCALING PARAMETER RECOMMENDATIONS")
            print(f"{'='*80}")
            print(f"\n📊 Current State:")
            print(f"  Articles: {current_articles}")
            print(f"  Query period: {current_days} days")
            print(f"\n🎯 Target:")
            print(f"  {target_outlets} outlets × {target_articles_per_outlet} articles = {target_total:,} total")
            print(f"\n💡 Recommendation:")
            print(f"  Query period: {recommended_days} days ({recommended_days/30:.1f} months)")
            print(f"  Expected articles: ~{expected_articles:,}")
            if recommendations['should_meet_target']:
                print(f"  ✅ Should meet target")
            else:
                print(f"  ⚠️  May not meet target - consider longer period or lower requirements")

        return recommendations


# Example usage
if __name__ == "__main__":
    print(__doc__)

    print("\n" + "="*80)
    print("EXAMPLE USAGE")
    print("="*80)

    print("""
# In your notebook, replace the data collection cell:

from gdelt_scaler import GDELTScaler

# Initialize scaler
scaler = GDELTScaler(verbose=True)

# Step 1: Estimate optimal parameters
recommendations = scaler.estimate_scaling_parameters(
    current_articles=313,
    current_days=60,
    target_articles_per_outlet=30,
    target_outlets=50
)

# Step 2: Query extended period (180 days)
# Note: You'll need to modify your existing query function to accept date ranges
df_large = scaler.query_extended_period(
    query_function=your_gdelt_query_function,  # Your existing function
    topic='economy',
    days_back=180,  # 6 months
    max_articles=15000
)

# Step 3: Filter to top outlets
df_filtered = scaler.filter_top_outlets(
    df_large,
    top_n=50,
    min_articles_per_outlet=30
)

# Step 4: Validate coverage
validation = scaler.validate_coverage(
    df_filtered,
    min_articles=30
)

# Step 5: Proceed with enrichment and clustering
# (Use df_filtered instead of df_original)
""")
