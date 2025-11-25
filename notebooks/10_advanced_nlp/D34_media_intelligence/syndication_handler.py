"""
Syndication Handler - Separate National from Regional Content

Key Innovation: Treats syndicated wire content as "national narrative baseline"
separate from regional clustering analysis.

Problem Solved:
- Syndicated articles with λ=0.0 were creating mega-clusters
- "Fact Check Team" stories scattered across 10+ clusters
- 40-50% of articles are syndicated, polluting regional analysis

Solution:
- Separate syndicated (λ=0.0) from local (λ>0.0) content
- Analyze syndicated as national baseline
- Cluster only local/regional content for geographic insights
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


class SyndicationHandler:
    """Separate syndicated (national) from local (regional) content"""

    def separate_content(self, df_enriched: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Split dataframe into syndicated and local content

        Args:
            df_enriched: DataFrame with 'lambda_spatial' column

        Returns:
            (df_syndicated, df_local): Two dataframes
        """

        if 'lambda_spatial' not in df_enriched.columns:
            raise ValueError("DataFrame must have 'lambda_spatial' column. Run adaptive weighting first.")

        # Separate by lambda value
        df_syndicated = df_enriched[df_enriched['lambda_spatial'] == 0.0].copy()
        df_local = df_enriched[df_enriched['lambda_spatial'] > 0.0].copy()

        total = len(df_enriched)
        syndicated_count = len(df_syndicated)
        local_count = len(df_local)

        print(f"\n{'='*80}")
        print(f"📊 CONTENT SEPARATION")
        print(f"{'='*80}")
        print(f"\n   Total articles: {total}")
        print(f"\n   Syndicated (national): {syndicated_count} articles ({syndicated_count/total*100:.1f}%)")
        print(f"      λ = 0.0 (geography irrelevant)")
        print(f"\n   Local (regional): {local_count} articles ({local_count/total*100:.1f}%)")
        print(f"      λ > 0.0 (geography matters)")

        return df_syndicated, df_local

    def analyze_national_baseline(self, df_syndicated: pd.DataFrame) -> Dict:
        """
        Analyze syndicated content as national narrative baseline

        This reveals:
        - Most common national stories
        - Geographic spread of syndicated content
        - Average sentiment of national coverage

        Args:
            df_syndicated: Dataframe of syndicated articles

        Returns:
            Dict with baseline metrics
        """

        if len(df_syndicated) == 0:
            print("\n⚠️  No syndicated content found")
            return None

        # Most common syndicated stories (by exact title match)
        top_stories = df_syndicated.groupby('title').size().sort_values(ascending=False).head(10)

        # Geographic spread
        locations = df_syndicated['location'].nunique() if 'location' in df_syndicated.columns else 0

        # Sentiment baseline (if available)
        avg_sentiment = None
        if 'sentiment_deep_score' in df_syndicated.columns:
            avg_sentiment = df_syndicated['sentiment_deep_score'].mean()

        # Sources
        top_sources = df_syndicated['source'].value_counts().head(5) if 'source' in df_syndicated.columns else pd.Series()

        # Duplication analysis
        unique_stories = df_syndicated['title'].nunique()
        total_instances = len(df_syndicated)
        duplication_rate = 1 - (unique_stories / total_instances) if total_instances > 0 else 0

        baseline = {
            'total_articles': total_instances,
            'unique_stories': unique_stories,
            'duplication_rate': duplication_rate,
            'geographic_spread': locations,
            'avg_sentiment': avg_sentiment,
            'top_stories': top_stories.to_dict(),
            'top_sources': top_sources.to_dict(),
        }

        # Print summary
        print(f"\n{'='*80}")
        print(f"📰 NATIONAL NARRATIVE BASELINE (Syndicated Content)")
        print(f"{'='*80}")

        print(f"\n🔢 Volume:")
        print(f"   Total articles: {baseline['total_articles']}")
        print(f"   Unique stories: {baseline['unique_stories']}")
        print(f"   Duplication rate: {baseline['duplication_rate']:.1%}")

        print(f"\n🌍 Geographic Reach:")
        print(f"   Locations covered: {baseline['geographic_spread']}")

        if avg_sentiment is not None:
            print(f"\n😊 Sentiment:")
            print(f"   Average: {avg_sentiment:.3f}")
            if avg_sentiment > 0.1:
                tone = "POSITIVE"
            elif avg_sentiment < -0.1:
                tone = "NEGATIVE"
            else:
                tone = "NEUTRAL"
            print(f"   Overall tone: {tone}")

        print(f"\n🔝 Top Syndicated Stories:")
        for i, (title, count) in enumerate(list(baseline['top_stories'].items())[:5], 1):
            print(f"   {i}. {title[:70]}...")
            print(f"      Instances: {count} ({count/total_instances*100:.1f}%)")

        print(f"\n📡 Top Sources:")
        for source, count in list(baseline['top_sources'].items())[:5]:
            print(f"   • {source}: {count} articles")

        print(f"\n💡 Interpretation:")
        print(f"   This represents the NATIONAL NARRATIVE that most Americans see")
        print(f"   regardless of location. Use this as a baseline to compare")
        print(f"   regional coverage patterns.")

        return baseline

    def print_comparison_guide(self):
        """Print guide for interpreting national vs regional analysis"""

        print(f"\n{'='*80}")
        print(f"📖 NATIONAL vs REGIONAL ANALYSIS GUIDE")
        print(f"{'='*80}")

        print(f"\n🌐 National Baseline (Syndicated):")
        print(f"   • Wire services (AP, Reuters, Bloomberg)")
        print(f"   • Network news (CNN, Fox, NBC)")
        print(f"   • Fact-check services")
        print(f"   • Corporate press releases")
        print(f"   → Represents what MOST Americans see")
        print(f"   → Geography is IRRELEVANT (same story everywhere)")

        print(f"\n🏘️  Regional Coverage (Local):")
        print(f"   • Local newspapers")
        print(f"   • Regional TV stations")
        print(f"   • Original reporting")
        print(f"   → Represents REGIONAL PERSPECTIVES")
        print(f"   → Geography MATTERS (different angles by location)")

        print(f"\n🔍 How to Use:")
        print(f"   1. National Baseline = What everyone sees")
        print(f"   2. Regional Clusters = Where coverage diverges")
        print(f"   3. Compare regional sentiment to national baseline")
        print(f"   4. Identify regional resistance/support patterns")

        print(f"\n💼 Business Value:")
        print(f"   • Policy analysts: Predict regional opposition")
        print(f"   • PR teams: Tailor messaging by region")
        print(f"   • Campaigns: Identify swing regions")

    def get_local_only_for_clustering(self, df_enriched: pd.DataFrame) -> pd.DataFrame:
        """
        Convenience method: Get local content ready for clustering

        Use this instead of the full df_enriched when running spatial clustering

        Args:
            df_enriched: Full enriched dataframe

        Returns:
            df_local: Only local/regional content (λ > 0.0)
        """

        _, df_local = self.separate_content(df_enriched)

        print(f"\n✅ Ready for regional clustering:")
        print(f"   {len(df_local)} local articles")
        print(f"   Syndicated content excluded")

        return df_local


# Example usage (for documentation)
if __name__ == "__main__":
    print(__doc__)

    print("\n" + "="*80)
    print("EXAMPLE USAGE")
    print("="*80)

    print("""
# In your notebook, after adaptive weighting:

from syndication_handler import SyndicationHandler

handler = SyndicationHandler()

# Separate content
df_syndicated, df_local = handler.separate_content(df_enriched)

# Analyze national baseline
national_baseline = handler.analyze_national_baseline(df_syndicated)

# Print interpretation guide
handler.print_comparison_guide()

# Use only local content for regional clustering
df_for_regional_clustering = df_local

# Then run clustering on df_for_regional_clustering instead of df_enriched
df_clustered = clusterer_adaptive.cluster_adaptive(
    df_for_regional_clustering,
    lambda_series=df_for_regional_clustering['lambda_spatial']
)
""")
