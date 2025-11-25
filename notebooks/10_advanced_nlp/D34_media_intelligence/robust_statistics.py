"""
Robust Statistical Tests for Small Samples

Problem:
Traditional statistical tests (t-test, ANOVA) require n≥30 per group
for valid results. With 313 articles across 70 locations, most regions
have <10 articles, making standard tests unreliable.

Solution:
Bootstrap-based methods that work with small samples (n≥5):
- Bootstrap confidence intervals (resampling with replacement)
- Permutation tests (non-parametric, no distribution assumptions)
- Effect size measures (magnitude of difference, not just significance)

Use this for:
- Regional sentiment comparisons
- Outlet bias detection with limited data
- Any comparison where sample sizes are <30
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Tuple, Optional


class RobustStatistics:
    """
    Bootstrap-based statistical tests for small samples

    Methods:
    - Bootstrap CI: Works with n≥5 per group
    - Permutation test: Distribution-free, robust to outliers
    - Effect sizes: Quantify magnitude of differences

    Advantages over traditional tests:
    - No normality assumption
    - Works with small samples
    - Resistant to outliers
    - Provides intuitive confidence intervals
    """

    def __init__(self, n_bootstrap: int = 1000, random_seed: Optional[int] = 42):
        """
        Initialize robust statistics calculator

        Args:
            n_bootstrap: Number of bootstrap samples (default: 1000)
            random_seed: Random seed for reproducibility
        """
        self.n_bootstrap = n_bootstrap

        if random_seed is not None:
            np.random.seed(random_seed)

    def bootstrap_ci(
        self,
        data: np.ndarray,
        statistic_func=np.mean,
        alpha: float = 0.05
    ) -> Tuple[float, float, float]:
        """
        Calculate bootstrap confidence interval

        Args:
            data: Sample data
            statistic_func: Function to calculate statistic (default: mean)
            alpha: Significance level (default: 0.05 for 95% CI)

        Returns:
            (point_estimate, ci_lower, ci_upper)
        """

        if len(data) < 5:
            raise ValueError("Need at least 5 samples for bootstrap")

        # Calculate point estimate
        point_estimate = statistic_func(data)

        # Bootstrap resampling
        bootstrap_estimates = []
        for _ in range(self.n_bootstrap):
            sample = np.random.choice(data, size=len(data), replace=True)
            bootstrap_estimates.append(statistic_func(sample))

        # Calculate CI
        ci_lower = np.percentile(bootstrap_estimates, (alpha/2) * 100)
        ci_upper = np.percentile(bootstrap_estimates, (1 - alpha/2) * 100)

        return point_estimate, ci_lower, ci_upper

    def regional_sentiment_with_ci(
        self,
        df: pd.DataFrame,
        sentiment_col: str = 'sentiment_deep_score',
        location_col: str = 'location',
        min_n: int = 5,
        alpha: float = 0.05
    ) -> pd.DataFrame:
        """
        Calculate regional sentiment with bootstrap confidence intervals

        Works with small samples (n≥5) unlike traditional t-tests (n≥30)

        Args:
            df: DataFrame with sentiment scores and locations
            sentiment_col: Column name for sentiment scores
            location_col: Column name for location (state/region)
            min_n: Minimum articles per region (default: 5)
            alpha: Significance level (default: 0.05)

        Returns:
            DataFrame with regional stats and confidence intervals
        """

        if sentiment_col not in df.columns:
            raise ValueError(f"Column '{sentiment_col}' not found in dataframe")

        # Calculate national baseline
        national_mean = df[sentiment_col].mean()
        national_std = df[sentiment_col].std()

        print(f"\n{'='*80}")
        print(f"REGIONAL SENTIMENT ANALYSIS (Bootstrap Method)")
        print(f"{'='*80}")

        print(f"\n📊 National Baseline:")
        print(f"   Mean: {national_mean:.4f}")
        print(f"   Std Dev: {national_std:.4f}")
        print(f"   Total Articles: {len(df)}")

        results = []

        for location in df[location_col].unique():
            location_data = df[df[location_col] == location][sentiment_col].values

            if len(location_data) < min_n:
                continue

            # Bootstrap CI
            try:
                mean_est, ci_lower, ci_upper = self.bootstrap_ci(
                    location_data,
                    statistic_func=np.mean,
                    alpha=alpha
                )
            except:
                continue

            # Check if CI excludes national mean (significance test)
            is_significant = (ci_upper < national_mean) or (ci_lower > national_mean)

            # Effect size (standardized mean difference)
            effect_size = (mean_est - national_mean) / national_std if national_std > 0 else 0

            results.append({
                'location': location,
                'mean_sentiment': mean_est,
                'ci_lower': ci_lower,
                'ci_upper': ci_upper,
                'ci_width': ci_upper - ci_lower,
                'n_articles': len(location_data),
                'deviation': mean_est - national_mean,
                'effect_size': effect_size,
                'significant': is_significant
            })

        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values('deviation', key=abs, ascending=False)

        # Print summary
        significant_count = results_df['significant'].sum()
        total_regions = len(results_df)

        print(f"\n🔍 Regional Analysis:")
        print(f"   Regions analyzed: {total_regions}")
        print(f"   Significant deviations: {significant_count} ({significant_count/total_regions*100:.1f}%)")
        print(f"   Min sample size: {min_n} articles")
        print(f"   Confidence level: {(1-alpha)*100:.0f}%")

        print(f"\n🎯 Interpretation:")
        print(f"   • Significant = 95% CI excludes national baseline")
        print(f"   • Effect sizes: Small (0.2), Medium (0.5), Large (0.8)")

        return results_df

    def permutation_test(
        self,
        group_a: np.ndarray,
        group_b: np.ndarray,
        n_permutations: int = 10000
    ) -> Dict:
        """
        Non-parametric permutation test for difference in means

        No assumptions about distribution. Works with small samples.

        Args:
            group_a: First group data
            group_b: Second group data
            n_permutations: Number of permutations (default: 10000)

        Returns:
            Dict with test results
        """

        # Observed difference
        obs_diff = group_a.mean() - group_b.mean()

        # Combine groups
        combined = np.concatenate([group_a, group_b])
        n_a = len(group_a)

        # Permutation distribution
        perm_diffs = []
        for _ in range(n_permutations):
            np.random.shuffle(combined)
            perm_a = combined[:n_a]
            perm_b = combined[n_a:]
            perm_diffs.append(perm_a.mean() - perm_b.mean())

        perm_diffs = np.array(perm_diffs)

        # Calculate p-value (two-tailed)
        p_value = np.mean(np.abs(perm_diffs) >= np.abs(obs_diff))

        # Effect size (Cohen's d)
        pooled_std = np.sqrt(((len(group_a) - 1) * group_a.std()**2 +
                               (len(group_b) - 1) * group_b.std()**2) /
                              (len(group_a) + len(group_b) - 2))

        cohens_d = obs_diff / pooled_std if pooled_std > 0 else 0

        return {
            'observed_difference': obs_diff,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'effect_size': cohens_d,
            'group_a_mean': group_a.mean(),
            'group_b_mean': group_b.mean(),
            'group_a_n': len(group_a),
            'group_b_n': len(group_b)
        }

    def print_regional_summary(
        self,
        results_df: pd.DataFrame,
        top_n: int = 10
    ):
        """
        Print formatted summary of regional sentiment analysis

        Args:
            results_df: DataFrame from regional_sentiment_with_ci()
            top_n: Number of top regions to display
        """

        print(f"\n{'='*80}")
        print(f"TOP REGIONAL DEVIATIONS FROM NATIONAL BASELINE")
        print(f"{'='*80}")

        # Most negative
        negative = results_df[results_df['deviation'] < 0].head(top_n)
        if len(negative) > 0:
            print(f"\n🔴 Most NEGATIVE vs National Average:\n")
            print(f"{'Location':<25} {'Mean':>8} {'95% CI':>20} {'n':>5} {'Sig?':>6} {'Effect':>8}")
            print("-"*80)

            for _, row in negative.iterrows():
                sig = "✓" if row['significant'] else ""
                ci_str = f"[{row['ci_lower']:.3f}, {row['ci_upper']:.3f}]"

                # Effect size label
                abs_effect = abs(row['effect_size'])
                if abs_effect > 0.8:
                    effect_label = "Large"
                elif abs_effect > 0.5:
                    effect_label = "Medium"
                elif abs_effect > 0.2:
                    effect_label = "Small"
                else:
                    effect_label = "Tiny"

                print(f"{row['location']:<25} {row['mean_sentiment']:>8.3f} {ci_str:>20} "
                      f"{int(row['n_articles']):>5} {sig:>6} {effect_label:>8}")

        # Most positive
        positive = results_df[results_df['deviation'] > 0].head(top_n)
        if len(positive) > 0:
            print(f"\n🟢 Most POSITIVE vs National Average:\n")
            print(f"{'Location':<25} {'Mean':>8} {'95% CI':>20} {'n':>5} {'Sig?':>6} {'Effect':>8}")
            print("-"*80)

            for _, row in positive.iterrows():
                sig = "✓" if row['significant'] else ""
                ci_str = f"[{row['ci_lower']:.3f}, {row['ci_upper']:.3f}]"

                abs_effect = abs(row['effect_size'])
                if abs_effect > 0.8:
                    effect_label = "Large"
                elif abs_effect > 0.5:
                    effect_label = "Medium"
                elif abs_effect > 0.2:
                    effect_label = "Small"
                else:
                    effect_label = "Tiny"

                print(f"{row['location']:<25} {row['mean_sentiment']:>8.3f} {ci_str:>20} "
                      f"{int(row['n_articles']):>5} {sig:>6} {effect_label:>8}")

        print(f"\n{'='*80}")
        print(f"NOTES:")
        print(f"  • 'Sig?' = Bootstrap 95% CI excludes national baseline")
        print(f"  • Effect sizes: Small (0.2), Medium (0.5), Large (0.8)")
        print(f"  • Method works with n≥5 (unlike t-test which needs n≥30)")
        print(f"{'='*80}")


# Example usage
if __name__ == "__main__":
    print(__doc__)

    print("\n" + "="*80)
    print("EXAMPLE USAGE")
    print("="*80)

    print("""
# In your notebook, replace traditional t-tests with bootstrap:

from robust_statistics import RobustStatistics

robust_stats = RobustStatistics(n_bootstrap=1000)

# Regional sentiment analysis (works with small samples)
results_df = robust_stats.regional_sentiment_with_ci(
    df_sentiment,
    sentiment_col='sentiment_deep_score',
    location_col='location',
    min_n=5  # Only need 5 articles, not 30!
)

# Print formatted summary
robust_stats.print_regional_summary(results_df, top_n=10)

# Compare two specific regions
region_a_data = df_sentiment[df_sentiment['location'] == 'Texas']['sentiment_deep_score'].values
region_b_data = df_sentiment[df_sentiment['location'] == 'California']['sentiment_deep_score'].values

perm_result = robust_stats.permutation_test(region_a_data, region_b_data)

print(f"Texas vs California:")
print(f"  Difference: {perm_result['observed_difference']:.3f}")
print(f"  P-value: {perm_result['p_value']:.3f}")
print(f"  Significant: {perm_result['significant']}")
print(f"  Effect size: {perm_result['effect_size']:.2f}")
""")
