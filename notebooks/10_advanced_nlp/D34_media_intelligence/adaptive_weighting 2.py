"""
Adaptive Spatial Weighting for Media Clustering

Key Innovation: Adjusts spatial weight based on content type
- Syndicated content: λ = 0.0 (geography irrelevant)
- Local news with local sources: λ = 0.4 (geography matters)
- Mixed/default: λ = 0.15 (balanced)
"""

import re
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class AdaptiveWeightCalculator:
    """
    Calculate content-aware spatial weights based on article provenance
    """

    # Known syndicated sources (expand as needed)
    SYNDICATED_SOURCES = [
        'ap.org', 'apnews.com', 'reuters.com', 'bloomberg.com',
        'afp.com', 'upi.com', 'prnewswire.com', 'businesswire.com',
        'marketwatch.com', 'cnbc.com', 'cnn.com', 'foxnews.com',
        'nbcnews.com', 'abcnews.go.com', 'cbsnews.com'
    ]

    # Syndication markers in article text
    SYNDICATION_MARKERS = [
        'Associated Press', 'AP reports', '(AP)', '(AP) --',
        'Reuters reports', '(Reuters)',
        'Bloomberg News',
        'This story was originally published',
        'Originally appeared on',
        'Distributed by',
        'Wire service report',
        'Staff and wire reports',
        'Staff report',
        'Wire reports',
        'Contributing:',
    ]

    # Local news indicators
    LOCAL_NEWS_INDICATORS = [
        'local', 'city', 'town', 'county', 'daily',
        'tribune', 'gazette', 'herald', 'times',
        'post', 'chronicle', 'journal', 'news',
        'observer', 'sentinel', 'dispatch'
    ]

    # Local official titles
    LOCAL_OFFICIAL_TITLES = [
        'mayor', 'councilmember', 'council member', 'alderman',
        'supervisor', 'commissioner', 'local official',
        'city manager', 'town manager', 'selectman',
        'city council', 'town council', 'board of supervisors'
    ]

    def __init__(self):
        self.syndication_cache = {}
        self.local_news_cache = {}
        self.stats = {
            'syndicated': 0,
            'local_with_quotes': 0,
            'local_only': 0,
            'default': 0
        }

    def detect_syndication(self, source: str, text: str, url: str) -> bool:
        """
        Detect if article is syndicated wire content

        Returns:
            True if syndicated, False if original reporting
        """
        # Check cache
        cache_key = f"{source}_{url[:50]}"  # Truncate URL for cache
        if cache_key in self.syndication_cache:
            return self.syndication_cache[cache_key]

        # Method 1: Source domain check
        source_lower = source.lower()
        if any(syn in source_lower for syn in self.SYNDICATED_SOURCES):
            self.syndication_cache[cache_key] = True
            return True

        # Method 2: Text markers (first 500 chars to avoid false positives)
        text_sample = text[:500].lower() if isinstance(text, str) else ""
        if any(marker.lower() in text_sample for marker in self.SYNDICATION_MARKERS):
            self.syndication_cache[cache_key] = True
            return True

        # Default: assume original
        self.syndication_cache[cache_key] = False
        return False

    def detect_local_news(self, source: str, location: str) -> bool:
        """
        Detect if source is local news outlet

        Heuristics:
        - Contains city/state name in domain
        - Regional news patterns
        """
        cache_key = f"{source}_{location}"
        if cache_key in self.local_news_cache:
            return self.local_news_cache[cache_key]

        source_lower = source.lower()
        location_lower = location.lower() if location else ""

        # Check if location name appears in source
        if location_lower:
            # Extract city/state from location string
            location_parts = [p.strip() for p in location_lower.replace(',', '').split() if len(p.strip()) > 4]
            for part in location_parts:
                # Skip generic terms
                if part in ['united', 'states', 'america', 'american', 'americans']:
                    continue
                if part in source_lower:
                    self.local_news_cache[cache_key] = True
                    return True

        # Check for local news indicators
        indicator_count = sum(1 for ind in self.LOCAL_NEWS_INDICATORS if ind in source_lower)
        if indicator_count >= 2:
            self.local_news_cache[cache_key] = True
            return True

        self.local_news_cache[cache_key] = False
        return False

    def has_local_quotes(self, text: str) -> bool:
        """
        Detect if article includes local sources/quotes

        Heuristics:
        - Contains local official titles
        - Has quoted speech with local context
        """
        if not isinstance(text, str) or len(text) < 100:
            return False

        text_lower = text.lower()

        # Check for local official mentions
        for title in self.LOCAL_OFFICIAL_TITLES:
            if title in text_lower:
                return True

        return False

    def calculate_lambda(self, row: pd.Series) -> float:
        """
        Calculate adaptive spatial weight for a single article

        Args:
            row: DataFrame row with columns: source, full_text, url, location

        Returns:
            float: Spatial weight λ ∈ [0.0, 0.4]
        """
        source = row.get('source', '')
        text = row.get('full_text', '') or row.get('text_for_clustering', '') or row.get('title', '')
        url = row.get('url', '')
        location = row.get('location', '')

        # Check syndication first (highest priority)
        is_syndicated = self.detect_syndication(source, text, url)

        if is_syndicated:
            self.stats['syndicated'] += 1
            return 0.0  # Pure semantic clustering for syndicated content

        # Check local news indicators
        is_local = self.detect_local_news(source, location)
        has_quotes = self.has_local_quotes(text)

        if is_local and has_quotes:
            self.stats['local_with_quotes'] += 1
            return 0.4  # Strong regional focus
        elif is_local or has_quotes:
            self.stats['local_only'] += 1
            return 0.25  # Moderate regional focus
        else:
            self.stats['default'] += 1
            return 0.15  # Default middle ground

    def calculate_all_lambdas(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate adaptive λ for entire dataset

        Returns:
            Series of λ values, one per article
        """
        # Reset stats
        self.stats = {
            'syndicated': 0,
            'local_with_quotes': 0,
            'local_only': 0,
            'default': 0
        }

        print(f"\n🔧 Calculating adaptive spatial weights for {len(df)} articles...")
        lambdas = df.apply(self.calculate_lambda, axis=1)

        # Print statistics
        total = len(df)
        print(f"\n📊 Adaptive Weight Distribution:")
        print(f"  λ = 0.0 (syndicated): {self.stats['syndicated']} ({100*self.stats['syndicated']/total:.1f}%)")
        print(f"  λ = 0.4 (local + quotes): {self.stats['local_with_quotes']} ({100*self.stats['local_with_quotes']/total:.1f}%)")
        print(f"  λ = 0.25 (local or quotes): {self.stats['local_only']} ({100*self.stats['local_only']/total:.1f}%)")
        print(f"  λ = 0.15 (default): {self.stats['default']} ({100*self.stats['default']/total:.1f}%)")

        return lambdas

    def get_statistics(self) -> Dict:
        """Return statistics about weight distribution"""
        return self.stats.copy()


def detect_duplicate_content(df: pd.DataFrame,
                            text_column: str = 'text_for_clustering',
                            similarity_threshold: float = 0.95,
                            min_duplicates: int = 5) -> pd.Series:
    """
    Detect syndicated content via text deduplication

    Alternative/supplement to source-based detection

    Args:
        df: DataFrame with articles
        text_column: Column containing text to compare
        similarity_threshold: Cosine similarity threshold (0.95 = 95% similar)
        min_duplicates: Minimum number of near-duplicates to mark as syndicated

    Returns:
        Boolean Series indicating syndicated articles
    """
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity

    print(f"\n🔍 Detecting syndicated content via text similarity...")

    # Generate embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    texts = df[text_column].fillna('').tolist()
    embeddings = model.encode(texts, show_progress_bar=False)

    # Compute similarity matrix
    sim_matrix = cosine_similarity(embeddings)

    # Mark articles with many near-duplicates as syndicated
    # (If 5+ other articles are 95% similar, it's likely syndicated)
    duplicate_counts = (sim_matrix > similarity_threshold).sum(axis=1) - 1  # Subtract self-similarity
    is_syndicated = duplicate_counts >= min_duplicates

    syndicated_count = is_syndicated.sum()
    print(f"  Found {syndicated_count} syndicated articles ({100*syndicated_count/len(df):.1f}%)")

    return pd.Series(is_syndicated, index=df.index)
