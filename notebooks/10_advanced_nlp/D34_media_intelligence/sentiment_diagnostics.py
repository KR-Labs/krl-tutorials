"""
Sentiment Analysis Diagnostics
Fixes 98% neutral sentiment by:
1. Diagnosing why sentiment is neutral
2. Adjusting thresholds if needed
3. Ensuring full-text analysis (not titles)
"""

import pandas as pd
import numpy as np
from typing import Dict


class SentimentDiagnostics:
    """
    Diagnose and fix sentiment analysis issues

    Common Problems:
    1. Analyzing titles instead of full text (Jina failing)
    2. Threshold too strict (everything classified neutral)
    3. News articles genuinely neutral (common for policy topics)
    4. Model miscalibrated for domain
    """

    @staticmethod
    def diagnose_sentiment_distribution(
        df: pd.DataFrame,
        sentiment_column: str = 'sentiment_deep',
        score_column: str = 'sentiment_deep_score',
        text_column: str = 'full_text'
    ) -> Dict[str, any]:
        """
        Analyze why sentiment is so neutral

        Returns:
            Dict with diagnostic information
        """
        print("="*80)
        print("🔍 SENTIMENT DISTRIBUTION DIAGNOSTICS")
        print("="*80)

        # Distribution
        if sentiment_column in df.columns:
            distribution = df[sentiment_column].value_counts()
            print(f"\nDistribution:")
            for label, count in distribution.items():
                pct = count / len(df) * 100
                print(f"   {label}: {count} ({pct:.1f}%)")

        # Score statistics
        if score_column in df.columns:
            scores = df[score_column].dropna()
            print(f"\nScore Statistics:")
            print(f"   Mean: {scores.mean():.3f}")
            print(f"   Median: {scores.median():.3f}")
            print(f"   Std Dev: {scores.std():.3f}")
            print(f"   Range: [{scores.min():.3f}, {scores.max():.3f}]")

            # Check if using full text or titles
            if text_column in df.columns:
                text_length = df[text_column].str.split().str.len().mean()
                print(f"\nText Length Analysis:")
                print(f"   Average words: {text_length:.0f}")
                if text_length < 50:
                    print(f"   ⚠️  WARNING: Very short text (likely titles, not full articles)")
                    print(f"   → This causes neutral sentiment (not enough context)")

                # Threshold analysis
                neutral_threshold = 0.1  # Typical threshold
                would_be_positive = (scores > neutral_threshold).sum()
                would_be_negative = (scores < -neutral_threshold).sum()

                print(f"\nThreshold Analysis (threshold={neutral_threshold}):")
                print(f"   Positive (score >{neutral_threshold}): {would_be_positive} ({would_be_positive/len(scores)*100:.1f}%)")
                print(f"   Negative (score <{-neutral_threshold}): {would_be_negative} ({would_be_negative/len(scores)*100:.1f}%)")
                print(f"   Neutral (|score| <{neutral_threshold}): {len(scores) - would_be_positive - would_be_negative} ({(len(scores) - would_be_positive - would_be_negative)/len(scores)*100:.1f}%)")

                # Diagnosis
                print(f"\n📋 DIAGNOSIS:")
                if text_length < 50:
                    print(f"   🚨 PRIMARY ISSUE: Analyzing titles, not full text")
                    print(f"   → FIX: Improve text enrichment success rate")
                    issue_type = 'short_text'
                elif scores.std() < 0.05:
                    print(f"   🚨 PRIMARY ISSUE: All scores clustered near 0 (threshold too strict)")
                    print(f"   → FIX: Lower neutral threshold to 0.05 or use relative scoring")
                    issue_type = 'strict_threshold'
                elif (would_be_positive + would_be_negative) / len(scores) < 0.3:
                    print(f"   ℹ️  LIKELY: Topic genuinely neutral (policy discussion)")
                    print(f"   → ACCEPTABLE: Consider aspect-based sentiment for more nuance")
                    issue_type = 'genuinely_neutral'
                else:
                    issue_type = 'unknown'

                print("="*80)

                return {
                    'distribution': distribution.to_dict() if sentiment_column in df.columns else {},
                    'mean_score': scores.mean(),
                    'std_score': scores.std(),
                    'avg_text_length': text_length,
                    'issue_type': issue_type
                }

        return {'error': 'Required columns not found'}

    @staticmethod
    def reclassify_with_adjusted_threshold(
        df: pd.DataFrame,
        score_column: str = 'sentiment_deep_score',
        new_threshold: float = 0.05
    ) -> pd.DataFrame:
        """
        Reclassify sentiment with adjusted threshold

        Args:
            df: Input dataframe
            score_column: Column with sentiment scores
            new_threshold: New threshold (default: 0.05, more sensitive)

        Returns:
            DataFrame with reclassified sentiment
        """
        df_adjusted = df.copy()

        def classify(score):
            if pd.isna(score):
                return 'neutral'
            elif score > new_threshold:
                return 'positive'
            elif score < -new_threshold:
                return 'negative'
            else:
                return 'neutral'

        if score_column in df.columns:
            df_adjusted['sentiment_adjusted'] = df[score_column].apply(classify)

            print(f"🔄 Reclassified sentiment with threshold={new_threshold}")
            print(f"\nNew distribution:")
            distribution = df_adjusted['sentiment_adjusted'].value_counts()
            for label, count in distribution.items():
                pct = count / len(df_adjusted) * 100
                print(f"   {label}: {count} ({pct:.1f}%)")

        return df_adjusted
